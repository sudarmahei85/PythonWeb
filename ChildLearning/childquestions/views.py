from django.shortcuts import render,redirect
from childquestions.models import problemForm,Problem,Users,problemSelectForm,Respgrp,Respgrpanswer,Rewards,rewardsForm
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
def problems(request):
    pf = problemForm()
    request.session['user_id']= '1abc'
    request.session['username']='Tester'
    respgrpdropdown = Respgrp.objects.all()     
    return render(request,'Problems.html',{'form':pf,'resp_lis':respgrpdropdown})

def problemSubmit(request):
    if request.method == 'POST':
        print('line1') 
        user_p = Users()
        user_p.users_id= request.session.get('user_id')
        user_p.username=request.session.get('username')
        prob = Problem.objects.create(Users=user_p)
        prob.save()
        pf = problemForm(request.POST,request.FILES,instance=prob)
        if pf.is_valid():
            pd = pf.cleaned_data
            print(pd)
            pf.save(commit=True)
            return  redirect('/problem/')
        else:
            print('line3')  
                                     
    return  redirect('/sendProblem/')

def all_json_answers(request, respgroup):
    current_respgrp = Respgrp.objects.get(respgrp_id=respgroup)
    answers = Respgrpanswer.objects.all().filter(Respgrp=current_respgrp)
    json_models = serializers.serialize("json", answers)
    return HttpResponse(json_models, content_type="application/json")

def problemSelect(request):
    print('line1;select') 
    user_s = Users()
    user_s.users_id= request.session.get('user_id')
    user_s.username=request.session.get('username')
    prob= Problem.objects.all().filter(Users=user_s)
    for pr in prob:
        print(pr.question)
    return render(request,'sendProblem.html',{'form':prob})   

def problemSend(request):
    if request.method == 'POST':
        print('line1') 
        user_p = Users()
        user_p.users_id= request.session.get('user_id')
        user_p.username=request.session.get('username')
        values = request.POST.getlist(u'problemId')
        print(values)
    prob= Problem.objects.filter(Users=user_p)
            
    return render(request,'sendProblem.html',{'form':prob}) 
  
def rewards(request):
    
    if request.method == 'POST':
        print('line1') 
        user_p = Users()
        user_p.users_id= request.session.get('user_id')
        user_p.username=request.session.get('username')
        rew = Rewards.objects.create(Users=user_p)
        rew.save()
        rw = rewardsForm(request.POST,request.FILES,instance=rew)
        if rw.is_valid():
            pd = rw.cleaned_data
            print('line2')        
            print(pd)
            rw.save(commit=True)
            return  redirect('/rewards/')
    else:
        rf = rewardsForm()    
       
    return render(request,'Reward.html',{'form':rf})

def homepage(request):
     
    return render(request,'Home.html')
   
