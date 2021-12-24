#список всех полученых постов
name = "https://www.instagram.com/nike/"

#разбиваем ссылку по слешу и получаем нужную нам часть
file_name = name.split(("/"))[-2]
print(file_name)

