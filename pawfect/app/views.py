from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings   


# Create your views here.
def shop_login(req):
    if 'eshop' in req.session:
        return redirect(shop_home)
    # if 'user' in req.session:
    #     return redirect(user_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['passwd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['eshop']=uname   #create session
                return redirect(shop_home)
            # else:
            #     login(req,data)
            #     req.session['user']=uname   #create session
            #     return redirect(user_home)
        else:
            messages.warning(req,'Invalid username or password.')
            return redirect(shop_login)
    
    else:
        return render(req,'login.html')

def shp_logout(req):
    req.session.flush()          #delete session
    logout(req)
    return redirect(shop_login)

# -----------------------------------shop------------------------------


def shop_home(req):
    if 'eshop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/home.html',{'data':data})
    else:
        return redirect(shop_login)

def add_prod(req):
    if 'eshop' in req.session:
        if req.method=='POST':
            # prd_id=req.POST['prd_id']
            pet_cate=req.POST['pet_cate']
            prd_cate=req.POST['prd_cate']
            prd_name=req.POST['prd_name']
            prd_price=req.POST['prd_price']
            ofr_price=req.POST['ofr_price']
            img=req.FILES['img']
            prd_dis=req.POST['prd_dis']
            data=Product.objects.create(pet=pet_cate,category=prd_cate,name=prd_name,price=prd_price,ofr_price=ofr_price,img=img,dis=prd_dis)
            data.save()
            return redirect(add_prod)
        else:
            return render(req,'shop/add_prod.html')
    else:
        return redirect(shop_login)
    
def edit_prod(req,pid):
    if 'eshop' in req.session:
        if req.method=='POST':
            pet_cate=req.POST['pet_cate']
            prd_cate=req.POST['prd_cate']
            prd_name=req.POST['prd_name']
            prd_price=req.POST['prd_price']
            ofr_price=req.POST['ofr_price']
            prd_dis=req.POST['prd_dis']
            img=req.FILES.get('img')
            if img:
                Product.objects.filter(pk=pid).update(pet=pet_cate,category=prd_cate,name=prd_name,price=prd_price,ofr_price=ofr_price,dis=prd_dis)
                data=Product.objects.get(pk=pid)
                data.img=img
                data.save()
            else:
                Product.objects.filter(pk=pid).update(pet=pet_cate,category=prd_cate,name=prd_name,price=prd_price,ofr_price=ofr_price,dis=prd_dis)
            return redirect(shop_home)
        else:
            data=Product.objects.get(pk=pid)
            return render(req,'shop/edit.html',{'product':data})
    else:
        return redirect(shop_login)
    
def delete_prod(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(shop_home)

def bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/bookings.html',{'buy':buy})
