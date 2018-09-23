# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

#rest
from rest_framework import status
from rest_framework.response import Response

#rest
from rest_framework.decorators import api_view

#injector
from injector import Injector

#service
from shortner.service import shortener_service, tag_service

#global
injector = Injector()

shortener_service = injector.get(shortener_service.shortener_service)

@login_required
@api_view(['GET'])
def url_list_controller(request):
    if request.method == 'GET':
        page = int(request.GET.get("page"))
        tags = request.GET.get("tags")

        return shortener_service.get_url_list(request, page, tags)

@login_required
@api_view(['GET'])
def url_list_download_controller(request):
    if request.method == 'GET':
        return shortener_service.download_url_list(request)

@api_view(['GET', 'PUT', 'DELETE'])
def url_change_controller(request, hash):
    if request.method == 'GET':
        return shortener_service.redirect_url(request, hash)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return shortener_service.put_url_info(request)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return shortener_service.delete_url_info(request)

@api_view(['GET'])
def url_iframe_controller(request, hash):
    if request.method == 'GET':
        return shortener_service.redirect_iframe_url(request, hash)

@login_required
@api_view(['GET', 'POST'])
def url_list_tag_controller(request):
    if request.method == 'GET':
        id = request.GET['id']

        return tag_service.get_url_tag(id)

    elif request.method == 'POST':
        id = request.data["id"]
        tag = request.data["tag"]

        return tag_service.post_url_tag(id, tag)

@login_required
@api_view(['GET'])
def url_detail_controller(request, hash):
    if request.method == 'GET':
        return shortener_service.get_url_info(request, hash)

@login_required
@api_view(['GET'])
def daily_source_controller(request, hash):
    if request.method == 'GET':
        return shortener_service.download_daily_source(request, hash)

@login_required
@api_view(['POST', 'GET'])
def url_create_controller(request):
    if request.method == 'POST':
        return shortener_service.post_url_info(request)

    elif request.method == 'GET':
        return shortener_service.get_url_info_page(request)
