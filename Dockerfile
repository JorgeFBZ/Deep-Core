# Django web app to manage and store drillhole data.
# Copyright (C) 2023 Jorge Fuertes Blanco

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

FROM python:3.9-slim-buster
ENV PYTHONBUFFERED=1
WORKDIR /django
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get install libgl1-mesa-glx
COPY . .
CMD ["python3", "manage.py", "migrate"]