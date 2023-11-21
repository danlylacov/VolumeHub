from datetime import datetime

# Пример строки с датой и временем
date_string = '2024-02-20 00:43:09.772115'

# Задайте формат строки (с миллисекундами)
date_format = '%Y-%m-%d %H:%M:%S.%f'

# Преобразуйте строку в объект datetime
date_object = datetime.strptime(date_string, date_format)

print(date_object)