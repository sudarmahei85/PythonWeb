from django.shortcuts import render,redirect
from childquestions.models import problemForm,Problem,problemSelectForm,Respgrp,Respgrpanswer,Rewards,rewardsForm,Devices,devicesForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from childquestions.forms import RegistrationForm
from django.core import serializers
from django.http import HttpResponse,HttpResponseRedirect
import xml.etree.ElementTree as ET
from django.db.models import Sum
from childquestions.generatexml import prettify
import os.path
import codecs
from django.core.exceptions import ValidationError
from ChildLearning.settings import MEDIA_ROOT,MEDIA_FILE_LINK
  
# Create your views here.
def problems(request):
    
    if request.user.is_authenticated():
        pf = problemForm()
        respgrpdropdown = Respgrp.objects.all()     
        return render(request,'Problems.html',{'form':pf,'resp_lis':respgrpdropdown})
    else:
        return HttpResponseRedirect('/login')
        
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('register')
        if form.is_valid():
            new_user = form.save()
            print('registered')
            return HttpResponseRedirect("/")
    else:
        form = RegistrationForm()
    return render(request, "Registration.html", {
        'form': form,
    })


def problemSubmit(request):
    if request.user.is_authenticated():
        rpf = problemForm() 
        respgrpdropdown = Respgrp.objects.all() 
        user_p = request.user
        pfl = Problem.objects.filter(Users=user_p)   
        try:
            if request.method == 'POST':
                print('line1') 
                prob = Problem.objects.create(Users=user_p)
                prob.save()
                pf = problemForm(request.POST,request.FILES,instance=prob)
                if pf.is_valid():
                    pd = pf.cleaned_data
                    print('saving')
                    pf.save(commit=True)
                    pfl = Problem.objects.filter(Users=user_p)  
                    return render(request,'Problems.html',{'form':rpf,'resp_lis':respgrpdropdown,'problist':pfl,'success':'Saved successfully'})
                prob.delete()
                return render(request,'Problems.html',{'form':pf,'resp_lis':respgrpdropdown,'problist':pfl,'error':pf._errors})
                    
            else:
                return render(request,'Problems.html',{'form':rpf,'resp_lis':respgrpdropdown,'problist':pfl})
        except:
            error='Error occured while saving. Please try again later'  
            return render(request,'Problems.html',{'form':rpf,'resp_lis':respgrpdropdown,'problist':pfl,'error':error})
    else:
        return  HttpResponseRedirect('/login') 

def all_json_answers(request, respgroup):
    current_respgrp = Respgrp.objects.get(respgrp_id=respgroup)
    answers = Respgrpanswer.objects.all().filter(Respgrp=current_respgrp)
    json_models = serializers.serialize("json", answers)
    return HttpResponse(json_models, content_type="application/json")

def problemSelect(request):
    if request.user.is_authenticated():
        print('line1;select') 
        user_s =request.user
        prob= Problem.objects.all().filter(Users=user_s)
        
        return render(request,'sendProblem.html',{'form':prob})   
    else:
        return  HttpResponseRedirect('/login') 
def Problemdel(request):
    if request.user.is_authenticated():
        rpf = problemForm() 
        respgrpdropdown = Respgrp.objects.all() 
        user_p = request.user
        pf = Problem.objects.filter(Users=user_p)
        try:
            if request.method == 'POST':
                print('line1 del') 
                values = request.POST.getlist(u'problemId')
                problemlist=Problem.objects.filter(problemId__in=values).delete()
                pf = Problem.objects.filter(Users=user_p)
                return render(request,'Problems.html',{'form':rpf,'resp_lis':respgrpdropdown,'problist':pf,'success':'Deleted successfully'})
            else:
                return render(request,'Problems.html',{'form':rpf,'problist':pf,'resp_lis':respgrpdropdown})
            
            
        except:
            error='Error occured while Deleting. Please try again later'   
            return(request,'Problems.html',{'form':rpf,'resp_lis':respgrpdropdown,'problist':pf,'error':error})
    else:
        return  HttpResponseRedirect('/login')           
    
