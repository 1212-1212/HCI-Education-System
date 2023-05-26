from django import forms
from .models import *


class LearnerRegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LearnerRegisterForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Learner
        exclude = ("user", "is_registered", "is_logged_in")
        widgets = {
            'password': forms.PasswordInput(),
        }


class LearnerLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LearnerLoginForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Learner
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Course
        fields = ['name', ]


class LessonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Lesson
        fields = ['title', ]


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        exclude = ('grade',)


class ChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Choice
        fields = "__all__"


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Post
        fields = ['text', 'files']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Comment
        fields = ['content', 'files']
