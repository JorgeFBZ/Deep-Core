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


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

'''
Validador de cuadricula UTM del modelo General_DH
'''
utm_zones = ['1N', '1S', '2N', '2S', '3N', '3S', '4N', '4S', '5N', '5S', '6N', '6S', '7N', '7S',
                '8N', '8S', '9N', '9S', '10N', '10S', '11N', '11S', '12N', '12S', '13N', '13S', '14N',
                '14S', '15N', '15S', '16N', '16S', '17N', '17S', '18N', '18S', '19N', '19S', '20N',
                '20S', '21N', '21S', '22N', '22S', '23N', '23S', '24N', '24S', '25N', '25S', '26N',
                '26S', '27N', '27S', '28N', '28S', '29N', '29S', '30N', '30S', '31N', '31S', '32N', 
                '32S', '33N', '33S', '34N', '34S', '35N', '35S', '36N', '36S', '37N', '37S', '38N',
                '38S', '39N', '39S', '40N', '40S', '41N', '41S', '42N', '42S', '43N', '43S', '44N',
                '44S', '45N', '45S', '46N', '46S', '47N', '47S', '48N', '48S', '49N', '49S', '50N',
                '50S', '51N', '51S', '52N', '52S', '53N', '53S', '54N', '54S', '55N', '55S', '56N', 
                '56S', '57N', '57S', '58N', '58S', '59N', '59S', '60N', '60S']

def UTM_Validator(form_input):
    if form_input not in utm_zones:
        raise ValidationError(
            _('%(Zone)s is not a correct UTM Zone'),
            params={'Zone': form_input},)
