from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class ProblemSet(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="problem_sets",
    )
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=300)

class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    problem_set = models.ForeignKey(
        ProblemSet,
        on_delete=models.CASCADE,
        related_name="problems",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="problems",
    )
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    difficulty = models.CharField(max_length=12)
    test_file = models.FileField(
        upload_to="problem_tests/"
    )
"""
TestCase class might get implemented but if it does then no csv files for tests

class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="test_cases",
    )
    input = models.TextField(max_length=300)
    expected_output = models.TextField(max_length=300)
"""
class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    content = models.TextField()
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

