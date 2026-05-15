import pygame.time
from pygame import Surface
import core
from scenes.scene import Scene
from objects import Ground, Allosaurus, Camera
from data_containers import objects as obj_container
from object_handlers import AllosaurusHandler


class WinScreen(Scene):
    INPUT_INTERVAL: int = 125

    def __init__(self):
        super().__init__()

        self.camera: Camera = Camera((0, 0))
        self.ground = Ground(int(core.video.get_screen_rect().width/Ground.BLOCK_W))
        self.allosaurus: Allosaurus = Allosaurus((
            core.video.get_screen_rect().centerx - Allosaurus.SIZE[0]/2,
            self.ground.touch_level - Allosaurus.SIZE[1] * 3,
        ))

        obj_container.clear()
        obj_container.add(self.ground)
        obj_container.add(self.allosaurus)
        obj_container.add(self.camera)

        self.label: Surface = core.gui.text_render(core.localization.translate("win"))
        self.label_pos: tuple[float, float] = (
            core.video.get_screen_rect().centerx - self.label.get_width()/2,
            self.ground.rect.bottom + core.gui.MARGIN[1]
        )

        self.next_jump_in: int = 0
        self.last_jumped_at: int = pygame.time.get_ticks()

    def on_finish(self) -> None:
        obj_container.clear()

    def update(self) -> None:
        if self.allosaurus.rect.bottom >= self.ground.touch_level:
            if pygame.time.get_ticks() - self.last_jumped_at >= self.next_jump_in:
                self.allosaurus.vel_y = Allosaurus.BASE_JUMP_ACCEL

        AllosaurusHandler.update(self.allosaurus)

    def draw(self):
        self.allosaurus.x = core.video.get_screen_rect().centerx - Allosaurus.SIZE[0]/2
        self.allosaurus.animate()
        self.allosaurus.draw(obj_container.get_camera().rect)

    def draw_gui(self) -> None:
        core.video.texture_blit(self.label, self.label_pos)

    def read_input(self) -> None:
        if pygame.time.get_ticks() - core.input.last_pressed_at() < self.INPUT_INTERVAL:
            return

        if core.input.pressed("confirm") or core.input.pressed("poop") or core.input.pressed("back"):
            self.done = True
            self.next_scene = 'SelectGameMode'
