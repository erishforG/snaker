# -*- coding: utf-8 -*-

#django
from django.contrib.auth.decorators import login_required

#rest
from rest_framework.decorators import api_view

#injector
from injector import Injector

#service
from shortner.service import tag_service

#global
injector = Injector()

tag_service = injector.get(tag_service.tag_service)

@login_required
@api_view(['GET'])
def tag_list_controller(request):
    if request.method == 'GET':
        page = request.GET['page']
        tags = request.GET['tags']

        return tag_service.get_tag_list(request, page, tags)