def rewards(request):
    if request.user.is_authenticated():
        rf = rewardsForm()
        rrf=rewardsForm()
        user_p = request.user
        rf = Rewards.objects.filter(Users=user_p)
        try:
            if request.method == 'POST':
                print('line1') 
                rew = Rewards.objects.create(Users=user_p)
                rw = rewardsForm(request.POST,request.FILES,instance=rew)
                if rw.is_valid():
                    pd = rw.cleaned_data
                    print('saving')        
                    rw.save(commit=True)
                    rf = Rewards.objects.filter(Users=user_p)
                    return render(request,'Reward.html',{'form':rrf,'reward':rf,'success':'Saved successfully'})
                rew.delete()
                rf = Rewards.objects.filter(Users=user_p)
                return render(request,'Reward.html',{'form':rrf,'reward':rf,'error':rw._errors})
            else:
                return render(request,'Reward.html',{'form':rrf,'reward':rf})
            
            
        except:
            error='Error occured while saving. Please try again later'   
            return render(request,'Reward.html',{'form':rrf,'reward':rf,'error':error})
    else:
        return  HttpResponseRedirect('/login')
def homepage(request):
    if request.user.is_authenticated(): 
        print('home Valid')
        return render(request,'Home.html')
    else:
        print('home else')
        return render(request,"Login.html")  
        
def loginpage(request):
    
    if request.user.is_authenticated(): 
        print('home Valid')
        return render(request,'Home.html')
    
    form = AuthenticationForm(None,request.POST)
    print('good')
    if form.is_valid():
        login(request, form.get_user())
        print('Success')
        return render(request,'Home.html')
    else:
        form = AuthenticationForm()   
    return render(request,"Login.html", {'form':form,})      

   
def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/login') 
        
def rewardsdel(request):
    if request.user.is_authenticated():
        rf = rewardsForm()
        rrf=rewardsForm()
        user_p = request.user
        rf = Rewards.objects.filter(Users=user_p)
        try:
            if request.method == 'POST':
                print('line1') 
                values = request.POST.getlist(u'rewards_id')
                results = [int(i) for i in values]
                rewardlist=Rewards.objects.filter(rewards_id__in=results).delete()
                rf = Rewards.objects.filter(Users=user_p)
                return render(request,'Reward.html',{'form':rrf,'reward':rf,'success':'Deleted successfully'})
            else:
                return render(request,'Reward.html',{'form':rrf,'reward':rf})
            
            
        except:
            error='Error occured while Deleting. Please try again later'   
            return render(request,'Reward.html',{'form':rrf,'reward':rf,'error':error})
    else:
        return  HttpResponseRedirect('/login')
def devices(request):
    if request.user.is_authenticated():
        df = devicesForm()
        user_p = request.user
        rf = Devices.objects.filter(Users=user_p)
        try:
            if request.method == 'POST':
                print('line1') 
                devin=Devices.objects.create(Users=user_p)
                dev = devicesForm(request.POST,instance=devin)
                if dev.is_valid():
                    pd = dev.cleaned_data
                    print('saving')    
                    print(pd)
                    dev.save(commit=True)
                    rf = Devices.objects.filter(Users=user_p)
                    return render(request,'Device.html',{'form':df,'devices':rf,'success':'Saved successfully'})
                devin.delete()
                return render(request,'Device.html',{'form':df,'devices':rf,'error':dev._errors})
            else:
                return render(request,'Device.html',{'form':df,'devices':rf})
            
            
        except:
            error='Error occured while saving. Please try again later'   
            return render(request,'Device.html',{'form':df,'devices':rf,'error':error})
    else:
        return  HttpResponseRedirect('/login') 
def devicesdel(request):
    if request.user.is_authenticated():
        df = devicesForm()
        user_p = request.user
        rf = Devices.objects.filter(Users=user_p)
        try:
            if request.method == 'POST':
                print('line1') 
                values = request.POST.getlist(u'deviceid')
                results = [int(i) for i in values]
                rflisy = Devices.objects.filter(deviceid__in=results).delete()
                rf = Devices.objects.filter(Users=user_p)
                return render(request,'Device.html',{'form':df,'devices':rf,'success':'Deleted successfully'})
                
            else:
                return render(request,'Device.html',{'form':df,'devices':rf})
            
            
        except:
            error='Error occured while Deleting. Please try again later'   
            return render(request,'Device.html',{'form':df,'devices':rf,'error':error})
    else:
        return  HttpResponseRedirect('/login')     
