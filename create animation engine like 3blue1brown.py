import numpy as np
import os
import subprocess as sp
import cairo
total=60
Width=1000
Height=1000

def draw(t,width,height):
    surface=cairo.ImageSurface(cairo.FORMAT_ARGB32,width,height)
    ctx=cairo.Context(surface)
    ctx.save()
    ctx.set_source_rgb(0.05,0,0)
    ctx.paint()
    ctx.restore()


    ctx.set_matrix(cairo.Matrix(width/8,0,
                                0,-height/8,
                                width/2,height/2))

    ctx.arc(0,0,t*2/total,0,2*np.pi)
    ctx.set_line_width(0.05)
    ctx.set_source_rgb(0,1,0)
    ctx.stroke()

    surface.write_to_png(F"ashish{t+1}.png")

draw(0,Width,Height)

for i in range(60):
  draw(i,Width,Height)



pro=sp.Popen([
    'ffmpeg',
    '-y',
    '-r','30',
    '-i','ashish%d.png',
    '-vcodec',
    'libx264',
    '-pix_fmt',
    'yuv420p',
     'my.mp4'
])
pro.wait()

for i in range(60):
    os.remove(f"ashish{i+1}.png")
os.startfile('my.mp4')

