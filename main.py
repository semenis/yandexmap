import pygame
import requests
import sys
import os

def resize(spn, event):
    if event.type == pygame.KEYDOWN:
        global changed
        if event.key == pygame.K_PAGEUP:
            changed = True
            if spn * 1.8 > 90:
                spn = 90
            elif spn < 1:
                spn *= 3
            else:
                spn = spn * 1.8
        elif event.key == pygame.K_PAGEDOWN and spn*0.5 >= 0:
            changed = True
            if 0.01 < spn < 1:
                spn *= 0.1
            elif spn > 1:
                spn *= 0.5
            else:
                spn = 0.01
    print(spn)
    return spn

###GUI
class Label:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.font_color = pygame.Color("gray")
        # Рассчитываем размер шрифта в зависимости от высоты
        self.font = pygame.font.Font(None, self.rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)


class Button(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("blue")
        # при создании кнопка не нажата
        self.pressed = False

    def render(self, surface):
        surface.fill(self.bgcolor, self.rect)
        self.rendered_text = self.font.render(self.text, 1, self.font_color)
        if not self.pressed:
            color1 = pygame.Color("white")
            color2 = pygame.Color("black")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 5, centery=self.rect.centery)
        else:
            color1 = pygame.Color("black")
            color2 = pygame.Color("white")
            self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 7, centery=self.rect.centery + 2)

        # рисуем границу
        pygame.draw.rect(surface, color1, self.rect, 2)
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom),
                         2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
            if self.rect.collidepoint(event.pos):
                global changed
                global curr_sloy
                if sloy.index(self.text) < 2:
                    self.text = sloy[sloy.index(self.text) + 1]
                    curr_sloy = self.text
                    changed = True
                else:
                    self.text = sloy[0]
                    curr_sloy = self.text
                    changed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

class TextBox(Label):
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.active = True
        self.blink = True
        self.blink_timer = 0

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.execute()
            elif event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
            else:
                self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.active = self.rect.collidepoint(event.pos)

    def update(self):
                if pygame.time.get_ticks() - self.blink_timer > 200:
                    self.blink = not self.blink
                    self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
                super(TextBox, self).render(surface)
                if self.blink and self.active:
                    pygame.draw.line(surface, pygame.Color("black"),
                                     (self.rendered_rect.right + 2, self.rendered_rect.top + 2),
                                     (self.rendered_rect.right + 2, self.rendered_rect.bottom - 2))
####

spn = 25
lon, lat = 133.795384, -25.694768
sloy = ('map', 'sat', 'skl')
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
        print(lon, lat)
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)


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
            delta = lon - const_change * spn
        if key == pygame.K_DOWN:  #
            lat -= const_change * spn
            delta = "lat+"
        if key == pygame.K_LEFT:  #
            lon -= const_change * spn
            delta = lon + const_change * spn
        if key == pygame.K_UP:  #
            lat += const_change * spn
            delta = "lat-"

        global changed
        changed = True

    try:
        map_request(lon=lon, lat=lat)

    except:
        if type(delta) == float:
            lon = -(delta)

        elif type(delta) == str:
            if delta == "lat-":
                lat -= const_change * spn
            else:
                lat += const_change * spn
    finally:
        return lon, lat


response = map_request()

# Запишем полученное изображение в файл.
map_file = load_image()
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

gui = GUI()
b1 = Button((10, 65, 150, 80), sloy[0])
gui.add_element(b1)

const_change, key, pressed = 0.5, None, False
running = True
changed = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.get_event(event)
        spn = resize(spn, event)
        key, pressed = update_map(event, key, pressed)
    lon, lat = move(const_change, lon, lat, spn, key, pressed)

    if changed:
        if curr_sloy == 'skl':
            changed = False
            response = map_request(lon, lat, spn, 'sat')
            map_file = load_image()
            screen.blit(pygame.image.load(map_file), (0, 0))

        changed = False
        response = map_request(lon, lat, spn, curr_sloy)
        map_file = load_image()
        screen.blit(pygame.image.load(map_file), (0, 0))

    gui.render(screen)
    gui.update()
    pygame.display.flip()

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)