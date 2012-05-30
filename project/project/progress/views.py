# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.simple import direct_to_template

@csrf_exempt
def has_cert(request):
    response = HttpResponse()
    certlist = request.POST.get('certs',None)
    if request.user.is_anonymous():
        response.content = 'not logged in!'
    elif certlist:
        certlist = json.loads(certlist)

        for certdata in certlist:
            if not Certificate.objects.find(user=request.user, **certdata):
                cert = Certificate.objects.create(user=request.user,**certdata)
        response.content = 'ok'
    else:
        response.content = json.dumps([x.__dict__ for x in Certificate.objects.filter(user=request.user)])
    response['Access-Control-Allow-Origin'] = '*'
    return response


def index(request):
    return direct_to_template(request, 'progress/index.html', {'user': request.user})

