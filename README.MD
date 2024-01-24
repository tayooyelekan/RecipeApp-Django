# Recipe App 

The Recipe App is a Django REST API designed to create, save, and share food recipes. Postgres is used as the database to store and manage the recipe data. The app allows users to perform various operations on the recipes, such as creating, reading, updating, and deleting them.

## Features

- User authentication system with login/register
- JWT tokens for API authentication
- CRUD functionality for users
- CRUD functionality for recipes 
- Swagger/OpenAPI documentation for API

## Usage

### Install Dependencies

pip install -r requirements.txt

### Run Migrations

python manage.py migrate

### Run Development Server

python manage.py runserver

## API Documentation

Swagger API schema and documentation available at:

http://localhost:8000/swagger

![Recipe App](templates/swagger.png)