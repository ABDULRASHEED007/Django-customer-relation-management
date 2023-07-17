from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .form import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records  =Record.objects.all()


    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in...")
            return redirect('home')
        else:
            messages.success(request,"Invalid credentials....")
            return redirect('home')
        
    else:
        return render(request, 'home.html', {'records':records})

    

def logout_user(request):
    logout(request)
    messages.info(request,'You are now Logged out....')
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, f"Account created for {username}!")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})    

    return render(request, 'register.html', {'form':form}) 


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.error(request, "Please Login to view your records.")
        return redirect('home')

    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.warning(request, "Record has been deleted successfully..!! ")
        return redirect('home')
    else:
        messages.error(request, "Please Login to Delete Records...")
        return redirect('home')

    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"New record added Successfully...!!! ")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request,'You need an account first.')
        return redirect('home')


    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record=Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.info(request, f"Your {current_record} record is updated")
            return redirect("home")
        return render(request, 'update_record.html', {'form':form})

    else:
        messages.error(request, "Login First To Update Your Record!")
        return redirect('home')