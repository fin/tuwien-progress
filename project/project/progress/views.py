# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
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
    response['Access-Control-Allow-Origin'] = '*'
    return response
