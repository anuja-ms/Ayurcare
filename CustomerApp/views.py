from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from AdminApp.models import tbl_district,tbl_location
from GuestApp.models import tbl_hospital,tbl_login,tbl_customer
from CustomerApp.models import tbl_booking,tbl_payment,tbl_feedback
from HospitalApp.models import tbl_package,tbl_packageservice,tbl_service
from django.http import JsonResponse,HttpResponse
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    login_id=request.session.get('login_id')
    if login_id:
        return render(request,'Customer/index.html')
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
         
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hospitalview(request):
    login_id=request.session.get('login_id')
    if login_id:
        district=tbl_district.objects.all()
        return render(request,'Customer/hospitalview1.html',{'district':district})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")
         

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillhospital(request):
    login_id=request.session.get('login_id')
    if login_id:
        lid=int(request.POST.get("lid"))
        hospital=tbl_hospital.objects.filter(location_id=lid).values()
        return JsonResponse(list(hospital),safe=False)
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def singleview(request,hospital_id):
    login_id=request.session.get('login_id')
    if login_id:
        hospital=tbl_hospital.objects.get(hospital_id=hospital_id)
        return render(request,"Customer/singleview.html",{'hospital':hospital})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packageview(request,id):
    login_id=request.session.get('login_id')
    if login_id:
        request.session['hospital_id']=id
        hos=tbl_package.objects.filter(hospital_id=id)
        return render(request,"Customer/packageview.html",{'hos':hos})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def serviceview(request,id):
    login_id=request.session.get('login_id')
    if login_id:
        request.session['package_id']=id
        ser=tbl_packageservice.objects.filter(package_id=id)
        return render(request,"Customer/serviceview.html",{'service':ser})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def packagebooking(request,id):
    login_id=request.session.get('login_id')
    if login_id:
        cus = tbl_customer.objects.get(login_id=request.session['login_id'])
        request.session['package_id'] = id
        package = tbl_package.objects.get(package_id=id)
        pck = tbl_packageservice.objects.filter(package_id=id)
        total_amount = sum(tbl_packageservice.service_id.amount for tbl_packageservice in pck)
        return render(request, "Customer/packagebooking.html", {'package': package, 'total_amount': total_amount, 'cus': cus})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def service_detail(request,service_id):
    login_id=request.session.get('login_id')
    if login_id:
        service = tbl_service.objects.get(service_id=service_id)
        return render(request,'Customer/service_detail.html', {'service': service})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def insertbooking(request, id):
    login_id=request.session.get('login_id')
    if login_id:
        # Get the current customer from the session
        cus = tbl_customer.objects.get(login_id=request.session['login_id'])
        # Get the package being booked
        package = tbl_package.objects.get(package_id=id)
        # Get the services associated with the package
        pck = tbl_packageservice.objects.filter(package_id=id)
        # Calculate the total amount for the package
        total_amount = sum(tbl_packageservice.service_id.amount for tbl_packageservice in pck)
        # Create a new booking entry in the Booking table (assuming it exists)
        booking = tbl_booking(
            customer_id=cus,
            package_id=package,
            t_amount=total_amount,
            status="Pending",  # You can set status as "Pending", "Confirmed", etc.
            require_date=request.POST.get('require_date'),  # Assuming booking date is passed in the form
        )
        # Save the booking instance
        booking.save()

        # Pass the necessary data and a flag to show the pop-up
        return render(request, "Customer/packagebooking.html", {
            'package': package,
            'total_amount': total_amount,
            'cus': cus,
            'booking_success': True  # Flag to trigger pop-up in the template
        })
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking_status(request):
    login_id = request.session.get('login_id')

    if not login_id:
        return HttpResponse("<script>alert('Authentication Required, please login first');window.location='/login';</script>")

    try:
        customer = tbl_customer.objects.get(login_id=login_id)
    except tbl_customer.DoesNotExist:
        return HttpResponse("<script>alert('Customer not found');window.location='/login';</script>")

    bookings = tbl_booking.objects.filter(customer_id=customer).select_related('package_id')
    
    booking_list = []
    
    for booking in bookings:
        # Fetch latest payment status
        payment_record = tbl_payment.objects.filter(booking_id=booking.booking_id).order_by('-payment_id').first()
        payment_status = payment_record.status if payment_record else "Pending"

        # Determine cancel button visibility
        show_cancel = booking.status in ["Accepted", "Paid"] and payment_status == "Completed"

        # Check if feedback already exists
        feedback_exists = tbl_feedback.objects.filter(customer_id=customer, package_id=booking.package_id).exists()

        booking_list.append({
            'booking': booking,
            'payment_status': payment_status,
            'show_cancel': show_cancel,
            'feedback_exists': feedback_exists  # Add feedback check
        })

    return render(request, "Customer/booking_status.html", {'bookings': booking_list})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_page(request, booking_id):
    login_id=request.session.get('login_id')
    if login_id:
        # Fetch booking details
        booking = tbl_booking.objects.filter(booking_id=booking_id).first()
        
        if not booking:
            return HttpResponse("Booking not found.", status=404)

        # Calculate Payment Details
        total_amount = booking.t_amount  # Total package price
        quarter_payment = round(total_amount / 4, 2)  # 1/4 payment
        admin_commission = round(quarter_payment * 0.05, 2)  # 5% commission on 1/4 payment
        hospital_amount = round(quarter_payment - admin_commission, 2)  # Hospital's share

        if request.method == 'POST':
            payment_method = request.POST.get('payment_method')
            payment_success = False  

            # Validate Payment Inputs
            if payment_method == 'credit_card':
                if request.POST.get('card_number') and request.POST.get('expiry_date') and request.POST.get('cvv'):
                    payment_success = True  
            elif payment_method == 'bank_transfer':
                if request.POST.get('bank_account') and request.POST.get('bank_name'):
                    payment_success = True  
            elif payment_method == 'upi':
                if request.POST.get('upi_id'):
                    payment_success = True  

            # Save Payment Record with Commission
            status = "Completed" if payment_success else "Failed"
            tbl_payment.objects.create(
                booking_id=booking,
                status=status,
                commission=admin_commission  # Storing the commission amount in tbl_payment
            )

            if payment_success:
                booking.status = "Paid"
                booking.save()
                messages.success(request, "✅ Payment Completed Successfully!")
                return redirect('booking_status')
            else:
                messages.error(request, "❌ Payment Failed! Please try again.")
                return redirect('payment', booking_id=booking_id)

        return render(request, 'Customer/payment.html', {
            'booking': booking,
            'total_amount': total_amount,
            'quarter_payment': quarter_payment,
            'admin_commission': admin_commission,
            'hospital_amount': hospital_amount
        })
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_profile(request):
    login_id = request.session.get('login_id')

    if not login_id:
        return redirect('login')  # Redirect to login page if not authenticated

    try:
        customer = tbl_customer.objects.get(login_id=login_id)
    except tbl_customer.DoesNotExist:
        return HttpResponse("<script>alert('Customer not found. Please contact support.');window.location='/login';</script>")

    return render(request, "Customer/customer_profile.html", {'customer': customer})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cprofile_edit(request):
    login_id=request.session.get('login_id')
    if login_id:
        # Get the logged-in customer based on the session or user authentication method
        customer= tbl_customer.objects.get(login_id=request.session.get('login_id'))

        if request.method == 'POST':
            # Manually update customer data (if POST request is made)
            customer.customer_name = request.POST.get('customer_name')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            customer.address = request.POST.get('address')
            
            # Handle file uploads (image and ID proof)
            if request.FILES.get('image'):
                customer.image = request.FILES['image']
            if request.FILES.get('idproof'):
                customer.idproof = request.FILES['idproof']

            # Save the updated customer record
            customer.save()
            
            # Redirect to the profile page after updating
            return redirect('customer_profile')

        return render(request, 'Customer/cprofile_edit.html', {'customer': customer})
    else:
        return HttpResponse("<script>alert('Authentication Required please login first');window.location='/login';</script>")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_feedback(request, booking_id):
    login_id = request.session.get('login_id')

    if not login_id:
        return HttpResponse("<script>alert('Authentication Required. Please login first');window.location='/login';</script>")

    try:
        booking = tbl_booking.objects.get(booking_id=booking_id)
    except tbl_booking.DoesNotExist:
        return HttpResponse("<script>alert('Invalid Booking');window.location='/customerapp/booking_status';</script>")

    # Check if feedback already exists for this package
    feedback_exists = tbl_feedback.objects.filter(customer_id=booking.customer_id, package_id=booking.package_id).exists()

    if request.method == 'POST':
        if not feedback_exists:
            feedback = tbl_feedback(
                customer_id=booking.customer_id,
                package_id=booking.package_id,
                rating=request.POST.get('rating'),
                feedback=request.POST.get('feedback')
            )
            feedback.save()

            messages.success(request, "Your feedback has been submitted successfully!")
            return redirect('booking_status')  # Redirect to booking status page after submission
        else:
            messages.warning(request, "You have already submitted feedback for this package.")

    return render(request, 'Customer/customer_feedback.html', {'package': booking.package_id, 'booking': booking, 'feedback_exists': feedback_exists})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.clear()
    return redirect('/')




