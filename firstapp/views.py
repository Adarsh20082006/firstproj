from django.shortcuts import render,redirect # type: ignore
from .models import Room,Topic,Message # type: ignore
from .forms import RoomForm,UserForm # type: ignore
from django.db.models import Q # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth import login,logout,authenticate # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.http import HttpResponse # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
# Create your views here.
# roooms=[
#     {'id':1 ,'name':'Python page',},
#     {'id':2 ,'name':'Java page',},
#     {'id':3 ,'name':'js page',},
#     {'id':4 ,'name':'other',},
#     ]
    

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    roooms=Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topic=Topic.objects.all()[0:4]
    total=roooms.count()
    comment=Message.objects.filter(Q(room__topic__name__contains=q))
    return render(request,'firstapp/home.html',{'rooms':roooms,'topics':topic,'count':total,'comments':comment})

def rooms(request,pk):
   
    page=Room.objects.get(id=pk)
    msgs=page.message_set.all().order_by('-created')
    participants=page.participants.all()
    if request.method=='POST':
        comment=Message.objects.create(
            user=request.user,
            room=page,
            body=request.POST.get('body')
        )
        page.participants.add(request.user)
        return redirect('room',pk=page.id)

    context={'page':page,'msgs':msgs,'participants':participants}
    return render(request,'firstapp/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    topics=Topic.objects.all()
    form=RoomForm() 
    if request.method=='POST':
       
       topic=request.POST.get('topic')
       topic,created=Topic.objects.get_or_create(name=topic)
       room=Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name') ,
           description=request.POST.get('description'),
        )
    #    room.save()
       return redirect('home') 
    context={'form':form,'topics':topics}
    return render(request,'firstapp/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
   topics=Topic.objects.all()
   room= Room.objects.get(id=pk)
   form=RoomForm(instance=room)
   if request.user!=room.host:
       return HttpResponse('You are not allowed')
       

   if request.method=='POST':
       topic=request.POST.get('topic')
       topic,created=Topic.objects.get_or_create(name=topic)
       room.name=request.POST.get('name')
       room.topic=topic
       room.description=request.POST.get('description')
       room.save()
       
       return redirect('room',pk=room.id) 
       
   context={'form':form,'topics':topics,'room':room}
   return render(request,'firstapp/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    # if request.method=='POST':
    room.delete()
    return redirect('home')
   
    # return render(request,'firstapp/delete.html',{'obj':room})

def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        uName=request.POST.get('username')
        pWord=request.POST.get('password')

        try:
            user=User.objects.get(username=uName)
        except:
            messages.error(request,"User doesn't exists")
        
        user=authenticate(request,username=uName,password=pWord)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Invalid Username or Password..!")
    context={'page':page}
    return render(request,'firstapp/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form=UserCreationForm()
    if request.method == 'POST':
        # fName=request.POST.get('fullname')
        #  uName=request.POST.get('username')
        #  pWord=request.POST.get('password')
        # cWord=request.POST.get('confirm_password')
         form=UserCreationForm(request.POST)
         if form.is_valid():
           
                user=form.save(commit=False)
                user.username=user.username
                user.save()
                #user=authenticate(request,username=uName,password=pWord)
                login(request,user)
                return redirect('home')
         else:
             messages.error(request,'Something went wrong')
    
    return render(request, 'firstapp/login_register.html',{'form':form})

@login_required(login_url='login')
def deleteMsg(request,pk):
    msg=Message.objects.get(id=pk)
    user=msg.user
    if request.user==user:
        # if request.method=='POST':
            msg.delete()
            return redirect('room',pk=msg.room.id)
    # return render(request,'firstapp/delete.html',{'obj':msg})
        

def profile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    comments=user.message_set.all()
    topic=Topic.objects.all()

    context={'rooms':rooms,'comments':comments,'topics':topic,'custom':user}
    return render(request, 'firstapp/profile.html',context)

def editUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
        form=UserForm(request.POST,instance=user)
    if form.is_valid():
        form.save()
        return redirect('user-profile',pk=user.id)
    else:
        messages.error(request,'Something went wrong')
    return render(request,'firstapp/edit-user.html',{'form':form})

def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    return render(request,'firstapp/topics.html',{'topics':topics})

def activityPage(request):
    room_msg=Message.objects.all()
    return render(request,'firstapp/activity.html',{'room_msg':room_msg})