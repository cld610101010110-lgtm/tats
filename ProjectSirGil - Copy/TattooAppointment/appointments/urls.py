from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # PUBLIC PAGES (NO LOGIN REQUIRED)
    path('landing/', views.landing_page, name='landing'),
    path('enquiry/submit/', views.enquiry_submit, name='enquiry_submit'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Protected appointment URLs (REQUIRE LOGIN)
    path('', views.index, name='index'),  # Dashboard at /appointments/
    path('new/', views.appointment_create, name='create'),
    path('manage/', views.manage_appointments, name='manage'),
    path('status/<int:pk>/', views.update_appointment_status, name='update-status'),
    path('list-fbv/', views.appointment_list_fbv, name='list-fbv'),
    path('list-cbv/', views.AppointmentListCBV.as_view(), name='list-cbv'),

    # Edit and Delete URLs
    path('edit/<int:pk>/', views.appointment_edit, name='edit'),
    path('delete/<int:pk>/', views.appointment_delete, name='delete'),
]