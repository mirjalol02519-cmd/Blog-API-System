# Blog API System

This project is a professional Blog API built with Django Rest Framework (DRF) and Token Authentication.

## Technologies Used

* Python
* Django & Django Rest Framework (DRF)
* Token Authentication
* SQLite
* django-environ

## Installation

### 1. Clone the repository and open the project folder

```bash
git clone <https://github.com/mirjalol02519-cmd/Blog-API-System>
cd Blog-API-System
```



## Installation

### 1. Clone the repository and open the project folder

```bash
git clone <github_repository_link>
cd blog_api_system
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

