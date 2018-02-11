import random

from anistate import AniState

DURATION = 10
SPEED = 50


class Ball:
    def __init__(self):
        self.x = random.randint(20, 380)
        self.y = 20
        self.vx = (random.random() * 10) - 5
        while abs(self.vx) < 2:
            self.vx = (random.random() * 10) - 5
        self.vy = 0
        self.ax = 0
        self.ay = 9.8

    def draw(self, ani: AniState):
        self.vx += self.ax * ani.dt
        self.vy += self.ay * ani.dt
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.vx = +0.9 * abs(self.vx)
        if self.x > 400:
            self.vx = -0.9 * abs(self.vx)
        if self.y > 300:
            self.vy = -0.9 * abs(self.vy)
        ani.fill((255, 0, 0)).circle(self.x, self.y, 10)


ball = None
size = 0


def callback(ani: AniState):
    global size, ball
    if ani.frame == 1:
        size = 0
        ball = Ball()

    (ani
     .size(5)
     .color((0, 0, 255, 64)).line(0, 0, ani.width, ani.height)
     .color((0, 255, 0, 64)).line(0, ani.height, ani.width, 0)
     .size(size)
     .color((255, 0, 0, 64)).point(ani.width / 2, ani.height / 2))

    size += SPEED * ani.dt

    (ani
     .color(None)
     .fill((0, 127, 0))
     .poly((0, 200, 50, 210, 100, 190, 200, 200, 400, 240, 400, 400, 0, 400))
     .fill((0, 255, 0))
     .box(0, 300, 400, 100)
    )
    ball.draw(ani)
