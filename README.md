This repository contains a Django-based API for user management and friend request functionality. Follow the steps below to set up and configure the project.

**Table of Contents:
Prerequisites
Installation
Configuration
Database Setup
Running the Server
API Endpoints
Prerequisites

Make sure you have the following installed on your system:

Python 3.8 or higher
Django 3.2 or higher
pip (Python package installer)
PostgreSQL (for production) or SQLite (for development)

**Installation & Configurations:
Clone the Repository:
git clone <repository_url>
cd <repository_name>


**Create and Activate a Virtual Environment:
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate


**Install Required Python Packages:
pip install -r requirements.txt


**Database Setup
**Apply Migrations:
python manage.py makemigrations
python manage.py migrate


**Create a Superuser:
python manage.py createsuperuser
Running the Server


**Start the Development Server:
python manage.py runserver

**API Endpoints:
Here is a brief overview of the available API endpoints:
User Registration: POST /register/
User Login: POST /login/
User Profile: GET /profile/
Search Users: GET /search/
Send Friend Request: POST /friend-request/
Respond to Friend Request: POST /friend-request-response/<int:pk>/
Friends List: GET /friends/
Pending Friend Requests: GET /pending-requests/
