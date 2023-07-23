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


from django.db import models
from django.core import validators
from DH_app.custom_validators import UTM_Validator

def image_directory_path(instance, filename):
    print (25*"==")
    print (f"{str(instance.project_id)}/{filename}")
    return f"{str(instance.project_id)}/{filename}"

# Modelo de datos de Proyectos
class Projects(models.Model):
    project_name = models.CharField(primary_key=True,max_length=100, unique=True, help_text="Name of the project", blank=False, null=False)
    comments = models.TextField(max_length=1000, help_text="Description of the project", blank= True)
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        db_table = "DH_app_projects"
  
    def __str__(self):
        return self.project_name


# Modelo de datos para los datos del sondeo
class General_DH(models.Model):
    ID = models.AutoField(primary_key=True, unique=True, help_text="Unique ID for the database management.")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, blank=False, null=False)
    DH_id = models.CharField(max_length=200, unique=True, help_text="Drillhole name.")
    start_date = models.DateField(help_text="Start date")
    end_date = models.DateField(help_text="Finalization date")
    teo_azimuth = models.FloatField(max_length=10, help_text="Theorical azimuth of the drillhole",
                validators=[validators.MinValueValidator(0), validators.MaxValueValidator(360)]) 
    teo_incl = models.FloatField(max_length=10, help_text="Theorical inclination of the drillhole", 
                validators=[validators.MinValueValidator(-90), validators.MaxValueValidator(90)]) 
    real_azimuth = models.FloatField(max_length=10, help_text="Real azimuth of the drillhole", 
                    validators=[validators.MinValueValidator(0),  validators.MaxValueValidator(360)]) 
    real_incl = models.FloatField(max_length=10, help_text="Real inclination of the drillhole", 
                validators=[validators.MinValueValidator(-90), validators.MaxValueValidator(90)]) 
    UTM_Zone = models.CharField(max_length=3, validators=[UTM_Validator])
    northing = models.FloatField(max_length=15, help_text="North coordinate of the collar.",
                                validators=[validators.MinValueValidator(0)])
    easting = models.FloatField(max_length= 15, help_text="Easting coordinate of the collar.",
                                validators=[validators.MinValueValidator(0)])
    elevation = models.FloatField(max_length=10, help_text="Elevation of the collar.")

    class Meta:
        verbose_name = "Sondeo"
        verbose_name_plural = "Sondeos"
        db_table = "DH_app_General_DH"



# Modelo de datos para las muestras
class Sample_model (models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    DH_id = models.ForeignKey(General_DH, on_delete=models.CASCADE)
    From = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])
    To = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])
    # Añadir los elementos analizados
    element_1 = models.FloatField(max_length=5,blank=True, null=True,
                                validators=[validators.MinValueValidator(0)])
    element_2 = models.FloatField(max_length=5,blank=True, null=True,
                                validators=[validators.MinValueValidator(0)])
    
    class Meta:
        verbose_name = "Muestra"
        verbose_name_plural = "Muestras"
        db_table = "DH_app_Sample_model"

# Modelo de datos para los desvios
class Desv_model (models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    DH_id = models.ForeignKey(General_DH, on_delete=models.CASCADE)
    From = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])
    To = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])

    inclination = models.FloatField(max_length=5,blank=True, null=True,
                                validators=[validators.MaxValueValidator(90),
                                            validators.MinValueValidator(-90)])
    azimuth = models.FloatField(max_length=10,blank=True, null=True, 
                                validators=[validators.MinValueValidator(0),
                                            validators.MaxValueValidator(360)]) 
    class Meta:
        verbose_name = "Desviación"
        verbose_name_plural = "Desviaciones"
        db_table = "DH_app_Desv_model"

class Images (models.Model):
    ID = models.AutoField(primary_key=True, unique=True)
    DH_id = models.ForeignKey(General_DH, on_delete=models.CASCADE, blank=False, null=False)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    Images = models.FileField(blank=False)

# Modelo de datos para el índice de litologias (Solo Admin)
class Lithos(models.Model):
    Litho = models.CharField(unique=True, max_length=500)
    Litho_label = models.CharField(unique=True, primary_key=True, max_length=10)
    Description = models.CharField(blank=True, max_length=1000)
    
    class Meta:
        verbose_name = "Litología"
        verbose_name_plural = "Litologías"
        db_table = "DH_app_Lithos"

# Modelo de datos para las litologias de los sondeos
class Lithos_DH(models.Model):
    ID = models.AutoField(unique=True, primary_key=True)
    DH_id = models.ForeignKey(General_DH, on_delete=models.CASCADE, blank=False, null=False)
    From = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])
    To = models.FloatField(max_length=10,blank=False, null=False,
                                validators=[validators.MinValueValidator(0)])
    Litho_label = models.ForeignKey(Lithos, on_delete=models.CASCADE, blank=False, null=False)

    class Meta:
        verbose_name = "Litología sondeo"
        verbose_name_plural = "Litologías sondeos"
        db_table = "DH_app_Lithos_DH"
