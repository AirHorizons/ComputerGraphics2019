import sys, math, glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window = 0
width, height = 1280, 720
radius = min(width, height)/2
oldx, oldy, mousepressed = 0, 0, False

#for debug
counter = 0

poscam = [0, 4.4, 4.4]
degree, znear, zfar = 90.0, 0.1, 300

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
    elif ch == 'v':
        degree /= 1.1

    glutPostRedisplay()

def normalize(x, y):
    global width, height, radius
    x, y = x - width/2, y - height/2
    #print('translated coordinate: ', x, y)
    if x**2 + y**2 > radius*radius:
        x, y = x/(math.sqrt(x**2 + y**2)), y/(math.sqrt(x**2 + y**2))
        return x, y, 0
    else:
        x, y = x/radius, y/radius
        return x, y, math.sqrt(1 - x**2 - y**2)

def crossproduct(u, v):
    return u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]

def dotproduct(u, v):
    dp = 0
    for i in range(len(u)):
        dp += u[i]*v[i]
    return dp

def length(a):
    return math.sqrt(dotproduct(a, a))

def getangle(u, v):
    return math.acos(dotproduct(u, v)/(length(u)*length(v)))

def rotatequaternion(u, v):
    real = [math.cos(getangle(u, v)/2)]
    imag = [num*math.sin(getangle(u, v)/2) for num in crossproduct(u, v)]
    real.extend(imag)
    return real

def qtproduct(a, b):
    return [a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
            a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
            a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
            a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
            ]

def qtconjugate(a):
    return [a[0], -a[1], -a[2], -a[3]]

def rotatecamera(camera, x, y):
    global oldx, oldy, poscam
    poscamlen = length(poscam)
    v1 = normalize(oldx, oldy)
    v2 = normalize(x, y)
    axis = crossproduct(v1, v2)
    theta = getangle(v1, v2)
    # reverse angle
    qtinv = rotatequaternion(v1, v2)
    print(qtinv)
    qt = qtconjugate(qtinv)
    camvec = [0]
    camvec.extend(camera)
    newqt = qtproduct(qtproduct(qt, camvec), qtinv)
    newpos = newqt[1:4]
    poscam = [num/length(newpos)*poscamlen for num in newpos]

def doMouse(button, state, x, y):
    global mousepressed, oldx, oldy
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mousepressed = True
            oldx, oldy = x, y
            #print('original coordinate: ', x, y)
            #print('normalized coordinate: ', normalize(x, y))
        elif state == GLUT_UP:
            mousepressed = False
            #print('original coordinate: ', x, y)
            #print('normalized coordinate: ', normalize(x, y))
            oldx, oldy = x, y
    glutPostRedisplay()

def doMotion(x, y):
    global counter
    if counter == 10:
        counter = 0
        print('theta: ', getangle(normalize(oldx, oldy), normalize(x, y))/math.pi*180)
        rotatecamera(poscam, x, y)
    else:
        counter += 1

def doPassiveMotion(x, y):
    global oldx, oldy
    oldx, oldy = x, y
    glutPostRedisplay()
    

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
    glutPassiveMotionFunc(doPassiveMotion)
    glutIdleFunc(draw)
    glutMainLoop()
