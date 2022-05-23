# Reactor project

## About the project

This is my submission for [Assignment fall 2022: Developers](https://www.reaktor.com/assignment-fall-2022-developers/).
The solution is done in [Django](https://www.djangoproject.com/), a python framework for creating web applications. The
production version of the code is being hosted at https://ee-reaktor-project.herokuapp.com/.

## Launching the code

The project can be launched from source code by using `docker-compose` or by running the code on your machine. Whichever
method you're using the web app will be available on http://127.0.0.1:8000

### If you're using `docker-compose`

* Make sure you have `Docker` and `docker-compose` installed
* Run the following command(s):
  ```bash
  docker-compose build
  docker-compose up
  # or 
  docker-compose up --build
  ```

### If you're launching on your machine

* Make sure you have `python3` and `pip3` installed. This project was built and tested on version `3.8.13`.

  **Note:** some systems have multiple python versions installed, therefore you might need to substitute `python`
  command
  with `python3` and `pip` with `pip3`
* Run the following commands in the root of the project:
  ```bash
  pip3 install -r requirements.txt
  python manage.py migrate
  python python manage.py runserver 0.0.0.0:8000
  ```
