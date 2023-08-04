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


'''
Funciones para el procesado de las imágenes por el modelo de Deep Learning
'''
import torch, os
import ultralytics
import cv2 as cv
from ultralytics import YOLO
import logging

def process_imgs(folder_path, model_path):
    # ultralytics.checks()
    images_path = os.path.join(folder_path, "images")
    p_images_path = os.path.join(folder_path, "processed_imgs")
    imgs = []
    imgs_name =[]
    processed_imgs = [img for img in os.listdir(p_images_path)]
    for img in os.listdir(images_path):
        if img not in processed_imgs:
            imgs.append(os.path.join(images_path,img))
            imgs_name.append(os.path.split(img)[-1])
    model = YOLO(model_path)
    results = model(imgs)

    for img, result in zip(imgs_name,results):
        res_plotted = result.plot()
        res_plotted = cv.imwrite(f"{p_images_path}/processed_{img}", res_plotted) # Linux
        #res_plotted = cv.imwrite(f"{p_images_path}\processed_{img}", res_plotted) # Windows
'''
Listar imágenes de una carpeta
'''
def list_images(folder):
    images = []
    for image in os.listdir(folder):
        img_path =os.path.join(folder, image).split("/Deep-Core/media/")[-1] # Linux
        #img_path =os.path.join(folder, image).split("\media")[-1] # Windows
        images.append(img_path)
    return images