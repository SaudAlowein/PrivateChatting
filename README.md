# Private chatting web-app
Web-application that offers private chatting between added friends.

To run make sure that the requirements are all installed (if you're on windows you will need to run Memurai since redis does not work out of the box).
Before running edit the server details in settings.py, it is the *DATABASES* dictionary.

* Do not use the default database that comes with Django (SQLITE) as it only allows single access which is problematic for this project

After editing open a command line in the root directory and run the following commands: 

``python manage.py makemigrations`` and ``python manage.py migrate``.

Finally, run the server using the command ``python manage.py runserver``. 


Simply copy the local host address and paste it into your browser.
