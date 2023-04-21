"""Game file."""

import pygame
import pygame_gui
import sys
import requests
import json
from config import *
from datetime import datetime


class Game():
    """Respresentation of game."""

    image_size = 50
    up_keys = [pygame.K_UP, pygame.K_w]
    down_keys = [pygame.K_DOWN, pygame.K_s]
    left_keys = [pygame.K_LEFT, pygame.K_a]
    right_keys = [pygame.K_RIGHT, pygame.K_d]
    all_keys = up_keys + down_keys + left_keys + right_keys

    def __init__(self, username: str, x_coordinate: int, y_coordinate: int, path_to_img: int) -> None:
        """Inizialisation method.

        Args:
            username (str): user's username.
            x_coordinate (int): x coordiante.
            y_coordinate (int): y coordinate.
            path_to_img (int): path to image.
        """
        self.username = username
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.image = pygame.image.load(path_to_img)

    def run(self):
        """Run the game by executing this function."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    requests.put(
                        UPDATE_URL,
                        data=json.dumps(
                            {
                                'username': self.username,
                                'x': self.x_coordinate,
                                'y': self.y_coordinate,
                            },
                        ),
                    )
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if keys[Game.up_keys[0]] or keys[Game.up_keys[1]]:
                self.y_coordinate = max(0, self.y_coordinate - 1)
            if keys[Game.down_keys[0]] or keys[Game.down_keys[1]]:
                self.y_coordinate = min(
                    HEIGHT - Game.image_size,
                    self.y_coordinate + 1,
                )
            if keys[Game.left_keys[0]] or keys[Game.left_keys[1]]:
                self.x_coordinate = max(0, self.x_coordinate - 1)
            if keys[Game.right_keys[0]] or keys[Game.right_keys[1]]:
                self.x_coordinate = min(
                    WIDTH - Game.image_size,
                    self.x_coordinate + 1,
                )
            for key in Game.all_keys:
                if keys[key]:
                    data_to_send = {
                        'time': str(datetime.now()),
                        'key_pressed': pygame.key.name(key),
                        'x': self.x_coordinate,
                        'y': self.y_coordinate,
                    }
                    requests.post(MAIN_URL, data=json.dumps(data_to_send))
            SCREEN.fill((255, 255, 255))
            SCREEN.blit(self.image, (self.x_coordinate, self.y_coordinate))
            pygame.display.update()


class RegAuthFabric():
    """Fabric for registration and authentification."""

    small_font_size = 40
    big_font_size = 100

    def __init__(
        self,
        manager: pygame_gui.UIManager,
            text_for_label: str,
            text_for_button: str,
            next_function=None,
    ) -> None:
        """Inizilalisation method.

        Args:
            manager (pygame_gui.UIManager): manager for gui.
            text_for_label (str): text for label.
            text_for_button (str): text for button.
            next_function (function, optional): next function that will called. Defaults to None.
        """
        self.manager = manager
        self.text_for_label = text_for_label
        self.text_for_button = text_for_button
        self.next_function = next_function

    def main_logic(self):
        """Run the reg or auth by executing this function."""
        top_label = pygame.font.SysFont("bahnschrift", RegAuthFabric.big_font_size).render(
            f"{self.text_for_label}",
            True,
            "black",
        )
        username_label = pygame.font.SysFont("bahnschrift", RegAuthFabric.small_font_size).render(
            "Никнейм:",
            True,
            "black",
        )
        username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((350, 275), (900, 50)),
            manager=manager,
            object_id='#username_entry',
        )
        password_label = pygame.font.SysFont("bahnschrift", RegAuthFabric.small_font_size).render(
            "Пароль:",
            True,
            "black",
        )
        password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((350, 375), (900, 50)),
            manager=manager,
            object_id='#password_entry',
        )
        submit_button = pygame_gui.elements.ui_button.UIButton(
            text=f'{self.text_for_button}',
            relative_rect=pygame.Rect((350, 475), (900, 50)),
            manager=manager,
            object_id='#submit',
        )
        error_label = pygame.font.SysFont("bahnschrift", 100).render(
            "",
            True,
            "red",
        )
        while True:
            UI_REFRESH_RATE = clock.tick(60) / 1000
            manager.update(UI_REFRESH_RATE)
            SCREEN.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (
                    event.type == pygame.USEREVENT and
                        event.user_type == pygame_gui.UI_BUTTON_PRESSED
                ):
                    username = username_input.text
                    password = password_input.text
                    if not username:
                        error_label = pygame.font.SysFont("bahnschrift", 100).render(
                            "Вы не ввели имя пользователя!",
                            True,
                            "red",
                        )
                    elif not password:
                        error_label = pygame.font.SysFont("bahnschrift", 100).render(
                            "Вы не ввели пароль!",
                            True,
                            "red",
                        )
                    else:
                        if self.text_for_label == 'Авторизация':
                            reqv = requests.post(
                                AUTH_URL,
                                data=json.dumps(
                                    {
                                        'username': username,
                                        'password': password,
                                    },
                                ),
                            )
                            if reqv.status_code == OK:
                                reqv_values = reqv.content.decode().split()
                                Game(
                                    reqv_values[0],
                                    int(reqv_values[1]),
                                    int(reqv_values[2]),
                                    'image.svg',
                                ).run()
                            else:
                                error_label = pygame.font.SysFont("bahnschrift", 100).render(
                                    f"{reqv.content.decode()}",
                                    True,
                                    "red",
                                )

                        else:
                            reqv = requests.post(
                                REGISTER_URL,
                                data=json.dumps(
                                    {
                                        'username': username,
                                        'password': password,
                                    },
                                ),
                            )
                            if reqv.status_code == CREATED:
                                self.manager.clear_and_reset()
                                self.next_function()
                            error_label = pygame.font.SysFont("bahnschrift", 100).render(
                                f"{reqv.content.decode()}",
                                True,
                                "red",
                            )
                manager.process_events(event)

            new_top_label = top_label.get_rect(center=(WIDTH / 2, 100))
            new_username_label = username_label.get_rect(center=(413, 250))
            new_password_label = password_label.get_rect(center=(406, 355))
            new_error_label = error_label.get_rect(center=(WIDTH / 2, 800))

            SCREEN.blit(top_label, new_top_label)
            SCREEN.blit(username_label, new_username_label)
            SCREEN.blit(password_label, new_password_label)
            SCREEN.blit(error_label, new_error_label)

            manager.draw_ui(SCREEN)

            pygame.display.update()


class Menu:
    """Main menu representation."""

    def __init__(self, manager: pygame_gui.UIManager) -> None:
        """Inizialisation method.

        Args:
            manager (pygame_gui.UIManager): manager for gui.
        """
        self.manager = manager

    def main_menu(self):
        """Run the menu by executing this function."""
        login_button = pygame_gui.elements.ui_button.UIButton(
            text='Войти',
            relative_rect=pygame.Rect((550, 375), (450, 50)),
            manager=self.manager,
            object_id='#submit',
        )
        register_button = pygame_gui.elements.ui_button.UIButton(
            text='Зарегистрироваться',
            relative_rect=pygame.Rect((550, 475), (450, 50)),
            manager=self.manager,
            object_id='#submit',
        )

        auth_function = RegAuthFabric(
            self.manager,
            'Авторизация',
            'Войти',
        ).main_logic
        reg_function = RegAuthFabric(
            self.manager,
            'Регистрация',
            'Зарегистрироваться',
            auth_function,
        ).main_logic
        while True:
            UI_REFRESH_RATE = clock.tick(60) / 1000
            self.manager.update(UI_REFRESH_RATE)
            SCREEN.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (
                    event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == login_button
                ):
                    auth_function()
                if (
                    event.type == pygame.USEREVENT and
                    event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                        event.ui_element == register_button
                ):
                    reg_function()
                self.manager.process_events(event)

            SCREEN.fill("white")
            self.manager.draw_ui(SCREEN)

            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    WIDTH, HEIGHT = 1600, 900
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly Game")

    font = pygame.font.SysFont('arial', 100)
    manager = pygame_gui.UIManager((1600, 900))
    clock = pygame.time.Clock()

    Menu(manager).main_menu()
