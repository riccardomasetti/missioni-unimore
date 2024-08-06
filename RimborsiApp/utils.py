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



from RimborsiApp.models import Spesa, SpesaMissione, Pasti


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

def migra_altre_spese():
    missioni = Missione.objects.all()

    for missione in missioni:
        if missione.altrespese:
            altre_spese = json.loads(missione.altrespese)
            for altrespese in altre_spese:
                if not altrespese.get("DELETE", False):
                    data = dt.strptime(altrespese["data"], '%Y-%m-%d').date()
                    importo = float(altrespese["s1"])
                    valuta = altrespese["v1"]
                    descrizione = altrespese.get("d1", "")

                    spesa = Spesa.objects.create(
                        data=data,
                        importo=importo,
                        valuta=valuta,
                        descrizione=descrizione
                    )

                    SpesaMissione.objects.create(
                        missione=missione,
                        spesa=spesa,
                        tipo="ALTRO"
                    )

def migra_convegni():
    missioni = Missione.objects.all()

    for missione in missioni:
        if missione.convegno:
            convegni = json.loads(missione.convegno)
            for convegno in convegni:
                if not convegno.get("DELETE", False):
                    data = dt.strptime(convegno["data"], '%Y-%m-%d').date()
                    importo = float(convegno["s1"])
                    valuta = convegno["v1"]
                    descrizione = convegno.get("d1", "")

                    spesa = Spesa.objects.create(
                        data=data,
                        importo=importo,
                        valuta=valuta,
                        descrizione=descrizione
                    )

                    SpesaMissione.objects.create(
                        missione=missione,
                        spesa=spesa,
                        tipo="CONVEGNO"
                    )

def migra_pasti():
    missioni = Missione.objects.all()

    for missione in missioni:
        if missione.scontrino:
            pasti = json.loads(missione.scontrino)
            for pasto in pasti:
                if not pasto.get("DELETE", False):
                    data = dt.strptime(pasto["data"], '%Y-%m-%d').date()
                    importo1 = float(pasto["s1"]) if pasto.get("s1") is not None else None
                    valuta1 = pasto.get("v1", "EUR")
                    descrizione1 = pasto.get("d1", "")

                    importo2 = float(pasto["s2"]) if pasto.get("s2") is not None else None
                    valuta2 = pasto.get("v2", "EUR")
                    descrizione2 = pasto.get("d2", "")

                    importo3 = float(pasto["s3"]) if pasto.get("s3") is not None else None
                    valuta3 = pasto.get("v3", "EUR")
                    descrizione3 = pasto.get("d3", "")

                    Pasti.objects.create(
                        missione=missione,
                        data=data,
                        importo1=importo1,
                        valuta1=valuta1,
                        descrizione1=descrizione1,
                        importo2=importo2,
                        valuta2=valuta2,
                        descrizione2=descrizione2,
                        importo3=importo3,
                        valuta3=valuta3,
                        descrizione3=descrizione3
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
    #migra_pernottamenti()
    #migra_convegni()
    #migra_altre_spese()
    migra_pasti()