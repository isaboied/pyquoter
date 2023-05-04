import subprocess

import pygame
import requests
import sys
import textwrap
from pygame.locals import *
import time
import os


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()
screen = pygame.display.set_mode((1200, 350))
clock = pygame.time.Clock()
pygame.display.set_caption('py-quoter by isaboied')
img = pygame.image.load(resource_path(
    "icon.jpg/icon.jpg"))  # quick note is that for pyinstaller to work I did this but if you want to run the script
# itself you should put icon.jpg instead of the one that is there
pygame.display.set_icon(img)

# Set up the colors
DARK_PURPLE = (128, 0, 128)
BLACK = (0, 0, 0)
LIGHT_PURPLE = (153, 50, 204)

# Set up the fonts
font = pygame.font.SysFont("Bahnshrift", 48)
button_font = pygame.font.SysFont("Bahnshrift", 24)

# Set up the text
quote_text = []
author_text = font.render("", True, BLACK)


def get_quote():
    response = requests.get("https://api.quotable.io/random")
    data = response.json()
    quote = data["content"]
    author = data["author"]
    return quote, author


def update_text():
    global quote_text
    global author_text
    quote, author = get_quote()
    wrapped_quote = textwrap.wrap(quote, width=50)
    quote_text = [font.render(line, True, BLACK) for line in wrapped_quote]
    author_text = font.render(author, True, BLACK)


update_text()

# Set up the timer
timer_start_time = time.time()
timer_duration = 20

# Set up the music
pygame.mixer.music.load(resource_path("background_music.mp3"))
pygame.mixer.music.play(-1)

# Set up the button
button_text = button_font.render("License", True, BLACK)
button_width = button_text.get_width() + 20
button_height = button_text.get_height() + 20
button_x = 1200 - button_width - 10
button_y = 10


def open_license():
    if sys.platform == "win32":
        os.startfile("License.txt")
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, "License.txt"])


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if button_x <= x <= button_x + button_width and button_y <= y <= button_y + button_height:
                open_license()

    screen.fill(DARK_PURPLE)

    # Draw the text
    y_offset = 10
    for line in quote_text:
        screen.blit(line, (10, y_offset))
        y_offset += line.get_height() + 10
    screen.blit(author_text, (10, y_offset))

    # Draw the timer bar
    time_elapsed = time.time() - timer_start_time
    progress = time_elapsed / timer_duration
    if progress >= 1:
        update_text()
        timer_start_time = time.time()
        progress = 0
    pygame.draw.rect(screen, BLACK, (10, y_offset + author_text.get_height() + 10, int(1180 * progress), 20))

    # Draw the button
    pygame.draw.rect(screen, LIGHT_PURPLE, (button_x, button_y, button_width, button_height))
    screen.blit(button_text, (button_x + 10, button_y + 10))

    pygame.display.update()
    clock.tick(30)
