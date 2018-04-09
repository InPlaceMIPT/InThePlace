FROM python:latest

RUN mkdir /code
ADD ./requirements.txt /code/requirements.txt
WORKDIR /code

# Install dependencies
RUN pip3 install --no-cache-dir -q -r requirements.txt
ADD ./ /code
# Expose is NOT supported by Heroku
# EXPOSE 5000

# Run the image as a non-root user
RUN adduser --system --no-create-home --disabled-password myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#CMD gunicorn --bind 0.0.0.0:$PORT django_server.wsgi
CMD python3 manage.py runserver 0.0.0.0:$PORT
