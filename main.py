import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Helper variables
display = (1000, 800)
fovy = 45


def load_texture(image) -> np.uintc:
    texture_surface = pygame.image.load(image)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texture


def set_perspective():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovy, (display[0] / display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


def buttons(key):
    """Rotates the object using keys."""
    global fovy

    if key == K_d:
        glRotatef(5, 0, 1, 0)
    elif key == K_a:
        glRotatef(-5, 0, 1, 0)
    elif key == K_w:
        glRotatef(-5, 1, 0, 0)
    elif key == K_s:
        glRotatef(5, 1, 0, 0)

    elif key == K_EQUALS:
        if fovy < 170:
            fovy += 5
        set_perspective()
    elif key == K_MINUS:
        if fovy > 10:
            fovy -= 5
        set_perspective()


def draw_plane(limit, delta):
    """Used to define plains."""
    glBegin(GL_POINTS)

    for x in np.arange(-limit, limit, delta):
        glColor(1, 0, 0)
        glVertex3d(x, 0, 0)

    for y in np.arange(-limit, limit, delta):
        glColor(0, 1, 0)
        glVertex3d(0, y, 0)

    for z in np.arange(-limit, limit, delta):
        glColor(0, 0, 1)
        glVertex3d(0, 0, z)

    glEnd()


def draw_sphere(radius, num_latitudes, num_longitudes):
    """Draws sphere using spherical coordinates system(I don't really understand the math part)."""
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    glColor(1, 1, 1)

    for i in range(num_latitudes):
        lat0 = math.pi * (-0.5 + float(i) / num_latitudes)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / num_latitudes)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(num_longitudes + 1):
            lng = 2 * math.pi * float(j) / num_longitudes
            x = math.cos(lng)
            y = math.sin(lng)

            glTexCoord2f(float(j) / num_longitudes, float(i) / num_latitudes)
            glVertex3f(x * zr0, y * zr0, z0)
            glTexCoord2f(float(j) / num_longitudes, float(i + 1) / num_latitudes)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()


def main():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    set_perspective()

    glTranslatef(0.0, 0.0, -5.0)

    pygame.key.set_repeat(10, 100)

    texture = load_texture(
        '2D_Earth.jpg')

    if texture is None:
        print("Failed to load texture.")
        pygame.quit()
        return

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                buttons(event.key)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_plane(1, 0.1)
        draw_sphere(1, 30, 30)

        pygame.display.flip()
        pygame.time.wait(30)


main()
