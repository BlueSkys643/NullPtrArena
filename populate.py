# Populate the database with meaningless data

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from arena.models import User, ProblemSet, Problem, Submission


# ============================================================
# Clear existing data
# ============================================================

print("Clearing existing data...")

Submission.objects.all().delete()
Problem.objects.all().delete()
ProblemSet.objects.all().delete()
User.objects.all().delete()


# ============================================================
# Create users
# ============================================================

print("Creating users...")

admin = User.objects.create_superuser(
    username="admin",
    email="admin@example.com",
    password="Admin123!"
)

user1 = User.objects.create_user(
    username="testuser1",
    email="testuser1@example.com",
    password="TestUser123!"
)

user2 = User.objects.create_user(
    username="testuser2",
    email="testuser2@example.com",
    password="TestUser123!"
)


# ============================================================
# Create problem sets
# ============================================================

print("Creating problem sets...")

set1 = ProblemSet.objects.create(
    author=admin,
    name="Admin Basics",
    description="Basic programming problems created by the administrator. Do these guided problems to learn the program."
)

set2 = ProblemSet.objects.create(
    author=admin,
    name="Admin Algorithms",
    description="Algorithm and data structure practice problems."
)

set3 = ProblemSet.objects.create(
    author=admin,
    name="Admin Challenge",
    description="More challenging programming problems."
)

set4 = ProblemSet.objects.create(
    author=user1,
    name="User Practice",
    description="A practice problem set created by the first test user."
)


# ============================================================
# Create problems
# ============================================================

print("Creating problems...")

# Set 1: 10 problems

set1_problems = [
    ("Hello World", "Print Hello World.", "EASY"),
    ("Add Two Numbers", "Read two numbers and print their sum.", "EASY"),
    ("Subtract Numbers", "Read two numbers and print their difference.", "EASY"),
    ("Multiply Numbers", "Read two numbers and print their product.", "EASY"),
    ("Even or Odd", "Determine whether an integer is even or odd.", "EASY"),
    ("Positive or Negative", "Determine whether an integer is positive or negative.", "EASY"),
    ("Maximum of Two", "Find the larger of two integers.", "EASY"),
    ("Maximum of Three", "Find the largest of three integers.", "EASY"),
    ("Count to N", "Print every integer from 1 through N.", "MEDIUM"),
    ("Sum to N", "Calculate the sum of all integers from 1 through N.", "MEDIUM"),
]

# Set 2: 6 problems

set2_problems = [
    ("Linear Search", "Search an array for a target value.", "EASY"),
    ("Binary Search", "Use binary search to find a target value.", "MEDIUM"),
    ("Reverse Array", "Reverse the elements of an array.", "MEDIUM"),
    ("Find Minimum", "Find the smallest value in an array.", "EASY"),
    ("Sort Numbers", "Sort a collection of integers in ascending order.", "MEDIUM"),
    ("Remove Duplicates", "Remove duplicate values from an array.", "HARD"),
]

# Set 3: 4 problems

set3_problems = [
    ("Fibonacci", "Calculate the nth Fibonacci number.", "MEDIUM"),
    ("Prime Check", "Determine whether a number is prime.", "MEDIUM"),
    ("Factorial", "Calculate the factorial of a non-negative integer.", "EASY"),
    ("Graph Traversal", "Traverse a graph using breadth-first search.", "HARD"),
]

# Set 4: 0 problems intentionally.


def create_problems(problem_set, problem_data):
    problems = []

    for name, description, difficulty in problem_data:
        problem = Problem.objects.create(
            problem_set=problem_set,
            author=problem_set.author,
            name=name,
            description=description,
            difficulty=difficulty,
            test_file="problem_tests/default.csv",
        )

        problems.append(problem)

    return problems


problems1 = create_problems(set1, set1_problems)
problems2 = create_problems(set2, set2_problems)
problems3 = create_problems(set3, set3_problems)


# ============================================================
# Create submissions
# ============================================================

print("Creating submissions...")

# Both submissions are for the first problem in Set 1.
test_problem = problems1[0]


# Passing submission from user 1
Submission.objects.create(
    problem=test_problem,
    author=user1,
    content='print("Hello World")',
    passed=True,
)


# Failing submission from user 2
Submission.objects.create(
    problem=test_problem,
    author=user2,
    content='print("Goodbye World")',
    passed=False,
)


# ============================================================
# Optional: generating test CSV files
# ============================================================
#
# This is NOT currently used. All problems use:
#     problem_tests/default.csv
#
# Example of creating a CSV file:
#
# import csv
# from django.core.files import File
#
# csv_path = "problem_tests/example.csv"
#
# with open(csv_path, "w", newline="") as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerow(["2", "3"])
#     writer.writerow(["5", "8"])
#
# with open(csv_path, "rb") as csv_file:
#     problem.test_file.save(
#         "example.csv",
#         File(csv_file),
#         save=True
#     )


print("Database populated successfully!")
print()
print("Users:")
print("  admin      / Admin123!")
print("  testuser1  / TestUser123!")
print("  testuser2  / TestUser123!")
print()
print("Problem sets:")
print("  Admin Basics      - 10 problems")
print("  Admin Algorithms  - 6 problems")
print("  Admin Challenge   - 4 problems")
print("  User Practice     - 0 problems")
print()
print("Submissions:")
print("  testuser1 - passing submission")
print("  testuser2 - failing submission")

