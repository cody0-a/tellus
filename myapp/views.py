from django.db.models import Count
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Story,Comment,Like
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
import json
from django.db import transaction
from urllib import request
from django.shortcuts import render
from django.http import HttpResponse

def quote_image_view(request):
    return render(request, 'myapp/quote_image.html')

def get_random_quote(request):
    try:
        with request.urlopen('https://api.quotable.io/random') as response:
            if response.status == 200:
                data = json.loads(response.read())
                return render(request, 'myapp/quote_partial.html', {
                    'content': data['content'],
                    'author': data['author']
                })
            else:
                raise Exception(f"API returned status code {response.status}")
    except Exception as e:
        return render(request, 'myapp/quote_partial.html', {
            'error': f'Failed to fetch quote: {str(e)}'
        })

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('story')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'myapp/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('story')



def home_view(request):
    stories = Story.objects.order_by('-created_at')[:9]  # Get the 9 most recent stories
    featured_story = Story.objects.filter(featured=True).first()
    
    paginator = Paginator(stories, 9)  # Show 9 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'stories': page_obj,
        'featured_story': featured_story,
    }
    return render(request, 'myapp/index.html', context)



def story_detail_view(request, pk):
    story = Story.objects.get(pk=pk)
    return render(request, 'myapp/story_detail.html', {'story': story})


@login_required
def create_story_view(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect(reverse('story_detail', kwargs={'pk': story.pk}))  # Changed this line
    else:
        form = StoryForm()
    return render(request, 'myapp/create_story.html', {'form': form})

@login_required
@transaction.atomic
def edit_profile_view(request):
    # Ensure the user has a profile
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'myapp/userprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def profile_view(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request, 'myapp/profile.html', context)

def story_list(request):
    stories = Story.objects.annotate(
        comment_count=Count('comments', distinct=True),
        like_count=Count('likes', distinct=True)
    ).select_related('user').order_by('-created_at')
    return render(request, 'story_list.html', {'stories': stories})


def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    comments = story.comments.select_related('user').order_by('-created_at')
    user_has_liked = story.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'story_detail.html', {
        'story': story,
        'comments': comments,
        'user_has_liked': user_has_liked
    })

@login_required
def add_comment(request, story_id):
    if request.method == 'POST':
        story = get_object_or_404(Story, id=story_id)
        content = request.POST.get('content')
        Comment.objects.create(story=story, user=request.user, content=content)
    return redirect('story_detail', story_id=story_id)

@login_required
def toggle_like(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    like, created = Like.objects.get_or_create(story=story, user=request.user)
    if not created:
        like.delete()
    return redirect('story_detail', story_id=story_id)


def published_story(request):
    published = Story.published.all()
    return render(request, 'myapp/published_story.html', {'published': published})

def chat(request):
    return render(request,'myapp/chat.html')
def about_view(request):
    return render(request, 'myapp/about.html')

def contact_view(request):
    return render(request, 'myapp/contact.html')
