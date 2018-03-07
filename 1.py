import pygame
import requests
import sys
import os

def resize(spn, event):
    if event.key == pygame.K_PAGEUP:
        if spn * 1.8 > 90:
            spn = 90
        elif spn < 1:
            spn *= 3
        else:
            spn = spn * 1.8
    elif event.key == pygame.K_PAGEDOWN and spn*0.5 >= 0:
        if 0.01 < spn < 1:
            spn *= 0.1
        elif spn > 1:
            spn *= 0.5
        else:
            spn = 0.01
    print(spn)
    return spn


spn = 25
lon, lat = 133.795384, -25.694768


def map_request():
    try:
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn), str(spn)]),
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

# Запишем полученное изображение в файл.
def load_image():
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


def move(event, const_change, lon, lat, key, pressed):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]:
            key = event.key
            pressed = True
    if event.type == pygame.KEYUP:
        if event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]:
            key = None
            pressed = False

    if pressed:
        if key == pygame.K_RIGHT:  #
            lat += const_change

        if key == pygame.K_DOWN:  #
            lon -= const_change

        if key == pygame.K_LEFT:  #
            lat -= const_change

        if key == pygame.K_UP:  #
            lon += const_change
    return lon, lat, key, pressed


# Инициализируем pygame


pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
response = map_request()
map_file = load_image()

# Переключаем экран и ждем закрытия окна.
running = True
vistrels = []

const_change, key, pressed = 0.1, None, False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and (lon, lat, key, pressed) == move(event,const_change, lon, lat, key, pressed):
            spn = resize(spn, event)
        else:
            lon, lat, key, pressed = move(event, const_change, lon, lat, key, pressed)
        print(lon, lat)
    response = map_request()
    map_file = load_image()

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)