# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (
    SignUpForm,
    AddRecordsForm,
    AddCaseType,
    AddCourtType,
    ClientForm,
    CaseForm,
)
from .models import cusRecord, CaseType, CourtType, Client, Case
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm


def login_user(request):
    records = cusRecord.objects.all()
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


def client_record(request, pk):
    if request.user.is_authenticated:
        customer_record = get_object_or_404(cusRecord, pk=pk)
        messages.success(request, "Client Record Access")
        return render(
            request,
            "main/client/client_popout.html",
            {"customer_record": customer_record},
        )
    else:
        messages.success(request, "Error Client Record")
        return redirect("view_client")


def client_view(request, username):
    record = cusRecord.objects.all()
    print(record)
    print("USER Authenticated: ", request.user.is_authenticated)

    if request.user.is_authenticated:
        messages.success(request, "Viewing")
        return render(
            request,
            "main/client/client_view.html",
            {"records": record, "username": username},
        )
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect(
            "view_client"
        )  # Redirect to the login page or any other appropriate URL


def delete_client(request, pk):
    if request.user.is_authenticated:
        delete_it = cusRecord.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("view_client", request.user)
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect("view_client", request.user)


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


def add_cus_record(request, username):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordsForm(request.POST)
            print(form)
            print(form.is_valid())
            if form.is_valid():
                record = form.save(commit=False)
                record.created_by = request.user
                record.save()
                messages.success(request, "Client record added successfully.")
                return redirect("add_client", username=username)
            else:
                # Debug: Print form errors to the console
                print("Form errors:", form.errors)
                messages.error(request, "There were errors in the form.")
                return redirect("add_client", username=username)
        else:
            form = AddRecordsForm()  # Create an empty form for GET requests
        return render(request, "main/client/client.html")
    else:
        return redirect("add_client")


def client_update(request, pk):
    context = {}
    if request.user.is_authenticated:
        # fetch the object related to passed id
        obj = get_object_or_404(cusRecord, id=pk)
        current_record = cusRecord.objects.get(id=pk)
        form = AddRecordsForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect("view_client", username=request.user)
        else:
            print("Form errors:", form.errors)
        context["form"] = form
        return render(
            request,
            "main/client/client_update.html",
            {"context": context, "record": current_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("view_client", username=request.user)


def list_case(request, username):
    return render(request, "main/case/list_case.html", {"username": username})


def add_case(request, username):
    record = cusRecord.objects.all()
    return render(
        request,
        "main/case/add_case_client.html",
        {"username": username, "records": record},
    )


def add_client_to_case(request, case_id):
    case = Case.objects.get(id=case_id)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.case = case
            client.save()
            return redirect("list_case")  # Redirect to a success page

    else:
        form = ClientForm()

    return render(request, "main/case/add_case.html", {"form": form, "case": case})


def add_case_clients(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST, prefix="client")
        case_form = CaseForm(request.POST, prefix="case")

        if client_form.is_valid() and case_form.is_valid():
            # Process client and case data here
            client = client_form.save(commit=False)
            case = case_form.save()

            # Associate the client with the case
            client.case = case
            client.save()

            return redirect("list_case", case_id=case.id)
    else:
        client_form = ClientForm(prefix="client")
        case_form = CaseForm(prefix="case")

    return render(
        request,
        "main/client/add_case.html",
        {
            "client_form": client_form,
            "case_form": case_form,
        },
    )


def add_client(request, username):
    return render(request, "main/client/client.html", {"username": username})


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
