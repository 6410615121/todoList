from user.models import todoUser ,Friend_request
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

def my_data_processor(request):
    # Check if request.user is an instance of AnonymousUser
    if isinstance(request.user, AnonymousUser):
        return {'notification': []}

    # Now you can use actual_user to get the todoUser
    try:
        to_user = todoUser.objects.get(user=request.user)
    except todoUser.DoesNotExist:
        # Create a new todoUser object for the user
        to_user = todoUser.objects.create(user=request.user)
    all_friend_request = Friend_request.objects.filter(To_user=to_user)

    # Ensure that notification is always an iterable
    notification = all_friend_request if all_friend_request else []

    return {'notification': notification,'todouser':to_user}