from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.core.mail import message, send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        user = request.user
        tasks = Tasks.objects.filter(user=user)
        context = {'tasks':tasks}
        return render(request, 'index.html',context)

def deleteTask(request,id):
    task = Tasks.objects.get(id=id)
    
    task.delete();
    messages.success(request,'Task deleted successfully','success')


    return redirect('/')


def addtask(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST['task']
        desc = request.POST['desc']
        task = Tasks(title=name,desc=desc,user=user)
        task.save();
        messages.success(request,'Task added successfully','success')

        return redirect('/')
    return render(request,'addtask.html')

def edittask(request,id):
    task = Tasks.objects.get(id=id)
    context = {'task':task}
    if request.method == 'POST':
        task.title = request.POST['task']
        task.desc = request.POST['desc']
        if 'checkbox' in request.POST:
            task.complete = True
        else:
            task.complete = False
        task.save();
        messages.success(request,'Task updated successfully','success')

        return redirect('/')
    
    return render(request,'edittask.html',context)

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request,'login.html')
    messages.success(request,'Login to continue','success')
    
    return render(request, 'login.html')

def registerUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.success(request,'*Username is already taken','success')
            return redirect('/register')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'This email already exists')
            return redirect('/register')
        else:
            user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password)
            user.save()

        subject = 'Your Account is Registered!'
        message = f'Hey {username}, Welcome to the Best Todolist app. Have any queries? Feel free to Email us your concern.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return redirect('/login')
    return render(request, 'register.html')

def logoutUser(request):
    logout(request)
    return redirect('/')
