# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import (
    SignUpForm,
    AddRecordsForm,
    AddClientRole,
    AddCourtType,
    CaseForm,
    AddClientForm,
    InvoiceForm,
    ReimburServiceFormSet,
    ReimburServiceForm,
    ProfServiceForm,
    ProfServiceFormSet
)
from .models import ClientRole, CourtType, ClientRecord, Case, Invoice, ReimburService, ProfService
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.views import View
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.views.generic import ListView

import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import pandas as pd


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
            return redirect("dashboard")
        else:
            messages.success(
                request, "There Was An Error Logging In, Please Try Again..."
            )
            return redirect("auth/login.html")

    else:
        return render(request, "auth/login.html", {"records": records})


from folium import GeoJson
@login_required()
def dashboard(request):
    case_information = Case.objects.all()
    client_information = ClientRecord.objects.all()
    invoice_information = Invoice.objects.all()
   
    quantity_case = len([x for x,y in enumerate(case_information)])
    quantity_client = len([x for x,y in enumerate(client_information)])
    quantity_invoice = len([x for x,y in enumerate(invoice_information)])

    df = pd.DataFrame(client_information.values())

    # Load the GeoJSON file containing Malaysia's boundaries
    geojson_layer = GeoJson(
        'myadmin/static/js/stanford-zd362bc5680-geojson.json',  # Replace with the actual path to your GeoJSON file
        name='Malaysia Boundaries',
        style_function=lambda feature: {
            'fillColor': 'green',  # Color for the boundary fill
            'color': 'black',       # Color for the boundary outline
            'weight': 1,           # Boundary outline thickness
            'fillOpacity': 0.1,    # Opacity of the boundary fill
        }
    )
    


    map1 = folium.Map(
        location=[3.79239, 109.69887],
        tiles='cartodbpositron',
        zoom_start=5,
    )
    # Add the GeoJSON layer to the map
    geojson_layer.add_to(map1)

    for client in client_information:
        if client.latitude and client.longitude:
            folium.Marker(
                location=[client.latitude, client.longitude],
                popup=client.full_name,  # You can customize the popup content
            ).add_to(map1)


    context = {
        "case_information": quantity_case,
        "client_information": quantity_client,
        "invoice_information": quantity_invoice,
        # 'map_html': map_html,
        'map1':map1._repr_html_()
    }
    messages.success(request, "You Have Been Log In...")
    return render(request, "main/dashboard.html",context )


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
            return redirect("login")
    else:
        form = SignUpForm()
        return render(request, "auth/register.html", {"form": form})

    return render(request, "auth/register.html", {"form": form})


