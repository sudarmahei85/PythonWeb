from django.db import models
from django.forms import ModelForm
from django import forms
import os.path

class users(models.Model):
    username = models.CharField(max_length=20)
    users_id= models.CharField(max_length=20,primary_key=True)
    class Meta:
         db_table ='users'
    def __unicode__(self):
        return self.users_id

def content_file_name(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (instance.problemId,ext)
        return os.path.join(filename)
    

class problem(models.Model):
    problemId=models.AutoField(primary_key=True)
    users = models.ForeignKey(users)
    question = models.TextField(max_length=200)
    answer =  models.TextField(max_length=20)
    weight= models.IntegerField(max_length=2)
    file = models.FileField(upload_to=content_file_name) 
    class Meta:
         db_table ='problems'
         
    def __unicode__(self):
       return self.problemId
   
class problemForm(ModelForm):
    class Meta:
        model = problem
        exclude=['users']
        fields = ['file','question','answer','weight']   

class problemSelectForm(ModelForm):
    class Meta:
        model = problem
        exclude=['users']
        fields = ['file','question','answer','weight']
        widgets = {
            'problemId': forms.CheckboxSelectMultiple()
        }
        
    def __init__(self, *args, **kwargs):
        def new_label_from_instance(self, obj):
            return obj.svgpreview

        super(problemSelectForm, self).__init__(*args, **kwargs)
        funcType = type(self.fields['labels'].label_from_instance)
        self.fields['problemId'].label_from_instance = funcType(new_label_from_instance, self.fields['problemId'], forms.models.ModelMultipleChoiceField) 

        
       
        

