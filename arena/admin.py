from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Problem, ProblemSet, Submission

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Problem)
admin.site.register(ProblemSet)
admin.site.register(Submission)