from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from base.models import Room, Topic, Message
from base.forms import RoomForm
from base.common.getTopicsInfo import getTopicsInfo
from base.common.getRoomsInfo import getRoomsInfo

# Create your views here.

def loginPage(request):
    
    page = 'login'
    context = {'page': page}
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip()
        
        if email == '' or password == '':
            messages.error(request, 'Please, fill all inputs')
            return render(request, 'base/login_register.html', context)
        
        try:
            user = User.objects.get(email=email)
            
        except Exception as e:
            messages.error(request, 'Email and/or password incorrect')
            return render(request, 'base/login_register.html', context)
            
        user = authenticate(request, username=user.username, password=password)
        
        # adds session into database
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email and/or password incorrect')
            return render(request, 'base/login_register.html', context)
        
    
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    
    form = UserCreationForm()
    context = {'form': form}
    
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        
        if any([field == '' for field in [username, email, password, confirm_password]]):
            messages.error(request, 'Please, fill all inputs')
            return render(request, 'base/login_register.html', context)
        
        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return render(request, 'base/login_register.html', context)
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
                )
            
            user.save()
            login(request, user)
            return redirect('home')
        except:
            messages.error(request, 'User already registered')
            return render(request, 'base/login_register.html', context)
    
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=query) |
        Q(name__icontains=query) |
        Q(description__icontains=query) 
        )
    room_count = rooms.count()
    room_messages = Message.objects.all().filter(Q(room__topic__name__icontains=query))[:7]
    
    topics_info = getTopicsInfo()
    rooms_info = getRoomsInfo(query=query)
    
    context = {
        'rooms_info': rooms_info,
        'topics_info': topics_info,
        'room_count': room_count,
        'room_messages': room_messages
        }
    
    return render(request, 'base/home.html', context)

@login_required(login_url='/login')
def room(request, pk):
    if not pk.isdigit():
        return render(request, 'base/room.html')
    
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('message_body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description').strip()
        
        if name == '' or description == '':
            messages.add_message(request=request, level=messages.ERROR, message='Name and description fields are mandatory')
        
        else:
            filledRoom = Room(
                name = name,
                description = description
            )
            
            filledRoom.host = request.user
            filledRoom.topic = Topic.objects.get(name=request.POST.get('topic'))
            filledRoom.save()
                
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Not allowed', status=401)
    
    if request.method == 'POST':
        updatedForm = RoomForm(request.POST, instance=room)
        updatedForm.save()
        return redirect("/")
        
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    print(request.path)
    
    if request.user != room.host:
        return HttpResponse('Not allowed', status=401)
    
    if request.method == 'POST':
        room.delete()
        return redirect("/")
    
    context = {'obj': room}
    return render(request, 'base/delete_room.html', context)

@login_required(login_url='/login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('Not allowed', status=401)
    
    if request.method == 'POST':
        message.delete()
        return redirect("/")
    
    context = {'obj': message}
    return render(request, 'base/delete_room.html', context)

@login_required(login_url='/login')
def userProfile(request, pk):
    
    user = User.objects.get(id=pk)
    created_rooms = Room.objects.filter(host=user).count()
    messages_sent = Message.objects.filter(user=user).count()
        
    context = {
        'user': user,
        'created_rooms': created_rooms,
        'messages_sent': messages_sent
        }
    return render(request, 'base/profile.html', context)