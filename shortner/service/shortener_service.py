# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseForbidden, HttpResponse

#log
import sys
import traceback

#hash
import math
import random

#time
import pytz
import datetime

#rest
from rest_framework import status
from rest_framework.response import Response

#graph
from graphos.renderers.gchart import PieChart
from graphos.sources.model import ModelDataSource

#user agent
from user_agents import parse

#model
from snaker import settings
from shortner.models import *

#excel
import xlsxwriter
import os

#injector
from injector import inject

class shortener_service:
    @inject
    def __init__(self):
        pass

    def get_url_list(self, request, page, tags):
        urls = None
        last_page = int(url.objects.count() / 20) + 1

        if tags is not None and page is not None:
            tag_query_str = self._tags_to_query_str(tags)
            tmp_url = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url WHERE tags LIKE "' + tag_query_str + '" ORDER BY id DESC')

            urls_range = "{} , {}".format((int(page) - 1) * 20, 20)
            urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url WHERE tags LIKE "' + tag_query_str + '" ORDER BY id DESC LIMIT ' + urls_range)

            last_page = int(len(list(tmp_url)) / 20) + 1

        if page is None and tags is None:
            try:
                urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url ORDER BY id DESC')
            except Exception as e:
                print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print(''.join('* ' + line for line in lines))

        if page is not None:
            try:
                urls_range = "{} , {}".format((page - 1) * 20, 20)
                urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url ORDER BY id DESC LIMIT ' + urls_range)
            except Exception as e:
                print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print(''.join('* ' + line for line in lines))

        if tags is not None:
            try:
                tag_query_str = self._tags_to_query_str(tags)
                urls = url.objects.raw(
                    'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url WHERE tags LIKE "' + tag_query_str + '" ORDER BY id DESC')
            except Exception as e:
                print('- url_list_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print(''.join('* ' + line for line in lines))

        return render(request, 'url_list.html', {'urls': urls, 'page': page, 'last_page': last_page, 'list_range': self._url_list_range(page, last_page)})

    def download_url_list(self, request):
        try:
            urls = url.objects.raw(
                'SELECT *, (SELECT count(1) FROM analytics WHERE url_id = url.id) AS count FROM url ORDER BY id DESC')

            self._create_urls_excel(urls)

            file_path = os.path.join(settings.BASE_DIR, '{}_urls.xlsx'.format(datetime.date.today()))
            filename = os.path.basename(file_path)

            with open(file_path, 'rb') as f:
                response = HttpResponse(f, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                os.remove(file_path)
                return response

        except Exception as e:
            print('- url_list_download GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def redirect_url(self, request, hash):
        try :
            rows = url.objects.filter(hash=hash).values()
            result_url = rows[0]

            links = url_link.objects.raw('SELECT *, (SELECT name FROM media WHERE id = url_link.media_id) as mediaName FROM url_link WHERE url_id = ' + str(result_url['id']))

            if result_url is not None:
                #user agent
                ua_string = request.META['HTTP_USER_AGENT']
                user_agent = parse(ua_string)

                insert_analytics = analytics(url_id=result_url['id'], created_at=datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')), os=user_agent.os.family, browser=user_agent.browser.family, device=user_agent.device.family, referer=request.META.get('HTTP_REFERER'))
                insert_analytics.save()

                if result_url['title'] is not None:
                    result_url['title'] = settings.BASE_TITLE

                for link in links :
                    if user_agent.os.family in link.mediaName and link.link:
                        result_url['long_url'] = link.link

                if '://' not in result_url['long_url']:
                    result_url['long_url'] = 'http://' + result_url['long_url']

                if result_url['show_utm'] == 1:
                    if '?' in result_url['long_url']:
                        result_url['long_url'] = result_url['long_url'] + '&' + settings.UTM
                    else :
                        result_url['long_url'] = result_url['long_url'] + '?' + settings.UTM

                print('- url_change_controller GET ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                print(result_url['long_url'])

                if result_url['type'] == 1:
                    return render(request, 'url_link.html', result_url)

                if result_url['show_redirection'] == 0:
                    #redirect
                    return redirect(result_url['long_url'])
                elif result_url['show_redirection'] == 1:
                    #link_redirect
                    return render(request, 'url_link_redirect.html', result_url)
            else :
                return Response("cannot add log to db", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print('- url_change_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def post_url_info(self, request):
        try:
            rows = url.objects.filter(hash=request.data['hash']).values()

            if rows and rows[0] :
                return Response("the hash already exists", status=status.HTTP_409_CONFLICT)
            else :
                if int(request.data['size_of_links']) > 0 :
                    url.objects.create(hash=request.data['hash'], long_url=request.data['links[0][link]'], title=request.data['title'], type=request.data['type'], description=request.data['description'], show_utm=request.data['utm'], show_redirection=request.data['show_redirection'], created_at=datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')))
                    inserted_url = url.objects.get(hash=request.data['hash'])

                    for i in range(int(request.data['size_of_links'])):
                        url_link.objects.create(link=request.data['links[' + str(i) + '][link]'], created_at=datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')), media_id=int(request.data['links[' + str(i) + '][media_id]']), url_id=int(inserted_url.id))

                    return Response("succeed to generate url", status=status.HTTP_200_OK)
                else :
                    return Response("failed to generate url links", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print('- url_create_controller POST error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def put_url_info(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        try:
            rows = url.objects.filter(hash=request.data['hash']).values()

            if rows and rows[0] and str(rows[0]['id']) != str(request.data['id']) :
                return Response("the hash already exists", status=status.HTTP_409_CONFLICT)
            else :
                url_link.objects.filter(url_id=request.data['id']).all().delete()

                for i in range(int(request.data['size_of_links'])):
                    url_link.objects.create(link=request.data['links[' + str(i) + '][link]'], created_at=datetime.datetime.now(tz=pytz.timezone('Asia/Seoul')), media_id=int(request.data['links[' + str(i) + '][media_id]']), url_id=int(request.data['id']))

                save_url = url.objects.get(id=int(request.data['id']))
                save_url.hash = request.data['hash']
                save_url.long_url = request.data['links[0][link]']
                save_url.title = request.data['title']
                save_url.type = request.data['type']
                save_url.show_utm = request.data['utm']
                save_url.description = request.data['description']
                save_url.show_redirection = request.data['show_redirection']
                save_url.save()

                return Response("succeed to modify url", status=status.HTTP_200_OK)
        except Exception as e:
            print('- url_change_controller PUT error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def delete_url_info(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        try:
            rows = url.objects.filter(hash=hash).values()
            if rows and rows[0] and str(rows[0]['id']) != str(request.data['id']) :
                return Response("the hash already exists", status=status.HTTP_409_CONFLICT)
            else :
                #count delete
                count.objects.filter(url_id=request.data['id']).all().delete()

                #analytics delete
                analytics.objects.filter(url_id=request.data['id']).all().delete()

                #url link delete
                url_link.objects.filter(url_id=request.data['id']).all().delete()

                #url delete
                url.objects.get(id=int(request.data['id'])).delete()

                return Response("succeed to modify url", status=status.HTTP_200_OK)
        except Exception as e:
            print('- url_change_controller DELETE error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def get_url_info(self, request, hash):
        try:
            rows = url.objects.filter(hash=hash).values()

            result_data = {}

            if rows:
                # get url
                result_url = rows[0]

                if result_url is not None:
                    # links
                    result_links = media.objects.raw(
                        'SELECT *, (SELECT name FROM media WHERE id = url_link.media_id) as mediaName FROM url_link WHERE url_id = ' + str(
                            result_url['id']))

                    # count
                    result_sum = analytics.objects.filter(url_id=str(result_url['id'])).count()
                    result_count = analytics.objects.raw(
                        'SELECT *, count(1) AS result FROM count WHERE url_id = ' + str(
                            result_url['id']) + ' GROUP BY count')
                    result_count_per_date = analytics.objects.raw(
                        'SELECT *, count(1) AS count, DATE(CONVERT_TZ(created_at, \'UTC\',\'Asia/Seoul\')) AS date, count(case when referer like "%%facebook%%" then 1 end) as facebook FROM analytics WHERE url_id = ' + str(
                            result_url[
                                'id']) + ' GROUP BY DATE(CONVERT_TZ(created_at, \'UTC\',\'Asia/Seoul\'))')

                    for count in result_count_per_date:
                        temp_count = {}
                        temp_count['date'] = count.created_at
                        temp_count['result'] = count.count
                        print(str(temp_count))

                    # analytics
                    result_analytics = {}
                    result_analytics['referer'] = analytics.objects.raw(
                        "SELECT *, count(1) as count, SUBSTR(referer, 1 , IF(LOCATE('/', referer, 9), LOCATE('/', referer, 9)-1, LENGTH(referer))) as urlHost FROM analytics WHERE url_id = " + str(
                            result_url['id']) + " GROUP BY urlHost ORDER BY count DESC")

                    # graph
                    os_query = analytics.objects.raw(
                        'SELECT *, count(1) as count FROM analytics WHERE url_id = ' + str(
                            result_url['id']) + ' GROUP BY os ORDER BY count DESC')
                    browser_query = analytics.objects.raw(
                        'SELECT *, count(1) as count FROM analytics WHERE url_id = ' + str(
                            result_url['id']) + ' GROUP BY browser ORDER BY count DESC')

                    temp_os_data = ModelDataSource(os_query, fields=['os', 'count'])
                    temp_browser_data = ModelDataSource(browser_query, fields=['browser', 'count'])

                    result_analytics['os'] = PieChart(temp_os_data)
                    result_analytics['browser'] = PieChart(temp_browser_data)

                    # media
                    result_media = media.objects.all()

                    # mapping
                    result_data['url'] = result_url
                    result_data['links'] = result_links
                    result_data['sum'] = result_sum
                    result_data['counts'] = result_count
                    result_data['analytics'] = result_analytics
                    result_data['countsPerDate'] = result_count_per_date
                    result_data['medias'] = result_media

            return render(request, 'url_info.html', result_data)
        except Exception as e:
            print('- url_detail_controller GET error ' + str(
                datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def redirect_iframe_url(self, request, hash):
        rows = url.objects.filter(hash=hash).values()
        result_url = rows[0]

        links = url_link.objects.raw('SELECT *, (SELECT name FROM media WHERE id = url_link.media_id) as mediaName FROM url_link WHERE url_id = ' + str(result_url['id']))

        if result_url is not None:
            # user agent
            ua_string = request.META['HTTP_USER_AGENT']
            user_agent = parse(ua_string)

            if result_url['title'] is not None:
                result_url['title'] = settings.BASE_TITLE

            if 'http://' not in result_url['long_url'] and 'https://' not in result_url['long_url']:
                result_url['long_url'] = 'http://' + result_url['long_url']

            for link in links:
                if user_agent.os.family in link.mediaName:
                    result_url['long_url'] = link.link

            if result_url['show_utm'] == 1:
                if '?' in result_url['long_url']:
                    result_url['long_url'] = result_url['long_url'] + '&' + settings.UTM
                else:
                    result_url['long_url'] = result_url['long_url'] + '?' + settings.UTM

            print('- url_iframe_controller GET ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            print(result_url['long_url'])

        return render(request, 'url_referer.html', result_url)

    def download_daily_source(self, request, hash):
        try:
            rows = url.objects.filter(hash=hash).values()
            # get url
            result_url = rows[0]

            result_count_per_date = analytics.objects.raw(
                'SELECT *, count(1) AS count, DATE(CONVERT_TZ(created_at, \'UTC\',\'Asia/Seoul\')) AS date, count(case when referer like "%%facebook%%" then 1 end) as facebook FROM analytics WHERE url_id = ' + str(
                    result_url['id']) + ' GROUP BY DATE(CONVERT_TZ(created_at, \'UTC\',\'Asia/Seoul\'))')

            self._create_daily_source_excel(result_count_per_date)

            filepath = os.path.join(settings.BASE_DIR, '{}_daily.xlsx'.format(datetime.date.today()))
            filename = os.path.basename(filepath)  # 파일명만 반환

            with open(filepath, 'rb') as f:
                response = HttpResponse(f, content_type='application/vnd.ms-excel')
                # 필요한 응답헤더 세팅
                response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                os.remove(filepath)
                return response

        except Exception as e:
            print('- url_list_download GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(''.join('* ' + line for line in lines))

    def get_url_info_page(self, request):
            try :
                # media
                result_media = media.objects.all()

                # mapping
                request_data = {}

                request_data['hash'] = self._create_hash(4, 6)
                request_data['medias'] = result_media

                return render(request, 'url_create.html', request_data)
            except Exception as e:
                print('- url_create_controller GET error ' + str(datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))))
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print(''.join('* ' + line for line in lines))

    def _create_hash(self, min_length, max_length):
        # generate hash
        if min_length <= 1:
            min_random = 0
        else:
            min_random = math.pow(74, min_length - 1)

        max_random = math.pow(74, max_length - 1)
        result_random = math.floor(random.random() * (max_random - min_random) + min_random)

        return self._value_to_string(int(result_random))

    def _value_to_string(self, value):
        x = value % 74
        y = math.floor(value / 74)

        if y > 0 :
            return self._value_to_string(int(y)) + self._value_to_char(int(x))
        else :
            return self._value_to_char(int(x))

    def _value_to_char(self, value):
        asciiDec = 48 + value

        if asciiDec > 57 and asciiDec < 65: # : ~ @
            asciiDec += 7
        elif asciiDec > 90 and asciiDec < 97:
            asciiDec += 6
        elif asciiDec > 122 :
            asciiDec -= 5

        print(asciiDec)

        return chr(asciiDec)

    def _url_list_range(self, current, last):
        if current < 3:
            return [n for n in range(1, 6)]
        elif last <= current + 2:
            return [n for n in range(last - 4, last + 1)]
        else:
            return [n for n in range(current - 2, current + 3)]


    def _create_urls_excel(self, raw_data):
        urls_array = []
        for data in raw_data:
            url = [
                data.id,
                'http://' + settings.BASE_URL + '/' + data.hash,
                data.title,
                data.count,
                data.created_at.strftime('%Y-%m-%d')
            ]
            urls_array.append(url)
        columns = [
            {'header': 'ID'},
            {'header': 'URL'},
            {'header': 'Title'},
            {'header': 'Count'},
            {'header': 'Date'}
        ]

        self._list_to_excel(urls_array, columns, "urls")

    def _create_daily_source_excel(self, raw_data):
        daily_sources = []
        for data in raw_data:
            daily_source = [
                data.date.strftime('%Y-%m-%d'),
                data.count,
                data.facebook
            ]
            daily_sources.append(daily_source)
        columns = [
            {'header': 'Date'},
            {'header': 'Count'},
            {'header': 'Facebook'}
        ]

        self._list_to_excel(daily_sources, columns, "daily")

    def _list_to_excel(self, array, columns=[], title=""):
        workbook = xlsxwriter.Workbook('{}_{}.xlsx'.format(datetime.date.today(), title))
        worksheet = workbook.add_worksheet()

        last_column = ''
        try:
            last_column = str(unichr(64 + len(columns)))
        except:
            last_column = 'E'
        row_count = str(len(array) + 1)

        worksheet.add_table('A1:'+last_column+row_count, {'data': array, 'columns': columns})

        workbook.close()

    def _tags_to_query_str(self, tags):
        tags_str = "%%"
        arr = tags.split(",")
        for i in arr:
            tags_str += i + "%%"

        return tags_str