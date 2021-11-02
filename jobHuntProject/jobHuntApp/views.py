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
        return redirect ('/jobs')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'profile.html', context)

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
        return redirect('/jobs')
    return redirect('/')

# LOG OUT
def logout(request):
    request.session.flush()
    return redirect('/')

def jobs(request): 
    if 'user_id' not in request.session:
        return redirect('/')
    context ={
        'user': User.objects.get(id=request.session
        ['user_id']), 
        'all_jobs': Job.objects.all()
    }
    return render(request, "jobs.html", context)

def create_entry(request):
    errors = Job.objects.job_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect ('/addlisting')
    else:

        Job.objects.create(
            company_name = request.POST['company_name'], 
            position = request.POST['position'], 
            status = request.POST['status'],
            created_by = User.objects.get(id=request.session['user_id'])
        )
        messages.success(request, "Job entry successfully added.")
    return redirect('/jobs')

def addlisting(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0]
    }
    return render(request, 'addlisting.html', context)
    

def user(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "profile.html", context)

# EDIT ENTRY
def edit_entry(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "job": Job.objects.get(id=job_id)
    }
    return render(request, "listingdetails.html", context)

# UPDATE ENTRY
def update(request, job_id):
    if 'user_id' not in request.session:
            return redirect('/')
    errors = Job.objects.job_validator(request.POST)
    if errors: 
        for val in errors.values():
            messages.error(request, val)
        
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_job = Job.objects.get(id=job_id)
        new_job.company_name = request.POST['company_name']
        new_job.position = request.POST['position']
        new_job.status = request.POST['status']
        new_job.users_follow_up.remove(user)
        new_job.save()
        messages.success(request, "Job entry successfully updated.")
    return redirect('/jobs')

# DELETE ENTRY
def delete(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    to_delete = Job.objects.get(id=job_id)
    to_delete.delete()
    messages.success(request, "Job removed from list.")
    return redirect('/jobs')

#FOLLOW UP CLICK
def followUp(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=request.session['user_id'])
    job.users_follow_up.add(user)
    job.save()
    messages.success(request, "Job marked for follow up.")
    return redirect('/jobs')

def noFollowUp(request, job_id):
    if 'user_id' not in request.session:
        return redirect('/')
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=request.session['user_id'])
    job.users_follow_up.remove(user)
    return redirect('/jobs')