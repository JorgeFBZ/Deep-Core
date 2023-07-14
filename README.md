<<<<<<< HEAD
# Aplicación de Sondeos Geológicos con Segmentación de Imágenes utilizando Django y YOLOv8

Este repositorio contiene una aplicación web desarrollada en Django que permite almacenar y gestionar datos de sondeos geológicos, así como realizar la segmentación de imágenes utilizando YOLOv8 para identificar tres categorías: cota, testigo y alta fracturación.

## Características

- Permite almacenar y gestionar datos de sondeos geológicos, incluyendo datos de análisis, imágenes y desvíos del sondeo.
- Proporciona una interfaz intuitiva y fácil de usar para visualizar y actualizar los datos de sondeos.
- Utiliza una base de datos para el almacenamiento persistente de los datos.
- Utiliza YOLOv8 para segmentar imágenes y diferenciar tres categorías: cota, testigo y alta fracturación.
- Proporciona resultados de segmentación de imágenes.

## Requisitos del sistema

- Para entrenar el modelo de clasificación y segmentación de imágenes es recomendable una GPU compatible con CUDA

## Instalación

1. Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/JorgeFBZ/DH_Logger_AI.git
```

2. Accede al directorio del proyecto:

```bash
cd DH_Logger_AI
```

3. Modificar la Secret key del archivo .env
Generar una nueva SECRET KEY
https://codinggear.blog/django-generate-secret-key/
o mediante https://djecrety.ir/

4. Crear la imagen Docker:
```bash
docker-compose build
docker-compose up
# Por defecto el nombre del contenedor es dh_logger_container
docker exec -it <nombre_contenedor> python manage.py migrate
docker exec -it <nombre_contenedor> python manage.py createsuperuser
```
5. Acceder a la aplicación:
```bash
<host-ip>:8000/home
```
## Screenshots
![Image text](https://github.com/JorgeFBZ/DH_Logger_AI/blob/main/screenshots/imgs.png)
![Image text](https://github.com/JorgeFBZ/DH_Logger_AI/blob/main/screenshots/samples.png)
![Image text](https://github.com/JorgeFBZ/DH_Logger_AI/blob/main/screenshots/ver_datos.png)
![Image text](https://github.com/JorgeFBZ/DH_Logger_AI/blob/main/screenshots/ver_sondeos.png)
=======
# Deep-Core
Aplicación web para la gestión de datos de sondeos.
>>>>>>> 2d8662f07404e4cb589b6915b3a15274a50d1161
