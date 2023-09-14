from django.urls import path
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path("register/", views.register_user, name="register"),

    # viewing for displaying
    path("", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("dashboard/<str:username>", views.dashboard, name="dashboard"),
    

    path("add_client_to_db/", views.add_client_to_db, name="add_client_to_db"),
    path(
        "add_client_view/<str:username>", views.add_client_view, name="add_client_view"
    ),
    path(
        "view_all_client/<str:username>", views.view_all_client, name="view_all_client"
    ),
    path("update_the_client/<int:pk>", views.update_client, name="update_client"),
    path("delete_the_client/<int:pk>", views.delete_client, name="delete_client"),
    # CREATE CASES TYPE
    path("case_type/<str:username>", views.case_type, name="case_type"),
    path("add_case_type/", views.add_case_type, name="add_case_type"),
    path("delete_case_type/<int:pk>/", views.delete_case_type, name="delete_case_type"),
    path("update_case_type/<int:pk>/", views.update_case_type, name="update_case_type"),
    # CREATE COURT TYPE
    path("court_type/<str:username>", views.court_type, name="court_type"),
    path("add_court_type/", views.add_court_type, name="add_court_type"),
    path(
        "delete_court_type/<int:pk>/", views.delete_court_type, name="delete_court_type"
    ),
    path(
        "update_court_type/<int:pk>/", views.update_court_type, name="update_court_type"
    ),
    # CASES
    path("list_case/<str:username>", views.list_case, name="list_case"),
    path("create_case_view/<str:username>/", views.create_case_view, name="create_case_view"),
    path("create_case_detail/", views.create_case_detail, name="create_case_detail"),
    path("update_case/<int:pk>/", views.update_case_client, name="update_case_client"),
    path("delete_case_client/<int:pk>/", views.delete_case, name="delete_case_client"),
    path("single_case_client/<int:pk>/", views.single_case_client, name="single_case_client"),



    # INVOICE
    # path("view_invoice/<str:username>/", views.view_invoice, name="view_invoice"),
    path('view_invoice/', views.InvoiceList.as_view(), name='view_invoice'),
    path('create_invoice/', views.InvoiceCreate.as_view(), name='create_invoice'),
    path('update/<int:pk>/', views.ProductUpdate.as_view(), name='update_invoice'),
    path('delete-services/<int:pk>/', views.delete_reimbur, name='delete_reimbur'),
    path('delete-prof_services/<int:pk>/', views.delete_proservice, name='delete_proservice'),
    path('pdf_invoice/<int:pk>/', views.PDFInvoiceView, name='pdf_invoice'),
  
]
