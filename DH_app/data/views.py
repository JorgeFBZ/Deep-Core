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
from django.contrib.auth.decorators import login_required, permission_required

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
'''
----------------------------------------------------
            IMPORTAR DATOS (CRUD BD)
----------------------------------------------------
'''

'''
Crear un proyecto
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.add_projects")
@api_view(["GET", "POST"])
def create_project(request):
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

'''
Borrar proyecto
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.delete_projects")
@api_view(["POST"])
def delete_project(request):    
    project_name = request.POST.get("project_id")
    token = str(request.POST.get("csrfmiddlewaretoken"))
    Projects.objects.filter(project_name=project_name).delete()
    delete_directory(project_name)
    return (render( request, 'data/show_projects.html', {"data": None, "messages": f"Borrado proyecto {project_name}"}))

'''
Visualizar sondeos de un proyecto
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.view_general_dh")
@api_view(["POST"])
def info_project(request):
    project_name = request.POST.get("project")
    print (project_name)
    token = str(request.POST.get("csrfmiddlewaretoken"))
    url = reverse(select_data)+f"?csrfmiddlewaretoken={token}&project={project_name}"
    return redirect(url)

'''
Visualizar proyectos de la BD
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.view_projects")
@api_view(["GET"])
def show_project(request):
    projects = Projects.objects.all().values_list()
    data_response = []

    for project in projects:
        project_name = project[0]
        comments = project[1]
        DH_count = int(General_DH.objects.filter(project_id=project_name).count())
        project_data = {"project_id": project_name, "comments": comments, "DH_count": DH_count}
        data_response.append(project_data)
    
    return (render( request, 'data/show_projects.html', {"data": data_response}))

'''
Crear un nuevo sondeo
''' 
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.add_general_dh")
@api_view(["GET",'POST'])
def new_hole (request):
    if request.method == "GET":
        projects = Projects.objects.all().values_list("project_name")
        projects = [i[0] for i in projects]
        return render(request, 'data/import_data.html', {"projects": projects})
    if request.method == "POST":
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

'''
Borrar sondeo de la BD
'''       
@login_required(login_url=settings.LOGIN_URL)
#FIXME Cambiar permisos
@permission_required("DH_app.delete_general_dh")
@api_view(["GET","POST"])
def delete_data (request):
    if request.method == "GET":
        ID = request.GET.get('ID')
        DH_data = General_DH.objects.filter(ID=ID).values()
        return render (request, 'data/delete_data.html', {'data': DH_data})
    if request.method == "POST":
        ID = request.POST.get("ID")
        General_DH.objects.filter(ID=ID).delete()
        return render (request, 'data/deleted_data.html', {"ID": ID})
        
'''
Actualizar datos de un sondeo
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.change_general_dh")
@api_view(["GET","POST"])
def update_data (request):
    if request.method == "GET":
        ID = request.GET.get('DH_id')
        DH_data = General_DH.objects.filter(DH_id=ID).values()
        return render (request, 'data/update_data.html', {'data': DH_data})
    
    if request.method == "POST":
        DH_id = request.POST.get("DH_id")
        DH_DB = General_DH.objects.filter(DH_id=DH_id) # DB data from ID
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
            DH_data = General_DH.objects.filter(DH_id=DH_id).values()[0]
            return render (request, 'data/show_data.html', {'data': DH_data})
        
        except Exception as e:
            logging.ERROR(e)
            return render (request, 'data/update_data.html', { "error": e })
            
'''
Visualizar datos de un sondeo (tabla -> General_DH)
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.view_general_dh")
@api_view(["GET"])
def show_dh_data (request):

    ID = request.GET.get('ID')       
    DH_data = General_DH.objects.filter(ID=ID).values()[0]
    return render (request, 'data/show_data.html', {'data': DH_data})


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
def select_data(request):
    form = SelectDataForm(request.GET).data
    project = form.get('project', None)

    if not project:
        projects = Projects.objects.all().values_list("project_name")
        projects = [p[0] for p in projects]
        return render (request, 'data/DH_selection.html', {"DH_data": None, "projects": projects})
    
    elif project != None:
        data = filter_DH(project)
        if data:
            return render (request,'data/DH_selection.html', {"DH_data": data, "projects": None}) 
        else:
            return render (request,'data/DH_selection.html', {"Error": True}) 

'''
----------------------------------------------------
            IMPORTAR FICHEROS
----------------------------------------------------
'''
@login_required(login_url=settings.LOGIN_URL)
@permission_required("DH_app.add_sample_model")
@api_view(["POST"])
def import_samples (request):

    if request.method == "POST":
        DH_id = request.POST.get("DH_id")

        if request.FILES.get("samples"):
            file = request.FILES.get("samples")
            data = file.read().decode("utf-8")
            csv_data = csv.reader(data.splitlines(), delimiter=settings.CSV_DELIMITER)
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
                    error = "Error al importar los datos: alguna de las columnas no contiene valores válidos"
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
                
                except Exception as e:
                    logging.ERROR(e)
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
@permission_required("DH_app.add_desv_model")
def import_deviations (request):

    if request.method == "POST":
        project_id = request.POST.get("project_id")
        DH_id = request.POST.get("DH_id")
        if request.FILES.get("deviations"):
            file = request.FILES.get("deviations")
            data = file.read().decode("utf-8")
            csv_data = csv.reader(data.splitlines(), delimiter=settings.CSV_DELIMITER) 
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
                    logging.ERROR(e)
                    error = "Error al importar los datos."
                    return render(request, "data/import_files.html", {"error": error})                            
            return render(request, "data/import_files.html", {"message": "Datos importados correctamente."})                            
        else:
            error = "No hay ningún fichero para importar."
            return render(request, "data/import_files.html", {"error": error})

    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET", "POST"])
