#В модуле реализована работа с внешним REST API
#Из целеввого каталога берутся файлы с данными
#Готовые данные записываются в новый файл

import json
import requests
import pandas as pd
import os


def api_request(msg, token):
    payload = {'c': 'keywords',
               'query': msg,
               'top': 10,
               'pos': 'NOUN, VERB',
               'expand': 0,
               'mwe': 0,
               'forms': 0,
               'clusters': 0,
               'format': 'json',
               'lang': 'ru',
               'token': token}
    r = requests.post('http://paraphraser.ru/api/',
                      data=payload)

    result = r.json()

    if result['code'] == 0:
        response = result['response']
        # print(msg)
        return response

    else:
        print('Error:', result['msg'])


r = requests.post('http://paraphraser.ru/token/',
                  data={'login': 'galagankv', 'password': '19750119'})
token = r.json().get('token', '')

# хотим перебрать файлы

scr_directory = '/home/user/2019/'
out_directory = '/home/user/2019_keywords/'

files = os.listdir(scr_directory)

#отбираем только csv файлы
csv_files = filter(lambda x: x.endswith('.csv'), files)

for csv_file in csv_files:

    #т.к. мы зависим от внешнего API, что бы не потерять всю обработанную информацию, заворачиваем в попытку-исключение
    try:
        print('Source: ' + scr_directory + str(csv_file))

        #считываем файл игнорируя ошибочные строки
        df_msg = pd.read_csv(scr_directory + str(csv_file), sep=';', warn_bad_lines=True, error_bad_lines=False)

        df_msg = df_msg.drop_duplicates().reset_index(drop=True)

        msg_list = df_msg['Msg'].to_list()

        df_json = pd.DataFrame(columns=('Msg', 'Keywords'))

        for msg in msg_list:

            msg = str(msg)

            if len(msg) == 0:
                continue

            print(len(msg.split()))

            if len(msg.split()) >= 10: #считаем сообщения короче 10 слов неинформативными
                if len(msg) <= 2000: #тексты более 2000 символов не обрабатываем - ограничение API

                    response = api_request(msg, token)

                    for item in response:

                        value_txt = ''

                        for value in response[item]:
                            value_txt = value_txt + value + ','

                        df_json.loc[len(df_json)] = [msg, value_txt]

        # df_json.to_csv(out_directory + str(csv_file.replace('.csv', '')) + '_keyword.csv', sep=';')
        # print('Done: ' + out_directory + str(csv_file.replace('.csv', '')) + '_keyword.csv')

    except Exception as ex:
        print(ex)
    finally:
        df_json.to_csv(out_directory + str(csv_file.replace('.csv', '')) + '_keyword.csv', sep=';')
        print('Done: ' + out_directory + str(csv_file.replace('.csv', '')) + '_keyword.csv')

