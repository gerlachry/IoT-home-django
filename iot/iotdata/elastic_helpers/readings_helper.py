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
from iotdata import models
from iotdata.models import Feed

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
idx_client = client.IndicesClient(es)


class Readings():

    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        """
        index sensor data to Elastic based on the data query_param json formatted
        """
        try:
            query_param = request.query_params
            self.log.info(query_param)
            data_param = json.loads(query_param['data'])
        except Exception, ex:
            self.log.error('error in query_params %s' % ex, exc_info=True, extra={'request': request})
        #index will be feed name and document type will be the feed type from metadata
        if 'feed_name' in data_param:
            idx = data_param['feed_name']
            data_param['timestamp'] = datetime.datetime.now()
            doc_type = get_feed_type(idx)
            if not doc_type:
                self.log.error('feed_name %s has no feed_type please set one up via admin console', idx, exc_info=True, extra={'request': request})
                return Response({'error': 'setup feed_type'}, status=status.HTTP_400_BAD_REQUEST)
            if not idx_client.exists(idx):
                self.log.info("creating index %s" % idx)
                setup_index(idx, 'sensor', None)
            self.log.info('writing to index %s data %s' % (idx, data_param))
            resp = es.index(index=idx, doc_type='sensor', id=None,  body=data_param)
            self.log.info('Indexing resp %s' % resp)
            #TODO: check for success in response from ES
            return Response(resp)
        else:
            content = {'error': 'missing required feed_name parameter'}
            self.log.error('request missing required feed_name query param', exc_info=True, extra={'request': request})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get(self, size=1, feed_name=None):
        """
        retrieve sensor readings for a given device
        """
        if not feed_name:
            #TODO: logic for getting all device names and last 10 readings from each one
            #self.log.error('no device_name provided', exc_info=True, extra={'request': request})
            #return Response({'error': 'missing required device name'}, status=status.HTTP_400_BAD_REQUEST)
            device_name = 'esp8266_001t'
            #devices = models.Device.objects.all
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
        self.log.debug(query_string)
        results = es.search(index=feed_name, body=query_string, size=size)
        self.log.debug(results)
        return results['hits']['hits']


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


def get_feed_type(feed_name):
    """lookup the feed_type for a given feed_name"""
    feed = Feed.objects.filter(feed_name=feed_name)
    if feed.exists and len(feed) == 1:
        print feed[0].feed_type
        return feed[0].feed_type
    else:
        return None