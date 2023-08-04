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


from django.urls import path, include, re_path
from DH_app.data.views import *
from DH_app import views

urlpatterns = [
    re_path(r'^home/', views.home, name='home'),
    path ("accounts/", include('django.contrib.auth.urls')),
    # Registro de usuarios
    path ("register/", views.register , name = 'register'),
    # Crear nuevo proyecto
    path ("newProject/", create_project, name= "create_project"),
    # Borrar proyecto 
    path ("delete_project/", delete_project, name= 'delete_project'),
    # Mostrar proyectos
    path ("show_projects/", show_project, name= 'show_projects'),
    # Predilección sondeos
    path ("info_projects/", info_project, name= 'info_projects'),

    # Nuevo sondeo
    path("new_dh/", new_hole, name= 'new_hole'),
    # Seleccionar sondeo
    path("SelectData/", select_data, name = 'data_selection'),
    # Visualizar datos sondeo
    path("ShowData/", show_dh_data, name = 'dh_show_data'),
    # Modificar sondeo
    path("updateData/", update_data, name = 'update_data'),
    # borrar sondeo
    path("deleteData/", delete_data, name = 'delete_data'),



    # Importar imágenes
    path("import_images/", upload_imgs, name = 'upload_imgs'),
    # Ver imagenes del sondeo
    path("ShowImages/", show_images, name = 'show_images'),
    # Procesar imágenes
    path("ProcessImages/", process_images, name = 'process_images'),

    # Muestras
    path("import_samples/", import_samples, name = 'import_samples'),
    path("show_samples/", show_samples, name = 'show_samples'),
    # Desvíos
    path("import_deviations/", import_deviations, name = 'import_deviations'),
    path("show_deviations/", show_deviations, name = 'show_desv'),
    # Litologías
    path("import_litho/", import_litho, name = 'import_litho'),
    path("show_litho/", show_litho, name = 'show_litho'),




]