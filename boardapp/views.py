from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.
#httpレスポンス(必ず入れる, url名, モデルの情報)

def signupfunc(request): #ユーザー作成
    print(request.POST) #データ取得
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username, '', password) #ユーザー作成
            return render(request, 'signup.html', {'some':100})
        except IntegrityError: #ユーザー重複してた場合
            return render(request, 'signup.html', {'error':'このユーザーは既に登録されています'}) 
    return render(request, 'signup.html',)

def loginfunc(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: #ユーザーが居ない場合ではない時=いる時
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html', {'context':'ログインできません'})
    return render(request, 'login.html', {})

@login_required #ログイン情報記憶
def listfunc(request):
    object_list = BoardModel.objects.all()
    ordering = ['-date_posted']
    return render(request, 'list.html', {'object_list':object_list})

def logoutfunc(request):
    logout(request)
    return redirect('login')

def detailfunc(request, pk):#pk:数字の情報(キーワード)
    object = get_object_or_404(BoardModel, pk=pk) #対象データ取得or404取得,(モデル,値,キーワード)
    return render(request, 'detail.html', {'object':object})

def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.goodtext:
        return redirect('list')
    else :
        object.good = object.good + 1
        object.goodtext = object.goodtext + ' ' + username
        object.save()
        return redirect('list')

def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else :
        object.read = object.read + 1
        object.readtext = object.readtext + ' ' + username
        object.save()
        return redirect('list')

#投稿を削除する関数(未完成)
def deletefunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    object.objects.all().delete()
    return redirect('list')

class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'sns_image')
    success_url = reverse_lazy('list')