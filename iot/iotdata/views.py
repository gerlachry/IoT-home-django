import logging

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from elasticsearch import Elasticsearch, client
from rest_framework.parsers import JSONParser
from localsettings import ES_HOST, ES_PORT
import json
import datetime

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
idx_client = client.IndicesClient(es)


class Readings(APIView):
    """API for handling sensor reading feeds which in turn index to elasticsearch
        Token authentication is required for this API
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    #parser_classes = (JSONParser, )

    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        """wanted to use POST and the body be the json but could not get the stream from the arduino wifi client to work so sending data as query_param"""
        try:
            query_param = request.query_params
            self.log.info(query_param)
        except Exception, ex:
            self.log.info('error in query_params %s' % ex)
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
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        results = 'all is ok'
        return Response(results)
        

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
