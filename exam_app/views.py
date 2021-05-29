# from _typeshed import FileDescriptor
from django.shortcuts import render, redirect, HttpResponse

from .models import *
import bcrypt
from django.contrib import messages

# Create your views here.
def index(request):

    return render(request,'index.html')

def create(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        password = request.POST['pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['f_name'],
                                    last_name = request.POST['l_name'],
                                    email = request.POST['email'],
                                    password = pw_hash)
        request.session['user_id'] = new_user.id
        request.session['name'] = new_user.first_name
        messages.success(request, "You have successfully registered!")
        return redirect('/user/dashboard')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                
                # messages.success(request, "You have successfully logged in!")
                return redirect('/user/dashboard')
            errors= messages.error(request,"Log in Email or password is not right")
        errors= messages.error(request,"Log in Email or password is not right")
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=request.session['user_id'])
    

    context = {
        'this_user':this_user,
        'other_trips': Trip.objects.all().exclude(creator=this_user).exclude(joined=this_user),
        'joined_trips': Trip.objects.filter(joined=this_user),
    }

    return render(request, 'dashboard.html',context)

def logout(request):
    
        request.session.flush()
        return redirect('/')

def new(request):
    if 'user_id' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render(request,"newtrip.html",context)

def create_trip(request):
    if request.method == 'POST':
        this_user = User.objects.get(id=request.session['user_id'])
        errors= Trip.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/new')
        new_trip = Trip.objects.create(destination=request.POST['destination'],
                                        start_date = request.POST['start_date'],
                                        end_date = request.POST['end_date'],
                                        plan = request.POST['plan'],
                                        creator = this_user)
        return redirect('/user/dashboard')

def delete_trip(request, trip_id):
    if 'user_id' not in request.session:
        return redirect("/")
    trip_to_delete = Trip.objects.get(id=trip_id)
    trip_to_delete.delete()
    return redirect('/user/dashboard')  

def edit_trip(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    
    
    context = {
        'this_trip':this_trip,
    }
    return render(request,'edit_trip.html',context)


def update_trip(request, trip_id):
    if request.method == 'POST':
        errors= Trip.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/trips/{trip_id}/edit')
        else:
            trip_to_update = Trip.objects.get(id=trip_id)
            trip_to_update.destination = request.POST['destination']
            trip_to_update.start_date = request.POST['start_date']
            trip_to_update.end_date = request.POST['end_date']
            trip_to_update.plan = request.POST['plan']
            trip_to_update.save()
            return redirect('/user/dashboard')
    return redirect('/user/dashboard')

def display_trip(request, trip_id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_trip = Trip.objects.get(id=trip_id)
    trip_creator = this_trip.creator
    context = {
        'this_trip':this_trip,
        'this_user':this_user,
        # 'other_joined' : Trip.objects.all().exclude(creator=this_user),#this is wrong
        'other_joined': this_trip.joined.all().exclude(id=trip_creator.id),
        # 'other_joined': this_trip.joined.all(),
    }
    return render(request,'display_trip.html',context)

def join(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.joined_trips.add(this_trip)
    return redirect('/user/dashboard')

def cancel(request, trip_id):
    this_trip = Trip.objects.get(id=trip_id)
    this_user = User.objects.get(id=request.session['user_id'])
    this_user.joined_trips.remove(this_trip)
    return redirect('/user/dashboard')


