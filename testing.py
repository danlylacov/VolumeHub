from datetime import datetime

now = datetime.utcnow()

# Форматируем дату и время в требуемом формате
formatted_date = now.strftime('%Y-%m-%d %H:%M:%S%z+00:00')

print(formatted_date)