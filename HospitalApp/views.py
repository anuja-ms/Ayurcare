from django.shortcuts import render,redirect,get_object_or_404
from GuestApp.models import tbl_hospital,tbl_login
from HospitalApp.models import tbl_package,tbl_service,tbl_packageservice,tbl_service
from CustomerApp.models import tbl_booking,tbl_payment,tbl_feedback
from django.http import HttpResponse,JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.urls import reverse


# Create your views here.
def index1(request):
    login_id=request.session.get('login_id')
    if login_id:
        return render(request,'Hospital/index1.html')
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packageinsert(request):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method == 'POST':
            package = request.POST.get("package_name")
            days = request.POST.get("noofdays")
            hospital_id = tbl_hospital.objects.get(login_id=request.session['login_id'])
            pck_obj = tbl_package()
            pck_obj.package_name = package
            pck_obj.image = request.FILES["image"]
            pck_obj.noofdays = days
            pck_obj.hospital_id = hospital_id
            pck_obj.save()
            return HttpResponse("<script>alert('Successfully Inserted..'); window.location='/hospitalapp/packageinsert/';</script>")
        return render(request, "Hospital/packageinsert.html")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def serviceinsert(request):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method=='POST':
            service=request.POST.get("service_name")
            amount=request.POST.get("amount")
            description=request.POST.get("description")
            hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
            sck_obj=tbl_service()
            sck_obj.service_name=service
            sck_obj.image=request.FILES["image"]
            sck_obj.amount=amount
            sck_obj.description=description
            sck_obj.hospital_id=hospital_id
            sck_obj.save()
            return HttpResponse("<script>alert('Successfully Inserted..'); window.location='/hospitalapp/serviceinsert/';</script>")
        return render(request, "Hospital/serviceinsert.html")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpackage(request):
    login_id=request.session.get('login_id')
    if login_id:
        hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
        pck=tbl_package.objects.filter(hospital_id=hospital_id)
        return render(request,"Hospital/viewpackage.html",{'pck':pck})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewservice(request):
    login_id=request.session.get('login_id')
    if login_id:
        hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
        sck=tbl_service.objects.filter(hospital_id=hospital_id)
        return render(request,"Hospital/viewservice.html",{'sck':sck})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletepackage(request,package_id):
    login_id=request.session.get('login_id')
    if login_id:
        pck=tbl_package.objects.get(package_id=package_id)
        pck.delete()
        return HttpResponse("<script>alert('Successfully Deleted..');window.location='/hospitalapp/viewpackage'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteservice(request,service_id):
    login_id=request.session.get('login_id')
    if login_id:
        sck=tbl_service.objects.get(service_id=service_id)
        sck.delete()
        return HttpResponse("<script>alert('Successfully Deleted..');window.location='/hospitalapp/viewservice'</script>")
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packageservice(request):
    login_id=request.session.get('login_id')
    if login_id:
        log_id = request.session['login_id']
        hospital = tbl_hospital.objects.get(login_id=log_id)

        if request.method == 'POST':
            pckid = request.POST.get('ddlpackage')
            serid = request.POST.get('ddlservice')

            if pckid and serid:
                p = tbl_package.objects.get(package_id=pckid)
                s = tbl_service.objects.get(service_id=serid)
                p_obj = tbl_packageservice()
                p_obj.package_id = p
                p_obj.service_id = s
                p_obj.save()

                return HttpResponse("<script>alert('Successfully Inserted..'); window.location='/hospitalapp/packageservice/';</script>")

        p = tbl_package.objects.filter(hospital_id=hospital)
        s = tbl_service.objects.filter(hospital_id=hospital)

        return render(request, "Hospital/packageservice.html", {'package': p, 'service': s})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpackageservice(request):
    login_id=request.session.get('login_id')
    if login_id:
        hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
        pck=tbl_packageservice.objects.filter(package_id=package_id)
        return render(request,"Hospital/viewpackageservice.html",{'pck':pck})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manage_booking(request):
    login_id = request.session.get('login_id')
    if login_id:
        log_id = request.session.get('login_id')  # Get logged-in hospital's login ID
        hospital = tbl_hospital.objects.get(login_id=log_id)  # Get the corresponding hospital
        bookings = tbl_booking.objects.filter(package_id__hospital_id=hospital)  # Filter bookings by hospital

        active_bookings = []  # Store active bookings
        cancelled_bookings = []  # Store cancelled bookings

        for booking in bookings:
            if booking.t_amount is not None:
                total_amount = float(booking.t_amount)  # Convert to float
                quarter_payment = round(total_amount / 4, 2)  # 1/4th Payment
                admin_commission = round(quarter_payment * 0.05, 2)  # 5% of 1/4 payment
                hospital_amount = round(quarter_payment - admin_commission, 2)  # Hospital receives after admin cut
            else:
                quarter_payment = 0
                admin_commission = 0
                hospital_amount = 0

            booking_data = {
                'booking': booking,
                'hospital_amount': hospital_amount,  # Correct hospital amount
                'admin_commission': admin_commission,  # Not shown to hospital, but correct in admin logs
            }

            if booking.status == "Cancelled":
                cancelled_bookings.append(booking_data)
            else:
                active_bookings.append(booking_data)

        return render(request, 'Hospital/manage_booking.html', {
            'active_bookings': active_bookings,
            'cancelled_bookings': cancelled_bookings
        })

    else:
        return HttpResponse("<script>alert('Authentication Required, please login first');window.location='/login';</script>")



# View for accepting a booking
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def accept_booking(request, booking_id):
    login_id=request.session.get('login_id')
    if login_id:
        booking = get_object_or_404(tbl_booking, booking_id=booking_id)
        booking.status = "Accepted"  # Update booking status to 'Accepted'
        booking.save()  # Save the changes
        return redirect('manage_booking')  # Redirect back to manage bookings page
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           
# View for rejecting a booking with a reason

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reject_booking(request, booking_id):
    login_id=request.session.get('login_id')
    if login_id:
        booking = get_object_or_404(tbl_booking, booking_id=booking_id)  # Get the booking by ID
        if request.method == "POST":  # Ensure it's a POST request
            reason = request.POST.get('reason')  # Get the rejection reason from the form
            booking.status = "Rejected"  # Update booking status to 'Rejected'
            booking.reason = reason  # Store the rejection reason in the database
            booking.save()  # Save the changes
        return redirect('manage_booking')  
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packageserviceview(request):
    login_id=request.session.get('login_id')
    if login_id:
        hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
        packages = tbl_package.objects.filter(hospital_id=hospital_id)  # Fetch all bookings
        return render(request, 'Hospital/packageserviceview.html', {'packages': packages})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillpackservice(request):
    login_id=request.session.get('login_id')
    if login_id:
        if request.method == "POST":
            pid = int(request.POST.get("pid"))
            # Fetch related services for the selected package
            services = tbl_packageservice.objects.filter(package_id=pid).select_related('service_id')
            # Prepare data to send as JSON
            service_data = []
            for service in services:
                service_data.append({
                    'service_name': service.service_id.service_name,
                    'amount': service.service_id.amount,
                    'image_url': service.service_id.image.url if service.service_id.image else ''
                })
            return JsonResponse(service_data, safe=False)
        return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_information(request):
    login_id=request.session.get('login_id')
    if login_id:
    # Fetch all accepted bookings with payment status and details
        hospital_id=tbl_hospital.objects.get(login_id=request.session['login_id'])
        bookings = tbl_payment.objects.filter(status='Completed',booking_id__package_id__hospital_id=hospital_id)

    # Pass the bookings to the template
        return render(request, 'Hospital/payment_information.html', {'bookings': bookings})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
           



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editpackage(request, package_id):
    login_id=request.session.get('login_id')
    if login_id:
        package = tbl_package.objects.filter(package_id=package_id).first()  # Fetch the package
        if not package:  # Handle the case where no package is found
            return redirect("viewpackage")
        if request.method == "POST":
            package.package_name = request.POST.get("package_name")
            package.noofdays = request.POST.get("noofdays")
            # Check if an image is uploaded
            if 'image' in request.FILES:
                package.image = request.FILES['image']
            package.save()
            return redirect("viewpackage")  # Redirect to the package list page
        return render(request, "Hospital/editpackage.html", {"package": package})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editservice(request, service_id):
    login_id=request.session.get('login_id')
    if login_id:
        service = tbl_service.objects.filter(service_id=service_id).first()
        if not service:
            return redirect('viewservice')  # Redirect if service is not found
        if request.method == "POST":
            service.service_name = request.POST.get("service_name")
            service.amount = request.POST.get("amount")
            # Update image only if a new one is uploaded
            if 'image' in request.FILES:
                service.image = request.FILES['image']
            service.save()
            return redirect('viewservice')  # Redirect to the service list page
        return render(request, "Hospital/editservice.html", {"service": service})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospital_profile(request):
    login_id=request.session.get('login_id')
    if login_id:
        # Get the login_id from the session
        login_id = request.session.get('login_id')
        if not login_id:
            # If there is no login_id in the session, redirect to login page
            return redirect('login')  # Make sure you define the correct URL for your login page
        try:
            # Fetch the customer with the login_id from the session
            hospital = tbl_hospital.objects.get(login_id=login_id)
        except tbl_hospital.DoesNotExist:
            hospital = None  # If the customer doesn't exist, set it to None
        return render(request, "Hospital/hospital_profile.html", {'hospital': hospital}) 
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile_edit(request):
    login_id=request.session.get('login_id')
    if login_id:
        # Get the logged-in customer based on the session or user authentication method
        hospital = tbl_hospital.objects.get(login_id=request.session.get('login_id'))
        if request.method == 'POST':
            # Manually update customer data (if POST request is made)
            hospital.hospital_name = request.POST.get('hospital_name')
            hospital.email = request.POST.get('email')
            hospital.phone = request.POST.get('phone')
            hospital.address = request.POST.get('address')
            # Handle file uploads (image and ID proof)
            if request.FILES.get('image'):
                hospital.image = request.FILES['image']
            if request.FILES.get('idproof'):
                hospital.idproof = request.FILES['idproof']
            # Save the updated customer record
            hospital.save()
            # Redirect to the profile page after updating
            return redirect('hospital_profile')
        return render(request, 'Hospital/profile_edit.html', {'hospital': hospital})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_feedback(request):
    login_id=request.session.get('login_id')
    if login_id:
        log_id = request.session.get('login_id')  # Get logged-in hospital's login ID
        hospital = tbl_hospital.objects.get(login_id=log_id)  # Get the corresponding hospital
        feedbacks = tbl_feedback.objects.filter(package_id__hospital_id=hospital).select_related('customer_id', 'package_id')

        return render(request, 'Hospital/view_feedback.html', {'feedbacks': feedbacks})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.clear()
    return redirect('/')


def hospital_password(request):
    login_id = request.session.get('login_id')

    if not login_id:
        return HttpResponse("<script>alert('Session Expired! Please login again'); window.location='/login';</script>")

    if request.method == 'POST':
        # Debugging - Print received values
        print(request.POST)

        current_password = request.POST.get("current_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # Check if all fields are filled
        if not current_password or not new_password or not confirm_password:
            messages.error(request, "All fields are required!")
            return render(request, "Hospital/hospital_password.html")

        try:
            user = tbl_login.objects.get(login_id=login_id)

            # Debugging: Print stored password & input password
            print("Stored Password:", user.password)
            print("Entered Current Password:", current_password)

            if user.password == current_password:  # ✅ Checking plain-text password
                if new_password == confirm_password:
                    user.password = new_password  # ⚠ Storing as plain text (not secure)
                    user.save()
                    return HttpResponse("<script>alert('Password Successfully Updated!'); window.location='" + reverse("hospital_profile") + "';</script>")
                else:
                    messages.error(request, "New passwords do not match!")
            else:
                messages.error(request, "Incorrect Old Password!")

        except tbl_login.DoesNotExist:
            messages.error(request, "Invalid User!")

    return render(request, "Hospital/hospital_password.html")