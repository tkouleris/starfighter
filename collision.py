class Collision:

    def check(self, object_1, object_2, sound=None):
        if object_1.visible is True and object_2.visible is True:
            collision = object_1.hitbox.colliderect(object_2.hitbox)
            if collision:
                if sound is not None:
                    sound.play()
                object_1.visible = False
                object_2.visible = False
            return collision
        return False


