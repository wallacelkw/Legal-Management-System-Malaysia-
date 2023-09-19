from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CaseType, CourtType, Case, ClientRecord, Invoice, ReimburService, ProfService
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


class AddCaseType(forms.ModelForm):
    case_type = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Cases Type"}
        ),
    )
    case_description = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Description"}
        ),
    )

    class Meta:
        model = CaseType
        exclude = ("user",)


class AddCourtType(forms.ModelForm):
    court_type = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Cases Type"}
        ),
    )
    court_description = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Description"}
        ),
    )

    class Meta:
        model = CourtType
        exclude = ("user",)

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = '__all__'



class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude= ('saved_by',
                  'paid')
        
        widgets = {
            'short_descriptions': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),


        }

class ReimburServiceForm(forms.ModelForm):

    class Meta:
        model = ReimburService
        fields = '__all__'
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
        fields = '__all__'
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