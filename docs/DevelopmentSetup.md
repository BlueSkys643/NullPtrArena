# NullPtrArena Development Environment Setup

This document explains how to set up the NullPtrArena development environment on a new machine.

## Prerequisites

Install the following on the new machine:

- [VS Code](https://code.visualstudio.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker CLI and Docker Engine)
- The VS Code **Dev Containers** extension
- Git

Docker Desktop should be running before starting the Dev Container.

## 1. Clone the Repository

Clone the NullPtrArena repository:

```bash
git clone <repository-url>
cd NullPtrArena
```

Open the project folder in VS Code.

## 2. Start the Dev Container

When VS Code detects the Dev Container configuration, choose:

**Reopen in Container**

The configuration in `.devcontainer/` uses Docker Compose to create the development environment.

The Compose configuration creates two containers:

- **app** — the development container containing the Django project
- **db** — the PostgreSQL database server

Docker Compose also creates a named PostgreSQL volume for persistent database storage.

The resulting structure is approximately:

```text
NullPtrArena
│
├── app container
│   └── Django / Python development environment
│
└── db container
    └── PostgreSQL
        └── postgres-data volume
```

The PostgreSQL volume is separate from the Git repository. It is not committed to Git.

## 3. Set Up the Python Virtual Environment

Inside the `app` Dev Container, create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the project's Python dependencies:

```bash
python -m pip install -r requirements.txt
```

If VS Code automatically activates `.venv`, you may not need to run the `source` command manually.

## 4. Set Up the Database

The PostgreSQL database starts as a new, empty database when the project is first run on a new machine.

Django's migration files are stored in the Git repository under each app's `migrations/` directory. They describe how to construct the database schema.

Run:

```bash
python manage.py migrate
```

Django will apply the migrations and create the required PostgreSQL tables.

You do **not** need to manually create the tables with SQL.

## 5. Verify the Setup

Check that Django can see the migrations:

```bash
python manage.py showmigrations
```

Applied migrations should be marked with:

```text
[X]
```

You can also verify that Django detects no missing model migrations:

```bash
python manage.py makemigrations
```

If the models and migration files are synchronized, Django should report:

```text
No changes detected
```

## Development Workflow

Once the environment is configured, normal development generally looks like:

```text
Edit models.py
     ↓
python manage.py makemigrations
     ↓
Review the migration
     ↓
python manage.py migrate
     ↓
Continue development
```

### Important: Do Not Recreate the Database for Normal Schema Changes

You normally **do not delete the PostgreSQL volume** when changing your models.

Django migrations are designed to update an existing database while preserving its data.

For example, adding a field to a model can result in:

```text
0001_initial.py
      ↓
0002_add_bio.py
      ↓
0003_add_tags.py
```

Each migration records a change to the database schema.

Deleting the PostgreSQL volume should generally only be done when intentionally starting the development database from scratch, such as when the database contains no important data and the migration history needs to be reset.

## Git and the Database

Git tracks the files needed to recreate the project, including:

- Django source code
- `models.py`
- Migration files
- `settings.py`
- `.devcontainer/docker-compose.yml`
- `requirements.txt`

Git does **not** track the PostgreSQL volume or its database files.

This means a new machine does not need a copy of the existing PostgreSQL volume. Instead:

1. Clone the repository.
2. Start the Dev Container.
3. Docker Compose creates PostgreSQL and its volume.
4. Create/install the Python environment.
5. Run `python manage.py migrate`.
6. Django recreates the database schema from the migration files.

## Quick Setup Checklist

For a new machine:

```text
[ ] Install Git
[ ] Install Docker Desktop
[ ] Install VS Code
[ ] Install the Dev Containers extension
[ ] Clone the NullPtrArena repository
[ ] Open the repository in VS Code
[ ] Reopen the project in the Dev Container
[ ] Create/activate .venv
[ ] Install requirements.txt
[ ] Run python manage.py migrate
[ ] Start developing
```

Once the Dev Container configuration is fully automated, the Python environment setup can also be automated so that opening the repository in the Dev Container handles most of these steps automatically.