def problemSend(request):
    if request.user.is_authenticated():
        try:
            if request.method == 'POST':
                print('line1') 
                user_p = request.user
                values = request.POST.getlist(u'problemId')
                print(values)
                problemlist= Problem.objects.filter(problemId__in=values)
                totalweight=Problem.objects.filter(problemId__in=values).aggregate(Sum('weight')).get('weight__sum')
                rewards=Rewards.objects.filter(Users=user_p)
                respgrp=Respgrp.objects.all()
                prob= Problem.objects.all().filter(Users=user_p)
                #<?xml version="1.0" encoding="UTF-8"?>
                pragmatic = ET.Element('appname_resource')
                
                # <rewards/>
                xmlrewards = ET.SubElement( pragmatic, 'rewards' )
                for re in rewards:
                    if re.shasum not in [None, '']:
                        if re.filetype=='Video':
                            xmlreward=ET.SubElement(xmlrewards,'reward')
                            video = ET.SubElement(xmlreward, 'video')
                            sha256sum = ET.SubElement(video, 'sha256sum')
                            sha256sum.text=re.shasum
                            guid = ET.SubElement(video, 'guid')
                            guid.text=re.guidvalue
                        elif re.filetype =='Audio': 
                            xmlreward=ET.SubElement(xmlrewards,'reward')
                            audio = ET.SubElement(xmlreward, 'audio')
                            sha256sum = ET.SubElement(audio, 'sha256sum')
                            sha256sum.text=re.sasum
                            guid = ET.SubElement(audio, 'guid')
                            guid.text=re.guidvalue 
                            retype = ET.SubElement(audio, 'type')
                            retype.text='vorbis'
              
                total_weight = ET.SubElement( pragmatic, 'total_weight' )
                total_weight.text=str(totalweight)   
                # <problems/>
                problems = ET.SubElement( pragmatic, 'problems' )
                for pr in problemlist:
                    xmlproblem = ET.SubElement( problems, 'problem',{'probid':str(pr.problemId),
                                              'weight':str(pr.weight),})
                                              
                    responses = ET.SubElement( xmlproblem, 'responses' )                          
                    response = ET.SubElement( responses, 'response',{'group':str(pr.AnswerGroup.respgrp_id),
                                              'answer':str(pr.Answer.respgrpanswer_id),})  
                    text = ET.SubElement( xmlproblem, 'text' )
                    text.text=str(pr.Question)                           
                    xmlimage = ET.SubElement(xmlproblem, 'image')
                    sha256sum = ET.SubElement(xmlimage, 'sha256sum')
                    sha256sum.text=pr.shasum
                    guid = ET.SubElement(xmlimage, 'guid')
                    guid.text=pr.guidvalue
                    retype = ET.SubElement(xmlimage, 'type')
                    retype.text=pr.filetype
                      
                xmlresponses = ET.SubElement( pragmatic, 'responses' )        
                for rs in respgrp:
                    group = ET.SubElement( xmlresponses, 'group',{'name':rs.AnswerGroup,
                                              'id':str(rs.respgrp_id),} )
                    rsanswer=Respgrpanswer.objects.filter(Respgrp=rs)
                    for ans in rsanswer:
                        item = ET.SubElement( group, 'item',{'id':str(ans.respgrpanswer_id),} )
                        text = ET.SubElement( item, 'text')
                        text.text=ans.Answer
               
                
                #data=prettify(pragmatic)
               
                filenames=Devices.objects.filter(Users=user_p)
                for filekey in filenames:
                    filename=MEDIA_FILE_LINK+filekey.DeviceKey+'.xml'
                    print(filename)
                    data=prettify(pragmatic)
                    if not os.path.exists(os.path.dirname(filename)):
                        os.makedirs(os.path.dirname(filename))
                    with codecs.open(filename, "wb",encoding='utf8') as f:
                        f.write(data)
                
                
            return render(request,'sendProblem.html',{'form':prob,'success':'Successfully Sent'})
        except:
            prob= Problem.objects.all().filter(Users=request.user)   
            error='Error occured while Sending. Please try again later'  
            return render(request,'sendProblem.html',{'form':prob,'error':error})
    else:
        return  HttpResponseRedirect('/login')
