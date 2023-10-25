# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
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
from uuid import uuid4
from .process import *
from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, ProfService, ReimburService
from .forms import InvoiceForm, ProfServiceForm, ReimburServiceForm
from django.contrib import messages
from collections import Counter
import json
from folium import GeoJson
from django.core.mail import send_mail
from django.conf import settings


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


@login_required()
def dashboard(request):
    case_information = Case.objects.all()
    client_information = ClientRecord.objects.all()
    invoice_information = Invoice.objects.all()

    #Urgency get it from case_information
    for i in case_information:
        print(i.sense_of_urgent)
   
    quantity_case = len([x for x,y in enumerate(case_information)])
    quantity_client = len([x for x,y in enumerate(client_information)])
    quantity_invoice = len([x for x,y in enumerate(invoice_information)])

    data = {1: [], 2: [], 3: []}  # Create dictionaries to store data based on labels
    label_order = ["High", "Medium", "Low"]

    # Retrieve the query of sense_of_urgent containing 'High', 'Medium', and 'Low'
    case_information_urgent = Case.objects.filter(sense_of_urgent__in=['High', 'Medium', 'Low'])

    # Extract the sense_of_urgent values into a list
    sense_of_urgent_values = [case.sense_of_urgent for case in case_information_urgent]

    # Count the occurrences of each label
    label_counts = dict(Counter(sense_of_urgent_values))

    # Define the order of labels
    label_order = ['High', 'Medium', 'Low']

    # Create a list of data corresponding to each label
    data = [label_counts[label] for label in label_order]



    label_order = json.dumps(label_order)
    print(label_order)
    print(data)

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
        'map1':map1._repr_html_(),
        'data_urgent' : data,
        'label_urgent': label_order
    }
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
                # Check if location_info is available
                if location_info: 
                    # Bind the form to a new instance of the ClientRecord model
                    client_record = form.save(commit=False)
                    client_record.latitude = location_info.latitude
                    client_record.longitude = location_info.longitude
                    client_record.save()

                messages.success(request, "Client record added successfully.")
                return redirect("view_all_client")
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
    
def single_client(request, pk):
    if request.user.is_authenticated:
        current_record = ClientRecord.objects.get(id=pk)
        return redirect("view_all_client", {
                                      "record": current_record})


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
                messages.error(request,case_form.errors)
                # print("Case Form errors:", case_form.errors)
         
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

from django.db.models import Q
def view_invoice(request):
    context = {}
    invoices = Invoice.objects.all()
    reimburService = ReimburService.objects.all()
    for brand in Invoice.objects.all():
        if brand.case == None:
            invoice_to_delete = Invoice.objects.get(pk = brand.pk)
            invoice_to_delete.delete()

    context['invoices'] = invoices
    return render(request,"main/invoice/invoice_list.html", context)


from django.urls import reverse




