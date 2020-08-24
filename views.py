from django.shortcuts import render, redirect
from .models import Applicant, Profile, Application, Combination
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def profile(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'applicant':Applicant.objects.all(),
    }
    return render(request, 'home/profile.html', context)
def dashboard(request):
    app = Application.objects.filter(applicant=request.session['id'])
    context = {
        'app':app,
        'comb': Combination.objects.all(),
    }
    return render(request, 'home/applications.html', context)

def add_profile(request):
    applicant = Applicant.objects.get(id=request.session['id'])
    Profile.objects.create(
        sex = request.POST['gender'],
        dob = request.POST['dob'],
        photo = request.POST['photo'],
        applicant = applicant
    )
    return redirect('/dashboard')

def register(request):
    errors = Applicant.objects.validate(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)

        return redirect('/')
    else:
        pwd = bcrypt.hashpw(request.POST['password'].encode('utf-8'),bcrypt.gensalt()).decode()
        new_applicant = Applicant.objects.create(first_name=request.POST['first_name'],
        					last_name=request.POST['last_name'],
        					email=request.POST['email'],
        					password=pwd)
        request.session['name'] = new_applicant.first_name+ " "+new_applicant.last_name
        request.session['email'] = new_applicant.email
        request.session['id'] = new_applicant.id
        return redirect('/profile')

def login(request):
    result = Applicant.objects.authenticate(request.POST['email'], request.POST['password'])
    if result ==False:
        messages.error(request, "Invalid Email/Password")
    else:
        applicants = Applicant.objects.get(email=request.POST['email'])
        request.session['applicant'] = applicants.first_name+ " "+applicants.last_name
        request.session['id'] = applicants.id
        return redirect('/dashboard')
    #messages.error(request, 'Incorrect Username or Password')
    return redirect('/')

    if len(results) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), results[0].password.encode()):
            request.session['id'] = results[0].id
            return redirect('/dashboard')
    else:
        messages.error(request, "This email has not been registered.")
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def applications(request):
    app = Application.objects.filter(applicant=request.session['id'])
    context = {
        'app':app,
        'comb': Combination.objects.all(),
    }
    return render(request, "home/applications.html", context)

def application_save(request):
    app = Application.objects.filter(applicant=request.session['id'])
    context = {
        'app':app,
        'comb': Combination.objects.all(),
    }
    return render(request, "home/applications.html", context)

def application_save(request):
    app = Applicant.objects.get(id=request.session['id'])
    #comb = Combination.objects.get(id = id)
    comb = Combination.objects.get(id=request.POST['combination'])
    Application.objects.create(
            applicant=app, 
            combination = comb, 
            school_year=request.POST['schoolyear'],
            essay=request.POST['essay']
            )
    return redirect('/dashboard')