def cancel_policy(request, booking_id):
    try:
        booking = tbl_booking.objects.get(booking_id=booking_id)
        package_name = booking.package_id.package_name  # ✅ Fetch the package name

        # ✅ Check if the booking is eligible for a refund
        time_difference = now().date() - booking.booking_date
        if time_difference.days <= 2:
            refund_percentage = 50  # ✅ 50% refund within 24-48 hours
        else:
            refund_percentage = 0  # ✅ No refund

        refund_amount = (booking.t_amount / 4) * (refund_percentage / 100)
        paid_amount = booking.t_amount / 4  # ✅ Calculate 1/4th payment

        context = {
            'booking': booking,
            'package_name': package_name,  # ✅ Pass package name to template
            'refund_percentage': refund_percentage,
            'refund_amount': refund_amount,
            'paid_amount': paid_amount,
        }
        return render(request, 'Customer/cancel_policy.html', context)

    except tbl_booking.DoesNotExist:
        return HttpResponse("<script>alert('Invalid Booking');window.location='/customerapp/booking_status';</script>")


def cancel_booking(request, booking_id):
    try:
        booking = tbl_booking.objects.get(booking_id=booking_id)

        if request.method == "POST":
            reason = request.POST.get("reason", "Not Provided")  # ✅ Get customer-selected reason

            # ✅ Ensure the booking is eligible for cancellation
            if booking.status in ["Accepted", "Paid"]:
                # ✅ Calculate refund eligibility (within 24-48 hours)
                time_difference = now().date() - booking.booking_date

                if time_difference.days <= 2:  
                    refund_amount = (booking.t_amount / 4) * 0.5  # ✅ 50% refund
                else:
                    refund_amount = 0  # ✅ No refund after 48 hours

                # ✅ Update booking status & save cancellation reason
                booking.status = "Cancelled"
                booking.reason = reason  # ✅ Save cancellation reason from the form
                booking.save()

                return redirect('booking_status')

            return HttpResponse("<script>alert('Booking cannot be cancelled');window.location='/customerapp/booking_status';</script>")

        return HttpResponse("<script>alert('Invalid Request');window.location='/customerapp/booking_status';</script>")

    except tbl_booking.DoesNotExist:
        return HttpResponse("<script>alert('Invalid Booking');window.location='/customerapp/booking_status';</script>")

