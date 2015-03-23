from django.db import models
from django.forms import ModelForm
from django import forms
import os.path
from django.core.files.storage import FileSystemStorage

class Users(models.Model):
    username = models.CharField(max_length=20)
    users_id= models.CharField(max_length=20,primary_key=True)
    class Meta:
        db_table ='users'
    def __unicode__(self):
        return self.users_id

def content_file_name(instance, filename):
        #ext = filename.split('.')[-1]
        filename = "%s/%s" % (instance.Users.users_id,filename)
        return os.path.join(filename)
    

class  Respgrp(models.Model):
    respgrp_id =models.AutoField(primary_key=True)
    respgrpname=models.TextField(max_length=45)
    class Meta:
        db_table ='respgrp'
    def __unicode__(self):
        return self.respgrp_id
    
class  Respgrpanswer(models.Model):
    respgrpanswer_id=models.AutoField(primary_key=True)
    Respgrp =models.ForeignKey(Respgrp)
    respgrpanswer=models.TextField(max_length=45) 
       
    class Meta:
        db_table ='respgrpanswer' 
         
    def __unicode__(self):
        return self.respgrpanswer_id
    
class MediaFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        if self.exists(name):
            # if the file exists, do not call the superclasses _save method
            return name
        # if the file is new, DO call it
        return super(MediaFileSystemStorage, self)._save(name, content)    
    
class Problem(models.Model):
    problemId=models.AutoField(primary_key=True)
    Users = models.ForeignKey(Users)
    question = models.TextField(max_length=200)
    answer =  models.ForeignKey(Respgrpanswer,db_column='respgrpanswer_id')
    weight= models.IntegerField(max_length=2)
    respgrp =models.ForeignKey(Respgrp)
    file = models.FileField(upload_to=content_file_name,storage=MediaFileSystemStorage()) 
    
    class Meta:
        db_table ='problems'
         
    def __unicode__(self):
        return self.problemId
    
class Rewards(models.Model):
    rewards_id=models.AutoField(primary_key=True)
    Users = models.ForeignKey(Users)
    rewardname = models.TextField(max_length=200)
    filename = models.FileField(upload_to=content_file_name,storage=MediaFileSystemStorage()) 
    
    class Meta:
        db_table ='rewards'
         
    def __unicode__(self):
        return self.rewards_id   
class problemForm(ModelForm):
    class Meta:
        model = Problem
        exclude=['Users']
        fields = ['file','question','respgrp','answer','weight'] 
        
class rewardsForm(ModelForm):
    class Meta:
        model = Rewards
        exclude=['Users']
        fields = ['rewardname','filename']         
  
class problemSelectForm(ModelForm):
    
    class Meta:
        model = Problem
        exclude=['users']
        fields = ['problemId','file','question','answer','weight']
        
     
           
       
        

