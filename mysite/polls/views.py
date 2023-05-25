from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Question, User, Choice, QuestionUser

def index(request):
    if 'user' in request.session:
        current_user = request.session['user']
        latest_question_list = Question.objects.order_by("-pub_date")
        user = User.objects.filter(username=request.session['user'])[0]
        question_list = []
        for question in latest_question_list:
            question_answered = False
            try:
                value = QuestionUser.objects.get(user=user, question= question)
                question_answered = True
            except: 
                question_answered = False
            if not question_answered:
                question_list.append(question)
        param = {'current_user': current_user,
                 "latest_question_list": question_list}
        if len(question_list)==0:
            return redirect('results')
        return render(request, 'polls/index.html', param)
    else:
        return render(request, 'polls/index.html')


def detail(request, question_id):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_id)
        choicetext = request.POST.get('choice')
        print(request.body)
        choice = Choice.objects.get(pk=choicetext)
        user = User.objects.filter(username=request.session['user'])[0]
        print(user)
        currentpoints = user.total_points
        if user:
            user.total_points=currentpoints+choice.points
            questionUser = QuestionUser(question=question, user= user)
            questionUser.save()
            user.save()
            return redirect('index')
        else:
            return HttpResponse('Please Login')

        return render(request, 'polls/')
    else:
        try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, "polls/detail.html", {"question": question})

def results(request):
    user = User.objects.filter(username=request.session['user'])[0]
    diagnosis = ''
    if(user.total_points<10):
        diagnosis = 'normal'
    elif(user.total_points>10 and user.total_points<20):
        diagnosis = 'You are gay'
    else:
        diagnosis = 'You are a bitch'
    param = {'diagnosis': diagnosis}
    return render(request, 'polls/result.html', param)

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        # print(uname, pwd)
        if User.objects.filter(username=uname).count()>0:
            return HttpResponse('Username already exists.')
        else:
            user = User(username=uname, password=pwd)
            user.save()
            return redirect('login')
    else:
        return render(request, 'polls/signup.html')



def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        check_user = User.objects.filter(username=uname, password=pwd)
        if check_user:
            request.session['user'] = uname
            return redirect('index')
        else:
            return HttpResponse('Please enter valid Username or Password.')

    return render(request, 'polls/login.html')


def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')

