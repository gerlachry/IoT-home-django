import logging
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template.defaulttags import register
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from elasticsearch import Elasticsearch, client

from auto.localsettings import ES_HOST, ES_PORT
from elastic_helpers import readings_helper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

es_helper = readings_helper.Readings()

@register.filter
def get_item(dictionary, key):
    """
    filter to use in html tags for looking up a dictionary value for a key
    """
    return dictionary.get(key)

@login_required
def home(request, template_name="base.html"):
    context = RequestContext(request)
    print request.GET.get('device_name')
    context['data'] = Feeds.get(Feeds(), request).data
    print context['data']
    return render_to_response(template_name, context)

@login_required
def about(request, template_name="iotdata/about.html"):
    context = RequestContext(request)
    #TODO: add in a service to gather high level stats from weather, switches, and video feeds
    context['data'] = ['device01', 'device02']
    return render_to_response(template_name, context)


@login_required
def overview(request, template_name="iotdata/overview.html"):
    context = RequestContext(request)
    #TODO: add in a service to gather all the weather data in some paginated fashion along with a most recent reading object
    #context['recent'] = {'temperature': '67', 'timestamp': '30-DEC-2015 15:03:00', 'humidity': '33'}
    #setattr(request, )
    #context['recent'] = es_helper.get(size=1, device_name='esp8266_001')
    # context['history'] = [{'temperature': '66', 'timestamp': '30-DEC-2015 15:03:00', 'humidity': '33'},
    #                       {'temperature': '67', 'timestamp': '30-DEC-2015 14:03:00', 'humidity': '33'},
    #                       {'temperature': '64', 'timestamp': '30-DEC-2015 13:03:00', 'humidity': '33'},
    #                       {'temperature': '64', 'timestamp': '30-DEC-2015 12:03:00', 'humidity': '33'}]
    # print context
    context['basement_temperature'] = es_helper.get(25, 'basement_temperature')
    context['basement_humidity'] = es_helper.get(25, 'basement_humidity')
    return render(request, template_name, context=context)


@login_required
def analysis(request, template_name="iotdata/analysis.html"):
    context = RequestContext(request)
    return render_to_response(template_name, context)


class Feeds(APIView):
    """API for handling sensor reading feeds which in turn index to elasticsearch
        Token authentication is required for this API
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    #parser_classes = (JSONParser, )
    SIZE = 1

    def __init__(self):
        self.log = logging.getLogger('Readings')

    def post(self, request):
        """
        index sensor data to Elastic based on the data query_param json formatted
            requires url parameters feed_name
        """
        print request
        return es_helper.post(request)

    def get(self, request):
        """
        retrieve most recent sensor readings for a given feed_name
        """
        self.log.debug('request : %s ' % request.query_params)
        try:
            query_param = request.query_params
            self.log.info(query_param)
        except Exception, ex:
            self.log.error('error fetching query_params %s' % ex, exc_info=True, extra={'request': request})
        if not query_param:
            #query_param['device_name'] = 'esp8266_001t'
            return Response('Missing required query parameters refer to api documentation', status=status.HTTP_400_BAD_REQUEST)
        if 'size' in query_param:
            size = query_param['size']
        else:
            size = self.SIZE
        return es_helper.get(self.SIZE, query_param['feed_name'])