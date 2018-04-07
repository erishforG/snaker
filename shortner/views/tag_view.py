# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

#rest
from rest_framework.decorators import api_view

#time
import pytz
import datetime

#log
import sys
import traceback

@login_required
@api_view(['GET'])
def tag_list_controller(request):
    if request.method == 'GET':
        # tag 존재 할 경우 태그 필터링 ex) WHERE tags LIKE "%4%"
        # page 존재 할 경우 결과값 범위 설정 ex) LIMIT 20,40
        # tag & page 존재 할 경우 태그 필터링한 값을 페이징 ex) WHERE tags LIKE "%1,3,4%" LIMIT 20,40

        page = request.GET['page']
        tags = request.GET['tags']

        # 태그 & page 존재
        if tags is not None and page is not None:
            tag_query_str = tags_to_query_str(tags)
            urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count'
                    'FROM url WHERE tags'
                    'LIKE "%' + tag_query_str + '%" ORDER BY id DESC'
            )
            last_page = int(urls.count() / 20) + 1
            return render(request, 'url_list.html', {'urls': urls, 'page': None, 'last_page': last_page,
                                                         'list_range': url_list_range(page, last_page)})


        if page is None: # 전체
            try:
                request.GET['tags']
                tag_query_str = tags_to_query_str(tags)
                urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url WHERE tags LIKE "%' + tag_query_str + '%" ORDER BY id DESC')
                last_page = int(url.objects.count() / 20) + 1
                return render(request, 'url_list.html', {'urls': urls, 'page': None, 'last_page': last_page,
                                                         'list_range': url_list_range(page, last_page)})
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
                                                     'list_range': url_list_range(page, last_page)})
        except Exception as e:
            print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))


def url_list_range(current, last):
    if current < 3:
        return [n for n in range(1, 6)]
    elif last <= current + 2:
        return [n for n in range(last - 4, last + 1)]
    else:
        return [n for n in range(current - 2, current + 3)]


def tags_to_query_str(categories):
    tags_str = "%"
    for i in categories.split(","):
        tags_str += i + "%"

    return tags_str

