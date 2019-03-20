import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window = 0
width, height = 800, 600

def doKeyboard(*args):
    ch = args[0].decode("utf-8")
    if ch == 'q':
        print('GoodBye!')
        sys.exit()
    glutPostRedisplay()

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glutSwapBuffers()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Twinkle Twinkle Tesseract")
    glutDisplayFunc(draw)
    glutKeyboardFunc(doKeyboard)
    glutIdleFunc(draw)
    glutMainLoop()
