from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='', view=views.get_dealerships, name='index'),

    path(route='about', view=views.about, name='about'),
    # path for contact us view
    path(route='contact', view=views.contact, name='contact'),

    path(route='registration', view=views.registration_request, name='registration'),

    path(route='', view=views.login_request, name='login'),

    path(route='logout', view=views.logout_request, name='logout'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)