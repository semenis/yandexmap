import pygame
import requests
import sys
import os


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
                if sloy.index(self.text) < 2:
                    self.text = sloy[sloy.index(self.text) + 1]
                    global curr_sloy
                    curr_sloy = self.text
                    global changed
                    changed = True
                else:
                    self.text = sloy[0]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False


####

spn = 25
lon, lat = 133.795384, -25.694768
sloy = ('map', 'sat', 'skl')
curr_sloy = sloy[0]


def map_request():
    try:
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn), str(spn)]),
            "l": curr_sloy
        }
        response = requests.get(api_server, params=params)
        print(curr_sloy)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
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


response = map_request()

# Запишем полученное изображение в файл.
map_file = load_image()
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

gui = GUI()

b1 = Button((10, 65, 150, 80), sloy[0])

# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
gui.add_element(b1)
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()

running = True
changed = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        gui.get_event(event)

    if changed:
        changed = False
        response = map_request()
        map_file = load_image()
        screen.blit(pygame.image.load(map_file), (0, 0))

    gui.render(screen)
    gui.update()
    pygame.display.flip()

pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)
