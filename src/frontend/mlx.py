from pymlx import Mlx
import os

def on_key(key, param):
    if key == 65307:  # ESC
        os._exit(0)

mlx = Mlx()
window = mlx.new_window(800, 600, "My Window")
mlx.key()
mlx.mlx_key_hook()
mlx.loop()
'''
['_ptr', '_callbacks', '__module__', '__firstlineno__', '__doc__',
'__init__', 'new_window', 'new_image', 'destroy_image', 'on_loop',
'loop', 'loop_end', 'destroy', '__enter__', '__exit__', '__static_attributes__',
'__dict__', '__weakref__', '__new__', '__repr__', '__hash__', '__str__', '__getattribute__',
'__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__',
'__ge__', '__reduce_ex__', '__reduce__', '__getstate__', '__subclasshook__',
'__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
'''
print(mlx.__dir__())