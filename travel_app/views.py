from django.shortcuts import render,redirect
from travel_app.models import regionModel,planModel,userModel,bookingModel,reviewModel
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from datetime import date
import re
import string
import random

# Create your views here.

# Validation myanmar phonenumber.
def validate_MM_phonenumber(phone):
    pattern = r'^(?:\+95\d{8,9}|09\d{8,9})$'
    if re.match(pattern, phone):
        return True
    else:
        return False
    
# Random code
def generate_random_code(length=6):
    characters= string.ascii_uppercase + string.digits
    random_code= ''.join(random.choice(characters) for _ in range(length))
    return random_code

def postList(request):
    regions= regionModel.objects.all().order_by('-name')
    plans= planModel.objects.all().order_by('title')
    if request.user.is_authenticated:
        current_user=userModel.objects.get(email=request.user.email)
        return render (request,'postList.html', {'regions': regions, 'plans': plans, 'current_user':current_user})
    else:
        return render (request,'postList.html', {'regions': regions, 'plans': plans})
    
def searchBy(request):
    regions= regionModel.objects.all().order_by('-name')
    search= request.GET.get('search')
    plans= planModel.objects.filter(title__icontains=search).order_by('title')
    if request.user.is_authenticated:
        current_user=userModel.objects.get(email=request.user.email)
        return render (request,'postList.html', {'regions': regions, 'plans': plans, 'search':search, 'current_user':current_user})
    else:
        return render (request,'postList.html', {'regions': regions, 'plans': plans, 'search':search})
    
@permission_required('travel_app.add_planmodel', login_url='login')
def postCreate(request):
    if request.method == 'GET':
        regions= regionModel.objects.all().order_by('name')
        if request.user.is_authenticated:
            current_user=userModel.objects.get(email=request.user.email)
            return render(request,'postCreate.html',{'regions': regions, 'current_user':current_user})
        else:
            return render(request,'postCreate.html',{'regions': regions})
    if request.method == 'POST':
        plan= planModel.objects.create(
            title= request.POST.get('title'),
            image= request.FILES.get('image'),
            region_id= request.POST.get('region'),
            detail= request.POST.get('detail'),
            price_for_adult_per_day= request.POST.get('adult'),
            price_for_child_per_day= request.POST.get('child'),
        )
        plan.save()
        return redirect('/main/postlist/')
    
def regionDetail(request,region_id):
    region= regionModel.objects.get(id= region_id)
    plans= planModel.objects.filter(region_id= region_id).order_by('title')
    if request.user.is_authenticated:
        current_user=userModel.objects.get(email=request.user.email)
        return render (request, 'regionDetail.html',{'region':region, 'plans':plans, 'current_user':current_user})
    else:
        return render (request, 'regionDetail.html',{'region':region, 'plans':plans})

@permission_required('travel_app.change_planmodel', login_url='login')
def postDetail(request,plan_id):
    if request.method== 'GET':
        plan= planModel.objects.get(id= plan_id)
        regions= regionModel.objects.all().order_by('name')
        if request.user.is_authenticated:
            current_user=userModel.objects.get(email=request.user.email)
            return render(request, 'postDetail.html', {'plan':plan, 'regions':regions, 'current_user':current_user})
        else:
            return render(request, 'postDetail.html', {'plan':plan, 'regions':regions})
    if request.method== 'POST':
        plan= planModel.objects.get(id=plan_id)
        plan.title= request.POST.get('title')
        plan.detail= request.POST.get('detail')
        plan.price_for_adult_per_day= request.POST.get('adult')
        plan.price_for_child_per_day= request.POST.get('child')
        plan.region_id= request.POST.get('region')
        
        plan.save()
        messages.success(request, "Plan updated successfully !")
        return redirect('/main/postlist/')

@permission_required('travel_app.delete_planmodel', login_url='login')
def postDelete(request,plan_id):
    if request.method== 'GET':
        plan= planModel.objects.get(id= plan_id)
        if request.user.is_authenticated:
            current_user=userModel.objects.get(email=request.user.email)
            return render(request, 'postDelete.html', {'plan':plan, 'current_user':current_user})
        else:
            return render(request, 'postDelete.html', {'plan':plan})
    if request.method== 'POST':
        plan= planModel.objects.filter(id= plan_id)
        plan.delete()
        messages.success(request, "Plan deleted successfully !")
        return redirect('/main/postlist/')
    
