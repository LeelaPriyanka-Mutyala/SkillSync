from django.contrib import admin
from .models import SkillListing, SwapRequest

@admin.register(SkillListing)
class SkillListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'listing_type', 'created_at')
    list_filter = ('category', 'listing_type')
    search_fields = ('title', 'description')

@admin.register(SwapRequest)
class SwapRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'listing', 'status', 'timestamp')