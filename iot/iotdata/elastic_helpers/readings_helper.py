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

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
idx_client = client.IndicesClient(es)


class Readings():
    SIZE = 100

    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        """index sensor data to Elastic based on the data query_param json formatted"""
        try:
            query_param = request.query_params
            self.log.info(query_param)
        except Exception, ex:
            self.log.error('error in query_params %s' % ex, exc_info=True, extra={'request': request})
        data_param = json.loads(query_param['data'])
        #index will be device name
        if 'device_name' in data_param:
            idx = data_param['device_name']
            data_param['timestamp'] = datetime.datetime.now()
            if not idx_client.exists(idx):
                setup_index(idx, 'sensor', None)
            self.log.info('writing to index %s data %s' % (idx, data_param))
            resp = es.index(index=idx, doc_type='sensor', id=None,  body=data_param)
            self.log.info('Indexing resp %s' % resp)
            return Response(resp)
        else:
            content = {'error': 'missing required device_name'}
            self.log.error('request missing required device_name query param', exc_info=True, extra={'request': request})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """retrieve most recent sensor readings for a given device"""
        try:
            query_param = request.query_params
            print query_param
            self.log.info(query_param)
        except Exception, ex:
            self.log.error('error in query_params %s' % ex, exc_info=True, extra={'request': request})
        if 'device_name' in query_param:
            device_name = query_param['device_name']
        else:
            self.log.error('no device_name provided', exc_info=True, extra={'request': request})
            return Response({'error': 'missing required device name'}, status=status.HTTP_400_BAD_REQUEST)
        if 'size' in query_param:
            size = query_param['size']
        else:
            size = self.SIZE
        query_string = {"query": {
            "match_all": {}
            },
            "size": size,
            "sort":  [
                {
                  "timestamp": {
                    "order": "desc"
                  }
                }
            ]
        }
        self.log.info(query_string)
        results = es.search(index=device_name, body=query_string, size=size)
        self.log.info(results['hits'])
        return Response(results['hits'])


def setup_index(index, doc_type, mappings):
    """create index"""
    resp = es.indices.create(index, ignore=400)
    #resp = es.indices.put_mapping(index=index, doc_type=doc_type, body=mappings)
    logging.log(logging.INFO, 'index created response %s' % resp)
    if 'acknowledged' in resp:
        if resp['acknowledged'] <> True:
            return False
        else:
            return True
    else:
        return False

