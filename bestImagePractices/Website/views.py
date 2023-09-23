from .models import Upload, FileUpload
from .forms import UploadForm, RawUploadForm, FileForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from octorest import OctoRest
from manage import make_client
from pathlib import Path
import os

# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, "home.html", {})


def contact_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about us",
        "my_condition": True,
        "my_number": 123,
        "my_list": [9, 8, 7, "Six"]
    }
    return render(request, "contact.html", my_context)


# Login
def login_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        messages.info(request, f"Welcome, {username}")
        return redirect('/')
    else:
        form = AuthenticationForm()
        return render(request, "login.html", context={"form": form})


# Register
def register_view(request, *args, **kwargs):
    if request.method == "POST":
        # TO ADD : User Creation
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', context={"form": form})


# Create your views here.

def upload_detail_view(request):
    # Passing in object from database to HTML
    obj = Upload.objects.get(id=1)
    context = {
        'title': obj.title,
        'quantity': obj.quantity
    }
    return render(request, "upload/detail.html", context)


def upload_create_view(request):
    # Passing in object from database to HTML
    form = UploadForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "upload/upload_create.html", context)

# File Upload View


@login_required
def file_upload_view(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                client = make_client()

                # Autofill the upload_by field for the File object
                obj = form.save(commit=False)
                obj.upload_by = request.user
                obj.save()
                loc = ""
                new_name = ""
                if client:
                    for filename, file in request.FILES.items():
                        new_name = request.FILES[filename].name
                    loc = new_name
                    uploaded_path = str(Path(__file__).resolve(
                    ).parent.parent / "uploads" / new_name)
                    client.upload(file=uploaded_path)
                else:
                    print(
                        "Unable to upload file to octoprint. Client likely unavailable.")

                return redirect('success/')
            except ValueError as err:
                print(err)
                form = FileForm()
    else:
        form = FileForm()
    return render(request, 'upload/upload_file.html', context={"form": form})


# Successful File Upload View
def success_view(request, *args, **kwargs):
    return render(request, "upload/success.html", {})

# Create your views here.


def queue_view(request, *args, **kwargs):
    client = make_client()
    if request.user.is_staff != True:
        raise Http404()
    try:
        for x in client.files()['files']:
            print(x['name'])
    except:
        print("Unable to list printer files. Client likely unavailable.")
    # Grab queue objects
    queryset = FileUpload.objects.all().order_by('upload_time')

    # Check printer status
    if client:
        status = "Nominal."
        try:
            state = client.printer()['state']

            if state['flags']['printing']:
                status = str(state['text']) + " / Currently printing!"
            else:
                ready = state['flags']['ready']
                if ready:
                    status = str(state['text']) + " / Ready to print!"
                else:
                    status = str(state['text']) + " / Not ready to print!"
        except:
            status = "Client currently disconnected."
    else:
        status = "Not so nominal."

    context = {
        "object_list": queryset,
        "printer_status": status
    }
    if request.method == "POST":
        print(request)
    return render(request, "upload/queue.html", context)


def delete_file(request, pk):
    # Ensure priviledged user
    if request.user.is_staff != True:
        raise Http404()
    if request.method == 'POST':
        file = get_object_or_404(FileUpload, pk=pk)
        new_name = file.file.name
        name = new_name
        try:
            client = make_client()
            client.delete(location=name)
        except:
            print("Failure to delete from octoprint.")
            return redirect('/queue')
        file.delete()

        return redirect('/queue')
    else:
        raise Http404()


def start_print(request, pk):
    # Ensure priviledged user
    if request.user.is_staff != True:
        raise Http404()
    if request.method == 'POST':
        client = make_client()
        file = get_object_or_404(FileUpload, pk=pk)
        access_name = file.file.name
        try:
            state = client.printer()['state']
            ready = state['flags']['printing']
            if ready == False:
                client.select(location=access_name)
                # client.home()
                client.start()
            else:
                print("Currently printing another job!")
        except:
            print("Failure to change printer state.")
        return redirect('/queue')
    else:
        raise Http404()


def pause_print(request, pk):
    # Ensure priviledged user
    if request.user.is_staff != True:
        raise Http404()
    if request.method == 'POST':
        client = make_client()
        file = get_object_or_404(FileUpload, pk=pk)
        access_name = file.file.name
        try:
            state = client.printer()['state']
            printing = state['flags']['printing']
            if printing:
                client.toggle()
            else:
                print("Printer is not currently printing!")
        except:
            print("Failure to change printer state.")
        return redirect('/queue')
    else:
        raise Http404()

def view_gcode(request, pk):
	# Ensure priviledged user
	if request.user.is_staff != True:
		raise Http404()
	if request.method == 'GET':
		file = get_object_or_404(FileUpload, pk=pk)
		context = {
			'file': file
		}
		return render(request, "view_gcode.html", context)
	else:
		raise Http404()

# def upload_create_view(request):
# 	my_form = RawUploadForm()
# 	if request.method == "POST":
# 		my_form = RawUploadForm(request.POST)
# 		if my_form.is_valid():
# 			# Now the data is good
# 			print(my_form.cleaned_data)
# 			my_form.save()
# 	context = {
# 		'form': my_form
# 	}
# 	return render(request, "upload/upload_create.html", context)
