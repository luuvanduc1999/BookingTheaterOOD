from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, get_list_or_404, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
 #the login_required decorator
from .models import dashboard, Ticket, Movie, Room
from .form import UpdateDashboardForm, CreateTicket, ConfirmTicket
from django.db.models import Q 
import datetime

import re
# Create your views here.
@login_required
def showInfo(request):
    profile = request.user
    param = {}
    param["profile"] = profile
    return render(request, 'profile.html', param)

@login_required
def editprofile(request):
    context ={}
    id=request.user.id
    obj = get_object_or_404(dashboard, id =id)
    form = UpdateDashboardForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
    context["form"] = form
    context["per"] = request.user.is_superuser
    return render(request, "update_profile.html", context)

@login_required
def showTicket(request):
    profile = request.user
    user=request.user.id
    obj = list(Ticket.objects.filter(user=user).order_by('id').reverse())
         
    idx=0
    if (len(obj)>0):
        item=obj[idx]
    else: item=None;

    param = {}
    param["obj"] = obj
    param["item"] = item
    if (item.type=="3D"):
        param["price"] = "{:,}".format(item.slot*30000)
    else:
        param["price"] = "{:,}".format(item.slot*20000)
    return render(request, 'ticket-list.html', param)

@login_required
def showTicketID(request, idx):
    profile = request.user
    user=request.user.id
    obj = list(Ticket.objects.filter(user=user).order_by('id').reverse())

    item=get_object_or_404(Ticket, id =idx)
    param = {}
    param["obj"] = obj
    param["item"] = item
    if (item.type=="3D"):
        param["price"] = "{:,}".format(item.slot*30000)
    else:
        param["price"] = "{:,}".format(item.slot*20000)
    return render(request, 'ticket-list.html', param)


@login_required
def createTicket(request):
    context ={}
    form = CreateTicket(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.user= request.user
        form.save()
    context["form"] = form
    return render(request, 'create-ticket.html', context)

class SearchResultsView(ListView):
    model = Movie
    paginate_by = 10
    ordering = ['-year']
    template_name = 'booking.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        if not query :
            query = ""
        object_list = Movie.objects.filter(
            Q(name__icontains=query) 
        )
        return object_list

@login_required
def movie_booking(request, movie_id):
    query = request.GET
    movie_info = Movie.objects.get(id=movie_id)
    room_list = Room.objects.all()
    ticket_list = Ticket.objects.all()

    time_list = ["8h", "11h", "14h", "17h", "20h",]
    date_list = []
    date_list.append(datetime.date.today().isoformat() )
    date_list.append( (datetime.date.today() + datetime.timedelta(days=1)).isoformat() )
    status = []
    if (query):
        for x in room_list:
            if (ticket_list.filter(room=x.id, time=query["time"], date=query["date"]).count()==0):
                status.append(1)
            else: 
                status.append(0)
        request.session['time'] = query["time"]
        request.session['date'] = query["date"]
    status_list=zip(room_list, status)    
    param = {}
    param["movie"]= movie_info
    param["date_list"] = date_list          
    param["time_list"] = time_list
    param["query"] = query
    param["status_list"] = status_list
    return render(request, 'select_time.html', param)    

@login_required
def completeBooking(request, movie_id, room_id):
    if ('time' not in request.session):
        return redirect('/booking/'+movie_id)
    movie = get_object_or_404(Movie,id=movie_id)
    room = get_object_or_404(Room,id=room_id)
    time = request.session['time']
    date = request.session['date']
    form = CreateTicket(request.POST or None)
    # del request.session['time']
    # del request.session['date']
    if form.is_valid():
        form = form.save(commit=False)
        form.user= request.user
        form.time=time
        form.date=date
        form.room=room
        form.movie=movie
        form.save()
        return redirect('/order')

    param = {'movie':movie, 'room':room, 'date':date, "time":time, "form":form}
    return render(request, 'complete-booking.html', param)    

@login_required
def showHomePage(request):
    per =  request.user.is_superuser
    return render(request, 'home.html', {'per':per})

class ConfirmPageView(ListView):
    model = Ticket
    paginate_by = 5
    search_fields = ['^confirm_code']
    template_name = 'confirm.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        if not query :
            query = "NULL"
        object_list = Ticket.objects.filter(confirm_code=query)

        return object_list

@login_required
def confirm_by_code(request, confirm_code):
    Ticket.objects.filter(confirm_code=confirm_code).update(confirmed='ON')
    return redirect('/confirm/?q='+confirm_code)
    