@login_required
def createInvoice(request):
    #create a blank invoice ....
    number = 'INV-'+str(uuid4()).split('-')[1]
    newInvoice = Invoice.objects.create(number=number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', slug=inv.slug)


def createBuildInvoice(request, slug):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(slug=slug)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    profService = ProfService.objects.filter(invoice=invoice)
    reimburService = ReimburService.objects.filter(invoice=invoice)


    context = {}
    context['invoice'] = invoice
    context['profService'] = profService
    context['reimburService'] = reimburService
    reimburdance_price = 0.0
    prof_price = 0.0
    for i in reimburService:
        reimburdance_price += float(i.reimbur_service_price)
    
    for i in profService:
        prof_price += float(i.prof_service_price)
    invoice.total_reimbur_service_price = reimburdance_price
    invoice.total_prof_service_price = prof_price
    invoice.final_total = reimburdance_price + prof_price
    invoice.save()

    if request.method == 'GET':
        prod_form  = ProfServiceForm()
        prod_form2  = ReimburServiceForm()
        inv_form = InvoiceForm(instance=invoice)
        context['prod_form'] = prod_form
        context['prod_form2'] = prod_form2
        context['inv_form'] = inv_form



        return render(request, 'main/invoice/create_invoice.html', context)

    if request.method == 'POST':
        prod_form  = ProfServiceForm(request.POST)
        prod_form2  = ReimburServiceForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
        print("INV FORM : ", inv_form.is_valid())
        if prod_form2.is_valid() and 'reimbur_service'in request.POST:
            print(prod_form2.cleaned_data['reimbur_service_price'])
            obj = prod_form2.save(commit=False)
            obj.invoice = invoice
            obj.save()
            messages.success(request, "Reimburdance Service added succesfully")
            return redirect('create-build-invoice', slug=slug)
        elif prod_form.is_valid() and 'prof_service' in request.POST:
            obj2 = prod_form.save(commit=False)
            obj2.invoice = invoice
            obj2.save()
            messages.success(request, "Professional Service added succesfully")
            return redirect('create-build-invoice', slug=slug)
        elif inv_form.is_valid() and 'case' in request.POST:
            inv_form.save()
            messages.success(request, "Invoice updated succesfully")
            return redirect('create-build-invoice', slug=slug)
        else:
            if inv_form.errors :
                messages.error(request, inv_form.errors)
            elif prod_form.errors:
                messages.error(request, prod_form.errors)
            elif prod_form2.errors:
                messages.error(request, prod_form2.errors)
            context['prod_form'] = prod_form
            context['prod_form2'] = prod_form2
            context['inv_form'] = inv_form
            # context['case_form'] = case_form
            return render(request, 'main/invoice/create_invoice.html', context)
    return render(request, 'main/invoice/create_invoice.html', context)




def updateBuildInvoice(request, slug):
    try:
        invoice = get_object_or_404(Invoice, slug=slug)
    except Invoice.DoesNotExist:
        messages.error(request, 'Invoice not found')
        return redirect('invoices')
    all_case = Case.objects.all()
    profService = ProfService.objects.filter(invoice=invoice)
    reimburService = ReimburService.objects.filter(invoice=invoice)

    reimburdance_price = sum(float(i.reimbur_service_price) for i in reimburService)
    prof_price = sum(float(i.prof_service_price) for i in profService)

    invoice.total_reimbur_service_price = reimburdance_price
    invoice.total_prof_service_price = prof_price
    invoice.final_total = reimburdance_price + prof_price
    invoice.save()

    if request.method == 'GET':
        prod_form = ProfServiceForm()
        prod_form2 = ReimburServiceForm()
        inv_form = updateInvoiceForm(instance=invoice)

        context = {
            'invoice': invoice,
            'profService': profService,
            'reimburService': reimburService,
            'prod_form': prod_form,
            'prod_form2': prod_form2,
            'inv_form': inv_form,
            'all_case' : all_case
        }

        return render(request, 'main/invoice/update_invoice.html', context)

    if request.method == 'POST':
        if 'reimbur_service' in request.POST:
            prod_form2 = ReimburServiceForm(request.POST)
            if prod_form2.is_valid():
                obj = prod_form2.save(commit=False)
                obj.invoice = invoice
                obj.save()
                messages.success(request, "Reimbursement Service added successfully")
            else:
                messages.error(request, prod_form2.errors)
        elif 'prof_service' in request.POST:
            prod_form = ProfServiceForm(request.POST)
            if prod_form.is_valid():
                obj2 = prod_form.save(commit=False)
                obj2.invoice = invoice
                obj2.save()
                messages.success(request, "Professional Service added successfully")
            else:
                messages.error(request, prod_form.errors)
        elif 'case' in request.POST:
            inv_form = updateInvoiceForm(request.POST, instance=invoice)
            if inv_form.is_valid():
                inv_form.save()
                messages.success(request, "Invoice updated successfully")
            else:
                messages.error(request, inv_form.errors)

        return redirect('update-build-invoice', slug=slug)

    return render(request, 'main/invoice/update_invoice.html', context)




from django.shortcuts import get_object_or_404, redirect

from django.http import HttpResponseRedirect

def deleteProfService(request, slug):
    try:
        prof_service = ProfService.objects.get(slug=slug)
        # Get the 'next' parameter from the request
        next_url = request.GET.get('next', 'create-build-invoice')
        prof_service.delete()
        messages.success(request, 'Professional Service deleted successfully.')
    except ProfService.DoesNotExist:
        messages.error(request, 'Professional Service not found.')
        next_url = 'create-build-invoice'

    return HttpResponseRedirect(next_url)

def deleteReimburService(request, slug):
    try:
        reimbur_service = ReimburService.objects.get(slug=slug)
        # Get the 'next' parameter from the request
        next_url = request.GET.get('next', 'create-build-invoice')
        reimbur_service.delete()
        messages.success(request, 'Reimbursement Service deleted successfully.')
    except ReimburService.DoesNotExist:
        messages.error(request, 'Reimbursement Service not found.')
        next_url = 'create-build-invoice'

    return HttpResponseRedirect(next_url)



def deleteInvoice(request, slug):
    try:
        Invoice.objects.get(slug=slug).delete()
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    return redirect('invoices')


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

#Creating a class based view
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import Context, Template
from xhtml2pdf import pisa
from io import BytesIO
import os

from fpdf import FPDF



class PDF(FPDF):
    def header(self) -> None:
        self.set_font('helvetica' ,'B', 20)
        self.cell(0, 10, 'LEE CHO & CO', border=False, ln=1, align='C')
        self.set_font('helvetica' ,'B', 10)
        self.cell(0,5 , 'Advocates & Solicitors', ln=1, align='C')
        self.set_font('helvetica' ,'', 10)
        self.cell(0,5 , 'No.13-1, Jalan Cetak 16/3, Seksyen 16,', ln=1,align='C')
        self.cell(0,5 , '40200 Shah Alam, Selangor Darul Ehsan.', ln=1, align='C')
        
        self.ln(1)
       # Tel and Fax
        tel_text = 'Tel: +603-5523 3513'
        fax_text = 'Fax: +603-5523 8513'
        total_width = self.w  # Total width of the page

        # Calculate the combined width of both cells
        tel_width = self.get_string_width(tel_text)
        fax_width = self.get_string_width(fax_text)
        total_text_width = tel_width + fax_width + 20  # 10 units of space

        # Calculate the starting x-coordinate to center the combined text
        x_start = (total_width - total_text_width) / 2

        # Set x position for Tel
        self.set_x(x_start)
        self.cell(tel_width, 5, tel_text, align='L')

        # Set x position for Fax
        self.set_x(x_start + tel_width + 20)
        self.cell(fax_width, 5, fax_text, align='L')

        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(3)
    

    def chapter_body(self, body):
        # Set font for chapter body
        self.set_font("helvetica",'' ,10)
        # MultiCell allows for text to flow and automatically wrap to the next line
        self.multi_cell(0, 5, body)
        self.ln()  # Move down after the paragraph

    def chapter_table(self, table_data):
        # Set font for the table
        self.set_font("Arial", size=10)
        
        # Define column widths
        col_widths = [80, 40, 40]  # Adjust as needed
        
        for row in table_data:
            for i, data in enumerate(row):
                self.cell(col_widths[i], 10, data, border=1)
            self.ln()

    def chapter_title_detail(self, title):
        # Set font for chapter title
        self.set_font("Arial", "B", 10)
        self.cell(0, 10, title, 0, 1, "L")
        self.ln(5)  # Move down a little

    def chapter_content(self, data):
        # Set font for the content
        self.set_font("Arial", size=10)
        for item in data:
            if isinstance(item, tuple):
                # If it's a tuple, it's a line item
                self.cell(100, 5, item[0], border=1)
                self.cell(45, 5, item[1], align="R", border=1)
                self.cell(45, 5, "", align="R", border=1)
                self.ln()
            else:
                # If it's not a tuple, it's a total
                self.cell(100, 5, "", border=1)
                self.cell(45, 5, "", border=1)
                self.cell(45, 5, item, align="R", border=1)
                self.ln()
        self.ln(5)  # Move down a little


def generate_pdf_invoice(request, pk):
    print("SLUG:::: ",pk)
    obj = Invoice.objects.get(pk=pk)
    reimburservice = obj.reimburservice_set.all()
    proservices = obj.profservice_set.all()
    case = Case.objects.get(pk=obj.case_id)
    clients = ClientRecord.objects.get(pk= case.clients_id)
    context = {'obj' : obj,
               'articles': reimburservice,
               'case' : case,
               'clients' : clients,
               'proservices' : proservices
               }
    
    pdf = PDF('P', 'mm', 'A4')



    # Add a page
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('helvetica', '', 10)
    pdf.ln(3)
    # Add the "Our Ref" and "Date" lines
    our_ref_text = f'Our Ref: {case.ref_no}'
    date_text = f'Date: {obj.invoice_date_time}'
    our_ref_width = pdf.get_string_width(our_ref_text)
    date_width = pdf.get_string_width(date_text)
    max_width = min(our_ref_width, date_width)

    pdf.cell(max_width, 5, our_ref_text, align='L')
    pdf.cell(0, 5, date_text, align='R', ln=1)

    # Set the position for the "To" section
    to_x = max_width  # X-coordinate, with additional spacing
    to_y = pdf.get_y()  # Y-coordinate
    print("X: ", to_x)

    # Add the "To" section aligned with "Our Ref"
    # pdf.set_xy(to_x, to_y)
    pdf.cell(0, 5, 'To: ')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.full_name, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.address1, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.address2, align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, f'{clients.city}, {clients.postcode}, {clients.state}', align='L')
    pdf.set_x(to_x-3)  # Adjust for additional spacing
    pdf.multi_cell(0, 5, clients.country, align='L')

    pdf.ln(3)
    pdf.set_font('helvetica', 'B', 10)

    # pdf.cell(0, 5, 'PROFESSIONAL CHARGES IN THE MATTER OF:-', ln=2, align='C')
    pdf.chapter_title('PROFESSIONAL CHARGES IN THE MATTER OF:-')
    pdf.chapter_body(obj.short_descriptions)

    # Add a chapter title for "PROFESSIONAL CHARGES"
    chapter_title = "PROFESSIONAL CHARGES"
    pdf.chapter_title_detail(chapter_title)

    proservices_data =[]
    for record in proservices:
        proservices_data.append((record.prof_service, f"RM {record.prof_service_price:.2f}"))

    # Add a total row
    total_price = obj.total_prof_service_price
    proservices_data.append( f"RM {total_price:.2f}")
    print("PROSERVUICES: ", proservices_data)
    # Add the professional charges content
    pdf.chapter_content(proservices_data)

    # Add a chapter title for "REIMBURSEMENTS"
    chapter_title = "REIMBURSEMENTS"
    pdf.chapter_title_detail(chapter_title)

    articles_data =[]
    for record in reimburservice:
        articles_data.append((record.reimbur_service, f"RM {record.reimbur_service_price:.2f}"))

    # Add a total row
    total_price = obj.total_reimbur_service_price
    articles_data.append(f"RM {total_price:.2f}")


    # Add the reimbursements content
    pdf.chapter_content(articles_data)

    # Add the "Total" section
    total = ["Total", f"RM {obj.final_total}"]
    pdf.chapter_content(total)


    pdf.output('pdf_2.pdf')

    return redirect('invoices')



def add_client_view(request ):
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


def sending_email(request, slug):
    invoices = Invoice.objects.all()
    obj = Invoice.objects.get(slug=slug)
    articles = obj.reimburservice_set.all()
    proservices = obj.profservice_set.all()
    case = Case.objects.get(pk=obj.case_id)
    clients = ClientRecord.objects.get(pk= case.clients_id)
    context = {'obj' : obj,
               'articles': articles,
               'case' : case,
               'clients' : clients,
               'proservices' : proservices,
               'invoices' : invoices
               }
    name = clients.full_name
    email = clients.email
    email_message = 'Greeting, This is my EMAIL TESTING HERE'
    send_mail(name,
              email_message,
              'settings.EMAIL_HOST_USER',
              [email],
              fail_silently=False)
    
    return render(request, "main/invoice/invoice_list.html", context)


    