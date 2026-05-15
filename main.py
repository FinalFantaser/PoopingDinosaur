import pygame
from core import config
from core import video
from core import audio
from core import gui
from core import input
from core import localization
import scenes

if __name__ == '__main__':
    data = config.read()

    video.init(data["video"])
    audio.init(data["audio"])
    gui.init()
    input.init(data["input"])
    localization.init(data["gui"])

    pygame.display.set_caption(localization.translate("title"))

    next_scene: str|None = 'MainMenu'

    while next_scene is not None:
        scene_class = getattr(scenes, next_scene)
        new_scene: scenes.Scene = scene_class()
        next_scene = new_scene.run()

    pygame.quit()