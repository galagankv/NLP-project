#В модуле происходит предварительная очистка данных в csv-файле
#Раьбота с данными через объект DataFrame и List

import pandas as pd
import re

#указываем исходный csv файл. Вот тут хорошо бы сделать интерактивный выбор файла
src_csv_file = '/home/user/2019 год.csv'

df_msg = pd.read_csv(src_csv_file, sep=';', warn_bad_lines=True, error_bad_lines=False)

df_msg = df_msg.drop_duplicates().reset_index(drop=True)

msg_list = df_msg['Msg'].to_list()

out_list = []

first = 0
last = 0

print(df_msg.shape)
print('msg_list = ', len(msg_list))

#в цикле делаем замены в строках через регулярные выражения
for msg in msg_list:

    msg_out = str(msg)

    msg_out = re.sub(r'\[([^]]+)\]',' ',msg_out)

    msg_out = re.sub(r'@.+?\b',' ',msg_out)

    #msg_out = re.sub(r'#.+?\b', ' ', msg_out)

    msg_out = re.sub(r'\bhttp.+\b',' ', msg_out)

    msg_out = re.sub(r',|\.|!|\?|<|>', ' ', msg_out)

    msg_out = re.sub(r' +', ' ', msg_out)

    msg_out = re.sub(r'^\s+|\s+$', '', msg_out)

    print(msg_out)

    out_list.append(str(msg_out))

print('out_list = ', len(out_list))

df_msg.reset_index(drop=True)

df_msg['Msg'] = out_list

df_msg.dropna(inplace=True)

dst_csv_file = '/home/user/2019 год_корр.csv'

df_msg.to_csv(dst_csv_file, sep=';')