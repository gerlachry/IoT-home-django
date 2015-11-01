from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from auto.localsettings import ES_HOST, ES_PORT
import json
import logging

logging.basicConfig(level=logging.INFO)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)

class Readings(APIView):
    """API for handling sensor reading feeds which in turn index to elasticsearch
        Token authentication is required for this API
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        json_data = json.loads(request.body)
        #index will be device name
        idx = json_data['device_name']
        self.log.info('writing to index %s data %s' % (idx, json_data))
        resp = es.index(index=idx, doc_type='sensor', id=None,  body=json_data)
        self.log.info('Indexing resp %s' % resp) 
        return Response(resp)

    def get(self, request):
        results = 'all is ok'
        return Response(results)
        

