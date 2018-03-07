import pygame
import requests
import sys
import os

def resize(spn, event):
    print(spn)
    if event.key == pygame.K_PAGEUP and spn < 90:
        spn += 10
    elif event.key == pygame.K_PAGEDOWN and spn > 0:
        spn -= 5
    return spn

spn = 25

response = None
try:
    map_request = "http://static-maps.yandex.ru/1.x/?ll=133.795384,-25.694768&spn={0},{0}&l=sat".format(str(spn))
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
except:
    print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
try:
    with open(map_file, "wb") as file:
        file.write(response.content)
except IOError as ex:
    print("Ошибка записи временного файла:", ex)
    sys.exit(2)
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
import random
running = True
vistrels = []
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            spn = resize(spn, event)
            response = None
            try:
                map_request = "http://static-maps.yandex.ru/1.x/?ll=133.795384,-25.694768&spn={0},{0}&l=sat".format(
                    str(spn))
                response = requests.get(map_request)

                if not response:
                    print("Ошибка выполнения запроса:")
                    print(map_request)
                    print("Http статус:", response.status_code, "(", response.reason, ")")
                    sys.exit(1)
            except:
                print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
                sys.exit(1)

            # Запишем полученное изображение в файл.
            map_file = "map.png"
            try:
                with open(map_file, "wb") as file:
                    file.write(response.content)
            except IOError as ex:
                print("Ошибка записи временного файла:", ex)
                sys.exit(2)
            screen.blit(pygame.image.load(map_file), (0, 0))
            # Переключаем экран и ждем закрытия окна.
            pygame.display.flip()

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)