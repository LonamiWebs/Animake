Animake
=======

This is a small helper program that aims at providing an easy-to-use
interface for animating small things, such as text, boxes, and other
basic shapes.

Based on [@expectocode's captivox](https://github.com/expectocode/captivox),
but modified to only provide a thin wrapper for rendering animations and
exporting the result to a video file.

To create your own scenes, add your own `.py` files inside the `scenes/`
directory. They **must** have a function definition called `callback` that
accepts a single `AniState` parameter, like so:

```python
def callback(ani):
    pass  # Use the input 'AniState' at will
```

Example
-------

Say you want to make a `quick` scene. You would create a `scenes/quick.py`
file and then add some code:

```python
import math

from PyQt5.QtGui import QColor


def callback(ani):
    if ani.time > 2 * math.pi:
        raise StopIteration

    ani.color(None)
    for y in range(5, ani.height - 5, 10):
        x = (1 + math.sin(ani.time + y * 0.03)) * ani.width / 2
        ani.fill(QColor.fromHsv((x + y) % 360, 127, 255)).circle(x, y, 10)

        x = ani.width / 2 - math.sin(ani.time + y * 0.06) * ani.width / 4
        ani.fill(QColor.fromHsv(y % 360, 127, 255)).circle(x, y, 5)
```

Run with `python3 gui.py quick` to get [this](https://i.imgur.com/qvIuRVl.mp4).
As you might have noticed, you can chain `ani.calls().together()`.


More details
------------

If the module defines a `DURATION` constant, after that period of time,
the scene will be restarted. To stop the scene earlier, you should
`raise StopIteration` (which will restart it). You can also set the
duration to `None` or `0` to represent infinite.

If the module defines a `start()` callback, it will be called every time
the simulation is restarted, before any call to `callback` occurs.