def bookingForm(request,plan_id):
    if request.method== 'GET':
        plan= planModel.objects.get(id=plan_id)
        current_date= date.today().strftime("%Y-%m-%d")
        reviews= reviewModel.objects.filter(plan_id= plan_id).order_by('created_time')
        users= userModel.objects.all()
        if request.user.is_authenticated:
            current_user=userModel.objects.get(email=request.user.email)
            return render (request, 'bookingForm.html',{'plan':plan, 'current_date':current_date, 'reviews':reviews, 'users':users, 'current_user':current_user})
        else:
            return render (request, 'bookingForm.html',{'plan':plan, 'current_date':current_date, 'reviews':reviews, 'users':users})
    if request.method== 'POST':
        if request.user.is_authenticated:
            plan= planModel.objects.get(id=plan_id)
            duration_day= int(request.POST.get('duration_day'))
            duration_type= int(request.POST.get('duration_type'))
            duration_total= duration_day * duration_type
            duration= f"{duration_total} day(s) and {duration_total-1} night(s)"
            
            booking_name= request.POST.get('booking_name')
            booking_email= request.POST.get('booking_email')
            booking_phone= request.POST.get('booking_phone')
            booking_date= request.POST.get('booking_date')
            total_cost= request.POST.get('total_cost')
            
            if booking_email == request.user.email :
                if validate_MM_phonenumber(booking_phone):
                    booking= bookingModel.objects.create(
                        booking_code= generate_random_code(),
                        booking_name= booking_name,
                        booking_email= booking_email,
                        booking_phone= booking_phone,
                        booking_date= booking_date,
                        duration= duration,
                        booking_plan= plan.title,
                        total_cost= total_cost,
                        plan_id= plan_id,
                        user_id= request.user.id,
                    )
                    booking.save()
                    return redirect('/main/booking_success/' + str(plan_id) + '/' + str(booking.id) + '/')
                else:
                    messages.error(request, "Sorry, Invalid phone number !")
                    return redirect('/main/booking/' + str(plan_id) + '/')                
            else:
                messages.error(request, "Sorry, That's not your email !")
                return redirect('/main/booking/' + str(plan_id) + '/')
        else:
            return redirect('/login/')
    
def loGin(request):
    if request.method== 'GET':
        return render(request, 'login.html')
    if request.method== 'POST':
        username_or_email= request.POST.get('username_or_email')
        password= request.POST.get('password')
        
        user_name_or_email_Check= User.objects.filter(Q(username= username_or_email)| Q(email= username_or_email)).exists()
        
        if not user_name_or_email_Check:
            messages.error(request, "Invalid username or email !")
            return redirect('/login/')
        else:
            user1= User.objects.get(Q(username= username_or_email)| Q(email= username_or_email))
            user2= userModel.objects.get(Q(username= username_or_email)| Q(email= username_or_email))
                
            if user2.password == password:
                login(request, user1)
                messages.success(request, "Logged in successfully")
                return redirect('/main/postlist/')
            else:
                messages.error(request, "Invalid password! Check again.")
                return redirect('/login/')                
    else:
        messages.error(request, "Invalid Server Request !")
        return redirect('/login/')
        
def siGnin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        
        if User.objects.filter(email= email).exists():
            messages.error(request, "Email has been already used !")
            return redirect('/signin/')
        elif User.objects.filter(username= username).exists():
            messages.error(request, "Username nas been already used !")
            return redirect('/signin/')
        else:
            password = request.POST.get('password')
            password_confirm = request.POST.get('passwordConfirm')
            if password == password_confirm:
                phone = request.POST.get('phone')
                if not validate_MM_phonenumber(phone):
                    messages.error(request, "Invalid phone number ! please use only Myanmar phone number")
                    return redirect('/signin/')
                else:
                    image = request.FILES.get('image')

                    # Create and save the User object
                    user1 = User.objects.create_user(
                        username= username,
                        password= password,
                        email= email,
                    )
                    user1.save()
                        # Retrieve and add the user to the 'users' group
                    users_group = Group.objects.get(name='users')
                    user1.groups.add(users_group)

                        # Create and save the custom userModel object
                    user2 = userModel.objects.create(
                        username=username,
                        email=email,
                        password=password,
                        phone=phone,
                        image=image,
                    )
                    user2.save()
                    login(request,user1)
                    return redirect('/main/postlist/')
            else:
                messages.error(request, "Please check your passwords again(not match) !")
                return redirect('/signin/')
    else:
        messages.error(request, "Invalid request method !")
        return redirect('/signin/')
    
