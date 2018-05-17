import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.db.utils import IntegrityError
from common import models

BASE_URL = 'https://esi.evetech.net/latest/'


def get_type(type_id):
    return requests.get(''.join(['https://esi.evetech.net/latest/universe/types/',
                                 str(type_id), '/'])).json()

def get_type_name(type_id):
    return get_type(type_id)['name']

def create_type_db():
    url_cats = BASE_URL + 'universe/categories/'
    cats = requests.get(url_cats).json()  # type: list
    for cat_id in cats:
        create_cat(cat_id)


def create_cat(cat_id):
    url_cat = ''.join([BASE_URL, 'universe/categories/', str(cat_id)])
    cat_info = requests_retry_session().get(url_cat).json()  # type: dict
    try:
        cat_model = models.Category.objects.create(id=cat_id,
                                                   name=cat_info['name'])
    except IntegrityError:
        print(str(cat_id), 'cat already exists')
        cat_model = models.Category.objects.get(id=cat_id)
    for group_id in cat_info['groups']:
        create_group(group_id, cat_model)

def create_group(group_id, cat_model):
    url_group = ''.join([BASE_URL, 'universe/groups/', str(group_id)])
    group_info = requests_retry_session().get(url_group).json()  # type: dict
    try:
        group_model = models.Group.objects.create(id=group_id,
                                                  name=group_info['name'],
                                                  category=cat_model)
    except IntegrityError:
        print(str(group_id), 'group already exists')
        group_model = models.Group.objects.get(id=group_id)
    for type_id in group_info['types']:
        create_type(type_id, group_model)

def create_type(type_id, group_model):
    url_group = ''.join([BASE_URL, 'universe/types/', str(type_id)])
    type_info = requests_retry_session().get(url_group).json()  # type: dict
    try:
        models.Type.objects.create(id=type_id, name=type_info['name'],
                                   group=group_model)
    except IntegrityError:
        print(str(type_id), 'type already exists')


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
