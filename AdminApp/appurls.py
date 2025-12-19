from django.urls import path
from AdminApp import views

from .views import ExportExcelPayment

urlpatterns = [
    path('adminhome/',views.adminhome, name='adminhome'),
    path('district',views.district,name='district'),
    path('district_process',views.district_process,name='district_process'),
    path('viewdistrict',views.viewdistrict,name='viewdistrict'),
    path('deletedistrict/<district_id>',views.deletedistrict,name='deletedistrict'),
    path('location',views.location,name='location'),
    path('location_process',views.location_process,name='location_process'),
    path('viewlocation',views.viewlocation,name='viewlocation'),
    path('filllocation',views.filllocation,name='filllocation'),
    path('deletelocation/<location_id>',views.deletelocation,name='deletelocation'),
    path('viewhospital',views.viewhospital,name='viewhospital'),
    path('singleview1/<hospital_id>',views.singleview1,name='singleview1'),
    path('accept_hospital/<hospital_id>', views.accept_hospital, name='accept_hospital'),
    path('reject_hospital/<hospital_id>', views.reject_hospital, name='reject_hospital'),
    path('editlocation/<location_id>',views.editlocation,name='editlocation'),
    path('editdistrict/<district_id>',views.editdistrict,name='editdistrict'),
    path('admin_earnings/', views.admin_earnings, name='admin_earnings'),
    path('hospital-pie-chart/', views.hospital_approval_pie_chart, name='hospital_pie_chart'),
    path('package_bar_chart/', views.package_bar_chart, name='package_bar_chart'),
    path('customer_bar_chart/', views.customer_bar_chart, name='customer_bar_chart'),
    path('feedback_pie_chart/', views.feedback_pie_chart, name='feedback_pie_chart'),
    path('ExportExcelPayment/', ExportExcelPayment.as_view(), name='ExportExcelPayment'),
    path('payment_report/', views.payment_report, name='payment_report'),
    path('feedbackview/', views.feedbackview, name='feedbackview'),
]