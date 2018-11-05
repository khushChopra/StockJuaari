from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import singlestock, profile, feedback
from .forms import ProfileForm, LoginForm, FeedbackForm, upform, poForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from random import randint
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .dbfeeder import ourdata


import feedparser
feeds = feedparser.parse('http://feeds.marketwatch.com/marketwatch/realtimeheadlines/')
# Create your views here.

def gita(request):

    return render(request, 'stock/bakwas.html', {})


def git(request):

#9148464923
    data = ourdata()
    data['Yearly'] = data['Yearly'].astype(float)
    data['Q1'] = data['Q1'].astype(float)
    data['Q2'] = data['Q2'].astype(float)
    data['Q3'] = data['Q3'].astype(float)
    data['Share'] = data['Share'].astype(str)
    data['Sector'] = data['Sector'].astype(str)
    data['Cap Category'] = data['Cap Category'].astype(str)
    data['Category'] = data['Category'].astype(str)
    print(data.dtypes)
    for d in [data]:
        d['Category'] = d['Category'].map({'YES': 'True', 'NO': 'False'})
    data['Category'] = data['Category'].astype(bool)
    print(data.dtypes)
    for i in range(len(data)):
        singlestock.objects.create(name=data['Share'][i], sector=data['Sector'][i], cap=data['Cap Category'][i],
                                   last_trade_price=data['Last Traded Price'][i], high=data['High Price'][i], low=data['Low Price'][i],
                                   yearly=data['Yearly'][i], q1=data['Q1'][i], q2=data['Q2'][i], q3=data['Q3'][i], hold=data['Category'][i])

    return HttpResponse('Sup')

def shift(l):
    n = randint(0,len(l))
    return l[n:] + l[:n]


def first(request):
    return HttpResponseRedirect('/stock/dashboard/')



def detailview(request, pid):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')
    context = { 'user' : profile.objects.get(user_ref= request.user) ,'feeds': feeds , 'bigasslist': shift(singlestock.objects.all())[:30], 'object' : get_object_or_404(singlestock, pk=pid)}
    return render(request, 'stock/detail.html', context)

def about(request):
    return render(request, 'stock/about.html', {'feeds': feeds })


def services(request):
    return render(request, 'stock/services.html', {'feeds': feeds })
'''
def contact(request):
    return render(request, 'stock/contact.html', {})
'''

