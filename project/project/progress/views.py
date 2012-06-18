# Create your views here.
from django.http import HttpResponse
from models import Certificate
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from project.tuprofile.models import Profile
from decimal import *
from django.views.generic.simple import direct_to_template
from django.core import serializers

@csrf_exempt
def has_cert(request):
    response = HttpResponse()
    certlist = request.POST.get('certs',None)
    user = request.user

    try:
        if request.GET.get('auth_token'):
            user = Profile.objects.get(auth_key=request.GET['auth_token']).user

        if user.is_anonymous():
            response.content = 'not logged in!'
        elif certlist:
            certlist = json.loads(certlist)

            for certdata in certlist:
                if not certdata['ects']: # Verleihung des BSc-Grads, etc
                    continue
                certdata['semst'] = Decimal(certdata['semst'])
                certdata['ects'] = Decimal(certdata['ects'])
                if not Certificate.objects.filter(user=user, **certdata):
                    cert = Certificate.objects.create(user=user,**certdata)
            response.content = 'ok'
        else:
            response.content = serializers.serialize('json', Certificate.objects.filter(user=user))
    except Exception, e:
        import traceback
        response.content = str(e) + '\n' + traceback.format_exc()
    response['Access-Control-Allow-Origin'] = '*'
    return response


def index(request):
    return direct_to_template(request, 'progress/index.html', {'user': request.user})

