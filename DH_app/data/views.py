"""
Django web app to manage and store drillhole data.
Copyright (C) 2023 Jorge Fuertes Blanco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from DH_app.serializer import ImportSerializer, ProjectSerializer
from DH_app.models import *
from DH_app.form import *
from django.contrib.auth.decorators import login_required

from DH_app.data.file_manager import *
import logging
import pandas as pd
import json, os, csv
from PIL import Image
from DH_app.data.process_images import *

def filter_DH (project):
    """
    Filtra los registros de la tabla General_DH según el proyecto especificado.

        Parámetros:
            - project: El ID del proyecto utilizado para filtrar los registros.

        Retorno:
            - Objeto JSON que contiene los registros filtrados en formato de diccionario, con las claves como índices.
"""
    data = General_DH.objects.all().values_list("ID","project_id", "DH_id","start_date","teo_azimuth", "teo_incl")
    data = pd.DataFrame(data, columns=["ID","project_id", "DH_id","start_date","teo_azimuth", "teo_incl"])
    data["start_date"] = data["start_date"].astype(str)
    DHs = data[data['project_id']== str(project)]
    DHs=DHs.to_json(orient="index", date_format="iso")
    data = json.loads(DHs)
    return data


@login_required(login_url=settings.LOGIN_URL)
@api_view(['GET', 'POST'])
def new_hole (request):
    """
    Vista basada en API para la creación de un nuevo sondeo en un proyecto.

    Métodos permitidos:
        - GET: Retorna la página de importación de datos con la lista de proyectos disponibles.
        - POST: Crea un nuevo sondeo en el proyecto especificado y guarda los datos importados.
            Cuerpo de la solicitud:
                - project: El nombre del proyecto en el que se creará el sondeo.
                - DH_id: El ID del sondeo.
    Retorno:
        - Si la solicitud es GET:
            - Página de importación de datos con la lista de proyectos disponibles.

        - Si la solicitud es POST y los datos son válidos:
            - Página de importación exitosa con los datos validados.

        - Si la solicitud es POST y los datos no son válidos:
            - Página de importación con los errores encontrados durante la validación de los datos.
        """
    if request.method == "GET":
        projects = Projects.objects.all().values_list("project_name")
        return render(request, 'data/import_data.html', {"projects": projects})
    
    elif request.method == "POST":
        form = DataImportForm(request.POST).data
        serializer = ImportSerializer(data = form)
        project_name = request.POST.get("project")
        DH_id = request.POST.get("DH_id")

        if serializer.is_valid():
            create_directory(project_name, DH_id)
            serializer.save()
            return render(request, "data/correct_import.html", {'data': serializer.validated_data})
        
        else:
            logging.error(serializer.errors)
            errors = [serializer.errors [error][0] for error in serializer.errors]
            key = [error for error in serializer.errors]
            errors = [[field +": "+error]for field, error in zip(key,errors)]
            return render(request, "data/correct_import.html", {'errors': errors})


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET", "POST"])
def create_project(request):
    """
    Vista basada en API para la creación de un nuevo proyecto.
    Métodos permitidos:
        - GET: Retorna la página de creación de un nuevo proyecto.

        - POST: Crea un nuevo proyecto con los datos proporcionados.
    Retorno:
        - Si la solicitud es GET:
            - Página de creación de un nuevo proyecto.

        - Si la solicitud es POST y los datos son válidos:
            - Página de proyecto creado con los datos validados.

        - Si la solicitud es POST y los datos no son válidos:
            - Página de proyecto creado con los errores encontrados durante la validación de los datos.
    """
    if request.method == "GET":
        return render(request, 'data/new_project.html')
    
    elif request.method == "POST":
        form = CreateProject(request.POST).data
        project_name = request.POST.get("project_name")
        serializer = ProjectSerializer(data = form)

        if serializer.is_valid():
            create_directory(project_name) 
            serializer.save()      
            return render (request, 'data/project_created.html', {'data': serializer.validated_data})
        
        else:
            logging.error(serializer.errors)
            return render (request, 'data/project_created.html',serializer.errors)

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET","POST"])
def modify_project(request):
    """
    Vista basada en API para modificar proyectos existentes.

    Métodos permitidos:
        - GET: Retorna la página con la lista de proyectos existentes y su información.

        - POST: Realiza una acción especificada (borrar o obtener información) sobre un proyecto existente.
            Cuerpo de la solicitud:
                - project_id: El ID del proyecto sobre el cual se realizará la acción.
                - action: La acción a realizar. Puede ser "delete" para borrar el proyecto o "info" para obtener información.
    
    Retorno:
        - Si la solicitud es GET:
            - Página con la lista de proyectos existentes y su información.

        - Si la solicitud es POST y la acción es "delete":
            - Página con la lista de proyectos actualizada después de borrar el proyecto especificado.

        - Si la solicitud es POST y la acción es "info":
            - Redirecciona a la página de obtención de información detallada del proyecto especificado.

        - Si la solicitud es POST y la acción no es válida:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

        - Si la solicitud no es GET o POST:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

    """
    if request.method == "GET":
        projects = Projects.objects.all().values_list()
        data_response = []

        for project in projects:
            project_name = project[0]
            comments = project[1]
            DH_count = int(General_DH.objects.filter(project_id=project_name).count())
            project_data = {"project_id": project_name, "comments": comments, "DH_count": DH_count}
            data_response.append(project_data)
       
        return (render( request, 'data/show_projects.html', {"data": data_response, "messages": None}))
    
    if request.method == "POST":
        project_name = request.POST.get("project_id")
        action = request.POST.get("action")
        token = str(request.POST.get("csrfmiddlewaretoken"))
        if action == "delete":
            Projects.objects.filter(project_name=project_name).delete()
            delete_directory(project_name)
            return (render( request, 'data/show_projects.html', {"data": None, "messages": f"Borrado proyecto {project_name}"}))

        if action == "info":
            url = reverse(select_data)+f"?csrfmiddlewaretoken={token}&project_id={project_name}"
            return redirect(url)
        else:
            return Response(request, status=status.HTTP_400_BAD_REQUEST)    
    else:
        return Response(request, status=status.HTTP_400_BAD_REQUEST)
  

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET","POST"])
def modify_data (request):
    """
    Vista basada en API para modificar proyectos existentes.

    Métodos permitidos:
        - GET: Retorna la página con la lista de proyectos existentes y su información.

        - POST: Realiza una acción especificada (borrar o obtener información) sobre un proyecto existente.

    Retorno:
        - Si la solicitud es GET:
            - Página con la lista de proyectos existentes y su información.

        - Si la solicitud es POST y la acción es "delete":
            - Página con la lista de proyectos actualizada después de borrar el proyecto especificado.

        - Si la solicitud es POST y la acción es "info":
            - Redirecciona a la página de obtención de información detallada del proyecto especificado.

        - Si la solicitud es POST y la acción no es válida:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

        - Si la solicitud no es GET o POST:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

    """
    ID = request.GET.get('ID')
    action = str(request.GET.get('action'))

    if request.method == "GET":
        
        DH_data = General_DH.objects.filter(ID=ID).values()
        project = DH_data[0]["project_id"]
        if action == "update":
            return render (request, 'data/update_data.html', {'data': DH_data, "action": action})
        if action == "delete":
            delete_directory(project, ID)
            return render (request, 'data/update_data.html', {'data': DH_data, "action": action})
        if action == "info":
            return render (request, 'data/update_data.html', {'data': DH_data, "action": action})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        ID = request.POST.get("ID")
        action = request.POST.get("action")
        print (request.content_params)

        if action == "update":
            DH_DB = General_DH.objects.filter(ID=ID) # DB data from ID
            form = DataImportForm(request.POST).data # New data
            try:
                data = {'project_id': form['project_id'],
                    'DH_id' : form['DH_id'],
                    'start_date' : form['start_date'],
                    'end_date' : form['end_date'],
                    'teo_azimuth': form['teo_azimuth'],
                    'real_azimuth' : form['real_azimuth'],
                    'teo_incl' : form['teo_incl'],
                    'real_incl' : form['real_incl'],
                    'UTM_Zone' : form['UTM_Zone'],
                    'northing' : form['northing'],
                    'easting' : form['easting'],
                    'elevation' : form['elevation']}

                DH_DB.update(**data)
                DH_data = General_DH.objects.filter(ID=ID)
                print (DH_data)
                return render (request, 'data/update_data.html', {'data': DH_data, "action": "info"})
            except Exception as e:
                logging.ERROR(e)
                return render (request, 'data/update_data.html', { "action": "info","error": e })
        
        if action == "delete":
            General_DH.objects.filter(ID=ID).delete()
            return render (request, 'data/deleted_data.html')
        
        else:
            return Response(request.data, status=status.HTTP_200_OK)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
def select_data(request):
    """
    Vista que permite seleccionar datos en función del proyecto proporcionado.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida.

    Comportamiento:
        - Verifica si la solicitud es de tipo GET.
        - Recupera el proyecto seleccionado de los parámetros de la solicitud.
        - Si no se proporciona ningún proyecto, recupera una lista de todos los proyectos disponibles.
        - Si se proporciona un proyecto, se filtran los datos en función del proyecto.
        - Si se encuentran datos, se muestra una plantilla con los datos filtrados y se omiten los proyectos.
        - Si no se encuentran datos, se muestra una plantilla de error.
        - Si la solicitud no es de tipo GET, se devuelve una respuesta de error con el código de estado HTTP 400 (Solicitud incorrecta).

    Retorno:
        HttpResponse: Una respuesta HTTP que contiene la plantilla HTML con los datos filtrados o un mensaje de error.

    Uso:
        Asegúrese de que el usuario esté autenticado antes de acceder a esta vista.
        Envíe una solicitud GET a la URL correspondiente para seleccionar datos según el proyecto proporcionado.
        La respuesta será una plantilla HTML que mostrará los datos filtrados o un mensaje de error si no se encuentran datos.

    Limitaciones:
        - Solo acepta solicitudes GET.
    """
    
    if request.method == "GET":
        form = SelectDataForm(request.GET).data
        project = form.get('project_id', None)

        if not project:
            projects = Projects.objects.all().values_list("project_name")
            return render (request, 'data/DH_selection.html', {"DH_data": None, "projects": projects})
        
        elif project != None:
            data = filter_DH(project)
            if data:
                return render (request,'data/DH_selection.html', {"DH_data": data, "projects": None}) 
            else:
                return render (request,'data/DH_selection.html', {"Error": True}) 

    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET", "POST"])
def upload_imgs(request):
    """
    Vista basada en API para cargar imágenes relacionadas con un sondeo específico.

    Métodos permitidos:
        - GET: Retorna la página de carga de imágenes.

        - POST: Realiza la carga de imágenes y las guarda en la ubicación correspondiente.
            Cuerpo de la solicitud:
                - DH_id: El ID del sondeo al cual pertenecen las imágenes.
                - Images: Lista de archivos de imagen a cargar.

    Retorno:
        - Si la solicitud es GET:
            - Página de carga de imágenes con los detalles del sondeo especificado.

        - Si la solicitud es POST y se cargan las imágenes correctamente:
            - Página de carga de imágenes con un mensaje de éxito.

        - Si la solicitud es POST y no se proporcionan imágenes o se produce un error:
            - Página de carga de imágenes con un mensaje de error.

        - Si la solicitud no es GET o POST:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

    """
    if request.method == "GET":
        ID = request.GET.get("ID")
        form = UploadFileForm()
        DH = General_DH.objects.filter(ID=ID).values()[0]
        return render(request, "data/import_files.html", {"DH": DH, "form":form})
    
    elif request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        ID = request.POST.get("DH_id")
        DH_data = General_DH.objects.filter(DH_id=ID).values().first()
        path = create_directory(DH_data["project_id"], DH_data["DH_id"]) # path a la carpeta del sondeo
        try:
            if request.FILES.getlist("Images"):
                count = 0
                img_files = request.FILES.getlist("Images")
                folder_path = os.path.join(path,"images")
                for file in img_files:
                    img_files = [i for i in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, i))]
                    if img_files:
                        last_img = img_files[-1]
                        last_num = int(last_img.split("_")[-1].split(".")[0]) + 1
                    else:
                        last_num = 1
                    path_img = os.path.join(folder_path,str(ID)+f"_{last_num}.jpg")
                    img =  Image.open (file)
                    img.save(path_img)
                    count +=1
                message = f"{count} Imagenes importadas correctamente"
                return render(request, "data/import_files.html", {"message": message})
            else: raise FileNotFoundError
        except Exception as e:
            error = "Se ha producido un error al importar las imagenes."
            return render(request, "data/import_files.html", {"error": error})


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET", "POST"])
def show_images(request):
    if request.method == "GET":
        project_id = request.GET.get("project_id")
        DH_id = request.GET.get("DH_id")
        path = create_directory (project_id, DH_id)
        images_path = os.path.join(path, "images")
        p_images_path = os.path.join(path, "processed_imgs")
        images = list_images(images_path)
        p_images= list_images(p_images_path)
        show_images = []

        if len(images) > len(p_images):
            p_images.extend([None]*(len(images)-len(p_images)))
            for i, j in zip(images, p_images):
                show_images.append([i,j])
        else:
            show_images = zip(images, p_images)
        return render(request, "data/show_images.html", {"images":show_images, "MEDIA_URL":settings.MEDIA_URL, "DH_id":DH_id, "project": project_id})

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        DH_id = request.POST.get("DH_id")
        path = create_directory (project_id, DH_id)
        model_path ="/django/media/YOLO_models/default.pt" # Path al modelo

        if not list_images(os.path.join(path,"images")):
            error = "No hay imagenes para este sondeo."
            return render(request, "data/show_images.html", {"error":error})
        else:
            process_imgs(path, model_path)
            images_path = os.path.join(path, "images")
            p_images_path = os.path.join(path, "processed_imgs")
            images = list_images(images_path)
            p_images= list_images(p_images_path)
            show_images = zip(images, p_images)
            return render(request, "data/show_images.html", {"images":show_images, "MEDIA_URL":settings.MEDIA_URL, "DH_id":DH_id, "project": project_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)

'''

'''
@login_required(login_url=settings.LOGIN_URL)
@api_view(["POST"])
def import_samples (request):
    """
    Vista basada en API para cargar imágenes relacionadas con un sondeo específico.
    El archivo .csv debe de tener las columnas en el mismo orden que las definidas en models.py (USAR "." COMO DECIMAL)

    Métodos permitidos:
        - GET: Retorna la página de carga de imágenes.
            Parámetros de consulta:
                - ID: El ID del sondeo al cual se cargarán las imágenes.

        - POST: Realiza la carga de imágenes y las guarda en la ubicación correspondiente.
            Cuerpo de la solicitud:
                - DH_id: El ID del sondeo al cual pertenecen las imágenes.
                - Images: Lista de archivos de imagen a cargar.
    Retorno:
        - Si la solicitud es GET:
            - Página de carga de imágenes con los detalles del sondeo especificado.

        - Si la solicitud es POST y se cargan las imágenes correctamente:
            - Página de carga de imágenes con un mensaje de éxito.

        - Si la solicitud es POST y no se proporcionan imágenes o se produce un error:
            - Página de carga de imágenes con un mensaje de error.

        - Si la solicitud no es GET o POST:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

    """
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        DH_id = request.POST.get("DH_id")
        path = create_directory (project_id, DH_id)

        if request.FILES.get("samples"):
            file = request.FILES.get("samples")
            data = file.read().decode("utf-8")
            csv_data = csv.reader(data.splitlines(), delimiter=";")
            next(csv_data) # saltar la primera fila con los encabezdos
            
            for row in csv_data:
                DH_id_file = row[0]
                try:
                    DH_id = General_DH.objects.get(DH_id = DH_id_file)
                    From = float(row[1])
                    To = float(row[2])
                    Element_1 = float(row[3])
                    Element_2 = float(row[4])
                except General_DH.DoesNotExist:
                    error = "El sondeo no esta en la base de datos."
                    return render(request, "data/import_files.html", {"error": error})

                except ValueError:
                    error = "Error al importar los datos: alguno de las columnas no contiene valores válidos"
                    return render(request, "data/import_files.html", {"error": error})
                except Exception:
                    error = "Error al importar los datos."
                    return render(request, "data/import_files.html", {"error": error})                            

                try:
                    Sample_model(
                        DH_id= DH_id,
                        From = From,
                        To = To,
                        element_1 = Element_1,
                        element_2 = Element_2
                    ).save()
                except Exception:
                    error = "Error al importar los datos."
                    return render(request, "data/import_files.html", {"error": error})                            
            return render(request, "data/import_files.html", {"message": "Datos importados correctamente."})                            
        else:
            error = "No hay ningún fichero para importar."
            return render(request, "data/import_files.html", {"error": error})

    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["POST"])
def import_deviations (request):
    """
    Vista basada en API para cargar imágenes relacionadas con un sondeo específico.
    El archivo .csv debe de tener las columnas en el mismo orden que las definidas en models.py (USAR "." COMO DECIMAL)

    Métodos permitidos:
        - GET: Retorna la página de carga de imágenes.
            Parámetros de consulta:
                - ID: El ID del sondeo al cual se cargarán las imágenes.

        - POST: Realiza la carga de imágenes y las guarda en la ubicación correspondiente.
            Cuerpo de la solicitud:
                - DH_id: El ID del sondeo al cual pertenecen las imágenes.
                - Images: Lista de archivos de imagen a cargar.
    Retorno:
        - Si la solicitud es GET:
            - Página de carga de imágenes con los detalles del sondeo especificado.

        - Si la solicitud es POST y se cargan las imágenes correctamente:
            - Página de carga de imágenes con un mensaje de éxito.

        - Si la solicitud es POST y no se proporcionan imágenes o se produce un error:
            - Página de carga de imágenes con un mensaje de error.

        - Si la solicitud no es GET o POST:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).

    """
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        DH_id = request.POST.get("DH_id")
        path = create_directory (project_id, DH_id)

        if request.FILES.get("deviations"):
            file = request.FILES.get("deviations")
            data = file.read().decode("utf-8")
            csv_data = csv.reader(data.splitlines(), delimiter=";")
            next(csv_data) # saltar la primera fila con los encabezdos
            for row in csv_data:
                DH_id_file = row[0]
                try:
                    DH_id = General_DH.objects.get(DH_id = DH_id_file)
                    From = float(row[1])
                    To = float(row[2])
                    inclination = float(row[3])
                    azimuth = float(row[4])
 
                except General_DH.DoesNotExist:
                    error = "El sondeo no esta en la base de datos."
                    return render(request, "data/import_files.html", {"error": error})
               
                except ValueError:
                    error = "Error al importar los datos: alguna de las columnas no contiene valores válidos"
                    return render(request, "data/import_files.html", {"error": error})
                
                except Exception:
                    error = "Error al cargar los datos."
                    return render(request, "data/import_files.html", {"error": error})                            

                try:
                    Desv_model(
                        DH_id= DH_id,
                        From = From,
                        To = To,
                        inclination = inclination,
                        azimuth = azimuth
                    ).save()
                except Exception as e:
                    error = "Error al importar los datos."
                    return render(request, "data/import_files.html", {"error": error})                            
            return render(request, "data/import_files.html", {"message": "Datos importados correctamente."})                            
        else:
            error = "No hay ningún fichero para importar."
            return render(request, "data/import_files.html", {"error": error})

    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url=settings.LOGIN_URL)
@api_view(["POST"])
def import_litho (request):
    if request.method == "POST":
        DH_id = request.POST.get("DH_id")
        Litho = Lithos.objects.values_list("Litho_label", flat=True)
        print(Litho)
        if request.FILES.get("litho"):
            file = request.FILES.get("litho")
            data = file.read().decode("utf-8")
            csv_data = csv.reader(data.splitlines(), delimiter=";")
            next(csv_data) # saltar la primera fila con los encabezdos
            for row in csv_data:
                DH_id_file = row[0]
                
                try:
                    DH_id = General_DH.objects.get(DH_id = DH_id_file)
                    From = float(row[1])
                    To = float(row[2])
                    Litho_label = row[3]
                    assert Litho_label in Litho

                except AssertionError:
                    error = f"La litología {Litho_label} no esta introducida. Contacte con el administrador."
                    return render(request, "data/import_files.html", {"error": error})
 
                except General_DH.DoesNotExist:
                    error = "El sondeo no esta en la base de datos."
                    return render(request, "data/import_files.html", {"error": error})

                except ValueError:
                    error = "Error al importar los datos: alguna de las columnas no contiene valores válidos"
                    return render(request, "data/import_files.html", {"error": error})
                
                except Exception:
                    error = f"Error al cargar los datos. {e}"
                    return render(request, "data/import_files.html", {"error": error})                            

                try:
                    Lithos_DH(
                        DH_id= DH_id,
                        From = From,
                        To = To,
                        Litho_label = Lithos.objects.get(Litho_label=Litho_label),
                    ).save()
                except Exception as e:
                    error = f"Error al cargar los datos. {e}"
                    return render(request, "data/import_files.html", {"error": error})                            
            return render(request, "data/import_files.html", {"message": "Datos importados correctamente."})                            
        
        else:
            error = "No hay ningún fichero para importar."
            return render(request, "data/import_files.html", {"error": error})

    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
def show_samples(request):
    """
    Vista basada en API para mostrar los datos de muestras de un sondeo específico.

    Métodos permitidos:
        - GET: Muestra los datos de muestras para un sondeo específico.
            Parámetros de consulta:
                - project_id: El ID del proyecto al cual pertenece el sondeo.
                - DH_id: El ID del sondeo.

    Retorno:
        - Si se proporcionan los parámetros de consulta adecuados:
            - Página que muestra los datos de muestras para el sondeo especificado.

        - Si no se proporcionan los parámetros de consulta adecuados:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).
    """
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Sample_model.objects.filter(DH_id=sondeo).values()
        return render(request, "data/show_samples.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
def show_deviations(request):
    """
    Vista basada en API para mostrar los datos de desviaciones de un sondeo específico.

    Métodos permitidos:
        - GET: Muestra los datos de desviaciones para un sondeo específico.

    Retorno:
        - Si se proporcionan los parámetros de consulta adecuados:
            - Página que muestra los datos de desviaciones para el sondeo especificado.

        - Si no se proporcionan los parámetros de consulta adecuados:
            - Respuesta con código de estado HTTP 400 (Solicitud incorrecta).
    """
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Desv_model.objects.filter(DH_id=sondeo).values()
        return render(request, "data/show_desv.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)
    

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
def show_litho(request):
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Lithos_DH.objects.filter(DH_id=sondeo)
        return render(request, "data/show_litho.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)
    