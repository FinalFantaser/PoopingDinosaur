from pygame.time import get_ticks
from objects import MissileSilo, Missile, TRexNew, Poo
from .object_handler import ObjectHandler
from data_containers import objects as obj_container

class MissileSiloHandler(ObjectHandler):
    @classmethod
    def update(cls, obj: MissileSilo):
        if cls.delete_if_passed_camera(obj):
            return

        obj.button_hitbox.y = obj.y

        curr_ticks = get_ticks()

        if not obj.empty:
            if obj.state == obj.State.READY:
                for activator in obj_container.main_layer().values():
                    if not isinstance(activator, (TRexNew, Poo)):
                        continue

                    if not getattr(activator, "hitbox", activator.rect).overlaps(obj.button_hitbox):
                        continue

                    if getattr(activator, "invincibility", 0) > 0 or activator.vel_y <= 0:
                        continue

                    obj.curr_frame = 0
                    obj.state = obj.State.EMPTY
                    break

            elif obj.state == obj.State.EMPTY:
                if obj.curr_frame == obj.total_frames - 1 and curr_ticks - obj.last_frame_change >= obj.anim_interval:
                    missile = Missile(obj.pos, -90)
                    missile_size = missile.curr_size
                    missile.x = obj.rect.center_x - missile_size[0]/2
                    missile.y = obj.y - missile_size[1]/2

                    obj_container.queue_add(missile)

                    obj.empty = True

        obj.last_update = curr_ticks

