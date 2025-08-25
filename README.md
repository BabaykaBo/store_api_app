
# Stores API 
Study project with Python and Flask. API for management stores.  

## Requirements
* Python >= 3.12
* Flask >= 3.1.1
* flask-smorest >= 0.46.1
* Flask-SQLAlchemy >= 3.1.1
* python-dotenv >= 1.1.1
* SQLAlchemy >= 2.0.43

## Run Locally  

Clone the project  

~~~bash  
  git clone https://github.com/BabaykaBo/store_api_app
~~~

Go to the project directory  

~~~bash  
  cd store_api_app
~~~

Copy `.flaskenv-example` to `.flaskenv`. Copy `.env-example` to `.env`. Set environment variables.

Install dependencies  

~~~bash  
pip install -r requirements.txt
~~~

Start the server  

~~~bash  
flask run
~~~

OR use `gunicorn`

~~~bash
 gunicorn wsgi:app --bind localhost:5000
~~~

See API with link: `http://127.0.0.1:5000/swagger-ui`

## License  

[MIT](https://choosealicense.com/licenses/mit/)
