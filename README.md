# Running the project, development.

* Install python 2.7.x
* Install PIP for your platform
* Install virtual environment
	`pip install virtualenv`
* Create a virtual environment (could be inside this directory)
	`virtualenv env`
* Activate the virtual env
	`source env/bin/activate`
* Install the packages
	`pip install -r requirements.txt`
* Run the tests
	`python manage.py test`
* Run the program
	`python manage.py calculate '{"rentDates":["2017-11-19T05:00:00.000Z","2017-11-20T05:00:00.000Z","2017-11-21T05:00:00.000Z"],"car":{"model":"Cherato","type":"sport"},"membership":false,"age":24}'`


# Docker deployment

`docker-compose build`

To run it as daemon:

`docker-compose up -d`

Only for the first use (or when needed):

`docker-compose exec web python manage.py migrate`
`docker-compose exec web python manage.py initialize`

Run the tests  like this:

`docker-compose exec web python manage.py test`

Run the program like this:

`docker-compose exec web python manage.py calculate '{"rentDates":["2017-11-19T05:00:00.000Z","2017-11-20T05:00:00.000Z","2017-11-21T05:00:00.000Z"],"car":{"model":"Cherato","type":"sport"},"membership":false,"age":24}'`

Stop

`docker-compose stop`