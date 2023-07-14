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

import os, shutil
from django.conf import settings

def create_directory(project,DH=None):
    if DH:
        try:
            folder_path =os.path.join(settings.MEDIA_ROOT,str(project),str(DH))
            os.makedirs(folder_path)
            # Crear directorios para las imagenes e imagenes procesadas
            os.makedirs(os.path.join(folder_path, "images"))
            os.makedirs(os.path.join(folder_path, "processed_imgs"))
        except FileExistsError:
            pass
    else:
        try:
            folder_path =os.path.join(settings.MEDIA_ROOT,str(project))
            os.makedirs(folder_path)
        except FileExistsError:
            pass
    return folder_path

def delete_directory(project, DH=None):
    if DH:
        folder_path =os.path.join(settings.MEDIA_ROOT,str(project),str(DH))
    else:
        folder_path =os.path.join(settings.MEDIA_ROOT,str(project))
    shutil.rmtree(folder_path, ignore_errors=True)
