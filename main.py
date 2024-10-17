import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Helper variables
display = (1000, 800)
fovy = 45


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


def draw_hexagon(r, segments, d0, d1):
    """Drawing hexagon using polar coordinates."""
    glBegin(GL_LINE_LOOP)
    glColor(1, 1, 1)
    for i in range(segments):
        theta = 2 * np.pi * i / segments - 0.525

        x = np.cos(theta) * r + d0 * np.sqrt(3)
        y = np.sin(theta) * r + d1 * 3 / 2

        glVertex2d(x, y)
    glEnd()


def draw_hexagonal_grid(number):
    """Draws hexagonal grid."""
    for i in range(-number, number + 1):
        for j in range(-number, number + 1):
            if j % 2 == 0:
                draw_hexagon(1, 6, i, j)
            else:
                draw_hexagon(1, 6, i + 0.5, j)


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
                return
            elif event.type == KEYDOWN:
                buttons(event.key)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_plane(1, 0.1)
        draw_hexagonal_grid(5)

        pygame.display.flip()
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
