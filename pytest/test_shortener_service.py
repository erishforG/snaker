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

    assert response.status_code == 200