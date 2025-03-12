import numpy.random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

from pandas.io.clipboard import lazy_load_stub_copy
from unicodedata import category


def find_common_prefix(strings):
    if not strings:
        return ""
    prefix = strings[0]
    for s in strings[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]  # Уменьшаем длину префикса
            if not prefix:
                return ""
    return prefix

print('Задание №1')

nums = numpy.random.normal(0,1,1000)
plt.hist(nums,bins=20)
plt.title("Гистограмма по 1000 случайных чисел")
plt.xlabel("Значение")
plt.ylabel("Количество")
plt.grid(True)
plt.show()

print('Задание №2')
nums_x = np.random.rand(5)
nums_y = np.random.rand(5)
plt.scatter(nums_x,nums_y)
plt.title("Диаграмма рассеивания из 5 пар случайных чисел")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


print('Задание №3')

df = pd.read_csv('divanparser.csv', encoding='utf-8')
first_col = df.columns[0]
last_col = df.columns[-1]
#print(f'Объем памяти по столбцам: {df.memory_usage(deep=True)}')
start_mem = df.memory_usage(deep=True).sum()
print(f'Общий объем занятой памяти после загрузки датафрейма: {start_mem}')
df[first_col] = df[first_col].str.replace(r'^.+/category/|/page-\d+','',regex=True)
#print(f'Объем памяти по столбцам: {df.memory_usage(deep=True)}')
print(f'Общий объем занятой памяти после очистки категорий: {df.memory_usage(deep=True).sum()}')
df[first_col] = df[first_col].astype('category')
#print(f'Объем памяти по столбцам: {df.memory_usage(deep=True)}')
print(f'Общий объем занятой памяти после преобразования столбца в категориальный тип: {df.memory_usage(deep=True).sum()}')
print(f'Всего категорий: {df[first_col].cat.categories}')
prefix = find_common_prefix(df[last_col].tolist())
print(f'Общее начало ссылки: {prefix}')
df[last_col] =  df[last_col].str.replace('^'+prefix,'',regex=True)
final_mem = df.memory_usage(deep=True).sum()
print(f'Общий объем занятой памяти после оптимизаций: {final_mem}\nОсвобождено: {start_mem-final_mem}\nИли {round((start_mem-final_mem)*100/start_mem)}%')

categ = round(df.groupby(first_col, observed=True)["price"].mean())
categ.index.name = "Категории"
print(categ)
for cat in df[first_col].cat.categories:
    category = df[df[first_col] == cat]
    category.reset_index(inplace=True)
    category.hist(column="price", bins=10, color = "green", edgecolor = "black")
    plt.title(f'Распределение цен по категории {cat}')
    plt.xlabel('Цена')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.show()


pass