import requests
import time
import json
import os
from sys import getdefaultencoding


ID_USER = 171691064
TOKEN = '98684d6dbee44f824e6b531181426e27295b6965a52e457fb62e9d2f94b97ba5a78d6b6083a65cebabb05'
GROUPS_GET = 'groups.get'
GROUPS_GET_MEMBERS = 'groups.getMembers'
GROUPS_GET_BY_ID = 'groups.getById'
FRIENDS_NUMBER = 0


def request(method, params):
    return requests.get(f'https://api.vk.com/method/{method}', params=params, verify=True)


def get_user_groups(user_id):
    params = dict(user_id=user_id, access_token=TOKEN, v=5.80)
    try:
        print("..\r")
        response = request(GROUPS_GET, params).json()['response']
        time.sleep(0.4)
    except Exception as except_error:
        print('Ошибка: {}'.format(except_error))
    else:
        return response


def get_name_groups(group_id):
    params = dict(group_id=group_id, access_token=TOKEN, v=5.80, fields='members_count')
    try:
        print("..\r")
        response = request(GROUPS_GET_BY_ID, params).json()['response']
        time.sleep(0.4)
    except Exception as except_error:
        print('Ошибка: {}'.format(except_error))
    else:
        for group in response:
            groups.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})
        return groups


def get_members_groups(my_groups, groups):
    for group in my_groups['items']:
        params = dict(group_id=group, access_token=TOKEN, v=5.80, filter='friends')
        try:
            response = request(GROUPS_GET_MEMBERS, params).json()['response']
            time.sleep(0.4)
        except Exception as except_error:
            print('Ошибка: {}'.format(except_error))
        else:
            if FRIENDS_NUMBER != 0:
                if response['count'] <= FRIENDS_NUMBER:
                    get_name_groups(group)
            else:
                if response['count'] == 0:
                    get_name_groups(group)
    return groups


def create_json(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "groups.json"), "w", encoding=getdefaultencoding()) as file:
        json.dump(data, file, ensure_ascii=False)


groups = []
print("Идет обработка запроса по пользователю: {}".format(ID_USER))
user_groups_id = get_user_groups(ID_USER)
get_members_groups(user_groups_id, groups)
create_json(groups)
print('Обработка завершена. Данные сохранены в файл: groups.json')
