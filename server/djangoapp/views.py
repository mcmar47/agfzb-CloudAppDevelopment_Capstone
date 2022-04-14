from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
     context = {}
     if request.method == "GET":
         return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
     context = {}
     if request.method == "GET":
         return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
     context = {}
     if request.method == "POST":
         # pull from dictionary
         username = request.POST['username']
         password = request.POST['pwd']
         # check auth
         user = authenticate(username=username, password=password) 
         if user is not None:
             # login if valid
             login(request, user)
             return render(request, 'djangoapp/index.html', context)
         else:
             return render(request, 'djangoapp/index.html', context)
     else:
         return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
     context = {}
     # get user from session id
     print("Log out the user `{}`".format(request.user.username))
     logout(request)
     # redirect back to the index.html
     return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
def registration_request(request):
     context = {}
     # rend if it is a GET req
     if request.method == 'GET':
         return render(request, 'djangoapp/registration.html', context)
     elif request.method == 'POST':
         # get user info
         username = request.POST['username']
         password = request.POST['pwd']
         first_name = request.POST['firstname']
         last_name = request.POST['lastname']
         user_exist = False
         try:
             User.objects.get(username=username)
             user_exist = True
         except:
             logger.debug("{} is new user".format(username))
         if not user_exist:
             # create new user
             user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
             login(request, user)
             return render(request, 'djangoapp/index.html', context)
         else:
             return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context={}
    url = "https://9bd9d7ac-0868-4878-94ab-e6b8fb6b2bfb-bluemix.cloudantnosqldb.appdomain.cloud"
    apikey="Qb_AUwHIy5_dOFoqB_YbErChHfvOjR6gv_AuAKtvt3uV"
    # Get dealers from the URL
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://us-south.functions.cloud.ibm.com/api/v1/namespaces/michaelcmar%40icloud.com_dev/actions/capstone-final/dealership"
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
        #print(context)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0#placeholder
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request("https://us-south.functions.cloud.ibm.com/api/v1/namespaces/michaelcmar%40icloud.com_dev/actions/capstone-final/review", review, dealerId=dealer_id)
            print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://9bd9d7ac-0868-4878-94ab-e6b8fb6b2bfb-bluemix.cloudantnosqldb.appdomain.cloud"
        apikey="Qb_AUwHIy5_dOFoqB_YbErChHfvOjR6gv_AuAKtvt3uV"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

