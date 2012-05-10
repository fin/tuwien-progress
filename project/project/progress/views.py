# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json

def has_cert(request):
    try:
        certlist = request.POST['certs']
        certlist = json.loads(certlist)

        for certdata in certlist:
            cert = Certificate.objects.create(**certdata)
    except Exception, e:
        response.data = 'lol'
    return response
