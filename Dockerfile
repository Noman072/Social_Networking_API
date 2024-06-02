# Dockerfile

FROM python:3.9

ENV PYTHONUNBUFFERED=1

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY . ./

RUN pip install pip --upgrade

RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Set the entry point
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
