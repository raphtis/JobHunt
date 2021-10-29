from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Add views here!!!
def index(request):
    request.session.flush()
    return render (request, "index.html")


# register page; a post redirect 
def register(request): 
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        # hash the password!!!!
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a new user
        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST ['email'], 
            password = hashed_pw
        )
        # create a new session
        request.session['user_id'] = new_user.id
        return redirect ('/success')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'success.html', context)

# LOG IN

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email = request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')

# LOG OUT
def logout(request):
    request.session.flush()
    return redirect('/')

