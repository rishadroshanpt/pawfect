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
        data1=Details.objects.all()
        return render(req,'shop/home.html',{'data':data,'data1':data1})
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
                prd_cate=req.POST['cate']
                cateImg=req.FILES['cateImg']
                data1=Category.objects.create(category=prd_cate,img=cateImg)
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
            pet_cate=req.POST['pet_cate']
            prd_cate=req.POST['prd_cate']
            prd_name=req.POST['prd_name']
  
            img=req.FILES['img']
            prd_dis=req.POST['prd_dis']
            data=Product.objects.create(pet=Pet.objects.get(pet=pet_cate),category=Category.objects.get(category=prd_cate),name=prd_name,img=img,dis=prd_dis)
            data.save()
            return redirect(details)
        else:
            data=Pet.objects.all()
            data1=Category.objects.all()
            return render(req,'shop/add_prod.html',{'data':data,'data1':data1})
    else:
        return redirect(shop_login)
    
def details(req):
    if 'eshop' in req.session:
        if req.method=='POST':
            product=req.POST['pro']
            weight=req.POST['weight']
            price=req.POST['price']
            ofrPrice=req.POST['offerPrice']
            stock=req.POST['stock']
            data=Details.objects.create(product=Product.objects.get(name=product),weight=weight,price=price,ofr_price=ofrPrice,stock=stock)
            data.save()
            return redirect(details)
        else:
            data=Product.objects.all()
            return render(req,'shop/details.html',{'data':data})
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
            weight=req.POST['weight']
            price=req.POST['price']
            ofrPrice=req.POST['offerPrice']
            stock=req.POST['stock']
            data=Details.objects.create(product=Product.objects.get(name=product),weight=weight,price=price,ofr_price=ofrPrice,stock=stock)
            data.save()
            return redirect(edit_details.pid)
        else:
            data=Details.objects.filter(product=pid)
            return render(req,'shop/edit_details.html',{'data':data})
    else:
        return redirect(shop_login)


def delete_prod(req,pid):
    data=Product.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    return redirect(shop_home)

# def bookings(req):
#     buy=Buy.objects.all()[::-1]
#     return render(req,'shop/bookings.html',{'buy':buy})
