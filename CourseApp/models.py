from django import forms
from django.contrib.auth.models import User
from django.db import models


# from django.forms import forms


class Learner(models.Model):
    user_name = models.CharField(null=False, blank=False, max_length=50)
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=False, blank=False, max_length=50)
    email = models.EmailField(null=False, blank=False, max_length=40, primary_key=True)
    password = models.CharField(max_length=32, blank=False, null=False)

    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to="student_images/")
    is_registered = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f"Name: {self.first_name} Surname: {self.last_name}"

    def welcome(self):
        return f"{self.first_name} {self.last_name}"


class Instructor(models.Model):
    user_name = models.CharField(null=False, max_length=50)
    first_name = models.CharField(null=False, max_length=50)
    last_name = models.CharField(null=False, max_length=50)
    email = models.EmailField(null=False, max_length=40)
    #  image = models.ImageField(upload_to="instructor_images/")
    birth_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    BACHELOR = 'Bachelor'
    MASTER = 'Master'
    DOCTORATE = 'Doctorate'
    DEGREES = [
        (BACHELOR, 'Bachelor'), (MASTER, 'Master'), (DOCTORATE, 'Doctorate'),
    ]
    degree = models.CharField(choices=DEGREES, default=BACHELOR, max_length=50)

    def __str__(self):
        return f" {self.first_name} {self.last_name} {self.degree}"


class Course(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.TextField(max_length=1000, default="")
    image = models.FileField(upload_to="course_images/", blank=True, null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(User, through='Enrollment')
    selected = models.BooleanField(default=False)

    def shortened_description(self):
        return self.description[:300] + "..."

    def __str__(self):
        return f"{self.name}"

    def instructors_string(self):
        str_repr_of_ins = [instr.__str__() for instr in self.instructors.all()]
        print(str_repr_of_ins)
        return ", ".join(str_repr_of_ins)

    def grade(self):
        total = 0
        lessons = Lesson.objects.filter(course__name=self.name).all()
        for lesson in lessons:
            if lesson.grade == 0:
                return 5
            total += lesson.grade

        return int(total / lessons.__len__())


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    order_no = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    video = models.FileField(upload_to='videos/', default="", null=True, blank=True)
    link = models.URLField(max_length=3000, null=True, blank=True)
    selected = models.BooleanField(default=False)
    grade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title}, {self.course.__str__()}"


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_of_enrollment = models.DateField()


class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)
    question_content = models.TextField(max_length=10000, null=True, blank=True, default="")
    question_content_image = models.FileField(upload_to='question_images/', null=True, blank=True, default="")
    grade = models.IntegerField(default=0)

    def __str__(self):
        return f"Content: {self.question_content} Lesson: {self.lesson.__str__()} Grade: {self.grade}"


class Choice(models.Model):
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField()
    question = models.ManyToManyField(Question)

    def __str__(self):
        return f"Content: {self.choice_text} Question: {self.question.all()}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    text = models.TextField(max_length=10000, default="")
    files = models.FileField(upload_to='student_images/', blank=True, default="")

    def __str__(self):
        return f"{self.author} {self.date_published} {self.text}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000, default="")
    files = models.FileField(upload_to='student_images/', blank=True, default="")

    def __str__(self):
        return f"{self.author} {self.date_published} {self.post}"