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


from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Projects)
class Projects_admin(admin.ModelAdmin):
    list_display = ("project_name","comments")

@admin.register(General_DH)
class DH_admin(admin.ModelAdmin):
    list_display = ("ID", "DH_id","project","teo_azimuth", "teo_incl")

@admin.register(Desv_model)
class Desv_model_admin(admin.ModelAdmin):
    list_display = ("DH_id", "From", "To", "inclination", "azimuth")

@admin.register(Sample_model)
class Sample_model_admin(admin.ModelAdmin):
    list_display = ("DH_id", "From", "To", "element_1", "element_2")

@admin.register(Lithos)
class Lithos_admin(admin.ModelAdmin):
    list_display = ("Litho", "Litho_label","Description")

@admin.register(Lithos_DH)
class Lithos_DH_admin(admin.ModelAdmin):
    list_display = ("DH_id", "From", "To", "Litho_label")