import sys, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window = 0
width, height = 1200, 1200


l, s= 0.5, 0.2
ds = 1 # modify to change rate of facial expression(?)

degree = 0.0
ROTATION_SPEED = 0.03 # modify to change speed of jumping
ROTATION_DIR = 1
MOVEMENT = 1

rd, gr, bl = 1, 1, 1
        

def doKeyboard(*args):
    ch = args[0].decode("utf-8")
    if ch == 'q':
        print('GoodBye!')
        sys.exit()
    glutPostRedisplay()

def drawhead(rd, gr, bl):
    global l, s, ds
    s += 0.001 * ds
    if s >= 0.3:
        ds = -1
    elif s < 0.1:
        ds = 1

    vertices = [
            [l, l, l], [l, l, -l], [l, -l, -l], [l, -l, l],
            [-l, l, l], [-l, l, -l], [-l, -l, -l], [-l, -l, l],
            [s, s, s], [s, s, -s], [s, -s, -s], [s, -s, s],
            [-s, s, s], [-s, s, -s], [-s, -s, -s], [-s, -s, s]
            ]
    edges = [
                [0, 1], [1, 2], [2, 3], [3, 0],
                [4, 5], [5, 6], [6, 7], [7, 4],
                [0, 4], [1, 5], [2, 6], [3, 7],
                [8, 9], [9, 10], [10, 11], [11, 8],
                [12, 13], [13, 14], [14, 15], [15, 12],
                [8, 12], [9, 13], [10, 14], [11, 15],
                [0, 8], [1, 9], [2, 10], [3, 11],
                [4, 12], [5, 13], [6, 14], [7, 15]
            ]
    faces = [
            [0, 1, 2, 3, 0], [4, 5, 6, 7, 4], [0, 1, 5, 4, 0], [2, 3, 7, 6, 2], [1, 2, 6, 5, 1], [3, 0, 4, 7, 3],
            [8, 9, 10, 11, 8], [12, 13, 15, 14, 12], [8, 9, 13, 12, 8], [10, 11, 15, 14, 10], [9, 10, 14, 13, 9], [11, 8, 12, 15, 11],
            [0, 1, 9, 8, 0], [1, 2, 10, 9, 1], [2, 3, 11, 10, 2], [3, 0, 8, 11, 3],
            [4, 5, 13, 12, 4], [5, 6, 14, 13, 5], [6, 7, 15, 14, 6], [7, 4, 12, 15, 7],
            [0, 2, 10, 8, 0], [1, 3, 11, 9, 1], [4, 6, 14, 12, 4], [5, 7, 15, 13, 5]
            ]
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    glColor4f(rd, gr, bl, 0.7)
    glLineWidth(2.5)
    for i in range(32):
        glBegin(GL_LINES)
        for j in range(2):
            glVertex3fv(vertices[edges[i][j]])
        glEnd()
    glColor4f(rd, gr, bl, 0.7)
    for i in range(12):
        glBegin(GL_POLYGON)
        for j in range(5):
            glVertex3fv(vertices[faces[i][j]])
        glEnd()

def drawbody(a, b, c, rd = 1.0, gr = 1.0, bl = 1.0):
    vertices = [
            [a, b, c], [a, b, -c], [-a, b, -c], [-a, b, c],
            [a, -b, c], [a, -b, -c], [-a, -b, -c], [-a, -b, c],
            ]

    edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
            ]
    faces = [
            [0, 1, 2, 3, 0], [4, 5, 6, 7, 4], [0, 1, 5, 4, 0], [2, 3, 7, 6, 2], [1, 2, 6, 5, 1], [3, 0, 4, 7, 3]
            ]
    glColor4f(rd, gr, bl, 0.7)
    glLineWidth(2.5)
    for i in range(12):
        glBegin(GL_LINES)
        for j in range(2):
            glVertex3fv(vertices[edges[i][j]])
        glEnd()
    glColor4f(rd, gr, bl, 0.3)
    for i in range(6):
        glBegin(GL_POLYGON)
        for j in range(5):
            glVertex3fv(vertices[faces[i][j]])
        glEnd()

def drawlimb(a, b, c, theta = 0, rd = 1.0, gr = 1.0, bl = 1.0):
    global MOVEMENT
    glPushMatrix()
    glTranslatef(b*math.sin(theta)/2, -b*math.cos(theta)/2, 0)
    glRotatef(theta*180/math.pi, 0.0, 0.0, 1.0)
    drawbody(a, b/2, c, 255/255, 224/255, 189/255)
    glPopMatrix()
    glPushMatrix()
    if MOVEMENT == 1:
        glTranslatef(b*math.sin(theta), -b*math.cos(theta)-b/2, 0)
        drawbody(a, b/2, c, rd, gr, bl)
    elif MOVEMENT == -1:
        glTranslatef(b*math.sin(theta)*3/2, -b*math.cos(theta)*3/2, 0)
        glRotatef(theta*180/math.pi, 0.0, 0.0, 1.0)
        drawbody(a, b/2, c, rd, gr, bl)
    glPopMatrix()

def draw():
    global degree, ROTATION_SPEED, ROTATION_DIR, MOVEMENT
    degree += ROTATION_SPEED * ROTATION_DIR
    if degree > math.pi/2:
        ROTATION_DIR = -1
    elif degree < 0:
        ROTATION_DIR = 1
        MOVEMENT *= -1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(0.0, 3.0, 0)
    drawhead(255/255, 224/255, 189/255)
    glPopMatrix()
    glPushMatrix()
    drawbody(1, 1.75, 1, 0.7, 0.7, 1.0)
    glPushMatrix()
    glTranslatef(0, -2.5, 0)
    drawbody(1, 0.75, 1, 0.7, 1.0, 0.7)
    glPopMatrix()
    glPushMatrix()
    # left arm
    glTranslatef(1.25, 2.5, 0)
    drawlimb(0.25, 3.0, 0.25, degree, 255/255, 224/255, 189/255)
    glPopMatrix()
    glPushMatrix()
    # right arm
    glTranslatef(-1.25, 2.5, 0)
    drawlimb(0.25, 3.0, 0.25, -degree, 255/255, 224/255, 189/255)
    glPopMatrix()
    glPushMatrix() 
    # left leg
    glTranslatef(0.75, -2.5, 0)
    drawlimb(0.25, 5.0, 0.25, degree/2, 255/255, 224/255, 189/255)
    glPopMatrix()
    glPushMatrix() 
    #right arm
    glTranslatef(-0.75, -2.5, 0)
    drawlimb(0.25, 5.0, 0.25, -degree/2, 255/255, 224/255, 189/255)
    glPopMatrix()
    glPopMatrix() 


    glutSwapBuffers()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("HOP HOP HOP!")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, width/height, 0.1, 300.0)
    gluLookAt(0.0, 4.4, 4.4, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutDisplayFunc(draw)
    glutKeyboardFunc(doKeyboard)
    glutIdleFunc(draw)
    glutMainLoop()
