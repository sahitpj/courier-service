#!python
#log/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect , Http404
from django.db.models import Q
from django.views import generic
from django.views.generic import View
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import UserForm, PostForm

# Create your views here.
# this login required decorator is to not allow to any  
# view without authenticating
def start(request):
    return render(request,"design.html")

@login_required(login_url="login/")
def home(request):
    parcels = Post.objects.all().order_by("-date")
    context = {"couriers": parcels}
    return render(request,"adminhomepage.html",context)

from django.shortcuts import render, get_object_or_404, redirect
def homepage(request):
    parcels = Post.objects.all().order_by("-date")
    parcels = parcels.filter(flag=0)
    for i in parcels:
        i.receiver  = i.receiver.capitalize()
        i.company = i.company.capitalize()
    query = request.GET.get("q")
    if query:
            parcels= parcels.filter(
            Q(company__icontains=query) |
            Q(receiver__icontains=query) |
            Q(hostelname__icontains=query)
        ).distinct()
    context = {"couriers": parcels}
    if (len(context["couriers"])==0):
        return render(request,"nothing.html",context)
    return render(request, "homepage3.html", context)
def hostelfilter(request,hostelname):
    parcels_list = Post.objects.all().order_by("-date")
    parcels_list = parcels_list.filter(Q(hostelname__icontains=hostelname))
    parcels_list = parcels_list.filter(flag=0)
    for i in parcels_list:
        i.receiver  = i.receiver.capitalize()
        i.company = i.company.capitalize()
    query = request.GET.get("q")
    if query:
        query = query.split()
        for i in query:
            parcels_list = parcels_list.filter(
                Q(company__icontains=i) |
                Q(receiver__icontains=i) |
                Q(hostelname__icontains=i)|
            Q(room__icontains=i)) .distinct()

        if len(parcels_list) == 0:
            lst = []
            for i in query:
                parcels_list = Post.objects.all().order_by("-date")
                parcels_list = parcels_list.filter(
                    Q(company__icontains=i) | Q(receiver__icontains=i) | Q(hostelname__icontains=i)).distinct()
                a = list(parcels_list)
                lst = lst + a
            parcels_list = lst
    if query:
        context = {"couriers": parcels_list}
        if (len(context["couriers"]) == 0):
            return render(request, "nothing.html", context)
        new_cour = (context["couriers"])[0].receiver
        context["new_cour"] = new_cour
        return render(request, "searchresults.html", context)
    context = {"couriers":parcels_list}
    if (len(context["couriers"])==0):
        return render(request,"nothing.html",context)
    new_cour = (context["couriers"])[0].receiver

    context["new_cour"] = new_cour
    return render(request, "homepage3.html", context)


class UserFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name)
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()


            user = authenticate(username=username,password=password)
            if user is not None:

                if user.is_active:
                    login(request, user)
                    return redirect(home)


        return render(request, self.template_name, {'form': form})
def form_create(request):
    if request.user.is_authenticated:
        form = PostForm(request.POST or None, request.FILES or None)
        context = {
            "form": form,
        }
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            context = {
                "title": "Thank you",
                "form":form,
            }
        return render(request, "addcourier.html", context)
    else:
        return render(request,'nologin.html')

def admin_show(request):
    if request.user.is_authenticated:
        parcels = Post.objects.all().order_by("-date")
        query = request.GET.get("q")
        if query:
                parcels= parcels.filter(
                Q(company__icontains=query) |
                Q(receiver__icontains=query) |
                Q(hostelname__icontains=query)
            ).distinct()
        context = {"couriers":parcels}
        return render(request, "adminhomepage.html", context)
    else:
        return render(request,'nologin.html')

def flagchanger(request,id):

    id=int(id)
    instance = get_object_or_404(Post, id=id)
    if instance:
        if instance.flag == 0:
            instance.flag=1
        else:
            instance.flag=0
        instance.save()
    instance.save()
    parcels = Post.objects.all().order_by("-date")
    context = {"couriers":parcels}
    return render(request, "adminhomepage.html", context)
'''def flagchanger(request,id):
    a = int(id)
    return render(request,'nothing.html',{})'''
def hostelfilteradmin(request ,hostelname):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    parcels = Post.objects.all().order_by("-date")
    parcels = parcels.filter(Q(hostelname__icontains=hostelname))
    query = request.GET.get("q")
    if query:
            parcels= parcels.filter(
            Q(company__icontains=query) |
            Q(receiver__icontains=query) |
            Q(hostelname__icontains=query)
        ).distinct()
    context = {"couriers": parcels}
    if (len(context["couriers"]) == 0):
        return render(request, "nothing.html", context)
    return render(request, "adminhomepage.html", context)