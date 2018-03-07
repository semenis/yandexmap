import pygame
import requests
import sys
import os

spn = 25
lon, lat = 133.795384, -25.694768
sloy = ("map", "sat", "skl")
curr_sloy = sloy[0]

def map_request(lon=lon, lat=lat, spn=spn, map=curr_sloy):
    try:
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn), str(spn)]),
            "l": map
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
        print(lon,lat)
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


def update_map(event, key, pressed):
    if event.type == pygame.KEYDOWN:
        if event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]:
            key = event.key
            pressed = True
    if event.type == pygame.KEYUP:
        if event.key in [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]:
            key = None
            pressed = False
    return key, pressed


def move(const_change, lon, lat, spn, key, pressed):
    delta = None
    if pressed:
        if key == pygame.K_RIGHT:  #
            lon += const_change * spn
            delta = "lon+"
        if key == pygame.K_DOWN:  #
            lat -= const_change * spn
            delta = lat
        if key == pygame.K_LEFT:  #
            lon -= const_change * spn
            delta = "lon-"
        if key == pygame.K_UP:  #
            lat += const_change * spn
            delta = lat

    try:
        map_request(lon=lon, lat=lat)

    except:
        if type(delta) == float:
            lat = -lat
        elif type(delta) == str:
            if delta == "lon-":
                lon += const_change * spn
            else:
                lon -= const_change * spn
    finally:
        return lon, lat



pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
response = map_request()
map_file = load_image()

# Переключаем экран и ждем закрытия окна.
running = True
vistrels = []

const_change, key, pressed = 0.3, None, False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        key, pressed = update_map(event, key, pressed)
    lon, lat = move(const_change, lon, lat, spn, key, pressed)
    print(lon, lat)
    response = map_request(lon, lat)
    map_file = load_image()

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