def admin_setting(request):
    context={}
    my_record = User.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        if request.method == "POST":
            # fetch the object related to passed id
            obj = get_object_or_404(User, id=request.user.id)
            current_record = User.objects.get(id=request.user.id)
            form = SignUpForm(request.POST, instance=obj)
            print(form)
            # print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect("dashboard")
            else:
                print("Form errors:", form.errors)
            context["form"] = form
        else:
            form = SignUpForm()
        return render(
            request,
            "navigation/admin_settings.html",
            {"context": context, "record": my_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("case_type")








# Setting -> CASE INFORMATION
@login_required
def client_role(request):
    records = ClientRole.objects.all()
    is_add = request.session.pop("is_add", False)
    is_update = request.session.pop("is_update", False)

    context = {
        "records": records,
        "is_add": is_add,
        "is_update": is_update,
    }
    return render(request, "main/setting/client_role.html", context)

@login_required
def add_client_role(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddClientRole(request.POST)
    
            if form.is_valid():
                form.save()
                messages.success(request, "Cases Added")
                request.session["is_add"] = True
                return redirect("client_role")
            else:
                print("CLIENT ROLE FORM ERROR: ", form.errors)
            
        else:
            form = AddClientRole()  # Create an empty form for GET requests
        return render(request, "main/setting/client_role.html", {"form": form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect("client_role")

@login_required
def update_client_role(request, pk):
    context = {}
    if request.user.is_authenticated:
        if request.method == "POST":
            # fetch the object related to passed id
            obj = get_object_or_404(ClientRole, id=pk)
            current_record = ClientRole.objects.get(id=pk)
            form = AddClientRole(request.POST, instance=obj)
            print(form)
            # print(form)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect("client_role")
            else:
                print("Form errors:", form.errors)
            context["form"] = form
        else:
            form = AddClientRole()
        return render(
            request,
            "main/setting/client_role.html",
            {"context": context, "record": current_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("case_type")

@login_required
def delete_client_role(request, pk):
    if request.user.is_authenticated:
        delete_it = ClientRole.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("client_role")
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect("client_role")


####-----------------####
####  COURT RECORD   ####
####-----------------####
# Setting -> COURT INFORMATION
def court_type(request):
    records = CourtType.objects.all()
    is_add = request.session.pop("is_add", False)
    is_update = request.session.pop("is_update", False)

    context = {
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
                return redirect("court_type")
            else:
                messages.error(request, "There were errors in the form.")
        else:
            form = AddCourtType()  # Create an empty form for GET requests
        return render(request, "main/setting/add_court_type.html", {"form": form})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect("court_type")


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
                return redirect("court_type")
            else:
                print("Form errors:", form.errors)
            context["form"] = form
        else:
            form = AddCourtType()
        return render(
            request,
            "main/setting/court_type.html",
            {"context": context, "record": current_record},
        )

    else:
        messages.success(request, "Update Error")
        return redirect("court_type")


def delete_court_type(request, pk):
    if request.user.is_authenticated:
        delete_it = CourtType.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("court_type")
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect("court_type")


####-----------------####
####  CLIENT RECORD  ####
####-----------------####


def add_client_to_db(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddClientForm(request.POST)
            if form.is_valid():
                city = form.cleaned_data["city"]
                postcode = form.cleaned_data["postcode"]
                state = form.cleaned_data["state"]
                location = f"{city}, {postcode}, {state}"
                geolocator = Nominatim(user_agent="myGeocoder")
                location_info = geolocator.geocode(location)
                print("Location Information: ", location_info )
                print("Latitude : ",location_info.latitude)
                print("Longtitude : ",location_info.longitude)
                # Check if location_info is available
                if location_info: 
                    # Bind the form to a new instance of the ClientRecord model
                    client_record = form.save(commit=False)
                    client_record.latitude = location_info.latitude
                    client_record.longitude = location_info.longitude
                    client_record.save()

                messages.success(request, "Client record added successfully.")
                return redirect("add_client_view")
            else:
                messages.error(request, form.errors)
                print("Form errors:", form.errors)

        else:
            form = AddRecordsForm()

        return render(request, "main/client/add_client.html", {"form": form})


def view_all_client(request):
    record = ClientRecord.objects.all()
    print(record)
    if request.user.is_authenticated:
        return render(
            request,
            "main/client/view_client.html",
            {"records": record},
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
            city = form.cleaned_data["city"]
            postcode = form.cleaned_data["postcode"]
            state = form.cleaned_data["state"]
            location = f"{city}, {postcode}, {state}"
            geolocator = Nominatim(user_agent="myGeocoder")
            location_info = geolocator.geocode(location)
            print("Location Information: ", location_info )
            print("Latitude : ",location_info.latitude)
            print("Longtitude : ",location_info.longitude)
            # Check if location_info is available
            if location_info: 
                # Bind the form to a new instance of the ClientRecord model
                client_record = form.save(commit=False)
                client_record.latitude = location_info.latitude
                client_record.longitude = location_info.longitude
                client_record.save()
           
            messages.success(request, "Record Has Been Updated!")
            return redirect("view_all_client")
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
        return redirect("view_all_client")
    else:
        return redirect("view_all_client")


###-----------------###
###   CREATE CASE --###
###-----------------###
def list_case(request, ):
    record = Case.objects.all()
    return render(request, "main/case/list_case.html", { "records": record})


def create_case_view(request ):
    courtInfo = CourtType.objects.all()
    caseInfo = ClientRole.objects.all()
    record = ClientRecord.objects.all()
    return render(
        request, "main/case/create_case.html", { 
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
                return redirect("list_case")
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
        case_info = ClientRole.objects.all()
        caseForm = CaseForm(request.POST, instance=case_record)
        if caseForm.is_valid():
            # print(caseForm)
            print("Court Type: ", case_record.clients)
            caseForm.save()
            # clientCaseForm.save()
            messages.success(request, "Record Has Been Updated")
            return redirect("list_case")
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
        return redirect("list_case")
    else:
        return redirect("list_case")

def single_case_client(request, pk):
    if request.user.is_authenticated:
        current_record = Case.objects.get(id=pk)
        return redirect("list_case", {
                                      "record": current_record})


def view_invoice(request):
    return render(request,"main/invoice/invoice_list.html", )

class InvoiceInline():
    form_class = InvoiceForm
    model = Invoice
    template_name = "main/invoice/create_invoice.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all ((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()
    
        for name,formset in named_formsets.items():
            print("NAME: ", name)
            print("FORMSET: ", formset)
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            print("formset_save_func : ", formset_save_func )
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('view_invoice')
    
    def formset_services_valid(self, formset):
        services = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in services:
            variant.invoice = self.object
            variant.save()

    def formset_prof_services_valid(self, formset):
        profservices = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in profservices:
            variant.invoice = self.object
            variant.save()

class InvoiceCreate(InvoiceInline, CreateView):

    def get_context_data(self, **kwargs):
        case = Case.objects.all()
        ctx = super(InvoiceCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['case_info'] = case
        
        return ctx
        # print("CTX: ",ctx)
        return ctx
    
    def get_named_formsets(self):
        if self.request.method =='GET':
            return {
                'services': ReimburServiceFormSet(prefix='services'),
                'prof_services' : ProfServiceFormSet(prefix='prof_services')
            }
        else:
            return{
                'services': ReimburServiceFormSet(self.request.POST or None, self.request.FILES or None, prefix='services'),
                'prof_services': ProfServiceFormSet(self.request.POST or None, self.request.FILES or None, prefix='prof_services'),
            }

class ProductUpdate(InvoiceInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'services': ReimburServiceFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='services'),
            'prof_services': ProfServiceFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='prof_services'),
        }


def delete_proservice(request, pk):
    try:
        image = ProfService.objects.get(id=pk)
    except ProfService.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('products:update_product', pk=image.product.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('products:update_product', pk=image.product.id)


def delete_reimbur(request, pk):
    try:
        variant = ReimburService.objects.get(id=pk)
    except ReimburService.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('view_invoice', pk=variant.product.id)

    variant.delete()
    messages.success(
            request, 'Variant deleted successfully'
            )
    return redirect('view_invoice', pk=variant.product.id)

from django.urls import reverse
class InvoiceList(ListView):
    model = Invoice
    template_name = "main/invoice/invoice_list.html"
    context_object_name = "invoices"

  

def PDFInvoiceView(request, pk):
    obj = Invoice.objects.get(pk=pk)
    articles = obj.reimburservice_set.all()
    proservices = obj.profservice_set.all()
    case = Case.objects.get(pk=obj.case_id)
    clients = ClientRecord.objects.get(pk= case.clients_id)


    context = {'obj' : obj,
               'articles': articles,
               'case' : case,
               'clients' : clients,
               'proservices' : proservices
               }
    return render(request,'main/invoice/pdf_view.html', context)


def add_client_view(request, ):
    return render(request, "main/client/add_client.html")


def balance_sheet(request, ):
    invoice = Invoice.objects.all()
    data = []
    total_price =[x.final_total for x in invoice]
    price = 0
    for x in total_price:
        price += x

    return render(request,'main/setting/balance_sheet.html', {
                                                              "invoice": invoice,
                                                              'total_price': price})

