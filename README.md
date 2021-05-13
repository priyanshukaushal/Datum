# Datum
Datum is a student management system made for use by teachers and students, so that teachers can upload marks and attendance of students and students can view their respective marks.
To run the website, first install python 3.9.1 or above. Create a virtual environment and intall django 3.1.6 in your Virtualenv.
Now so to folder containing the manage.py file and run the following commands :
python manage.py migrate
python manage.py makemigrations app_one

To create a new admin :
python manage.py createsuperuser

Finally run the Website :
python manage.py runserver

