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


from django.shortcuts import render, redirect
from DH_app.form import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.http import HttpResponse

def home (request):
    return render(request,"home.html")

@require_http_methods(["GET", "POST"])
def register (request):
    if request.method == "GET":
        # Render registration form
        return render (request, "registration/register.html",{"form": CustomUserCreationForm })
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save() 
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get( "password1")
            user = authenticate( username = username, password = raw_password)
            login(request, user)
            return render(request,"home.html")
        
        else:
           err = form.errors.get_json_data()
           errors = [{k:[e["message"] for e in err[k]]} for k in err]
           return render(request,"registration/register_error.html", context={"errors":errors})
