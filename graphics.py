import pygame


class GUI:
    """
    Класс-контейнер для GUI элементов
    """
    def __init__(self):
        self.elements = []

    def add_element(self, element):  # добавить элемент
        self.elements.append(element)

    def render(self, surface): # отрисовать элемент
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self): # обновить элемент
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):  # передать событие элементу
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                element.get_event(event)


class Label:
    """
    Класс-табличка.
    """
    def __init__(self, rect, text, text_color=pygame.Color('black'), background_color=pygame.Color('white'),
                 font_size=None, x=None, y=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.text_color = text_color
        self.background_color = background_color
        self.x = self.rect.x + 2 if x is None else x
        self.y = self.rect.y + 2 if y is None else y
        if font_size is None:
            # Calculating the font's size
            self.font = pygame.font.Font("fonts/6551.ttf", self.rect.height - 4)
        else:
            self.font = pygame.font.Font("fonts/6551.ttf", font_size)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):
        if self.background_color == -1:
            surface.fill(pygame.Color("black"), self.rect)
        else:
            surface.fill(self.background_color, self.rect)

        # Отрисовка текста
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = self.x, self.y
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 1, self.text_color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width - 100:
                    x = self.x  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = self.x  # Reset the x.
            y += word_height  # Start on new row.


class Button(Label):
    """
    Класс кнопки.
    """
    def __init__(self, rect, text):
        super().__init__(rect, text)
        self.font_color = pygame.Color('black')
        self.bgcolor = pygame.Color("blue")
        # при создании кнопка не нажата
        self.pressed = False
        self.illumination = False  # подсвечивание

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
        pygame.draw.line(surface, color2, (self.rect.right - 1, self.rect.top), (self.rect.right - 1, self.rect.bottom), 2)
        pygame.draw.line(surface, color2, (self.rect.left, self.rect.bottom - 1),
                         (self.rect.right, self.rect.bottom - 1), 2)
        # выводим текст
        surface.blit(self.rendered_text, self.rendered_rect)
        if self.illumination:
            temp_s = pygame.Surface((self.rect.width, self.rect.height))
            temp_s.set_alpha(190)  # устанавливаем прозрачность
            temp_s.fill(pygame.Color('lightblue'))
            surface.blit(temp_s, (self.rect.x, self.rect.y))

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False
        elif event.type == pygame.MOUSEMOTION:  # если мышь движется
            if self.rect.collidepoint(event.pos):  # и попадает в область кнопки
                self.illumination = True  # подсветка кнопки
            else:
                self.illumination = False


class TextBox(Label):
    """
    Класс-поле для ввода текста.
    """
    def __init__(self, rect, text, max_len=None):
        super().__init__(rect, text)
        self.active = True
        self.blink = True
        self.blink_timer = 0
        self.cursor_index = 0 if text == "" else len(text)
        self.max_len = None if max_len is None else max_len

    def get_event(self, event):
        # сложные штуки тут, но все понятно
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if len(self.text) > 0:
                    self.text = self.text[:self.cursor_index - 1] + self.text[self.cursor_index:]
                    self.cursor_index -= 1
            elif event.key == pygame.K_LEFT:
                if self.cursor_index >= 1:
                    self.cursor_index -= 1
            elif event.key == pygame.K_RIGHT:
                if self.cursor_index < len(self.text):
                    self.cursor_index += 1
            else:
                if self.max_len is None:
                    if self.font.render(self.text[:self.cursor_index] + event.unicode + self.text[self.cursor_index:],
                                        1, self.text_color).get_rect(x=self.rect.x + 2,
                                                                     centery=self.rect.centery).width <= self.rect.width:
                        self.text = self.text[:self.cursor_index] + event.unicode + self.text[self.cursor_index:]
                        self.cursor_index += 1
                else:
                    if len(self.text[:self.cursor_index] + event.unicode +
                                   self.text[self.cursor_index:]) <= self.max_len:
                        self.text = self.text[:self.cursor_index] + event.unicode + self.text[self.cursor_index:]
                        self.cursor_index += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)

    def update(self):
        # мигание курсора
        if pygame.time.get_ticks() - self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pygame.time.get_ticks()

    def render(self, surface):
        super(TextBox, self).render(surface)
        self.rendered_text = self.font.render(self.text[:self.cursor_index], 1, self.text_color)
        self.rendered_rect = self.rendered_text.get_rect(x=self.rect.x + 2, centery=self.rect.centery)
        if self.blink and self.active:
            pygame.draw.line(surface, pygame.Color("black"),
                             (self.rendered_rect.right, self.rendered_rect.top + 2),
                             (self.rendered_rect.right, self.rendered_rect.bottom - 2))
