import math
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Helper variables

display = (800, 800)
fovy = 45
pi = math.pi


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


def clip(u, start, end):
    """Is used as a helper function the klein bottle."""
    if u < start:
        return start
    elif u > end:
        return end
    else:
        return u


def draw_klein_bottle(segments):
    """A \"simple\" method to draw klein bottle(no)."""
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    for i in range(segments):
        u = 2 * np.pi * i / segments
        for j in np.arange(segments):
            v = 2 * np.pi * j / segments

            x = 4 * np.cos(u) * (1 + np.sin(u)) + 2 * (2 - np.cos(u)) * np.cos(clip(u, 0, np.pi)) * np.cos(v)
            y = 10 * np.sin(u) + 2 * (2 - np.cos(u)) * np.sin(clip(u, 0, np.pi)) * np.cos(v)
            z = (2 - np.cos(u)) * np.sin(v)

            glVertex3d(x, y, z)
    glEnd()


def draw_mobius_strip(uStep, vStep):
    """Draws a möbius strip."""
    glBegin(GL_POINTS)
    glColor(1, 1, 1)
    for u in np.arange(0, 2 * np.pi, 2 * np.pi / (uStep - 1)):
        for v in np.arange(-1, 1, 2 / (vStep - 1)):
            x = (1 + v / 2 * np.cos(u / 2)) * np.cos(u)
            y = (1 + v / 2 * np.cos(u / 2)) * np.sin(u)
            z = v / 2 * np.sin(u / 2)

            glVertex3f(x, y, z)
    glEnd()


def main():
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    set_perspective()

    glTranslatef(0.0, 0.0, -5.0)

    pygame.key.set_repeat(10, 100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                buttons(event.key)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_plane(10, 0.1)
        draw_klein_bottle(50)

        pygame.display.flip()
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
