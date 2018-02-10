from anistate import AniState


def callback(ani: AniState):
    (ani
     .size(5)
     .color((0, 0, 255, 64)).line(0, 0, ani.width, ani.height)
     .color((0, 255, 0, 64)).line(0, ani.height, ani.width, 0)
     .size(ani.frame)
     .color((255, 0, 0, 64)).point(ani.width / 2, ani.height / 2))
