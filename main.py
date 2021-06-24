import pygame
from graphics import *
from weather import *
import sys


# Инициализация pygame, основные параметры.
pygame.init()
width, height = 500, 700
size = width, height
screen = pygame.display.set_mode(size)


def terminate():
    """
    Заверешение работы.
    """
    pygame.quit()
    sys.exit()


def city_info(city):
    """
    Вывод информации о городе.
    """
    # gui элементы
    gui = GUI()
    rendered_weather = Label((0, 0, 20, 20), get_current_weather(city), pygame.Color('black'), pygame.Color("lightblue"))
    rendered_forecast = Label((0, 120, 20, 20), get_forecast_weather(city), pygame.Color('black'), pygame.Color("lightblue"))
    back = Button((400, 650, 80, 30), "Back")
    gui.add_element(back)
    gui.add_element(rendered_weather)
    gui.add_element(rendered_forecast)

    # основной цикл экрана
    while True:
        screen.fill(pygame.Color("lightblue"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            gui.get_event(event)

        if back.pressed:
            main()

        gui.render(screen)

        pygame.display.flip()


def main():
    """
    Главное меню.
    """

    # создание и доабвление gui элементов
    gui = GUI()
    gui.add_element(Label((180, 150, 150, 30), "Weather app", pygame.Color('orange'), pygame.Color("lightblue")))
    gui.add_element(Label((175, 200, 150, 30), 'Type the city:', pygame.Color('orange'), pygame.Color('lightblue')))
    enter_city = TextBox((165, 250, 200, 30), "")
    gui.add_element(enter_city)
    b1 = Button((220, 300, 80, 30), "Enter")
    gui.add_element(b1)

    # основной цикл главного меню
    while True:
        screen.fill(pygame.Color("lightblue"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            # передаем события пользователя GUI-элементам
            gui.get_event(event)
            # отрисовываем все GUI-элементы
        if b1.pressed:
            city = enter_city.text
            #print(city)
            city_info(city)
        gui.render(screen)
        # обновляеем все GUI-элементы
        gui.update()

        pygame.display.flip()


if __name__ == "__main__":
    main()
