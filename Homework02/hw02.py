import sys, math, glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window = 0
width, height = 1280, 720
oldx, oldy, mousepressed = 0, 0, False

poscam = [0, 4.4, 4.4]
degree, znear, zfar = 90.0, 0.1, 300


def doMouse(button, state, x, y):
    global mousepressed
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mousepressed = True
        elif state == GLUT_UP:
            mousepressed = False
    glutPostRedisplay()

def doKeyboard(*args):
    global poscam, degree
    # TODO
    ch = args[0].decode("utf-8")
    if ch == 'q':
        print('GoodBye!')
        sys.exit()
    elif ch == 'z':
        for i in range(3):
            poscam[i] *= 1.1
    elif ch == 'x':
        for i in range(3):
            poscam[i] /= 1.1
    elif ch == 'c':
        degree *= 1.1
        print('degree: ', degree)
    elif ch == 'v':
        degree /= 1.1
        print('degree: ', degree)

    glutPostRedisplay()

def doMotion(x, y):
    pass
    

def drawcube():
    a = 1
    vertices = [
            [a, a, a], [a, -a, a], [-a, -a, a], [-a, a, a],
            [a, a, -a], [a, -a, -a], [-a, -a, -a], [-a, a, -a]
            ]
    edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]  
            ]
    glColor4f(1, 1, 1, 0)
    glLineWidth(2.5)
    for i in range(len(edges)):
        glBegin(GL_LINES)
        for j in range(2):
           glVertex3fv(vertices[edges[i][j]]) 
        glEnd()

def draw():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(degree, width/height, znear, zfar)
    gluLookAt(poscam[0], poscam[1], poscam[2], 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    drawcube()

    glutSwapBuffers()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Awesome Camera Viewer")

    print('Press [Q] to quit')

    glutDisplayFunc(draw)
    glutKeyboardFunc(doKeyboard)
    glutMouseFunc(doMouse)
    glutMotionFunc(doMotion)
    glutIdleFunc(draw)
    glutMainLoop()
