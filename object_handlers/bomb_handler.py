from pygame.mask import Mask
from pygame.time import get_ticks
from objects import Rect, Layer, Direction, Object, Ground, Camera, Bomb, Explosion, Skyscraper
from .object_handler import ObjectHandler
from data_containers import objects as obj_container, game_data


class BombHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: Bomb):
        if cls.delete_if_passed_camera(obj):
            return

        cls.physics(obj)
        cls.collisions(obj)

        obj.last_update = get_ticks()


    @classmethod
    def physics(cls, obj: Bomb) -> None:
        obj.vel_x = max(0.0, obj.vel_x - obj.X_SLOWDOWN_RATE * obj.update_delta)
        super().physics(obj)

    @classmethod
    def collisions(cls, bomb: Bomb) -> None:
        detonate = False

        if bomb.rect.bottom >= obj_container.get_ground().touch_level:
            detonate = True
        else:
            for skyscraper in obj_container.main_layer():
                if not isinstance(skyscraper, Skyscraper):
                    continue

                if not skyscraper.rect.overlaps(bomb.rect):
                    continue

                if skyscraper.health > 0:
                    if skyscraper.health == skyscraper.MAX_HEALTH:
                        detonate = True
                    else:
                        mask = Mask(bomb.size, True)
                        offset = skyscraper.x - bomb.x, skyscraper.y - bomb.y

                        if mask.overlap(skyscraper.bit_mask, offset):
                            detonate = True

        if detonate:
            explosion = Explosion(damage=True).instead_of(bomb)
            obj_container.queue_delete(bomb)
            obj_container.queue_add(explosion)
