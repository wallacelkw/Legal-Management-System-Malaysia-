from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path("register/", views.register_user, name="register"),

    # viewing for displaying
    path("", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin_setting/", views.admin_setting, name="admin_setting"),

    path("add_client_to_db/", views.add_client_to_db, name="add_client_to_db"),
    path(
        "add_client_view/", views.add_client_view, name="add_client_view"
    ),
    path(
        "view_all_client/", views.view_all_client, name="view_all_client"
    ),
    path("update_the_client/<int:pk>", views.update_client, name="update_client"),
    path("delete_the_client/<int:pk>", views.delete_client, name="delete_client"),
    path("single_client/<int:pk>/", views.single_client, name="single_client"),

    # CREATE CASES TYPE
    path("client_role/", views.client_role, name="client_role"),
    path("add_client_role/", views.add_client_role, name="add_client_role"),
    path("delete_client_role/<int:pk>/", views.delete_client_role, name="delete_client_role"),
    path("update_client_role/<int:pk>/", views.update_client_role, name="update_client_role"),
    # CREATE COURT TYPE
    path("court_type/", views.court_type, name="court_type"),
    path("add_court_type/", views.add_court_type, name="add_court_type"),
    path(
        "delete_court_type/<int:pk>/", views.delete_court_type, name="delete_court_type"
    ),
    path(
        "update_court_type/<int:pk>/", views.update_court_type, name="update_court_type"
    ),
    # CASES
    path("list_case/", views.list_case, name="list_case"),
    path("create_case_view/", views.create_case_view, name="create_case_view"),
    path("create_case_detail/", views.create_case_detail, name="create_case_detail"),
    path("update_case/<int:pk>/", views.update_case_client, name="update_case_client"),
    path("delete_case_client/<int:pk>/", views.delete_case, name="delete_case_client"),
    path("single_case_client/<int:pk>/", views.single_case_client, name="single_case_client"),



    # INVOICE
    path('invoices/', views.view_invoice, name='invoices'),
    path('invoices/create',views.createInvoice, name='create-invoice'),
    path('invoices/create-build/<slug:slug>',views.createBuildInvoice, name='create-build-invoice'),
    path('invoices/update-build/<slug:slug>',views.updateBuildInvoice, name='update-build-invoice'),
    # path('pdf/<int:pk>', views.generate_pdf_invoice, name="generate-pdf"),
    path('sending_email/<slug:slug>', views.sending_email, name="sending_email"),
    path('invoices/pdf-build/<int:pk>',views.generate_pdf_invoice, name='generate_pdf_invoice'),

    #Delete an invoice
    path('invoices/create-build/deleteProfS/<slug:slug>/', views.deleteProfService, name='delete_prof'),
    path('invoices/create-build/deleteReimburS/<slug:slug>/', views.deleteReimburService, name='delete_reimbur'),
    path('invoices/delete/<slug:slug>',views.deleteInvoice, name='delete-invoice'),

    path('pdf_invoice/<int:pk>/', views.PDFInvoiceView, name='pdf_invoice'),

    path('balance_sheet/', views.balance_sheet, name='balance_sheet'),
    
  
]
