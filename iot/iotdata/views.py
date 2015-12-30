import logging
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaulttags import register
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from elasticsearch import Elasticsearch, client

from auto.localsettings import ES_HOST, ES_PORT
from elastic_helpers import readings_helper

logging.basicConfig(level=logging.DEBUG)

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
idx_client = client.IndicesClient(es)

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
    context['data'] = Readings.get(Readings(), request).data
    print context['data']
    return render_to_response(template_name, context)

@login_required
def overview(request, template_name="iotdata/overview.html"):
    context = RequestContext(request)
    #TODO: add in a service to gather high level stats from weather, switches, and video feeds
    context['data'] = ['device01', 'device02']
    return render_to_response(template_name, context)


@login_required()
def weather(request, template_name="iotdata/weather.html"):
    context = RequestContext(request)
    #TODO: add in a service to gather all the weather data in some paginated fashion along with a most recent reading object
    context['recent'] = {'temperature': '67', 'timestamp': '30-DEC-2015 15:03:00', 'humidity': '33'}
    context['history'] = [{'temperature': '66', 'timestamp': '30-DEC-2015 15:03:00', 'humidity': '33'},
                          {'temperature': '67', 'timestamp': '30-DEC-2015 14:03:00', 'humidity': '33'},
                          {'temperature': '64', 'timestamp': '30-DEC-2015 13:03:00', 'humidity': '33'},
                          {'temperature': '64', 'timestamp': '30-DEC-2015 12:03:00', 'humidity': '33'}]
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
        print request
        return self.es_helper.post(request)

    def get(self, request):
        """retrieve most recent sensor readings for a given device"""
        return self.es_helper.get(request)