@permission_required("DH_app.add_images")
def upload_imgs(request):

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
                    img_files.sort()
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
            logging.ERROR("Upload ERROR:", e)
            error = "Se ha producido un error al importar las imagenes."
            return render(request, "data/import_files.html", {"error": error})


@login_required(login_url=settings.LOGIN_URL)
@api_view(["POST"])
@permission_required("DH_app.add_lithos_dh")
def import_litho (request):
    DH_id = request.POST.get("DH_id")
    Litho = Lithos.objects.values_list("Litho_label", flat=True)

    if request.FILES.get("litho"):
        file = request.FILES.get("litho")
        data = file.read().decode("utf-8")
        csv_data = csv.reader(data.splitlines(), delimiter=settings.CSV_DELIMITER) 
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
            
            except Exception as e:
                logging.ERROR("Upload Error: ",e)
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

'''
----------------------------------------------------
            VISUALIZAR DATOS
----------------------------------------------------
'''

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
@permission_required("DH_app.view_images")
def show_images(request):
    project_id = request.GET.get("project_id")
    DH_id = request.GET.get("DH_id")
    path = create_directory (project_id, DH_id)
    images_path = os.path.join(path, "images")
    p_images_path = os.path.join(path, "processed_imgs")

    images = list_images(images_path)
    p_images= list_images(p_images_path)
    print (images_path)
    show_images = []
    if not images:
        error = "No hay imágenes para este sondeo. "
        return render(request, "data/show_images.html", {"error": error, "DH_id":DH_id, "project": project_id})

    if len(images) > len(p_images):
        p_images.extend([None]*(len(images)-len(p_images)))
        for i, j in zip(images, p_images):
            show_images.append([i,j])
    else:
        show_images = zip(images, p_images)
    return render(request, "data/show_images.html", {"images":show_images, "MEDIA_URL":settings.MEDIA_URL, "DH_id":DH_id, "project": project_id})

@login_required(login_url=settings.LOGIN_URL)
@api_view(["POST"])
@permission_required("DH_app.add_images")
def process_images(request):
    try:
        project_name= request.POST.get("project_id")
        if " " in project_name:
            project_id = project_name.replace(" ","_")
        else:
            project_id = project_name
        DH_name = request.POST.get("DH_id")
        if " "in DH_name:
            DH_id = DH_name.replace(" ","_")
        else:
            DH_id = DH_name
        path = create_directory (project_id, DH_id)

        model_path =os.path.join(settings.MEDIA_ROOT,"YOLO_models/default.pt") # Path al modelo
        if os.path.exists(model_path):
            pass
        else:
            error = "El modelo introducido no es válido."
            raise FileNotFoundError

        if not list_images(os.path.join(path,"images")):
            error = "No hay imágenes para este sondeo."
            raise FileNotFoundError
        else:
            process_imgs(path, model_path)
            images_path = os.path.join(path, "images")
            p_images_path = os.path.join(path, "processed_imgs")
            images = list_images(images_path)
            p_images= list_images(p_images_path)
            show_images = zip(images, p_images)
            return render(request, "data/show_images.html", {"images":show_images, "MEDIA_URL":settings.MEDIA_URL, "DH_id":DH_name, "project": project_name})
    
    except Exception as e:
        error_render= "Error al procesar las imágenes. "+ error
        # logging.ERROR(str(e))
        return render(request, "data/show_images.html", {"error":error_render})


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
@permission_required("DH_app.view_sample_model")
def show_samples(request):
    
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Sample_model.objects.filter(DH_id=sondeo).values()
        return render(request, "data/show_samples.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
@permission_required("DH_app.view_desv_model")
def show_deviations(request):
    
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Desv_model.objects.filter(DH_id=sondeo).values()
        return render(request, "data/show_desv.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)
    

@login_required(login_url=settings.LOGIN_URL)
@api_view(["GET"])
@permission_required("DH_app.view_lithos_dh")
def show_litho(request):
    if request.method == "GET":
        DH_id = request.GET.get("DH_id")
        sondeo = get_object_or_404(General_DH, DH_id=DH_id)
        data = Lithos_DH.objects.filter(DH_id=sondeo)
        return render(request, "data/show_litho.html", {"data": data, "DH_id": DH_id})
    else:
        return Response( status=status.HTTP_400_BAD_REQUEST)
    