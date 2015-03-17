from django.shortcuts import render
from childquestions.models import problemForm,problem,users,problemSelectForm
from django.forms.models import model_to_dict

# Create your views here.
def problems(request):
     pf = problemForm()
     request.session['user_id']= '1abc'
     request.session['username']='Tester'
            
     return render(request,'Problems.html',{'form':pf})

def problemSubmit(request):
    if request.method == 'POST':
        print('line1') 
        user = users()
        user.users_id= request.session.get('user_id')
        user.username=request.session.get('username')
        prob = problem.objects.create(users=user)
        prob.save()
        pf = problemForm(request.POST,request.FILES,instance=prob)
        if pf.is_valid():
            pd = pf.cleaned_data
            print('line2')        
            print(pd)
            pf.save(commit=True)
            
            return (request,'Problems.html') 
        else:
            print('line3')  
            form =problemForm()
                         
    return render(request,'result.html')

def problemSend(request):
    print('line1') 
    user = users()
    user.users_id= request.session.get('user_id')
    user.username=request.session.get('username')
    prob= problem.objects.filter(users=user)
    
        
    return render(request,'result.html',{'form':prob})   

 
   
