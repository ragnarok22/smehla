title Instalando proyecto
cls
py manage.py makemigrations
py manage.py makemigrations accounts news services
py manage.py migrate
cls
echo Creando usuario administrador
py manage.py createsuperuser
pause
