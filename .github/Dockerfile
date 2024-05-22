FROM python:3.9-alpine


# Create a working directory
WORKDIR /app

# Clone the project repository
COPY . .

# Install project dependencies
#COPY requirements.txt .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the Django app
EXPOSE 8000

# Start the Django app using Gunicorn
CMD python manage.py migrate && gunicorn -b 0.0.0.0:800 RecipeApp.wsgi:application
