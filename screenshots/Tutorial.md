# 1. Instalación:

##  1.1. Requisitos:
Git: [Instalación de Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
Docker:[Instalación de Docker](https://docs.docker.com/engine/install/)

Requisitos recomendables para personalizar y entrenar el modelo de clasificación de imágenes:
* Python
* Tarjeta gráfica compatible con CUDA.
* [CVAT](https://www.cvat.ai/post/how-to-install-cvat-on-windows)

## 1.2. Instalación:
* Clonar el repositorio de Github en el servidor.
```
git clone https://github.com/JorgeFBZ/Deep-Core.git
```
* Acceder a la carpeta del repositorio:
```
cd Deep-Core
```
* Generar una nueva secret-key para la aplicación mediante uno de estos enlaces https://codinggear.blog/django-generate-secret-key/
o mediante https://djecrety.ir/ . Sustituir la ya existente en el archivo **.env**.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/secret-key.png)


* Generar la imagen Docker:
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/docker-compose.png)
```bash
docker-compose build
docker-compose up
```

* En otro terminal ejecutar:
```bash
# Por defecto el nombre del contenedor es deep_core_container
docker images # ver las imágenes disponibles
docker exec -it <nombre_contenedor> python manage.py makemigrations
docker exec -it <nombre_contenedor> python manage.py migrate
```

* Crear el usuario root. Este usuario tiene todos los permisos y solamente se debe de usar para la gestión de la app:
```bash
 docker exec -it <nombre_contenedor> python manage.py createsuperuser
 """
 Introducir nombre de usuario y contraseña del usuario Root
```
* Acceder a la aplicación: 
```bash
<ip-servidor>:8000/home
```
## 1.3. Crear grupos de usuarios:
* Acceder a la aplicación como superusuario.

* Acceder a la página de administración. En esta página se pueden gestionar los usuarios, los grupos de permisos y las litologías válidas para importar.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/administracion.png)

* Acceder a Grupos / Crear nuevo grupo.
Es recomendable crear al menos dos grupos, uno para usuarios de administración y otro para el resto de usuarios.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/grupos.png)

Al grupo de administración se recomienda asignar:
* Todos los permisos que contengan "DH_app".
  
Permisos para crear, borrar y modificar usuarios.
* "auth| usuario | Can add user"
* "auth| usuario | Can delete user"
* "auth| usuario | Can change user"
* "auth| usuario | Can view user"
  
Permitir modificar al administrador los grupos de permisos.
* "auth| permiso | Can add permission"
* "auth| permiso | Can view permission"
* "auth| permiso | Can change permission"

Para el resto de usuarios se pueden asignar los permisos que se requieran y crear los grupos que sean necesarios.

## 1.4. Crear usuarios:
Se puede crear un nuevo usuario desde el formulario de registro de la app o desde la página de administración
* En la página de administración/Usuarios. (En esta página también se pueden modificar y borrar los usuarios existentes)
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/usuarios.png)
* Crear nuevo usuario, asignar nombre de usuario y contraseña.
* Asignar permisos correspondientes.
# 2. Guía de uso:
En el menú izquierdo es posible:
* Visualizar los proyectos existentes.
* Crear un nuevo proyecto.
* Crear un nuevo sondeo.
* Seleccionar sondeos.
## 2.1. Crear un nuevo proyecto:
Para poder crear nuevos sondeos es necesario asignarlos a un proyecto ya existente, por lo que es necesario crear un proyecto antes de importar nuevos sondeos.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/crear_proyecto.png)
## 2.2. Visualizar proyectos:
En esta página se pueden visualizar los proyectos ya existentes en la base de datos y, además, borrar y visualizar los sondeos que contiene dicho proyecto.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/proyectos.png)

Si se borra un proyecto, se borrarán todos los sondeos y datos asociados al mismo.

## 2.3. Crear un nuevo sondeo:
Introducir la información necesaria en el formulario y seleccionar el proyecto al que pertenece el sondeo del menú desplegable.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/crear_proyecto.png)

## 2.4. Visualizar información de los sondeos:
### 2.4.1. Importar datos de un sondeo:
Por defecto, los archivos .csv que se importan a la aplicación están delimitados por tabuladores. Para modificar este parámetro a un delimitador de ";" hay que modificar la línea 230 del archivo DH_logger/settings.py

Para importar datos de un sondeo, se selecciona un sondeo y se pulsa en el botón indicado en la imagen inferior.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/importar_1.png)
Dentro de la página se pueden importar imágenes, datos de desvíos, datos de muestras y datos de litologías para el sondeo seleccionado.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/importar_datos.png)
### 2.4.2. Visualizar datos de un sondeo:
Para visualizar los datos de un sondeo, se pulsa en el botón indicado en la imagen inferior.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/ver_datos.png)
En esta página se pueden ver los diferentes datos del sondeo en formato tabla, asi como ejecutar el proceso de clasificación de las imágenes.
### 2.4.3. Editar datos de un sondeo:
Para editar los datos de un sondeo, se pulsa en el botón indicado en la imagen inferior.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/editar_datos.png)
En esta versión solamente es posible editar los datos del emboquille. La edición y borrado del resto de datos se realiza en la página de administración.
### 2.4.4. Borrar un sondeo:
Para borrar los datos de un sondeo, se pulsa en el botón indicado en la imagen inferior.
![Image text](https://github.com/JorgeFBZ/Deep-core/blob/master/screenshots/tutorial/borrar_sondeo.png)
Al borrar un sondeo, se borrarán todos los datos asociados al mismo.
