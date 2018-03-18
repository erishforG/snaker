# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import redirect

#rest
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponseForbidden

#model
from session.models import *

#encryption
import base64

@api_view(['POST', 'GET'])
def login_controller(request):
    if request.method == 'POST':
        # user check
        test_user = user.objects.get(user_id=request.data['id'])

        if(test_user is not None) :
            if(base64.b64decode(test_user.password).decode() == request.data['password']) :
                request.session['admin_id'] = test_user.id
                request.session.set_expiry(0)
                return Response("login success", status=status.HTTP_200_OK)

        return Response("login fail", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'GET':
        return render(request, "login.html")

@api_view(['GET'])
def logout_controller(request):
    if not request.session.get('admin_id', None):
        return HttpResponseForbidden()

    if request.method == 'GET' :
        del request.session['admin_id']

        return redirect('login_controller')