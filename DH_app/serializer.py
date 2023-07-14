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


from DH_app.models import General_DH, Projects
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta ():
        model = Projects
        fields = ['project_name', 'comments']

class ImportSerializer (serializers.ModelSerializer):
    class Meta():
        model = General_DH
        fields = '__all__'

