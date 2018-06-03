# -*- coding: utf-8 -*-

#django
from django.shortcuts import render
from django.http import JsonResponse

#time
import pytz
import datetime

#rest
from rest_framework import status
from rest_framework.response import Response

#log
import sys
import traceback

#model
from shortner.models import *

#injector
from injector import inject

class tag_service:
    @inject
    def __init__(self):
        pass

    def get_tag_list(self, request, page, tags):
        # tag 존재 할 경우 태그 필터링 ex) WHERE tags LIKE "%4%"
        # page 존재 할 경우 결과값 범위 설정 ex) LIMIT 20,40
        # tag & page 존재 할 경우 태그 필터링한 값을 페이징 ex) WHERE tags LIKE "%1,3,4%" LIMIT 20,40

        # 태그 & page 존재
        if tags is not None and page is not None:
            tag_query_str = self._tags_to_query_str(tags)
            urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count'
                    'FROM url WHERE tags'
                    'LIKE "%' + tag_query_str + '%" ORDER BY id DESC'
            )
            last_page = int(urls.count() / 20) + 1
            return render(request, 'url_list.html', {'urls': urls, 'page': None, 'last_page': last_page,
                                                         'list_range': self._url_list_range(page, last_page)})

        if page is None: # 전체
            try:
                tag_query_str = self._tags_to_query_str(tags)
                urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url WHERE tags LIKE "%' + tag_query_str + '%" ORDER BY id DESC')
                last_page = int(url.objects.count() / 20) + 1
                return render(request, 'url_list.html', {'urls': urls, 'page': None, 'last_page': last_page,
                                                         'list_range': self._url_list_range(None, last_page)})
            except Exception as e:
                print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print(''.join('* ' + line for line in lines))

        try:    # 페이지 네이션
            page = int(page)  # sql 쿼리는 0부터 시작
            urls_range = "{} , {}".format((page - 1) * 20, 20)
            last_page = int(url.objects.count() / 20) + 1
            urls = url.objects.raw(
                'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url ORDER BY id DESC LIMIT ' + urls_range)
            return render(request, 'url_list.html', {'urls': urls, 'page': page, 'last_page': last_page,
                                                     'list_range': self._url_list_range(page, last_page)})
        except Exception as e:
            print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def get_url_tag(request, id):
        try:
            get_url = url.objects.get(id=id)
            result_data = {}
            if get_url:
                result_data["id"] = str(get_url.id)
                result_data["tags"] = get_url.tags

                return JsonResponse(result_data)
            else:
                return Response("failed to get url ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print('- url_detail POST error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def post_url_tag(request, id, tag):
        try:
            save_url = url.objects.get(id=id)

            if save_url:
                arr = []
                if save_url.tags is not None:
                    arr = save_url.tags.split(",")

                if tag in arr:
                    arr.remove(tag)
                else:
                    arr.append(tag)
                arr.sort()

                if len(arr):
                    save_url.tags = ','.join(str(x) for x in arr)
                else:
                    save_url.tags = None
                save_url.save()

                updated_data = {"id":id, "tags":save_url.tags}
                return JsonResponse(updated_data)
            else:
                return Response("failed to get url ", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print('- url_detail POST error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def _url_list_range(self, current, last):
        if current < 3:
            return [n for n in range(1, 6)]
        elif last <= current + 2:
            return [n for n in range(last - 4, last + 1)]
        else:
            return [n for n in range(current - 2, current + 3)]


    def _tags_to_query_str(self, categories):
        tags_str = "%"
        for i in categories.split(","):
            tags_str += i + "%"

        return tags_str

