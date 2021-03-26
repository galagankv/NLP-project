#модуль для разбивки большого csv-файла на несколько частей

import pandas as pd

#указываем исходный csv файл. Вот тут хорошо бы сделать интерактивный выбор файла
src_csv_file = '/home/user/2019 год_корр.csv'

df_msg = pd.read_csv(src_csv_file, sep=';', warn_bad_lines=True, error_bad_lines=False)

#исключаем дубликаты строк, пересчитываем индексы
df_msg = df_msg.drop_duplicates().reset_index(drop=True)

min_index = 0

#задаем количество строк в целевом файле
delta = 100

max_index = len(df_msg.index)

template_csv_file = '/home/user/2019/2019_'

#разделяем файл
while min_index <= max_index:

    #вырезаем нужное количество строк из исходного датафрейма
    df_out = df_msg.iloc[min_index:min(min_index + delta, max_index)]

    print(df_out)

    df_out.to_csv(template_csv_file + str(min_index) + '_' + str(min(min_index + delta, max_index)) + '.csv', sep=';')

    min_index = min_index + delta