def confirmEmailToResetPw(request):
    if request.method== "GET":
        return render(request, 'confirmEmailToResetPw.html')
    if request.method== "POST":
        email= request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return redirect('/reset_password/' + email + '/')
        else:
            messages.error(request, "Email not found !")
            return redirect('/confirm_email_to_reset_pw/')
            
def resetPassword(request,email):
    if request.method== "GET":
        return render(request, 'resetPassword.html',{'email':email})
    if request.method== "POST":
        password= request.POST.get('password')
        passwordConfirm= request.POST.get('passwordConfirm')
        if password== passwordConfirm:
            user1= User.objects.filter(email=email).first()
            user1.set_password('passwordConfirm')
            user1.save()
            
            user2= userModel.objects.get(email=email)
            user2.password= passwordConfirm
            user2.save()
            
            return redirect('/reset_password_successful/')
        else:
            messages.error(request, "Please check your passwords again(not match) !")
            return redirect('/reset_password/' + email + '/')
        
def resetPasswordSuccessful(request):
    return render(request, 'resetPasswordSuccessful.html')
    
def loGout(request):
    logout(request)
    messages.success(request, "Logged out successfully !")
    return redirect('/main/postlist/')
        
def bookingSuccess(request,plan_id,booking_id):
    booking= bookingModel.objects.get(id= booking_id)
    plan= planModel.objects.get(id=plan_id)
    return render(request, 'booking_success.html', {'plan':plan, 'booking':booking})

@permission_required('travel_app.view_usermodel', login_url='login')
def usersTable(request,user_id):
    users= userModel.objects.all().order_by('username')
    current_user=userModel.objects.get(id=user_id)
    return render(request, 'usersTable.html', {'users':users, 'current_user':current_user})

@permission_required('travel_app.view_bookingmodel', login_url='login')
def bookingsTable(request,user_id):
    bookings= bookingModel.objects.all().order_by('booking_status','booking_date')
    current_user=userModel.objects.get(id=user_id)
    return render(request, 'bookingsTable.html', {'bookings':bookings, 'current_user':current_user})

@permission_required('travel_app.change_bookingmodel', login_url='login')
def bookingStatusConfirm(request,user_id,booking_id):
    if request.method== 'POST':
        booking= bookingModel.objects.get(id= booking_id)
        booking.booking_status= True
        
        booking.save()
        return redirect('/myadmin/bookings/' + str(user_id) + '/')
    
@permission_required('travel_app.view_planmodel', login_url='login')
def plansTable(request,user_id):
    plans= planModel.objects.all().order_by('title')
    current_user=userModel.objects.get(id=user_id)
    return render(request, 'plansTable.html', {'plans':plans, 'current_user':current_user})

@permission_required('travel_app.view_bookingmodel', login_url='login')
def userBookings(request,user_id,currentuser_id):
    bookings= bookingModel.objects.filter(user_id= user_id).order_by('-created_time')
    current_user=userModel.objects.get(id=currentuser_id)
    return render(request, 'userBookings.html', {'bookings':bookings, 'current_user':current_user})

@permission_required('travel_app.delete_bookingmodel', login_url='login')
def bookingCancel(request,user_id,currentuser_id,booking_id):
    if request.method== 'POST':
        booking= bookingModel.objects.filter(id=booking_id)
        booking.delete()
        messages.success(request, 'Booking canceled')
        return redirect('/main/mybookings/' + str(user_id) + '/' + str(currentuser_id) + '/')
    
@permission_required('travel_app.add_reviewmodel', login_url='login')
def reviewCreate(request,user_id,plan_id):
    if request.method== "POST":
        new_review= reviewModel.objects.create(
            review= request.POST.get('review'),
            user_id= user_id,
            plan_id= plan_id,
        )
        new_review.save()
        return redirect('/main/booking/' + str(plan_id) + '/')
    
@permission_required('travel_app.delete_reviewmodel', login_url='login')
def reviewDelete(request,review_id,plan_id):
    review= reviewModel.objects.get(id= review_id)
    review.delete()
    return redirect('/main/booking/' + str(plan_id) + '/')

@permission_required('travel_app.change_reviewmodel', login_url='login')
def reviewEdit(request,review_id,plan_id):
    if request.method== "POST":
        review= reviewModel.objects.get(id= review_id)
        review.review= request.POST.get('review')
        
        review.save()
        return redirect('/main/booking/' + str(plan_id) + '/')