def process_cancellation(request, booking_id):
    try:
        booking = tbl_booking.objects.get(booking_id=booking_id)

        if request.method == "POST":
            reason = request.POST.get("cancellation_reason", "No reason provided")

            # ✅ Check refund policy
            time_difference = now().date() - booking.booking_date
            if time_difference.days <= 2:
                refund_amount = (booking.t_amount / 4) * 0.5  # ✅ 50% refund
            else:
                refund_amount = 0  # ✅ No refund

            # ✅ Update booking status & refund amount
            booking.status = "Cancelled"
            booking.reason = reason
            booking.refund_amount = refund_amount  # ✅ Save refund amount
            booking.save()

            return redirect('booking_status')

        return HttpResponse("<script>alert('Invalid Request');window.location='/customerapp/booking_status';</script>")

    except tbl_booking.DoesNotExist:
        return HttpResponse("<script>alert('Invalid Booking');window.location='/customerapp/booking_status';</script>")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    login_id = request.session.get('login_id')

    if not login_id:
        return HttpResponse("<script>alert('Session Expired! Please login again'); window.location='/login';</script>")

    if request.method == 'POST':
        old_password = request.POST.get("old_password", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        # 🔍 Debugging - Print received values
        print("Old Password:", old_password)
        print("New Password:", new_password)
        print("Confirm Password:", confirm_password)

        if not old_password or not new_password or not confirm_password:
            return HttpResponse("<script>alert('All fields are required!'); window.location='" + reverse("change_password") + "';</script>")

        try:
            user = tbl_login.objects.get(login_id=login_id)

            if user.password == old_password:  # 🔴 Plain-text password checking
                if new_password == confirm_password:
                    user.password = new_password  # ⚠ Storing passwords as plain text (Not Secure)
                    user.save()
                    return HttpResponse("<script>alert('Password Successfully Updated!'); window.location='" + reverse("customer_profile") + "';</script>")
                else:
                    return HttpResponse("<script>alert('New passwords do not match!'); window.location='" + reverse("change_password") + "';</script>")
            else:
                return HttpResponse("<script>alert('Incorrect Old Password!'); window.location='" + reverse("change_password") + "';</script>")

        except tbl_login.DoesNotExist:
            return HttpResponse("<script>alert('Invalid User!'); window.location='" + reverse("change_password") + "';</script>")

    return render(request, "Customer/change_password.html")


