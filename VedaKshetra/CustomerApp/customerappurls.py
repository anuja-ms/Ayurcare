from django.urls import path
from CustomerApp import views
urlpatterns = [
    path('index/',views.index, name='index'),
    path('fillhospital',views.fillhospital,name='fillhospital'),
    path('hospitalview',views.hospitalview, name='hospitalview'),
    path('singleview/<hospital_id>',views.singleview,name='singleview'),
    path('packageview/<id>',views.packageview, name='packageview'),
    path('serviceview/<id>',views.serviceview, name='serviceview'),
    path('packagebooking/<id>',views.packagebooking, name='packagebooking'),
    path('service_detail/<service_id>', views.service_detail, name='service_detail'),
    path('insertbooking/<id>',views.insertbooking, name='insertbooking'),
    path('booking_status/', views.booking_status, name='booking_status'),
    path('cancel-policy/<int:booking_id>/', views.cancel_policy, name="cancel_policy"),
    path('payment/<int:booking_id>/', views.payment_page, name='payment'),
    path('profile/', views.customer_profile, name='customer_profile'),
    path('cprofile_edit/', views.cprofile_edit, name='cprofile_edit'),
    path("customer_feedback/<booking_id>/", views.customer_feedback, name="customer_feedback"), 
    path('logout/', views.logout, name='logout'),
    path('process-cancellation/<int:booking_id>/', views.process_cancellation, name="process_cancellation"),
    path('change-password/', views.change_password, name='change_password'),
]   