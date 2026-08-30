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
- id
- username
- email
- profile pic
- bio

### Problem
- id
- title
- description
- test file

### Submission
- PK userid
- PK problemid
- PK submission number
- pass/fail
- code file

### Collection
- collection name
- collection id

### Collection problem
- PK collection id
- PK problem id

## 4. Relationships
users create submissions to problems
a collection has many problems it contains as collection problems

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


## 10. Migration Plan


## 11. Open Questions
