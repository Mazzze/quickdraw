from PIL import Image, ImageDraw
import os
import cv2
import numpy as np
import math
import random

#size
im_x = 1000
im_y = 1000
img = Image.new('RGB', (im_x,im_y), color = 'black')
#img = Image.open('gspot.png', 'r')

xtot = img.size[0]
ytot = img.size[1]

# math funkktion
def abs_list(lst):
    sum = 0
    for i in lst:
        sum += i**2
    return np.sqrt(sum)

def vektor_sub(u,v):
    p = []
    for i in range(len(u)):
        p.append(u[i]-v[i])
    return p

def vektor_add(u,v):
    p = []
    for i in range(len(u)):
        p.append(u[i]+v[i])
    return p

def find_dist(u, v):
    return abs_list(vektor_sub(u,v))

def random_color(min=0, max=255):
    return (random.randint(min, max),random.randint(min, max),random.randint(min, max))

def color_all(color, image_):
    pixels = image_.load()
    for i in range(image_.size[0]):
        for j in range(image_.size[1]):
            pixels[i,j] = (color[0],color[1],color[2])

def draw_circle(pos, size, color, image_):
    pixels = image_.load()
    for i in range(image_.size[0]):
        for j in range(image_.size[1]):
            if np.sqrt((i-pos[0])**2+(j-pos[1])**2) <= size:
                pixels[i,j] = (color[0],color[1],color[2])

def draw_negcircle(pos, size, color, image_):
    pixels = image_.load()
    for i in range(image_.size[0]):
        for j in range(image_.size[1]):
            if np.sqrt((i-pos[0])**2+(j-pos[1])**2) >= size:
                pixels[i,j] = (color[0],color[1],color[2])

def draw_square(qtq, color, image_):
    pixels = image_.load()
    for i in range(int(qtq[0][0]),int(qtq[1][0])):
        for j in range(int(qtq[0][1]),int(qtq[1][1])):
            pixels[i,j] = (color[0],color[1],color[2])



def shadedball(pos, size, color, image_, lightpositions_):
    look_x = range(math.floor(pos[0]-size),math.floor(pos[0]+size))
    look_y = range(math.floor(pos[1]-size),math.floor(pos[1]+size))

    ball_center = pos
    head_to_screan = 1

    pixels = image_.load()
    for i in look_x:
        if i < image_.size[0]-1 and i > 0:
            for j in look_y:
                if j < image_.size[1]-1 and j > 0:
                    if np.sqrt((i-pos[0])**2+(j-pos[1])**2) <= size:

                        light_constant = 0
                        for lightpos in lightpositions_:
                            lightpos = vektor_sub(lightpos,pos)
                            on_ball_pos = [i-pos[0] ,j-pos[1], np.sqrt(size**2 -(i-pos[0])**2 -(j-pos[1])**2)]
                            cos_angle = np.dot(on_ball_pos,lightpos)/(abs_list(on_ball_pos)*abs_list(lightpos))
                            light_fagt = cos_angle*100/find_dist(on_ball_pos,lightpos)
                            if light_fagt < 0:
                                light_fagt = 0
                            light_constant += light_fagt
                            new_r = pixels[i,j][0]+int(color[0]*light_constant)
                            new_g = pixels[i,j][1]+int(color[1]*light_constant)
                            new_b = pixels[i,j][2]+int(color[2]*light_constant)
                            pixels[i,j] = (new_r,new_g,new_b)

def sun(pos, size, color, image_):
    look_x = range(math.floor(pos[0]-size),math.floor(pos[0]+size))
    look_y = range(math.floor(pos[1]-size),math.floor(pos[1]+size))
    pixels = image_.load()
    print('sun')
    for i in look_x:
        if i < image_.size[0]-1 and i > 0:
            for j in look_y:
                if j < image_.size[1]-1 and j > 0:
                    if np.sqrt((i-pos[0])**2+(j-pos[1])**2) <= size:
                        light_constant = 2*(1-(find_dist(pos, [i,j,pos[2]])/size)**2)
                        new_r = pixels[i,j][0]+int(color[0]*light_constant)
                        new_g = pixels[i,j][1]+int(color[1]*light_constant)
                        new_b = pixels[i,j][2]+int(color[2]*light_constant)
                        pixels[i,j] = (new_r,new_g,new_b)

color_all((0,0,0), img)
#draw_circle([xtot/2,ytot/2], xtot*0.9/2, (255,255,255), img)
#shadedball([xtot/2,ytot/2], xtot*0.9/2, [255,255,255], img, [1,-1,2])
#draw_square(((0,0),(xtot/2,ytot/2)), (0,0,0), img)
#draw_square(((xtot/2,ytot/2),(xtot,ytot)), (0,0,0), img)
#draw_negcircle([xtot/2,ytot/2], xtot/2, (0,255,0), img)
"""
#makes all (0,255,0) colerd pixels transperent
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if item[0] == 0 and item[1] == 255 and item[2] == 0:
        newData.append((0, 255, 0, 0))
    else:
        newData.append(item)
img.putdata(newData)
"""
def solarsystem(image_):
    planet_amount = 100
    planet_schade_maximum = 255
    backgroundcolor = (0,0,0)

    color_all(backgroundcolor, image_)
    sun_color = random_color(100,255)
    lightpositions = []
    sun_pos = [xtot/2,ytot/2,-ytot]

    lightpositions.append(sun_pos)

    for i in range(int(planet_amount/2)):
        pos_ball = [random.randrange(xtot),random.randrange(ytot),-random.randrange(ytot,2*ytot)]
        print(i, 'bh')
        size = random.randint(int(xtot/20),int(xtot/16))
        draw_circle(pos_ball, size, (0,0,0), img)
        shadedball(pos_ball, size, random_color(0,planet_schade_maximum), img, lightpositions)
        shadedball(pos_ball, size, sun_color, img, lightpositions)

    sun(sun_pos, xtot/16, sun_color, image_)

    for i in range(int(planet_amount/2)):
        pos_ball = [random.randrange(xtot),random.randrange(ytot),-random.randrange(ytot)]
        print(i, 'fo')
        size = random.randint(int(xtot/20),int(xtot/16))
        draw_circle(pos_ball, size, (0,0,0), img)
        shadedball(pos_ball, size, random_color(0,planet_schade_maximum), img, lightpositions)
        shadedball(pos_ball, size, sun_color, img, lightpositions)


solarsystem(img)

#lightpos = [xtot/2,-ytot/2,1000]   random.randint(int(xtot/6),int(xtot/5))
#color_all((50,0,0), img)
#for i in range(7):
#    pos_ball = [random.randrange(xtot),random.randrange(ytot),random.randrange(2000)]
#    print(pos_ball)
#    shadedball(pos_ball, random.randint(0,xtot/5), [random.randint(0,255),random.randint(0,255),random.randint(0,255)], img, lightpos)
img.save('solarsystem.png')
