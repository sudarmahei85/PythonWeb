from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
import hashlib
import os.path
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError

# class Users(models.Model):
#     username = models.CharField(max_length=20)
#     users_id= models.CharField(max_length=20,primary_key=True)
#     class Meta:
#         db_table ='users'
#     def __unicode__(self):
#         return self.users_id

#def content_file_name(instance, filename):
        #ext = filename.split('.')[-1]
     #   h=instance.guidvalue
     #   basename, ext = os.path.splitext(filename)
     #   return os.path.join(h + ext.lower())
    
def simple_upload_to(field_name, path='files'):
    def upload_to(instance, filename):
        name = md5_for_file(getattr(instance, field_name).chunks())
        instance.shasum=sha_for_file(getattr(instance, field_name).chunks())
        instance.guidvalue=name
        dot_pos = filename.rfind('.')
        ext = filename[dot_pos:][:10].lower() if dot_pos > -1 else '.unknown'
        if ext=='.mp4' or ext=='.avi' :
            instance.filetype='Video'
        elif  ext=='.mp3':
            instance.filetype='Audio'
        
        name += ext
        return os.path.join(name)
    return upload_to
def md5_for_file(chunks):
    md5 = hashlib.md5()
    for data in chunks:
        md5.update(data)
    return md5.hexdigest()

def sha_for_file(chunks):
    sha = hashlib.sha256()
    for data in chunks:
        sha.update(data)
    return sha.hexdigest()

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg','.jpeg']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported. Please upload only jpg or jpeg')
    
def validate_file_video_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4','.avi','.mp3']
    if not ext in valid_extensions:
        raise ValidationError(u'File not supported.Please upload only .mp4,.avi or .mp3')
    
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
    Users = models.ForeignKey(User,db_column='id')
    question = models.TextField(max_length=200)
    answer =  models.ForeignKey(Respgrpanswer,db_column='respgrpanswer_id')
    weight= models.IntegerField(max_length=2)
    respgrp =models.ForeignKey(Respgrp)
    file = models.FileField(upload_to=simple_upload_to('file'),validators=[validate_file_extension],storage=MediaFileSystemStorage()) 
    shasum =models.TextField(max_length=200)
    guidvalue= models.TextField(max_length=200)
    filetype=models.TextField(max_length=4)
    
    class Meta:
        db_table ='problems'
         
    def __unicode__(self):
        return self.problemId
    
class devicemapping(models.Model):  
    Users = models.ForeignKey(User,db_column='id')
    deviceid= models.AutoField(primary_key=True)
    devicekey=models.TextField(max_length=200)
    class Meta:
        db_table ='device_mapping'
         
    def __unicode__(self):
        return self.deviceid
    
class Rewards(models.Model):
    rewards_id=models.AutoField(primary_key=True)
    Users = models.ForeignKey(User,db_column='id')
    rewardname = models.TextField(max_length=200)
    file = models.FileField(upload_to=simple_upload_to('file'),validators=[validate_file_video_extension],storage=MediaFileSystemStorage()) 
    shasum =models.TextField(max_length=200)
    guidvalue= models.TextField(max_length=200)
    filetype=models.TextField(max_length=4)
    
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
        fields = ['rewardname','file']         
  
class problemSelectForm(ModelForm):
    
    class Meta:
        model = Problem
        exclude=['users']
        fields = ['problemId','file','question','answer','weight']
        
     
           
       
        

