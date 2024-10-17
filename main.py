import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Helper variables:

display = (800, 800)
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


def z(x, y):
    return x ** 2 + y ** 2


def z1(x, y):
    return x ** 2 + y ** 2 + 1


def getstep(a, b, n):
    return (max(a, b) - min(a, b)) / n


def draw_hyperbolic_paraboloid1(ffunct, xmin, ymin, xmax, ymax, nx, ny, RR, GG, BB):
    stepx = getstep(xmin, xmax, nx)
    stepy = getstep(ymin, ymax, ny)

    glBegin(GL_LINES)
    x = xmin
    while x <= xmax:
        y = ymin
        while y <= ymax:
            glColor(RR, GG, BB)
            glVertex3f(x, y, ffunct(x, y))
            glColor(RR, GG, BB)
            glVertex3f(x, (y + stepy), ffunct(x, y + stepy))
            glColor(RR, GG, BB)
            glVertex3f((x + stepx), y, ffunct(x + stepx, y))
            glColor(RR, GG, BB)
            glVertex3f((x + stepx), (y + stepy), ffunct(x + stepx, y + stepy))
            y += stepy
        x += stepx

    y = ymin
    while y <= ymax:
        x = xmin
        while x <= xmax:
            glColor(RR, GG, BB)
            glVertex3f(x, y, ffunct(x, y))
            glColor(RR, GG, BB)
            glVertex3f((x + stepx), y, ffunct(x + stepx, y))
            glColor(RR, GG, BB)
            glVertex3f(x, (y + stepy), ffunct(x, y + stepy))
            glColor(RR, GG, BB)
            glVertex3f((x + stepx), (y + stepy), ffunct(x + stepx, y + stepy))
            x += stepx
        y += stepy
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

        draw_hyperbolic_paraboloid1(z, -3, -3, 3, 3, 20, 20, 1, 0, 0)
        draw_hyperbolic_paraboloid1(z1, -3, -3, 3, 3, 20, 20, 0, 1, 0)

        pygame.display.flip()
        pygame.time.wait(30)


if __name__ == "__main__":
    main()
