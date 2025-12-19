from django.shortcuts import render,redirect
from GuestApp.models import tbl_login,tbl_hospital,tbl_customer
from AdminApp.models import tbl_district,tbl_location
from django.http import HttpResponse
from email.message import EmailMessage
import smtplib

# Create your views here.
def login(request):
    return render(request,'Guest/login.html')

def login_process(request):
    if request.method == 'POST':
        username = request.POST.get("login_username")
        password = request.POST.get("login_password")
        if tbl_login.objects.filter(username=username, password=password).exists():
            logindata = tbl_login.objects.get(username=username, password=password)
            request.session['login_id'] = logindata.login_id
            role = logindata.role
            if role == 'admin':
                return redirect('/adminapp/adminhome')
            elif role == 'hospital':
                if logindata.status == "Confirmed":
                    return redirect('/hospitalapp/index1') 
                else:
                    return render(request, 'Guest/login.html', {"error": "Hospital account not confirmed yet."})  # Prevent None return
            elif role == 'customer':
                return redirect('/customerapp/index')
            else:
                return render(request, 'Guest/login.html', {"error": "Invalid role assigned."})  # Handle unexpected roles
        else:
            return render(request, 'Guest/login.html', {"error": "Incorrect username or password"}) 
    return render(request, 'Guest/login.html')  # Ensure response is always returned 

def hospitalreg(request):
    district=tbl_district.objects.all()
    return render(request,'Guest/hospitalreg.html',{'district':district})

def index2(request):
    return render(request,'Guest/index2.html')

def hospitalreg_process(request):
    if request.method=="POST":
        lob=tbl_login()
        lob.username=request.POST.get("txtuname")
        lob.password=request.POST.get("txtpassword")
        lob.role="hospital"
        lob.status="Not Confirmed"
        lob.save()
        cob=tbl_hospital()
        cob.hospital_name=request.POST.get("hospital_name")
        cob.email=request.POST.get("email")
        cob.phone=request.POST.get("phone")
        cob.address=request.POST.get("address")
        cob.image=request.FILES["image"]
        cob.idproof=request.FILES["idproof"]
        cob.location_id=tbl_location.objects.get(location_id=request.POST.get("location"))
        cob.login_id=lob
        cob.save()
        
        Email=request.POST.get('email')
        hos_name=request.POST.get('hospital_name') 
        msg = EmailMessage()
        msg.set_content(f"""
Dear {hos_name},

Thank you for registering with VedaKshetra! 🌿

We have received your hospital registration request and are currently reviewing the details. Our team will verify your information and notify you once your account is approved.

What’s Next?
🔍 Verification Process: Our team will review your details and documents.
⏳ Approval Notification: You’ll receive an email once your registration is approved.
🚀 Start Offering Services: After approval, you can list your treatments and begin receiving bookings.

If you have any questions, feel free to contact our support team. We appreciate your patience and look forward to partnering with you in promoting holistic healthcare.

Best Regards,
Team VedaKshetra

""")
        msg['Subject'] = "Hospital Registration Received – Pending Verification"
        msg['from'] = 'adithyasunil5002@gmail.com'
        msg['To'] = {Email}
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('adithyasunil5002@gmail.com','byvn azdc ftlh ezbk')
            smtp.send_message(msg)


        return HttpResponse("<script>alert('sucessfully inserted..');window.location='/guestapp/hospitalreg';</script>")

def customerreg(request):
    district=tbl_district.objects.all()
    return render(request,'Guest/customerreg.html',{'district':district})
    
def customerreg_process(request):
    if request.method=="POST":
        lob=tbl_login()
        lob.username=request.POST.get("username")
        lob.password=request.POST.get("password")
        lob.role="customer"
        lob.status="Confirmed"
        lob.save()
        cob=tbl_customer()
        cob.customer_name=request.POST.get("customer_name")
        cob.email=request.POST.get("email")
        cob.phone=request.POST.get("phone")
        cob.address=request.POST.get("address")
        cob.image=request.FILES["image"]
        cob.idproof=request.FILES["idproof"]
        cob.location_id=tbl_location.objects.get(location_id=request.POST.get("location"))
        cob.login_id=lob
        cob.save()

        Email=request.POST.get('email')  # to address
        custname=request.POST.get('customer_name') 
        msg = EmailMessage()
        msg.set_content(f"""
Dear {custname},

Namaste! 🌿

Welcome to VedaKshetra, your trusted platform for holistic healing and traditional Ayurvedic treatments. We are delighted to have you on board.

With your account, you can now:
✅ Explore a wide range of Ayurvedic wellness packages
✅ Book treatments at renowned hospitals and wellness centers
✅ Track your bookings and manage your appointments easily
✅ Share your feedback and experiences with others

We are committed to bringing you the best Ayurvedic care and ensuring a seamless experience.

If you have any questions or need assistance, feel free to reach out to our support team.

Wishing you health and wellness,
Team VedaKshetra 

""")
        msg['Subject'] = "Welcome to VedaKshetra – Your Journey to Wellness Begins!"
        msg['from'] = 'adithyasunil5002@gmail.com'
        msg['To'] = {Email}
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('adithyasunil5002@gmail.com','byvn azdc ftlh ezbk')
            smtp.send_message(msg)
        
        return HttpResponse("<script>alert('sucessfully inserted..');window.location='/guestapp/customerreg';</script>")  



def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username")

        # ✅ Check if user exists
        if tbl_login.objects.filter(username=username).exists():
            user = tbl_login.objects.get(username=username)

            # ✅ Use the role as a security question (No new field needed)
            security_question = "What is your role? (Customer / Hospital)"

            return render(request, "Guest/security_question.html", {
                "question": security_question,
                "username": username
            })

        else:
            return HttpResponse("<script>alert('Username not found!');window.location='/forgot-password';</script>")

    return render(request, "Guest/forgot_password.html")


def verify_security_answer(request):
    if request.method == "POST":
        username = request.POST.get("username")
        answer = request.POST.get("answer").strip().lower()

        # ✅ Check if user exists
        if tbl_login.objects.filter(username=username).exists():
            user = tbl_login.objects.get(username=username)

            # ✅ Use role as the correct answer
            correct_answer = user.role.lower()

            if answer == correct_answer:
                return render(request, "Guest/reset_password.html", {"username": username})
            else:
                return HttpResponse("<script>alert('Incorrect answer!');window.location='/forgot-password';</script>")

    return HttpResponse("<script>alert('Something went wrong!');window.location='/forgot-password';</script>")


def reset_password_process(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        # ✅ Check if user exists
        if tbl_login.objects.filter(username=username).exists():
            user = tbl_login.objects.get(username=username)

            # ✅ Update password
            user.password = new_password  # Hash the password if needed
            user.save()

            return HttpResponse("<script>alert('Password reset successfully!');window.location='/login';</script>")

    return HttpResponse("<script>alert('Something went wrong!');window.location='/forgot-password';</script>")


