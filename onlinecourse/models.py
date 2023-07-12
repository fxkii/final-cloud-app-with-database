import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation


# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()


# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_1 = models.Choices()
    grade_point = 70

    def get_valuation(self, selected_ids):
        all_answers =self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
            return True
        else:
            return False
class Choice(models.Model):
    

#  <HINT> Create a Choice Model with:
    # Used to persist choice content for a question
    # One-To-Many (or Many-To-Many if you want to reuse choices) relationship with Question
    # Choice content
    # Indicate if this choice of the question is a correct one or not
    # Other fields and methods you would like to design
# class Choice(models.Model):

# <HINT> The submission model
# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
#class Submission(models.Model):
#    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
#    choices = models.ManyToManyField(Choice)
#    Other fields and methods you would like to design

QUESTION_1= "Authentication is a process that does what?"
    QUESTION_2= "What does Bootstrap provide for Django?"
    QUESTION_3= "When Django users run a runserver command line, what does it start?"
    QUESTION_4= "What does Django use name spacing for when you add static files to an app?"
    QUESTION_MODES = [(QUESTION_1),(QUESTION_2),(QUESTION_3),(QUESTION_4)]
    

#Question 1 choices
    Q1_C1 = "Validates User Identity"
    Q1_C2 = "Checks users access permissions"
    Q1_C3 = "Creates user credentials"
    Q1_C4 = "Groups are based on permissions"
    #Question 2 choices
    Q2_C1 = "Code examples"
    Q2_C2 = "Databases"
    Q2_C3 = "HTML and CSS templates"
    Q2_C4 = "Server interfaces"
    #Question 3 choices
    Q3_C1 = "Storage server"
    Q3_C2 = "File server"
    Q3_C3 = "Minimal development web server"
    Q3_C4 = "Barebones backend server"
    #Question4 choices
    Q4_C1 = "Uniquely refers to static files that use the same name, across multiple apps"
    Q4_C2 = "Tracks static files in each apps"
    Q4_C3 = "Limits the number of static files in an app"
    Q4_C4 = "Sorts static files"