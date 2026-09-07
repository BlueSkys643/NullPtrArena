# Database Design

## 1. Purpose
the database will contain code problems and a limited amount of user submissions.

## 2. Design Goals
- contain an organized uniform collection of coding problems
- track users last 10 submissions of each problem
- identify collections of problems and sort them into categories
- track badges/achievements acquired by users

## 3. Entities
### User
- uuid
- username
- email
- profile pic
- bio

### ProblemSet
- setid
- title
- description

### Problem
- id
- title
- description
- test file

### Submission
- PK FK userid
- PK FK problemid
- PK submission number
- pass/fail
- code file

## 4. Relationships
every problem has one and only one author 
every problem set has one and only one creator 
every problem belongs to one and only one created set 
every submission has one and only one problem it is for and one and only one author 
users can exist without creating problems, sets, or submissions 
a problem set can have many problems or no problems 
users can create multiple submissions but only the 3 most recent submissions and single most recent correct submission are saved for each problem

## 5. Schema


## 6. Constraints & Rules
- only one user per email
- only the 10 most recent submissions of each problem for each user
- a submission belongs to exactly one user
- a submission belongs to exactly one problem
- a submission cannot be modified after creation

## 7. Indexes
user - username, email

## 8. Delete / Update Behavior
if a user is deleted so must all there submission be deleted as well
if a problem is deleted submission must be archived


## 9. Security Considerations
user passwords will be handled by django's auth system and stored using django's hash mechanisms
database credentials will not be coded into source code in production. Secret management mechanisms should be used like environment variables.
foreign key relationships will enforce valid relationships between users, problem sets, problems, and submissions
users should only be permitted to modify/delete resources that are authorized to manage.
database acces is restricted to the django application and not publicly exposed.

## 10. Migration Plan
Django migrations will be used to manage changes to the PostgreSQL database schema.

When the data model changes:

1. Update the appropriate Django model in `models.py`.
2. Run `python manage.py makemigrations`.
3. Review the generated migration.
4. Commit the migration file to Git.
5. Run `python manage.py migrate` to apply the migration to the development database.

Migration files will be stored in the repository and used to recreate the database schema on new development environments.

## 11. Open Questions
- should a user be allowed to delete a problem after submission have been made?
- should deleting a user delete their problems, problem sets, and submissions
- how should the database enforce the submission retention policy
- should problem set names be unique?
- should problem names be unique within a set?
- how will tags be represented?
- how will user-curated problem sets be represented?