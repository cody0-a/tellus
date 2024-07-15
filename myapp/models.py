from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.db.models.signals import post_save
from django.dispatch import receiver
class Publishedmanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True)
    website = models.URLField(max_length=200, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    
    # Social media links
    twitter = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    github = models.URLField(max_length=200, blank=True)
    
    # Preferences
    receive_newsletter = models.BooleanField(default=False)
    dark_mode = models.BooleanField(default=False)
    
    # Additional personal information
    gender = models.CharField(max_length=20, blank=True, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ])
    interests = models.TextField(blank=True, help_text="Comma-separated list of interests")
    
    # Account status
    account_verified = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()



class Story(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    excerpt = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)


    published = Publishedmanager()

    objects = models.Manager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Stories"


class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # is_published = models.BooleanField(default=False)
    # published = Publishedmanager()
    objects = models.Manager()


    def __str__(self):
        return f"Comment by {self.user.username} on {self.story}"

class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('story', 'user')

    def __str__(self):
        return f"Like by {self.user.username} on {self.story}"