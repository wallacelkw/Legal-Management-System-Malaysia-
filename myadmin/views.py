# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (
    SignUpForm,
    AddRecordsForm,
    AddCaseType,
    AddCourtType,
    CaseForm,
    AddClientForm,
)
from .models import CaseType, CourtType, ClientRecord, Case
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

def login_user(request):
    records = User.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect("dashboard", username=user.username)
        else:
            messages.success(
                request, "There Was An Error Logging In, Please Try Again..."
            )
            return redirect("auth/login.html")

    else:
        return render(request, "auth/login.html", {"records": records})


def dashboard(request, username):
    messages.success(request, "You Have Been Log In...")
    return render(request, "main/dashboard.html", {"username": username})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect("login")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


# Setting -> CASE INFORMATION
def case_type(request, username):
    records = CaseType.objects.all()
    is_add = request.session.pop("is_add", False)
    is_update = request.session.pop("is_update", False)

    context = {
        "username": username,
        "records": records,
        "is_add": is_add,
        "is_update": is_update,
    }
    return render(request, "main/setting/case_type.html", context)


def add_case_type(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddCaseType(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Cases Added")
                request.session["is_add"] = True
                return redirect("case_type", username=request.user)
            else:
                messages.error(request, "There were errors in the form.")
        else:
            form = AddCaseType()  # Create an empty form for GET requests
        return render(request, "main/setting/add_case_type.html", {"form": form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect("case_type", username=request.user)


def update_case_type(request, pk):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            # fetch the object related to passed id
            obj = get_object_or_404(CaseType, id=pk)
            current_record = CaseType.objects.get(id=pk)
            form = AddCaseType(request.POST, instance=obj)
            print(form)
            # print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect("case_type", username=request.user)
            else:
                print("Form errors:", form.errors)
            context["form"] = form
        else:
            form = AddCaseType()
        return render(
            request,
            "main/setting/case_type.html",
            {"context": context, "record": current_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("case_type", username=request.user)


def delete_case_type(request, pk):
    if request.user.is_authenticated:
        delete_it = CaseType.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("case_type", request.user)
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect("case_type", request.user)


####-----------------####
####  COURT RECORD   ####
####-----------------####
# Setting -> COURT INFORMATION
def court_type(request, username):
    records = CourtType.objects.all()
    is_add = request.session.pop("is_add", False)
    is_update = request.session.pop("is_update", False)

    context = {
        "username": username,
        "records": records,
        "is_add": is_add,
        "is_update": is_update,
    }
    return render(request, "main/setting/court_type.html", context)


def add_court_type(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddCourtType(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Cases Added")
                request.session["is_add"] = True
                return redirect("court_type", username=request.user)
            else:
                messages.error(request, "There were errors in the form.")
        else:
            form = AddCaseType()  # Create an empty form for GET requests
        return render(request, "main/setting/add_court_type.html", {"form": form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect("court_type", username=request.user)


def update_court_type(request, pk):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            # fetch the object related to passed id
            obj = get_object_or_404(CourtType, id=pk)
            current_record = CourtType.objects.get(id=pk)
            form = AddCourtType(request.POST, instance=obj)
            print(form)
            # print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect("court_type", username=request.user)
            else:
                print("Form errors:", form.errors)
            context["form"] = form
        else:
            form = AddCaseType()
        return render(
            request,
            "main/setting/court_type.html",
            {"context": context, "record": current_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("court_type", username=request.user)


def delete_court_type(request, pk):
    if request.user.is_authenticated:
        delete_it = CourtType.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("court_type", request.user)
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect("court_type", request.user)


####-----------------####
####  CLIENT RECORD  ####
####-----------------####


def add_client_to_db(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddClientForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Client record added successfully.")
                return redirect("add_client_view", request.user)
            else:
                messages.error(request, form.errors)
                print("Form errors:", form.errors)

        else:
            form = AddRecordsForm()

        return render(request, "main/client/add_client.html", {"form": form})


def view_all_client(request, username):
    record = ClientRecord.objects.all()
    print(record)
    if request.user.is_authenticated:
        return render(
            request,
            "main/client/view_client.html",
            {"records": record, "username": username},
        )
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect("view_all_client")


def update_client(request, pk):
    context = {}
    if request.user.is_authenticated:
        # fetch the object related to passed id
        obj = get_object_or_404(ClientRecord, id=pk)
        current_record = ClientRecord.objects.get(id=pk)
        form = AddClientForm(request.POST, instance=obj)
        # print(form)
        # print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect("view_all_client", username=request.user)
        else:
            print("Form errors:", form.errors)
        context["form"] = form
    else:
        form = AddClientForm()
    return render(
        request,
        "main/client/update_client.html",
        {"context": context, "record": current_record},
    )


def delete_client(request, pk):
    if request.user.is_authenticated:
        delete_it = ClientRecord.objects.get(id=pk)
        delete_it.delete()
        return redirect("view_all_client", request.user)
    else:
        return redirect("view_all_client", request.user)


###-----------------###
###   CREATE CASE --###
###-----------------###
def list_case(request, username):
    record = Case.objects.all()
    return render(request, "main/case/list_case.html", {"username": username, "records": record})


def create_case_view(request, username):
    courtInfo = CourtType.objects.all()
    caseInfo = CaseType.objects.all()
    record = ClientRecord.objects.all()
    return render(
        request, "main/case/create_case.html", {"username": username, 
                                                "records": record,
                                                "courtInfo" : courtInfo,
                                                "caseInfo": caseInfo}
    )

def create_case_detail(request):
    if request.user.is_authenticated:
        if request.method =="POST":
            case_form = CaseForm(request.POST)
            if case_form.is_valid() :
                case = case_form.save()
                return redirect("list_case", request.user)
            else:
                print("Case Form errors:", case_form.errors)
         
        else:
            case_form = CaseForm()
        return render(request, 'main/case/create_case.html',{'case_form': case_form})


def update_case_client(request, pk):
    context = {}
    if request.user.is_authenticated:
        case_record = get_object_or_404(Case, id=pk)
        case_primary_record = Case.objects.get(id=pk)
        caseclient_info = Case.objects.all()
        court_info = CourtType.objects.all()
        client_info = ClientRecord.objects.all()
        case_info = CaseType.objects.all()
        caseForm = CaseForm(request.POST, instance=case_record)
        if caseForm.is_valid():
            # print(caseForm)
            print("Court Type: ", case_record.clients)
            caseForm.save()
            # clientCaseForm.save()
            messages.success(request, "Record Has Been Updated")
            return redirect("list_case", username=request.user)
        else:
            print("caseForm Error: ",caseForm.errors)
        context["form"] = caseForm
    else:
        caseForm = CaseForm()
    
    return render(request, "main/case/update_case_client.html", {"record": case_primary_record,
                                                                   "context": context,
                                                                   "caseInfo": case_info,
                                                                   "clientInfo":client_info,
                                                                   "courtInfo":court_info,
                                                                   "caseClientInfo": caseclient_info})

def delete_case(request, pk):
    if request.user.is_authenticated:
        delete_it = Case.objects.get(id=pk)
        delete_it.delete()
        return redirect("list_case", request.user)
    else:
        return redirect("list_case", request.user)

def single_case_client(request, pk):
    if request.user.is_authenticated:
        current_record = Case.objects.get(id=pk)
        return redirect("list_case", {"username": request.user,
                                      "record": current_record})



def add_client_view(request, username):
    return render(request, "main/client/add_client.html", {"username": username})


# Create your views here.
def button_view(request, username):
    return render(request, "main/button.html", {"username": username})


# Create your views here.
def typography_view(request, username):
    return render(request, "main/typography.html", {"username": username})


# Create your views here.
def element_view(request, username):
    return render(request, "main/element.html", {"username": username})


# Create your views here.
def widget_view(request, username):
    return render(request, "main/widget.html", {"username": username})


# Create your views here.
def form_view(request, username):
    return render(request, "main/form.html", {"username": username})


# Create your views here.
def table_view(request, username):
    return render(request, "main/table.html", {"username": username})


# Create your views here.
def chart_view(request, username):
    return render(request, "main/chart.html", {"username": username})


# Create your views here.
def signin_view(request, username):
    return render(request, "main/signin.html", {"username": username})


# Create your views here.
def signup_view(request, username):
    return render(request, "main/signup.html", {"username": username})


# Create your views here.
def view_404(request, username):
    return render(request, "main/error/404.html", {"username": username})


# Create your views here.
def blank_view(request, username):
    return render(request, "main/error/blank.html", {"username": username})
