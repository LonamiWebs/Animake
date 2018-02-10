from anistate import AniState


SPEED = 50
size = 0


def callback(ani: AniState):
    global size
    (ani
     .size(5)
     .color((0, 0, 255, 64)).line(0, 0, ani.width, ani.height)
     .color((0, 255, 0, 64)).line(0, ani.height, ani.width, 0)
     .size(size)
     .color((255, 0, 0, 64)).point(ani.width / 2, ani.height / 2))

    size += SPEED * ani.dt
