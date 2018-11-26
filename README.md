# SMEHLA
Para ejecutar el proyecto se necesita tener instalado:
- [Python versión 3.6.5](https://www.python.org/downloads/release/python-365/) o superior
- [Django version 2.1.1](https://www.djangoproject.com/download/) o superior (abrir la consola y escribir `pip install Django==2.1.1`)
- [pillow](https://pypi.org/project/Pillow/) (abrir la consola y escribir `pip install Pillow`)

## Para conprobar que todo está instalado correctamente
Escribir en la consola python --version y saldrá la versión de python que está instalado
Para comprobar la versión de Django:
- Escribir en la consola `python`
- Escribir en la consola `import django`
- Escribir en la consola `print(django.get_version())` y saldrá la versión de Django que tiene instalado

## Tener el proyecto en su máquina
Primero debe descargar el proyecto o clonarlo con [Git](https://git-scm.com/) con el comando `git clone https://github.com/ragnarok22/smehla.git`. Una vez hecho esto debe crear la base de datos (por defecto usa SQlite):
- Abrir la consola en la dirección donde se encuentra el proyecto y escribir `python manage.py makemigrations`.
- Una vez realizado esto escribir `python manage.py migrate` y ya se ha creado la base de datos.
- Debe crear un usuario administrador la primera vez que ejecuta el programa, para hacerlo escriba `python manage.py createsuperuser` y siga las instrucciones.

## Ejecutar el sitio
Para ejecutar el sitio abra la consola en la dirección donde descargó el proyecto y escriba `python manage.py runserver`. La página se ejecutará localmente en el puerto 8000. Abra el navegador en la dirección [http://127.0.0.1:8000](http://127.0.0.1:8000) y podrá ver el sitio ejecutándose en su computador. En caso de que desee que desde otro computador se vea ejecute el comando `python manage.py runserver 0.0.0.0`.
