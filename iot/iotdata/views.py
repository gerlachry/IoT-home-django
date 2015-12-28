import logging
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from elasticsearch import Elasticsearch, client

from auto.localsettings import ES_HOST, ES_PORT
from elastic_helpers import readings_helper

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
idx_client = client.IndicesClient(es)

@login_required
def home(request, template_name="base.html"):
    context = RequestContext(request)
    # qset = Study.objects.all()
    # if request.GET.get('nct', False):
    #     qset = qset.exclude(nctid=None)
    # if request.GET.get('prefix', None):
    #     prefix = request.GET['prefix']
    #     qset = qset.filter(study_id__startswith=prefix)
    #     context['prefix'] = prefix
    #
    # context['studies'] = qset
    return render_to_response(template_name, context)


class Readings(APIView):
    """API for handling sensor reading feeds which in turn index to elasticsearch
        Token authentication is required for this API
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    #parser_classes = (JSONParser, )
    es_helper = readings_helper.Readings()

    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        """index sensor data to Elastic based on the data query_param json formatted"""
        return self.es_helper.post(request)

    def get(self, request):
        """retrieve most recent sensor readings for a given device"""
        return self.es_helper.get(request)