from .models import SwapRequest

def unread_requests(request):
    if request.user.is_authenticated:
        count = SwapRequest.objects.filter(receiver=request.user, status='Pending').count()
        return {'unread_count': count}
    return {'unread_count': 0}