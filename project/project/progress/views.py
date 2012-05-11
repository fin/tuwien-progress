# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json

def has_cert(request):
    response = HttpResponse()
    try:
        certlist = request.POST['certs']
        certlist = json.loads(certlist)

        for certdata in certlist:
            cert = Certificate.objects.create(**certdata)
        response.body = 'ok'
    except Exception, e:
        response.body = 'lol'
    return response
