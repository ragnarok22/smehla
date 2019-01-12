# SMEHLA
Para ejecutar el proyecto se necesita tener instalado:
- [Python versión 3.6.5](https://www.python.org/downloads/release/python-365/) o superior
- [Django version 2.1.1](https://www.djangoproject.com/download/) o superior (abrir la consola y escribir `pip install Django==2.1.1`)
- [pillow](https://pypi.org/project/Pillow/) (abrir la consola y escribir `pip install Pillow`)
- [gettext](https://mlocati.github.io/articles/gettext-iconv-windows.html) para windows

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

### Instalar y ejecutar el proyecto mucho más fácil
Para la creación de la base de datos y la creación del primer usuario administrador ejecute `install_project.bat` y siga las indicaciones para crear el usuario administrador. Para ejecutar el sitio solo tiene que ejecutar el fichero `start_project.bat`.

## Configuración avanzada
Este proyecto tiene un módulo para que la configuración del sitio sea mucho más fácil (correo, base de datos, etc). 
Dentro del proyecto hay un fichero de configuración por defecto llamado [config-default.ini](config-default.ini) que 
contiene una configuración de ejemplo. Dentro de ella se pueden configurar varios elementos:
- **SECRET_KEY**: contiene una cadena de caracteres que es usada por el sitio para encriptar las contraseñas.
- **ALLOWED_HOSTS**: en este se ponen las direcciones donde va a estar ejecutandose el sitio. Por ejemplo, si el sitio 
está siendo ejecutado en la dirección IP 192.168.0.100 y con DNS [http://sitio.example.com](http://sitio.example.com) 
entonces habría que poner ambas en el fichero de configuración **separados por un espacio** de la siguiente forma: 
`192.168.0.100 sitio.example.com`.
- **TIMEZONE**: Zona horaria dónde va a estar montado el sitio.
- **ADMINS**: Es donde se pone el nombre y el correo de el/los administrador/es del sitio. si se tiene uno solo se pone: 
`Juan Perez, juan@example.com`. Si es más de uno se pondrían separados por *;* Ejemplo: `Jhon Doe, admin@example.com;
 Adam Loving, adam@example.com`.

#### Configuración del correo
- **EMAIL_HOST**: Aquí se pone la dirección de salida de tu configuración de correo. Si tienes dudas contacta con tu 
 proveedor de correo. Ejemplo: `smtp.example.com`.
- **EMAIL_PORT**: Aquí se pone el puerto de salida de tu configuración de correo. Si tienes dudas contacta con tu 
 proveedor de correo. Ejemplo: `25`.
- **EMAIL_HOST_USER**: Nombre de usuario del correo que va a usar el sitio para enviar correo. Ejemplo si el correo es
 información@example.com: `informacion`.
- **EMAIL_HOST_PASSWORD**: Contraseña del usuario de correo que va a usar el sitio para enviar correos. Ejemplo: 
 `password123`. **La contraseña no puede tener espacios**.

#### Configuración de la base de datos
El sitio soporta dos tipos de base de datos: SQLite y PostgreSQL. Si se usa SQLite solo tendrá que poner en la 
configuración el nombre de la base de datos con la extensión `sqlite3`, si usa PostgreSQL entonces tendrá que poner la 
dirección, el puerto, etc. Antes de escoger que base de datos va a usar, por favor, mire los pro y contras de ambos 
tipo de base de datos
- **NAME**: Nombre de la base de datos. Si la base de datos es de tipo SQLite, solo tiene que poner esta información 
con la extensión `sqlite3`, ejemplo: `sitio.sqlite3`. Si es PostgreSQL entonces es solo el nombre de la base de datos. 
Ejemplo: `sitio`.
- **HOST**: Dirección dónde está montado el servidor de PostgreSQL. Recuerde que en el servidor debe habilitarlo para
que el sitio pueda acceder a él. Ejemplo: `192.168.45.100` ó `servidor.basedatos.com`.
- **PORT**: Puerto del servidor PostgreSQL. Por defecto el que usa es `5432`.
- **USER**: Nombre de usuario con el que se va a conectar al servidor PostgreSQL. este usuario tiene que tener permisos
de lectura y escritura en la base de datos.
- **PASSWORD**: La contraseña del usuario con el que se va a conectar al servidor PostgreSQL. **No puede tener espacios
en blanco**.

Por último, todo esto debe estar en un fichero llamado `config.ini`, utilice el fichero
[config-default.ini](config-default.ini) como guía.

## Dudas
Si tienes dudas crea un nuevo [issue en Github](https://github.com/ragnarok22/smehla/issues/new) y has tu pregunta.