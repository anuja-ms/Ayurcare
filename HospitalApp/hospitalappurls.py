from django.urls import path
from HospitalApp import views
urlpatterns = [
    path('index1/',views.index1, name='index1'),
    path('packageinsert/',views.packageinsert,name='packageinsert'),
    path('serviceinsert/',views.serviceinsert,name='serviceinsert'),
    path('viewpackage',views.viewpackage,name='viewpackage'),
    path('viewservice',views.viewservice,name='viewservice'),
    path('deletepackage/<package_id>',views.deletepackage,name='deletepackage'),
    path('deleteservice/<service_id>',views.deleteservice,name='deleteservice'),
    path('packageservice/',views.packageservice,name='packageservice'),
    path('manage-booking/', views.manage_booking, name='manage_booking'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('packageserviceview/', views.packageserviceview, name='packageserviceview'),
    path('payment_information/', views.payment_information, name='payment_information'),
    path('editpackage/<int:package_id>/', views.editpackage, name="editpackage"),
    path('editservice/<int:service_id>/', views.editservice, name='editservice'),
    path('fillpackservice',views.fillpackservice,name='fillpackservice'),
    path('profile/', views.hospital_profile, name='hospital_profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('hospital/view_feedback/', views.view_feedback, name='view_feedback'),
    path('hospital_password/', views.hospital_password, name='hospital_password'), 
]