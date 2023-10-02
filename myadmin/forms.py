from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import ClientRole, CourtType, Case, ClientRecord, Invoice, ReimburService, ProfService
from django.forms import formset_factory
from django.forms import inlineformset_factory


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        ),
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""
        self.fields[
            "username"
        ].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""
        self.fields[
            "password1"
        ].help_text = "<ul class=\"form-text text-muted small\"><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul>"

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""
        self.fields[
            "password2"
        ].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


class AddClientForm(forms.ModelForm):
    class Meta:
        model = ClientRecord
        fields = (
            "full_name",
            "identity",
            "gender",
            "phone_number",
            "email",
            "address1",
            "address2",
            "city",
            "postcode",
            "state",
            "country",
            "agent_fullname",
            "agent_ph",
            "agent_identity",
            "remark",
            "latitude",
            "longitude"
        )


# Create Add Record Form
class AddRecordsForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "First Name", "class": "form-control"}
        ),
        label="",
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Last Name", "class": "form-control"}
        ),
        label="",
    )
    gender = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Gender", "class": "form-control"}
        ),
        label="",
    )
    date_of_birth = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Date of Birth", "class": "form-control"}
        ),
        label="",
    )
    phone_number = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Phone Number", "class": "form-control"}
        ),
        label="",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        label="",
    )

    # customer address
    address1 = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Address 1", "class": "form-control"}
        ),
        label="",
    )
    address2 = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Address 2", "class": "form-control"}
        ),
        label="",
    )
    city = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "City", "class": "form-control"}
        ),
        label="",
    )
    state = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "State", "class": "form-control"}
        ),
        label="",
    )
    postcode = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Postcode", "class": "form-control"}
        ),
        label="",
    )
    country = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Country Name", "class": "form-control"}
        ),
        label="",
    )

    # emergency contact
    emergency_contact_full_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Full Name", "class": "form-control"}
        ),
        label="",
    )
    emergency_contact_relationship = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Relationship", "class": "form-control"}
        ),
        label="",
    )
    emergency_contact_phone_number = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "EC Phone Number", "class": "form-control"}
        ),
        label="",
    )
    emergency_contact_email = forms.EmailField(
        required=True,
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "Email", "class": "form-control"}
        ),
        label="",
    )

    class Meta:
        model = ClientRecord
        exclude = ("user",)


class AddClientRole(forms.ModelForm):
    class Meta:
        model = ClientRole
        exclude = ("user",)


class AddCourtType(forms.ModelForm):
    class Meta:
        model = CourtType
        exclude = ("user",)

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'

class updateInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(updateInvoiceForm, self).__init__(*args, **kwargs)
        # Customize the label for the 'short_descriptions' field
        self.fields['short_descriptions'].label = 'Description'
        self.fields['case'].label = ''
    class Meta:
        model = Invoice
        exclude = ('saved_by', 'paid',)
        fields = ["case", "short_descriptions"]
        widgets = {
            'short_descriptions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required': 'required',
            
                }
            ),
            'case': forms.TextInput(  # Render as plain text
                attrs={
                    'style': 'display: none;',
                }
            )
        }


class InvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.custom_choices = [('-----', '--Select a Case--')]
        # Extract unique identifiers from Invoice objects in invoice_data
        invoice_data = [i.case.ref_no for i in Invoice.objects.all() if i.case]
        case_data = [str(j.ref_no) for j in Case.objects.all()]
    
        # Check for duplicates
        set1 = set(invoice_data)
        set2 = set(case_data)
        items_not_in_list1 = list(set2 - set1)

        for case in items_not_in_list1:
            d_t = (case, case)
            self.custom_choices.append(d_t)
        
        for i in Invoice.objects.all():
            print(i)
        
        self.fields['short_descriptions'].label = 'Description'
        self.fields['case'] = forms.ChoiceField(
                                        label='Choose a Case',
                                        choices = self.custom_choices,
                                        widget=forms.Select(attrs={'class': 'form-control'}),)
        



    class Meta:
        model = Invoice
        exclude= ('saved_by',
                  'paid',)
        
        fields = ["case", "short_descriptions"]
        widgets = {

            'short_descriptions': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'required' : 'required'
                    }
                ),
            'case' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'label' : 'Reference No'
                }
            )
        }

    def clean_case(self):
        c_case = self.cleaned_data['case']
        print(c_case)
        if c_case == '-----':
            print('HARD-------')
            return False
        else:
             # Get the existing Case instance associated with the Invoice
            invoice_instance = self.instance  # Get the current instance of the form
            print("INSTANCES : ",invoice_instance)
            if invoice_instance and invoice_instance.case:
                return invoice_instance.case
            else:
                return Case.objects.get(ref_no=c_case)



class ReimburServiceForm(forms.ModelForm):

    class Meta:
        model = ReimburService
        fields = ['reimbur_service', 'reimbur_service_price']
        widgets = {
            'service': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),

            'unit_price': forms.NumberInput(
            attrs={
                'onblur': 'findTotal_uniPrice()',
                'class' : 'unit_price'
                }
            ),
         
        }

class ProfServiceForm(forms.ModelForm):

    class Meta:
        model = ProfService
        fields = ['prof_service', 'prof_service_price']
        widgets = {
            'prof_service': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'prof_service_price' : forms.NumberInput(
            attrs={
                'onblur' : 'findTotal_proPrice()',
                'class' : 'prof_service_price'
                }
            ),
        }


# LineItemFormset = formset_factory(LineItemForm, extra=1)
ProfServiceFormSet = inlineformset_factory(Invoice, ProfService,form = ProfServiceForm,extra=1, can_delete=True, can_delete_extra=True)
ReimburServiceFormSet = inlineformset_factory(Invoice, ReimburService,form = ReimburServiceForm,extra=1, can_delete=True, can_delete_extra=True)
# CaseInvoiceFormSet = inlineformset_factory(Case, Invoice,form =InvoiceForm,extra=1, can_delete=True, can_delet_extra=True)




# class CaseSelectForm(forms.ModelForm):

#     def __init__(self,*args,**kwargs):
#         self.initial_case = kwargs.pop('initial_case')
#         self.CASE_LIST = Case.objects.all()
#         self.INVOICE_LIST = Invoice.objects.all()
#         self.CASE_CHOICES = [('-----', '--Select a Case--')]
#         self.CHECK_DUPLICATE_CASE =[]

      
#         # for case in self.CASE_LIST:
#         #     d_t = (case.ref_no, case.ref_no)
#         #     self.CASE_CHOICES.append(d_t)


#         super(CaseSelectForm,self).__init__(*args,**kwargs)

#         # Extract unique identifiers from Invoice objects in invoice_data
#         invoice_data = [i.case.ref_no for i in Invoice.objects.all() if i.case]
#         case_data = [str(j.ref_no) for j in Case.objects.all()]
    
#         # Check for duplicates
#         set1 = set(invoice_data)
#         set2 = set(case_data)

#         items_not_in_list1 = list(set2 - set1)
    
#         for case in items_not_in_list1:
#             d_t = (case, case)
#             self.CASE_CHOICES.append(d_t)

     
#         # self.fields['ref_no'].queryset = Invoice.objects.exclude(uniqueId=initial_case.uniqueId)
#         self.fields['ref_no'] = forms.ChoiceField(
#                                         label='Choose a related Case',
#                                         choices = self.CASE_CHOICES,
#                                         widget=forms.Select(attrs={'class': 'form-control'}),)

#     class Meta:
#         model = Case
#         fields = ['ref_no']


#     def clean_case(self):
#         c_case = self.cleaned_data['ref_no']
#         if c_case == '-----':
#             return self.initial_case
#         else:
#             return Case.objects.get(uniqueId=c_case)



