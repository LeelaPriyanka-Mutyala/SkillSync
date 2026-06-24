from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class SkillListing(models.Model):
    CATEGORY_CHOICES = (
        ('Tech', 'Programming & Tech'),
        ('Academic', 'Academic Subjects'),
        ('Arts', 'Music & Arts'),
        ('Languages', 'Languages'),
    )
    TYPE_CHOICES = (
        ('Teaching', 'I can teach this'),
        ('Learning', 'I want to learn this'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True) # For clean URLs
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    listing_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id) if self.id else slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} ({self.listing_type})"

class SwapRequest(models.Model):
    STATUS_CHOICES = (('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined'))
    
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    listing = models.ForeignKey(SkillListing, on_delete=models.CASCADE)
    message = models.TextField(max_length=300)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(SkillListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Prevent a user from favoriting the same listing twice
    class Meta:
        unique_together = ('user', 'listing')

    def __str__(self):
        return f"{self.user.username} favorited {self.listing.title}"