from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model  # Use this instead of importing User directly
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .models import CustomUser  # Optional, but you can keep this for reference

def index(request):
    return render(request, "chat/index.html")

# Use get_user_model() to refer to the correct model (CustomUser or default User)
User = get_user_model()

def store_active_chat(user, sender):
    """Store the sender in the recipient's active chat list."""
    active_chats = cache.get(f"active_chats_{user}", set())
    active_chats.add(sender)
    cache.set(f"active_chats_{user}", active_chats, timeout=86400)  # Store for 1 day

@login_required
def user_list(request):
    my_username = request.user.username  # Get the logged-in user's username
    users = User.objects.exclude(username=my_username)  # Exclude the logged-in user by username
    rooms = []
    
    # Iterate through each user in the users list
    for user in users:
        if len(my_username) < len(user.username):
            u = f"{my_username}_{user.username}"
        elif len(my_username) > len(user.username):
            u = f"{user.username}_{my_username}"
        elif my_username < user.username:
            u = f"{my_username}_{user.username}"
        else:
            u = f"{user.username}_{my_username}"
        rooms.append(u)
            
    users_rooms = zip(users, rooms)
    
    # Get active chats from cache
    active_chats = cache.get(f"active_chats_{request.user.username}", set())    

    return render(request, "chat/user_list.html", {
        "users_rooms": users_rooms,
        "active_chats": active_chats  # Pass active chat data
    })

@login_required
def chat_room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': request.user.username  # Pass the username from the authenticated user
    })

@csrf_exempt
def register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User registered successfully"})

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("chat:user_list")  # ✅ Redirect to "user_list"
        else:
            return render(request, "chat/login.html", {"error": "Invalid credentials"})

    return render(request, "chat/login.html")

@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect("chat:index")
    # return JsonResponse({"message": "Logged out successfully"})
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "chat/register.html", {"error": "Passwords do not match"})

        if CustomUser.objects.filter(username=username).exists():
            return render(request, "chat/register.html", {"error": "Username already taken"})

        user = CustomUser.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        login(request, user)  # Log the user in after registration
        return redirect("chat:login")  # Redirect to login page

    return render(request, "chat/register.html")

def about(request):
    return render(request, "chat/about.html")
