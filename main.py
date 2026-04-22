import pygame
from core import config
from core import video
from core import gui
from core import input
from core import localization
import scenes

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    # pygame.mixer.init()

    pygame.init()
    data = config.read()
    video.init(data["video"])
    gui.init()
    input.init(data["input"])
    localization.init(data["gui"])

    next_scene: str|None = 'Test'

    while next_scene is not None:
        scene_class = getattr(scenes, next_scene)
        new_scene: scenes.Scene = scene_class()
        next_scene = new_scene.run()

    pygame.font.quit()
    pygame.quit()