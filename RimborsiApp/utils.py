from wsgiref.util import FileWrapper
import os
import mimetypes
import re
import requests
import sys
import json
sys.path.append('/home/administrator/missioni-unimore')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Rimborsi.settings")
import django
django.setup()
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from sendfile import sendfile
from RimborsiApp.models import ModuliMissione, Missione
from django.utils.encoding import smart_str
from datetime import datetime as dt                 #avoiding conflicts



from RimborsiApp.models import Spesa, SpesaMissione


def migra_pernottamenti():
    missioni = Missione.objects.all()

    for missione in missioni:
        if missione.pernottamento:
            pernottamenti = json.loads(missione.pernottamento)
            for pernottamento in pernottamenti:
                if not pernottamento.get("DELETE", False):
                    data = dt.strptime(pernottamento["data"], '%Y-%m-%d').date()
                    importo = float(pernottamento["s1"])
                    valuta = pernottamento["v1"]
                    descrizione = pernottamento.get("d1", "")

                    spesa = Spesa.objects.create(
                        data=data,
                        importo=importo,
                        valuta=valuta,
                        descrizione=descrizione
                    )

                    SpesaMissione.objects.create(
                        missione=missione,
                        spesa=spesa,
                        tipo="PERNOTTAMENTO"
                    )


def get_prezzo_carburante():
    # Set the URL you want to webscrape from
    url = 'https://dgsaie.mise.gov.it/prezzi_carburanti_settimanali.php?lang=it_IT'
    # Connect to the URL
    response = requests.get(url)
    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    prezzo = soup.find('table', class_="table table-sm table-borderless").findAll(
        'tr', class_="bg-light")[0].find('strong').text
    prezzo = re.sub('\.+', '', prezzo)
    prezzo = re.sub(',+', '.', prezzo)
    prezzo = float(prezzo) / 1000

    return prezzo

@login_required
def download(request, id, field):
    missione = get_object_or_404(Missione, pk=id)
    moduli_missione = missione.modulimissione
    if not moduli_missione.is_user_allowed(request.user):
        return HttpResponseForbidden('Sorry, you cannot access this file')

    file = getattr(moduli_missione, field)
    filename = file.name.split('/')[1]
    wrapper = FileWrapper(file.open())

    type = mimetypes.guess_type(filename)[0]
    response = HttpResponse(wrapper, content_type=type)
    response['Content-Length'] = os.path.getsize(file.path)
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    return response


if __name__ == "__main__":
    migra_pernottamenti()