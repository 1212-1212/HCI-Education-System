from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.forms import Form
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.functional import SimpleLazyObject

from .forms import *
from django.http import HttpResponse
from django.template import loader


# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request, 'login.html', context={"form": LearnerLoginForm})
    else:
        form_data = LearnerLoginForm(data=request.POST)
        # print(form_data.data)
        learner_email = form_data.data['email']
        learner_password = form_data.data['password']
        is_registered = Learner.objects.filter(email=learner_email, password=learner_password).exists()
        # print(is_registered)
        if is_registered:
            learner = Learner.objects.filter(email=learner_email, password=learner_password).first()
            learner.is_logged_in = True
            learner.save()
            # print(learner.is_logged_in)
            # print(Learner.objects.all().first().is_logged_in)
            # return render(request, 'index.html',
            #               context={"learner": learner, "courses": Course.objects.all(), "form": CourseForm})
            return redirect(index)

        else:
            return redirect(register)


def register(request):
    if request.method == "POST":
        form_data = LearnerRegisterForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            learner = form_data.save(commit=False)
            form_data = form_data.cleaned_data
            learner.user = request.user
            learner.first_name = form_data['first_name']
            learner.last_name = form_data['last_name']
            learner.user_name = form_data['user_name']
            learner.birth_date = form_data['birth_date']
            learner.email = form_data['email']
            learner.password = form_data['password']
            learner.is_registered = True
            learner.save()
            # print(Learner.objects.all())
            return redirect('login')
    context = {"form": LearnerRegisterForm}
    return render(request, 'register.html', context=context)


def index(request):
    if request.method == 'POST':
        form_data = CourseForm(data=request.POST)
        name = form_data.data['name']
        if Course.objects.filter(selected=True).first() is not None:
            course = Course.objects.filter(selected=True).first()
            course.selected = False
            course.save()
        course = Course.objects.filter(name=name).first()
        course.selected = True
        course.save()
        return redirect(lectures)

    else:
        # print(type(request.user))
        # print(request.user)
        learner = None
        if request.user in User.objects.all():
            learner = Learner.objects.filter(user=request.user).first()
        if learner is not None:
            context = {"learner": Learner.objects.filter(user=request.user).first(), "courses": Course.objects.all(),
                       "form": CourseForm}
        else:
            context = {"courses": Course.objects.all(),
                       "form": CourseForm}

        return render(request, 'index.html', context=context)


def lectures(request):
    query_set = Lesson.objects.filter(course__selected=True).all()
    if request.method == 'POST':
        form_data = LessonForm(data=request.POST)
        # print(form_data.data)
        title = form_data.data['name']
        # print(title)
        if Lesson.objects.filter(selected=True).first() is not None:
            lesson = Lesson.objects.filter(selected=True).first()
            lesson.selected = False
            lesson.save()
        lesson = Lesson.objects.filter(title=title).first()
        lesson.selected = True
        lesson.save()
        query_set = Lesson.objects.filter(course__selected=True, selected=True)
        print(query_set)
        return redirect(video)
    else:
        query_set = Lesson.objects.filter(course__selected=True).all()
        # print(query_set)
        # print(Lesson.objects.all())
        context = {"lectures": query_set}
        return render(request, 'lectures.html', context=context)


def video(request):
    return render(request, 'video.html', context={"lecture": Lesson.objects.filter(selected=True).first()})


def test(request):
    questions = Question.objects.filter(lesson__course__selected=True, lesson__selected=True).all()
    choices = Choice.objects.filter(question__lesson__selected=True, question__course__selected=True).all()
    query_set = {}
    for question in questions:
        query_set[question] = []
    for choice in choices:
        for question in questions:
            # print(question.question_content)
            # print(choice.question.first())
            # print("\n")
            if question == choice.question.first():
                query_set[question].append(choice)
    if request.method == 'GET':
        # print(query_set)

        return render(request, 'test.html', context={"questions": questions, "choices": choices, "queryset": query_set})
    else:
        print(request.POST)
        score = wrong = correct = total = 0
        for question, choices in query_set.items():
            total += 1
            # print(request.POST.get(question.question_content))
            # print(request.POST.keys())
            # print(request.POST[question.question_content])
            correct_choice = ""
            for choice in choices:
                if choice.is_correct:
                    correct_choice = choice.choice_text
                    break
            #  print(request.POST)
            if question.question_content in request.POST:

                if request.POST[question.question_content] == correct_choice:
                    print(request.POST[question.question_content])
                    print(correct_choice)
                    correct += 1
                    score += 10
                else:
                    wrong += 1
            else:

                wrong += 1

        # print(score)
        lesson = Lesson.objects.filter(course__selected=True, selected=True).first()
        lesson.grade = int(score / (total * 10) * 10)
        lesson.save()
        # print(lesson.grade)
        context = {'lesson': Lesson.objects.all(), 'form': LessonForm}
        # print(Lesson.objects.all().first().grade)
        # print(context)
        return redirect(tests)


def tests(request):
    query_set = Lesson.objects.filter(course__selected=True).all()
    if request.method == 'POST':
        form_data = LessonForm(data=request.POST)
        # print(form_data.data)
        title = form_data.data['name']
        # print(title)

        if Lesson.objects.filter(selected=True).first() is not None:
            lesson = Lesson.objects.filter(selected=True).first()
            lesson.selected = False
            lesson.save()
        lesson = Lesson.objects.filter(title=title).first()
        lesson.selected = True
        lesson.save()
        query_set = Lesson.objects.filter(course__selected=True, selected=True)
        # print(query_set)
        return redirect(test)
    context = {"lessons": query_set, 'form': LessonForm}
    # return render(request, 'test.html', context=context)
    return render(request, 'tests.html', context=context)


def logout(request):
    learner = Learner.objects.filter(user=request.user, is_registered=True, is_logged_in=True).first()

    # print(learner)
    learner.is_logged_in = False
    learner.save()
    return redirect(index)


def forum(request):
    if request.method == "POST":
        form_data = Form(data=request.POST, files=request.FILES)

        if "post" not in form_data.data.keys():
            form_data = PostForm(data=request.POST, files=request.FILES)
            # print(form_data.data)
            if form_data.is_valid():
                post = form_data.save(commit=False)
                form_data = form_data.cleaned_data
                post.files = form_data['files']
                post.author = request.user
                post.text = form_data['text']
                post.date_published = datetime.now()
                post.save()

        else:
            form_data = CommentForm(data=request.POST, files=request.FILES)
            post = form_data.data['post']
            # print(form_data.data)
            if form_data.is_valid():
                comment = form_data.save(commit=False)
                form_data = form_data.cleaned_data
                comment.files = form_data['files']
                comment.content = form_data['content']
                post_data = post
                # print(post_data)
                post_data = str(post_data).split(" ")
                post_author = post_data[0]
                # print(post_author)
                post_date_published = post_data[1] + " " + post_data[2]
                post_text = " ".join(post_data[3:])
                # print(post_text)
                post = Post.objects.filter(author__username=post_author, text=post_text) \
                    .first()
                # print(post)
                comment.date_published = datetime.now()
                comment.post = post
                comment.author = request.user
                # print(comment)
                comment.save()
            # print(post)

    posts = Post.objects.all()
    query_dict = {}
    for post in posts:
        comments = Comment.objects.filter(post=post).all()
        query_dict[post] = comments
    comments = Comment.objects.all()

    return render(request, 'forum.html',
                  context={"post_form": PostForm, "comment_form": CommentForm, "query_dict": query_dict,
                           "posts": posts, "comments": comments})
