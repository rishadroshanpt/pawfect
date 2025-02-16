from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings   
import math,random
import razorpay
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from itertools import islice



# Create your views here.
def shop_login(req):
    # print(req.session['user1'])

    # print(req.session['eshop'])
    if 'eshop' in req.session:
        return redirect('shopHome')
    if 'user' in req.session:
        return redirect('userHome')
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        if data:
            login(req,data)
            if data.is_superuser:
                req.session['eshop']=uname   #create session
                return redirect(shop_home)
            else:
                req.session['user']=uname   #create session
                return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shop_login)
    
    else:
        return render(req,'login.html')
    
def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shop_login)
    
def OTP(req):
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        otp=OTP(req)
        if User.objects.filter(email=email).exists():
            messages.error(req, "Email is already in use.")
            return redirect(register)
        else:
            send_mail('Your registration OTP ,',f"OTP for registration is {otp}", settings.EMAIL_HOST_USER, [email])
            messages.success(req, "Registration successful. Please check your email for OTP.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'register.html')

def validate(req,name,password,email,otp):
    if req.method=='POST':
        uotp=req.POST['uotp']
        if uotp==otp:
            data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
            data.save()
            messages.success(req, "OTP verified successfully. You can now log in.")
            return redirect(shop_login)
        else:
            messages.error(req, "Invalid OTP. Please try again.")
            return redirect("validate",name=name,password=password,email=email,otp=otp)
    else:
        return render(req,'validate.html',{'name':name,'pass':password,'email':email,'otp':otp})



# -----------------------------------shop------------------------------


def shop_home(req):
    if 'eshop' in req.session:
        data=Pet.objects.all()
        return render(req,'shop/home.html',{'data':data})
    else:
        return redirect(shop_login)
    
def shop_petType(req,pid):
    if 'eshop' in req.session:
        data=Category.objects.filter(pet=pid)
        return render(req,'shop/petType.html',{'data':data})
    else:
        return redirect(shop_login)
    
def shopProds(req,pid):
    if 'eshop' in req.session:
        data=Product.objects.filter(category=pid)
        return render(req,'shop/shopProds.html',{'data':data})
    else:
        return redirect(shop_login)
    
def shopProd(req,pid):
    if 'eshop' in req.session:
        data=Product.objects.get(pk=pid)
        data1=Details.objects.filter(product=pid)
        data2=Details.objects.get(product=pid,pk=data1[0].pk)
        if req.GET.get('dis'):
            dis=req.GET.get('dis')
            data2=Details.objects.get(product=pid,pk=dis)
        return render(req,'shop/shopProd.html',{'data':data,'data1':data1,'data2':data2})
    else:
        return redirect(shop_login)
    
def add_pet(req):
    if 'eshop' in req.session:
        if req.method=='POST':
            if 'pet_form' in req.POST:
                pet_cate=req.POST['pet']
                petImg=req.FILES.get('petImg')
                data=Pet.objects.create(pet=pet_cate,img=petImg)
                data.save()
            # return redirect(add_pet)
            elif 'category_form' in req.POST:
                pet_cate=req.POST['pet_cate']
                prd_cate=req.POST['cate']
                cateImg=req.FILES['cateImg']
                data1=Category.objects.create(pet=Pet.objects.get(pet=pet_cate),category=prd_cate,img=cateImg)
                data1.save()
            return redirect(add_pet)
        else:
            data=Pet.objects.all()
            data1=Category.objects.all()
            return render(req,'shop/pet.html',{'data':data,'data1':data1})
    else:
        return redirect(shop_login)
    
def delete_pet(req,pid):
    data=Pet.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(add_pet)

def edit_pet(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            pet=req.POST['pet']
            img=req.FILES.get('petImg')
            if img:
                Pet.objects.filter(pk=pid).update(pet=pet)
                data=Pet.objects.get(pk=pid)
                url=data.img.url
                og_path=url.split('/')[-1]
                os.remove('media/'+og_path)
                data.img=img
                data.save()
            else:
                Pet.objects.filter(pk=pid).update(pet=pet)
            return redirect(add_pet)
        else:
            data=Pet.objects.get(pk=pid)
            return render(req,'shop/editPet.html',{'data':data})
    else:
        return redirect(shop_login)
    
def delete_category(req,pid):
    data=Category.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(add_pet)

def edit_category(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            cate=req.POST['cate']
            img=req.FILES.get('cateImg')
            if img:
                Category.objects.filter(pk=pid).update(category=cate)
                data=Category.objects.get(pk=pid)
                url=data.img.url
                og_path=url.split('/')[-1]
                os.remove('media/'+og_path)
                data.img=img
                data.save()
            else:
                Category.objects.filter(pk=pid).update(category=cate)
            return redirect(add_pet)
        else:
            data=Category.objects.get(pk=pid)
            return render(req,'shop/editCategory.html',{'data':data})
    else:
        return redirect(shop_login)

def add_prod(req):
    if 'eshop' in req.session:
        if req.method=='POST':
            # pet_cate=req.POST['pet_cate']
            prd_cate=req.POST['prd_cate']
            prd_name=req.POST['prd_name']
            img=req.FILES['img']
            prd_dis=req.POST['prd_dis']
            data=Product.objects.create(category=Category.objects.get(category=prd_cate),name=prd_name,img=img,dis=prd_dis)
            data.save()
            pk=data.pk
            return redirect("details",pid=pk)
        else:
            data=Pet.objects.all()
            data1=Category.objects.all()
            return render(req,'shop/add_prod.html',{'data':data,'data1':data1})
    else:
        return redirect(shop_login)
    
def details(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            product=req.POST['pro']
            dis=req.POST['dis']
            price=req.POST['price']
            ofrPer=req.POST['offerPer']
            stock=req.POST['stock']
            p=int(price)
            op=int(ofrPer)
            ofrPrice=float(p-((p*op)/100))
            data=Details.objects.create(product=Product.objects.get(id=product),dis=dis,price=price,ofr_per=ofrPer,ofr_price=ofrPrice,stock=stock)
            data.save()
            return redirect("details",pid=pid)
        else:
            data=Product.objects.get(pk=pid)
            pk=data.pk
            return render(req,'shop/details.html',{'pk':pk})
    else:
        return redirect(shop_login)

def edit_prod(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            prd_name=req.POST['prd_name']
            prd_dis=req.POST['prd_dis']
            img=req.FILES.get('img')
            if img:
                Product.objects.filter(pk=pid).update(name=prd_name,dis=prd_dis)
                data=Product.objects.get(pk=pid)
                url=data.img.url
                og_path=url.split('/')[-1]
                os.remove('media/'+og_path)
                data.img=img
                data.save()
            else:
                Product.objects.filter(pk=pid).update(name=prd_name,dis=prd_dis)
            return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit.html',{'product':data})
    else:
        return redirect(shop_login)
    
def edit_details(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            product=req.POST['pro']
            dis=req.POST['dis']
            price=req.POST['price']
            ofrPer=req.POST['offerPer']
            stock=req.POST['stock']
            p=int(price)
            op=int(ofrPer)
            ofrPrice=float(p-((p*op)/100))
            data=Details.objects.create(product=Product.objects.get(pk=product),dis=dis,price=price,ofr_per=ofrPer,ofr_price=ofrPrice,stock=stock)
            data.save()
            return redirect("edit_details",pid=pid)
        else:
            data=Details.objects.filter(product=pid)
            data1=Product.objects.get(pk=pid)
            return render(req,'shop/edit_details.html',{'data':data,'data1':data1})
    else:
        return redirect(shop_login)
    
def edit_detail(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            price=req.POST['price']
            ofrPer=req.POST['offerPer']
            stock=req.POST['stock']
            p=int(price)
            op=int(ofrPer)
            ofrPrice=float(p-((p*op)/100))
            Details.objects.filter(pk=pid).update(price=price,ofr_per=ofrPer,ofr_price=ofrPrice,stock=stock)
            data=Details.objects.get(pk=pid)
            data=data.product.pk
            return redirect("edit_details",pid=data)
        else:
            data=Details.objects.get(pk=pid)
            ofr=int(data.ofr_per)
            return render(req,'shop/editDetails.html',{'data':data,'ofr':ofr})
    else:
        return redirect(shop_login)


def delete_details(req,pid):
    data=Details.objects.get(pk=pid)
    data.delete()
    return redirect(shop_home)

def delete_prod(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(shop_home)

def booking(req):
    data=Bookings.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'data':data})


# -----------------------------------shop------------------------------

def user_home(req):
    # print(req.session['user1'])

    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        pro=Product.objects.all()[: : -1]
        data = list(islice(pro, 10))
        data1=Details.objects.all()
        data3 = Details.objects.filter(ofr_per__gt=20)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/home.html',{'data':data,'data1':data1,'pet':pet,'cat':cat,'user':user,'data3':data3})
    else:
        return redirect(shop_login)
    
def petType(req,pid):
    if 'user' in req.session:
        data=Category.objects.filter(pet=pid)
        data2=Product.objects.all()
        data3=[]
        for i in data2:
            if int(i.category.pet.pk) == int(pid) :
                data3.append(i)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/petType.html',{'data':data,'data3':data3,'pet':pet,'cat':cat})
    else:
        return redirect(shop_login)

def products(req,pid):
    if 'user' in req.session:
        data=Product.objects.filter(category=pid)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/products.html',{'data':data,'pet':pet,'cat':cat})
    else:
        return redirect(shop_login)
    
def product(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Product.objects.get(pk=pid)
        data1=Details.objects.filter(product=pid)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        fav=Fav.objects.filter(user=user)
        f=0
        for i in fav:
            if i.pro.pk==data.pk:
                f=1
                break
        data2=Details.objects.get(product=pid,pk=data1[0].pk)
        if req.GET.get('dis'):
            dis=req.GET.get('dis')
            data2=Details.objects.get(product=pid,pk=dis)
        return render(req,'user/product.html',{'data':data,'data1':data1,'data2':data2,'pet':pet,'cat':cat,'f':f})
    else:
        return redirect(shop_login)
    
def addCart(req,pid):
    if 'user' in req.session:
        prod=Details.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        try:
            data=Cart.objects.get(user=user,pro=prod)
            data.qty+=1
            data.price=data.pro.ofr_price*data.qty
            data.save()
        except:
            price=prod.ofr_price
            data=Cart.objects.create(user=user,pro=prod,qty=1,price=price)
            data.save()
        prod.stock-=1
        prod.save()
        return redirect(viewCart)
    else:
        return redirect(shop_login)  
    
def addFav(req,pid):
    if 'user' in req.session:
        prod=Product.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        try:
            data=Fav.objects.get(user=user,pro=prod)
            if data:
                return redirect(viewFav)
        except:
            data=Fav.objects.create(user=user,pro=prod)
            data.save()
        return redirect(viewFav)
    else:
        return redirect(shop_login)  

def viewFav(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Fav.objects.filter(user=user)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/viewFav.html',{'data':data,'pet':pet,'cat':cat})
    else:
        return redirect(shop_login) 

def deleteFav(req,pid):
    if 'user' in req.session:
        data=Fav.objects.get(pk=pid)
        data.delete()
        return redirect(viewFav)
    else:
        return redirect(shop_login) 


def viewCart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=user)
        total=0
        for i in data:
            total+=i.price
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/viewCart.html',{'data':data,'pet':pet,'cat':cat,'total':total})
    else:
        return redirect(shop_login) 
    
def deleteCart(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        data.delete()
        return redirect(viewCart)
    else:
        return redirect(shop_login) 

def cartIncrement(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        if data.pro.stock>0:
            data.qty+=1
            data.price=data.pro.ofr_price*data.qty
            pro=data.pro
            pro.stock-=1
            pro.save()
            data.save()
        return redirect(viewCart)
    else:
        return redirect(shop_login) 
       
def cartDecrement(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        if(data.qty>0):
            data.qty-=1
            data.price=data.pro.ofr_price*data.qty
            pro=data.pro
            pro.stock+=1
            pro.save()
            data.save()
        if data.qty==0:
            data.delete()
        return redirect(viewCart)
    else:
        return redirect(shop_login) 
    
def buyNow(req,pid):
    if 'user' in req.session:
        prod=Details.objects.get(pk=pid)
        discount=int(prod.price-prod.ofr_price)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if data:
            return redirect("orderSummary",prod=prod.pk,data=data,discount=discount)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect("orderSummary",prod=prod.pk,data=data,discount=discount)
            else:
                return render(req,"user/addAddress.html")
    else:
        return redirect(shop_login) 

def orderSummary(req,prod,data,discount):
    if 'user' in req.session:
        prod=Details.objects.get(pk=prod)
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        if req.method == 'POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/orderSummary.html',{'prod':prod,'data':data,'discount':discount,'pet':pet,'cat':cat})
        req.session['address']=addr.pk
        req.session['det']=prod.pk
        if pay == 'paynow':
            return redirect("payment")    
        else:
            return redirect("book")
    else:
        return redirect(shop_login)

# def payment(req,pid,address):
#     if 'user' in req.session:
#         # user=User.objects.get(username=req.session['user'])
#         pet=Pet.objects.all()
#         cat=Category.objects.all()
#         data=Details.objects.get(pk=pid)
#         price=data.ofr_price
#         addr=Address.objects.get(pk=address)
#         return render(req,'user/payment.html',{'price':price,'data':data,'address':addr,'pet':pet,'cat':cat})
#     else:
#         return redirect(shop_login) 
    
def order_payment(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        data = Details.objects.get(pk=req.session['det'])
        name = user.first_name
        amount = data.ofr_price
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(shop_login)

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect("book",pid=data,address=address)  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return redirect("book")  
 

    else:

        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  

def book(req):
    if 'user' in req.session:
        address=Address.objects.get(pk=req.session['address'])
        prod=Details.objects.get(pk=req.session['det'])
        user=User.objects.get(username=req.session['user'])
        data=Bookings.objects.create(user=user,pro=prod,qty=1,price=prod.ofr_price,address=Address.objects.get(pk=address.pk))
        data.save()
        prod.stock-=1
        prod.save()
        return redirect(bookings)
    else:
        return redirect(shop_login)

    
def bookings(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Bookings.objects.filter(user=user)[: : -1]
        pet=Pet.objects.all()
        cat=Category.objects.all()
        return render(req,'user/bookings.html',{'data':data,'pet':pet,'cat':cat})
    else:
        return redirect(shop_login) 
    
def buyAll(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        discount=0
        for i in cart:
            discount+=(float(i.pro.price-i.pro.ofr_price)*i.qty)
        price=0
        for i in cart:
            price+=(i.pro.price)*i.qty
        total=price-discount
        data=Address.objects.filter(user=user)
        if data:
            # return render(req,'user/orderSummary2.html',{'cart':cart,'data':data,'discount':discount,'price':price,'total':total})
            return redirect("orderSummary2",discount=discount,price=price,total=total)
        else:
            if req.method=='POST':
                user=User.objects.get(username=req.session['user'])
                name=req.POST['name']
                phn=req.POST['phn']
                house=req.POST['house']
                street=req.POST['street']
                pin=req.POST['pin']
                state=req.POST['state']
                data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
                data.save()
                return redirect("orderSummary2",discount=discount,price=price,total=total)
            else:
                return render(req,"user/addAddress.html")
    else:
        return redirect(shop_login) 
    
def orderSummary2(req,discount,price,total):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        cart=Cart.objects.filter(user=user)
        pet=Pet.objects.all()
        cat=Category.objects.all()
        if req.method == 'POST':
            address=req.POST['address']
            pay=req.POST['pay']
            addr=Address.objects.get(user=user,pk=address)
        else:
            return render(req,'user/orderSummary2.html',{'cart':cart,'data':data,'discount':discount,'price':price,'total':total,'discount':discount,'pet':pet,'cat':cat})
        req.session['address']=addr.pk
        if pay == 'paynow':
            return redirect("payment2")    
        else:
            return redirect("book2")
    else:
        return redirect(shop_login)

def payment2(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        cart=Cart.objects.filter(user=user)
        discount=0
        for i in cart:
            discount+=(float(i.pro.price-i.pro.ofr_price)*i.qty)
        price=0
        for i in cart:
            price+=(i.pro.price)*i.qty
        total=price-discount
        amount = total
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment2.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback2",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(shop_login)

@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect("book2")  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return redirect("book2")  
 

    else:

        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  

def book2(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        address=Address.objects.get(pk=req.session['address'])
        cart=Cart.objects.filter(user=user)
        for i in cart:
            data=Bookings.objects.create(user=i.user,pro=i.pro,qty=i.qty,price=i.price,address=Address.objects.get(pk=address.pk))
            data.save()
        cart.delete()
        return redirect(bookings)
    else:
        return redirect(shop_login)
      
def deleteBookings(req,pid):
    if 'user' in req.session:
        data=Bookings.objects.get(pk=pid)
        data.delete()
        return redirect(bookings)
    else:
        return redirect(shop_login)
    
def address(req):
    if 'user' in req.session:
        pet=Pet.objects.all()
        cat=Category.objects.all()
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            house=req.POST['house']
            street=req.POST['street']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,house=house,street=street,pin=pin,state=state)
            data.save()
            return redirect(address)
        else:
            return render(req,"user/addAddress.html",{'data':data,'pet':pet,'cat':cat})
    else:
        return redirect(shop_login) 
    
def delete_address(req,pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(address)
    else:
        return redirect(shop_login)