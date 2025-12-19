from django.urls import path

from GuestApp import views
urlpatterns = [
   
    path('login',views.login,name='login'),
    path('login_process',views.login_process,name='login_process'),
    path('hospitalreg/',views.hospitalreg,name='hospitalreg'),
    path('',views.index2, name='index2'),
    path('hospitalreg_process',views.hospitalreg_process,name='hospitalreg_process'),
    path('customerreg/',views.customerreg,name='customerreg'),
    path('customerreg_process',views.customerreg_process,name='customerreg_process'),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-security-answer/", views.verify_security_answer, name="verify_security_answer"),
    path("reset-password-process/", views.reset_password_process, name="reset_password_process"),
]