# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from project.tuprofile.models import Profile

from django.views.generic.simple import direct_to_template

@csrf_exempt
def has_cert(request):
    response = HttpResponse()
    certlist = request.POST.get('certs',None)
    user = request.user

    if request.GET.get('auth_token'):
        user = Profile.objects.get(auth_key=request.GET['auth_token']).user

    if user.is_anonymous():
        response.content = 'not logged in!'
    elif certlist:
        certlist = json.loads(certlist)

        for certdata in certlist:
            if not Certificate.objects.find(user=user, **certdata):
                cert = Certificate.objects.create(user=user,**certdata)
        response.content = 'ok'
    else:
        response.content = json.dumps([x.__dict__ for x in Certificate.objects.filter(user=user)])
    response['Access-Control-Allow-Origin'] = '*'
    return response


def index(request):
    return direct_to_template(request, 'progress/index.html', {'user': request.user})

