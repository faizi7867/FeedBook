from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.cache import never_cache

from Feed.models import Message, Comment


@never_cache
def login_fun(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        uname = request.POST["tbusername"]
        pword = request.POST["tbpass1"]
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(request, user)
            request.session['name'] = user.username
            return redirect("home")
        else:
            return redirect("login")

@never_cache
def register_fun(request):
    if request.method == 'GET':
        return render(request, "register.html")

    else:
        p1 = request.POST["tbpass1"]
        p2 = request.POST["tbpass2"]
        un = request.POST["tbusername"]
        em = request.POST["tbemail"]
        if p1 == p2:
            u = User.objects.create_superuser(un, em, p1)
            u.save()
            return redirect("login")
        else:
            return redirect('register')

@never_cache
def logout_fun(request):
    del request.session['name']
    logout(request)
    return redirect("login")


@never_cache
def home(request):
    messages = Message.objects.all()
    context = {'messages':messages,}
    return render(request,"home.html",context)

@login_required
def create_new_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            message = Message.objects.create(user=request.user, content=content)
            message.save()
            return redirect('home')

    return render(request,'create_message.html')


def delete_message(request,id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('home')


def view_message(request,id):
    message = Message.objects.get(id=id)
    comments = Comment.objects.filter(message=message)
    context={'message':message,'comments':comments}
    return render(request,'view_message.html',context=context)


def update_message(request,id):
    message = Message.objects.get(id=id)
    if request.method == 'POST':
        content = request.POST.get('content')
        message.content = content
        message.save()
        return redirect(home)
    else:
        context = {'message':message}
        return render(request,'update_message.html',context=context)


def add_comment(request):
    comment = request.POST.get('comment')
    if comment:
        mes_id  = request.POST.get('message_id')

        comment =  Comment.objects.create(user=request.user, content=comment,message=Message.objects.get(id=mes_id))
        comment.save()
        return redirect('home')
    return  None

