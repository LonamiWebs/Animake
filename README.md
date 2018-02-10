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
