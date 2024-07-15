from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='story'),
    path('story/<int:pk>/', story_detail_view, name='story_detail'),
    path('about/', about_view, name='about'),
    path('quote-image/', quote_image_view, name='quote_image'),
    path('api/random-quote/', get_random_quote, name='random_quote'),
    path('create/',create_story_view,name='create_story'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit-profile'),
    path('logout/', logout_view, name='logout'),
    path('login/',login_view,name='login'),
    path('', story_list, name='story_list'),
    path('story/<int:story_id>/', story_detail, name='story_detail'),
    path('story/<int:story_id>/comment/', add_comment, name='add_comment'),
    path('story/<int:story_id>/like/', toggle_like, name='toggle_like'),
    path('register/', register_view, name='register'), 
    path('contact/', contact_view, name='contact'),
]