def contact(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            k = feedback.objects.create(name= request.POST['name'], content= request.POST['content'])
            return HttpResponse('Thanks')
    else:
        form = FeedbackForm()
    return render(request, 'stock/contact.html', {'form':form,'feeds': feeds })

def dashboard(request):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')

    if(len(profile.objects.filter(user_ref= request.user))==0):
        new_profile = profile.objects.create(name = request.user.first_name, user_ref = request.user, company = "Not entered", email = request.user.email)
    else:
        context = {'user': profile.objects.get(user_ref=request.user), 'bigasslist': shift(singlestock.objects.all())[:30],
                   'feeds': feeds}
        return render(request, 'stock/dashboard.html', context)

    context = { 'user' : profile.objects.get(user_ref= request.user) , 'bigasslist': shift(singlestock.objects.all())[:30],'feeds': feeds }
    return render(request, 'stock/dashboard.html', context)


'''
class ListView(generic.ListView):
    template_name = 'stock/listview.html'

    def get_queryset(self):
        return singlestock.objects.all()


'''



def noti(request):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')

    tat = singlestock.objects.all()
    hh = tat.order_by('high')[::-1][0:5]
    by = tat.order_by('yearly')[::-1][0:5]


    context = { 'by':by,'hh':hh,'user' : profile.objects.get(user_ref= request.user) ,'feeds': feeds , 'bigasslist': shift(singlestock.objects.all())[:30]}

    return render(request, 'stock/noti.html', context)


def addtolist(request , pid):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')
    stock = get_object_or_404(singlestock, pk= pid)
    pro = get_object_or_404(profile, user_ref= request.user)

    pro.stocks.add(stock)
    pro.save()
    a = '/stock/' + str(pid)+'/'
    return HttpResponseRedirect(a)


def remove(request , pid):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')
    stock = get_object_or_404(singlestock, pk= pid)
    pro = get_object_or_404(profile, user_ref= request.user)

    pro.stocks.remove(stock)
    pro.save()
    a = '/stock/' + str(pid)+'/'
    return HttpResponseRedirect(a)


def signup(request):
    return render(request, 'stock/signup.html', {})

def search(request):
    query = request.POST['searched']
    a = singlestock.objects.filter(name__icontains=query)
    return render(request, 'stock/listview.html', { 'object_list' : a ,'feeds': feeds , 'user' : profile.objects.get(user_ref= request.user) })

'''
def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('detail', pk=post.pk)
    else:
        form = NameForm()
    return render(request, 'stock/form.html', {'form':form})
'''

def profileregister(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            if len(User.objects.filter(username= request.POST['email_ID']))!=0:
                return HttpResponse('email ID already registered')

            if request.POST['password'] == request.POST['confirm_password']:
                user = User.objects.create_user(username=request.POST['email_ID'], email=request.POST['email_ID'], password=request.POST['password'])
                profile.objects.create(user_ref= user, name=request.POST['name'], email= request.POST['email_ID'], age= 0, company= request.POST['company'])
                # authenticate(username= request.POST['email_ID'], password=request.POST['password'])
                #login(request, user)
                return HttpResponseRedirect('bakwas/')

            else:
                return HttpResponse("Passwords didn't match")

    else:
        form = ProfileForm()
    return render(request, 'stock/form.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if len(User.objects.filter(username= request.POST['email_id']))!=0:
                user= authenticate(username= request.POST['email_id'], password= request.POST['password'])
                if user is None:
                    return HttpResponse("User doesn't exist")

                else:
                    login(request, user)
                    return HttpResponseRedirect('/stock/')
            else:
                return HttpResponse("Error")

    else:
        form = LoginForm()
    return render(request, 'stock/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    print(5)
    return HttpResponseRedirect('/')

def paaa(request):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')
    context = { 'user' : profile.objects.get(user_ref= request.user) ,'feeds': feeds , 'bigasslist': shift(singlestock.objects.all())[:30]}
    return render(request, 'stock/profiles.html', context)


def edit(request):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')

    if request.method == 'POST':
        form = poForm(request.POST)
        if form.is_valid():
            k = profile.objects.get(user_ref= request.user)
            k.age = request.POST['age']
            k.company = request.POST['company']
            k.save()
            return HttpResponseRedirect('/stock/profile/')
    else:
        form = poForm()

    context = { 'user' : profile.objects.get(user_ref= request.user) ,'feeds': feeds , 'bigasslist': shift(singlestock.objects.all())[:30], 'form':form}
    return render(request, 'stock/editp.html', context)


def listview(request):
    return HttpResponseRedirect('/stock/all/0/1')


def pagi(request, fby, page):
    if (not request.user.is_authenticated):
        return HttpResponse('login first')
    tat = singlestock.objects.all()

    if fby == '0':
        tat = tat.order_by('name')
    elif fby == '1':
        tat = tat.order_by('high')
    elif fby == '2':
        tat = tat.order_by('yearly')
    elif fby == '3':
        tat = tat.order_by('name')[::-1]
    elif fby == '4':
        tat = tat.order_by('high')[::-1]
    elif fby == '5':
        tat = tat.order_by('yearly')[::-1]
    #return HttpResponse(str(fby)+' ' +str(pag))

    paginator = Paginator(tat, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    page = int(page)

    #return HttpResponse(str(paginator.num_pages))
    context = { 'user' : profile.objects.get(user_ref= request.user) ,'feeds': feeds , 'object_list': users, 'bigasslist': shift(singlestock.objects.all())[:30], 'fby': fby, 'page': page, 'pn': page -1, 'pp': page + 1}

    return render(request, 'stock/listview.html', context)