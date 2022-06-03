
import pandas as pd
import seaborn as sns
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
df1 = pd.read_csv("D:\\MCA\sem 3\\Mini project\\spamham.csv")
df = df1.where((pd.notnull(df1)), '')
df.loc[df["Category"] == 'ham', "Category",] = 1
df.loc[df["Category"] == 'spam', "Category",] = 0
# split data as label and text . System should be capable of predicting the label based on the  text
df_x = df['Message']
df_y = df['Category']
from .forms import *
from .models import *
# split the table - 80 percent for training and 20 percent for test size
x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, train_size=0.6, test_size=0.4, random_state=4)
# feature extraction, coversion to lower case and removal of stop words using TFIDF VECTORIZER
tfvec = TfidfVectorizer(min_df=1, stop_words='english', lowercase=True)
x_trainFeat = tfvec.fit_transform(x_train)

x_testFeat = tfvec.transform(x_test)
# SVM is used to model
y_trainSvm = y_train.astype('int')
classifierModel = LinearSVC()
classifierModel.fit(x_trainFeat, y_trainSvm)
predResult = classifierModel.predict(x_testFeat)

def index(request):
    return render(request,'index.html')
def upload2(request):
    return render(request,'upload2.html')

def register(request):
    reg=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.save()
            profile=profile_form.save(commit=False)
            profile.user=user
            profile.save()

            reg=True
        else:
            HttpResponse("Invalid Form")
    else:
        user_form=UserForm()
        profile_form=ProfileForm()
    return render(request,'register.html',{'register':reg,'user_form':user_form,'profile_form':profile_form})

def upload(request):
    reg=False
    res=''
    if request.method=="POST":
        spam=request.POST.get('spamtxt')
        print(spam)
        uploadform=UploadForm(data=request.POST)
        message_to_test=[spam]
        x_testFeat = tfvec.transform(message_to_test)
        predResult = classifierModel.predict(x_testFeat)
        print(predResult)
        if(predResult[0]==1):
            res='No Spam'
        else:
            res='Spam'
        print('Classification is',res)
        if uploadform.is_valid():
            #user=uploadform.save()
            #user.save()
            reg=True
            return render(request,'upload2.html',context={'result':res})
        else:
            HttpResponse("Invalid Form")
    else:
        uploadform=UploadForm()
    return render(request,'upload.html',context={'result':res,'uploadform':uploadform})

def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse('Not active')
        else:
            return HttpResponse("Invalid username or Password")
    else:
        return render(request,'login.html')

def dashboard(request):
    return render(request,'dashboard.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')
