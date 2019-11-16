# Cheap Hotels

> UTN - 2019

 - Bernardo Chiletto
 - Mariano Fernandez

### Project Setup

- Install **python 3.6.3**

- Install **pip**

- Install **Django 1.11.17**

```Bash
$ pip install Django==1.11.17
```

- Install **pillow**

````Bash
$ pip install Pillow
````

- Go to the project root

````Bash
$ cd iQuilar\src\iquilar
````

- Migrate Initial Data

````bash
$ python manage.py migrate

$ python manage.py loaddata auth-data.json
````

- Migrate Bookings Models
````bash
$ python manage.py makemigrations bookings
$ python manage.py migrate bookings
````

- Seed Premade Authentication Rules and Users/Cities

````Bash
$ python manage.py loaddata mock-data.json
````

- Start the development server
````Bash
$ python manage.py runserver
````

- Enter the admin site at

    - `http://127.0.0.1:8000/admin/`

- Premade user data:
	- Superuser:

		username: superuser

		password: super123

	- Admin:

		username: admin

		password: adder123

	- Owners:

		- jane.doe:

			username: jane.doe

			password: j4n3123456

		- john.doe:

			username: john.doe

			password: j0hn123456		

- Create more reservations like owner then you can visit de bookings page normaly.