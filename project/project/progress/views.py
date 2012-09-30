# Create your views here.
from django.http import HttpResponse
from models import Certificate, Curriculum
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from project.tuprofile.models import Profile
from decimal import *
from django.views.generic.simple import direct_to_template
from django.core import serializers
import pprint
import copy


@csrf_exempt
def cert(request):
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
                query = dict([(str(k), v,) for k,v in certdata.iteritems() if (k in ['lvatype', 'lvano']) ])

                create = dict([(str(k), v,) for k,v in certdata.iteritems()])
                if not Certificate.objects.filter(user=user, **query):
                    cert = Certificate.create(user=user,**create)
            response.content = 'ok'
        else:
            response.content = serializers.serialize('json', Certificate.objects.filter(user=user))
    except Exception, e:
        import traceback
        response.content = str(e) + '\n' + traceback.format_exc()
    response['Access-Control-Allow-Origin'] = '*'
    return response

def curriculum(request, pk):
    c = Curriculum.objects.get(pk=pk)
    user = request.user
    if not user.is_anonymous():
        x = c.decorate(Certificate.objects.filter(user=user))
    return direct_to_template(request, 'progress/curriculum.html', {'user': request.user, 'curriculum': x})

def index(request):
    return direct_to_template(request, 'progress/index.html', {'user': request.user, 'curriculums': Curriculum.objects.all()})

def certificate(request, id):
    pass

