from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from AdminApp.models import tbl_district,tbl_location
from GuestApp.models import tbl_hospital,tbl_login
from CustomerApp.models import tbl_payment,tbl_booking,tbl_feedback
from HospitalApp.models import tbl_package
from email.message import EmailMessage
import smtplib
from django.db.models import Count
import xlwt
from django.views.generic import View
from django.views.decorators.cache import cache_control
from datetime import datetime

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminhome(request):
    login_id = request.session.get('login_id')

    if login_id:
        # ✅ Fetch hospital approval status
        hospital_labels = []
        hospital_data = []
        hospital_queryset = tbl_hospital.objects.values('login_id__status').annotate(total=Count('hospital_id'))

        for entry in hospital_queryset:
            hospital_labels.append(entry['login_id__status'])  # Fetch status from Login model
            hospital_data.append(entry['total'])

        # ✅ Fetch feedback ratings distribution
        feedback_labels = []
        feedback_data = []
        feedback_queryset = tbl_feedback.objects.values('rating').annotate(total=Count('feedback_id'))

        for entry in feedback_queryset:
            feedback_labels.append(f"{entry['rating']} Stars")  # Dynamic labels
            feedback_data.append(entry['total'])  # Dynamic data

        # ✅ Fetch customer booking data
        booking_labels = []
        booking_data = []
        booking_queryset = tbl_booking.objects.values('customer_id__customer_name').annotate(total=Count('booking_id'))

        for entry in booking_queryset:
            booking_labels.append(entry['customer_id__customer_name'])  # Customer Name
            booking_data.append(entry['total'])  # Total Bookings

        return render(request, 'Admin/adminhome.html', {
            'hospital_labels': hospital_labels,
            'hospital_data': hospital_data,
            'feedback_labels': feedback_labels,
            'feedback_data': feedback_data,
            'booking_labels': booking_labels,
            'booking_data': booking_data,
        })

    else:
        return HttpResponse("<script>alert('Authentication Required. Please log in first');window.location='/login';</script>")

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def district(request):
    login_id=request.session.get('login_id')
    if login_id:
        return render(request,'Admin/district.html')
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def district_process(request):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method=='POST':
            dname=request.POST.get("disname")
            cob=tbl_district()
            cob.district_name=dname 
            if tbl_district.objects.filter(district_name=dname).exists():
                return HttpResponse("<script>alert('Already Exixts..');window.location='/adminapp/district';</script>")
            else:
                cob.save() #insert query
                return HttpResponse("<script>alert('sucessfully inserted..');window.location='/adminapp/district';</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewdistrict(request):
    login_id=request.session.get('login_id')
    if login_id:
        district=tbl_district.objects.all()
        return render(request,'Admin/viewdistrict.html',{'district':district})   
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedistrict(request,district_id):
    login_id=request.session.get('login_id')
    if login_id:
        cob=tbl_district.objects.get(district_id=district_id)
        cob.delete()
        return HttpResponse("<script>alert('Successfully Deleted..');window.location='/adminapp/viewdistrict'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def location(request):
    login_id=request.session.get('login_id')
    if login_id:
        districts=tbl_district.objects.all()
        return render(request,'Admin/location.html',{'districts':districts}) 
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def location_process(request):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method=='POST':
            district_id=request.POST.get("district_id")
            lname=request.POST.get("lname")
            lob=tbl_location()
            lob.location_name=lname
            lob.district_id=tbl_district.objects.get(district_id=district_id)
            if tbl_location.objects.filter(location_name=lname,district_id=district_id).exists():
                return HttpResponse("<script>alert('Already Exixts..');window.location='/adminapp/location';</script>")
            else:
                lob.save() #insert query
                return HttpResponse("<script>alert('sucessfully inserted..');window.location='/adminapp/location';</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewlocation(request):
    login_id=request.session.get('login_id')
    if login_id:
        district=tbl_district.objects.all()
        return render(request,'Admin/viewlocation.html',{'district':district})   
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    login_id=request.session.get('login_id')
    if login_id:
        did=int(request.POST.get("did"))
        location=tbl_location.objects.filter(district_id=did).values()
        return JsonResponse(list(location),safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletelocation(request,location_id):
    login_id=request.session.get('login_id')
    if login_id:
        lob=tbl_location.objects.get(location_id=location_id)
        lob.delete()
        return HttpResponse("<script>alert('Successfully Deleted..');window.location='/adminapp/viewlocation'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewhospital(request):
    login_id=request.session.get('login_id')
    if login_id:
        hospital=tbl_hospital.objects.filter(login_id__status='Not Confirmed')
        return render(request,'Admin/viewhospital.html',{'hospital':hospital})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def singleview1(request,hospital_id):
    login_id=request.session.get('login_id')
    if login_id:
        hospital=tbl_hospital.objects.get(hospital_id=hospital_id)
        return render(request,"Admin/singleview1.html",{'hospital':hospital})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def accept_hospital(request, hospital_id):
    login_id=request.session.get('login_id')
    if login_id:
        login=tbl_login.objects.get(login_id=hospital_id)
        hospital = tbl_hospital.objects.get(login_id=login)
        mailid = hospital.email
        hos_name=hospital.hospital_name
        login.status='Confirmed'
        login.save()
        msg = EmailMessage()
        msg.set_content(f"""
    Dear {hos_name},

    Namaste! 🌿

    We are pleased to inform you that your registration with VedaKshetra has been successfully verified and approved. You can now start offering your Ayurvedic treatments and services to customers seeking holistic healing.

    What’s Next?
    ✅ Login to your dashboard: Manage bookings, update services, and track payments.
    ✅ List your treatments: Attract customers by showcasing your unique Ayurveda therapies.
    ✅ Start receiving bookings: Engage with customers and provide quality healthcare services.

    🔗 Access your account here: [Login Link]

    If you have any questions or need support, feel free to reach out to us. We look forward to working with you in spreading authentic Ayurvedic wellness!

    Best Regards,
    Team VedaKshetra

    """)
        msg['Subject'] = "Registration Completed"
        msg['from'] = 'adithyasunil5002@gmail.com'
        msg['To'] = {mailid}
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('adithyasunil5002@gmail.com','byvn azdc ftlh ezbk')
            smtp.send_message(msg)
        return viewhospital(request)
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject_hospital(request, hospital_id):
    login_id=request.session.get('login_id')
    if login_id:
        login=tbl_login.objects.get(login_id=hospital_id)
        hospital = tbl_hospital.objects.get(login_id=login)
        mailid = hospital.email
        hos_name=hospital.hospital_name
        login.status='Rejected'
        login.save()
        msg = EmailMessage()
        msg.set_content(f"""
    Dear {hos_name},

    Thank you for your interest in partnering with VedaKshetra. After reviewing your application, we regret to inform you that your registration request has been rejected due to [reason for rejection].
    If you believe this decision was made in error or if you have any questions, please feel free to reach out to us at [support email].
    We appreciate your time and effort, and we encourage you to reapply in the future if the necessary criteria are met.
    Best regards,
    VedaKshetra Team
    """)
        msg['Subject'] = "Registration Completed"
        msg['from'] = 'adithyasunil5002@gmail.com'
        msg['To'] = {mailid}
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('adithyasunil5002@gmail.com','byvn azdc ftlh ezbk')
            smtp.send_message(msg)
        return viewhospital(request)
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
         


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editlocation(request,location_id):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method=='POST':
            lname=request.POST.get("txtlocation")
            loc = tbl_location.objects.get(location_id=location_id)
            loc.location_name = lname
            loc.save()
            return viewlocation(request)
        loc=tbl_location.objects.get(location_id=location_id)
        return render(request,"Admin/editlocation.html",{'loc':loc})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)        
def editdistrict(request,district_id):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method=='POST':
            dname=request.POST.get("txtdis")
            dl = tbl_district.objects.get(district_id=district_id)
            dl.district_name = dname
            dl.save()
            return viewdistrict(request)
        dl=tbl_district.objects.get(district_id=district_id)
        return render(request,"Admin/editdistrict.html",{'dl':dl})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_earnings(request):
    login_id=request.session.get('login_id')
    if login_id:
        bookings = tbl_booking.objects.filter(status="Paid")  # Fetch only paid bookings
        earnings = []

        total_commission = 0  # To track total earnings

        for booking in bookings:
            quarter_payment = booking.t_amount / 4  # 1/4th Payment
            admin_commission = round(quarter_payment * 0.05, 2)  # 5% of 1/4 payment
            hospital_amount = round(quarter_payment - admin_commission, 2)  # Amount hospital receives

            total_commission += admin_commission  # Accumulate total earnings

            earnings.append({
                'booking_id': booking.booking_id,
                'customer': booking.customer_id.customer_name,
                'package': booking.package_id.package_name,
                'total_amount': booking.t_amount,
                'quarter_payment': quarter_payment,
                'admin_commission': admin_commission,
                'hospital_amount': hospital_amount,
                'payment_status': "Paid"
            })

        return render(request, 'Admin/admin_earnings.html', {
            'earnings': earnings,
            'total_commission': total_commission
        })
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
         


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospital_approval_pie_chart(request):
    labels = []
    data = []
    
    queryset = tbl_hospital.objects.values('login_id__status').annotate(total=Count('hospital_id'))

    for entry in queryset:
        labels.append(entry['login_id__status'])  # Fetch status from Login model
        data.append(entry['total'])

    return render(request, 'Admin/hospital_pie_chart.html', {
        'labels': labels,
        'data': data,
    })
   
    
        
         



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def package_bar_chart(request):
    labels = []
    data = []

    # Query: Count total bookings per package
    queryset = tbl_booking.objects.values('package_id__package_name').annotate(total=Count('booking_id'))

    for entry in queryset:
        labels.append(entry['package_id__package_name'])
        data.append(entry['total'])

    return render(request, 'admin/package_bar_chart.html', {
        'labels': labels,
        'data': data,
    })
    
        


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_bar_chart(request):
    labels = []
    data = []

    # Query: Count total bookings per customer
    queryset = tbl_booking.objects.values('customer_id__customer_name').annotate(total=Count('booking_id'))
    
    for entry in queryset:
        labels.append(entry['customer_id__customer_name'])  # Customer Name
        data.append(entry['total'])  # Total Bookings

    return render(request, 'Admin/customer_bar_chart.html', {
        'labels': labels,
        'data': data,
    })
    
    
       


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedback_pie_chart(request):
    labels = []
    data = []

    # Fetch ratings and count occurrences
    queryset = tbl_feedback.objects.values('rating').annotate(total=Count('feedback_id'))

    for entry in queryset:
        labels.append(f"{entry['rating']} Stars")  # Dynamic labels
        data.append(entry['total'])  # Dynamic data

    return render(request, 'Admin/feedback_pie_chart.html', {
        'labels': labels,
        'data': data,
    })
        
    

# View the payment report in an HTML page


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_report(request):
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)

    payments = tbl_payment.objects.select_related('booking_id__customer_id')

    if from_date and to_date:
        payments = payments.filter(payment_date__range=[from_date, to_date])
    else:
        from_date, to_date = "", ""  # Reset dates if no filter applied

    context = {
        'payments': payments,
        'from_date': from_date,
        'to_date': to_date
    }
    return render(request, 'Admin/payment_report.html', context)

        

# Export the payment report to Excel


class ExportExcelPayment(View):
    def get(self, request):
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="payment_report_{from_date}_to_{to_date}.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Payment Report')

        # Define column headings
        row_num = 0
        columns = ['Payment ID', 'Booking ID', 'Customer Name', 'Amount', 'Status', 'Payment Date']
        style = xlwt.easyxf('font: bold 1')

        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title, style)

        # Fetch payment data
        payments = tbl_payment.objects.select_related('booking_id__customer_id').values_list(
            'payment_id', 'booking_id__booking_id', 'booking_id__customer_id__customer_name',
            'booking_id__t_amount', 'status', 'payment_date'
        )

        # Filter by date range if provided
        if from_date and to_date:
            try:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()

                if from_date_obj <= to_date_obj:
                    payments = payments.filter(payment_date__range=[from_date_obj, to_date_obj])
                else:
                    payments = []  # Return empty if invalid date range
            except ValueError:
                payments = []  # Return empty if invalid date format

        # Write data to Excel
        for row in payments:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                if isinstance(cell_value, (str, int, float)):
                    ws.write(row_num, col_num, cell_value)
                elif hasattr(cell_value, 'strftime'):
                    ws.write(row_num, col_num, cell_value.strftime('%Y-%m-%d'))
                else:
                    ws.write(row_num, col_num, str(cell_value))

        wb.save(response)
        return response

            
        
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.clear()
    return redirect('/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def feedbackview(request):
    if 'login_id' in request.session:
        hospitals = tbl_hospital.objects.all()  # Fetch all hospitals
        selected_hospital_id = request.GET.get('hospital_id')

        if selected_hospital_id:
            feedbacks = tbl_feedback.objects.filter(
                package_id__hospital_id=selected_hospital_id
            ).select_related('customer_id', 'package_id')
        else:
            feedbacks = None  # No feedbacks initially

        return render(request, 'Admin/feedbackview.html', {
            'hospitals': hospitals,
            'feedbacks': feedbacks,
            'selected_hospital_id': selected_hospital_id
        })
    else:
        return HttpResponse("<script>alert('Authentication Required. Please login first');window.location='/login';</script>")
