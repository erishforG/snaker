import pytest

# database settings
from snaker import settings

#injector
from injector import Injector

#service
from shortner.service import shortener_service

#global
injector = Injector()

shortener_service = injector.get(shortener_service.shortener_service)


@pytest.fixture(scope='session')
def django_db_setup():
    settings

@pytest.mark.django_db
def test_get_url_list():
    response = shortener_service.get_url_list(None, 1, None)

    print (response)

    assert response.status_code == 200

@pytest.mark.django_db
def test_post_url_info():
    data = {'hash': 'N45i4', 'title': 'snaker', 'utm': '1', 'type': '0', 'description': '', 'show_redirection': '1', 'links[0][media_id]': '1', 'links[0][link]': '', 'links[1][media_id]': '2', 'links[1][link]': '', 'links[2][media_id]': '3', 'links[2][link]': '', 'size_of_links': '3'}
    response = shortener_service.post_url_info(data)

    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_url_info():
    data = {'id': '1'}
    response = shortener_service.delete_url_info(data)

    assert response.status_code == 200