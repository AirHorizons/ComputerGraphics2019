import sys, math, glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

window = 0
width, height = 1280, 720
radius = min(width, height)/2
oldx, oldy, mousepressed = 0, 0, False

axis, theta = None, 0

# if state is 0, drag means rotation. if 1, drag means translation.
state = 0
moving = False

center = [0, 0, 0]
poscam = [0, 4.4, 4.4]
upvec = [0.0, 1.0, 0.0]
originalposcam = [0, 4.4, 4.4]
degree, znear, zfar = 90.0, 0.1, 300

def doKeyboard(*args):
    global poscam, center, degree, state
    # TODO
    ch = args[0].decode("utf-8")
    if ch == 'q':
        print('GoodBye!')
        sys.exit()
    elif ch == 'x':
        for i in range(3):
            poscam[i] = (poscam[i]-center[i])*1.1 + center[i]
    elif ch == 'z':
        for i in range(3):
            poscam[i] = (poscam[i]-center[i])/1.1 + center[i]
    elif ch == 'v':
        degree *= 1.1
    elif ch == 'c':
        degree /= 1.1
    elif ch == '1':
        state = 0
    elif ch == '2':
        state = 1
    glutPostRedisplay()


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
    cosangle = dotproduct(u, v)/length(u)/length(v)
    if cosangle > 1:
        return 1
    elif cosangle < -1:
        return -1
    return math.acos(cosangle)

def normalize(x, y):
    global width, height, radius
    x, y = 2*x/width-1, 1-2*y/height
    d = math.sqrt(x*x+y*y)
    z = math.cos((math.pi/2.0)*(d if d < 1.0 else 1.0))
    return [num/length([x, y, z]) for num in [x, y, z]]
    #norm = [x, -y, radius]
    #return [num/length(norm) for num in norm]

def rotatequaternion(u, v):
    real = [math.cos(getangle(u, v)/2)]
    imag = [num*math.sin(getangle(u, v)/2) for num in crossproduct(u, v)]
    real.extend(imag)
    real = [num/length(real) for num in real]
    return real

def qtproduct(a, b):
    return [
            a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
            a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
            a[0]*b[2]-a[1]*b[3]+a[2]*b[0]+a[3]*b[1],
            a[0]*b[3]+a[1]*b[2]-a[2]*b[1]+a[3]*b[0]
            ]

def qtconjugate(a):
    return [a[0], -a[1], -a[2], -a[3]]

def mvmult(m, v):
    return [
            m[0][0]*v[0], m[0][1]*v[1], m[0][2]*v[2], m[0][3]*v[3],
            m[1][0]*v[0], m[1][1]*v[1], m[1][2]*v[2], m[1][3]*v[3],
            m[2][0]*v[0], m[2][1]*v[1], m[2][2]*v[2], m[2][3]*v[3],
            m[3][0]*v[0], m[3][1]*v[1], m[3][2]*v[2], m[3][3]*v[3]
            ]

def rotatecamera(x, y):
    global oldx, oldy, poscam, originalposcam, center, upvec
    poscamlen = length(poscam)
    v1 = normalize(oldx, oldy)
    v2 = normalize(x, y)
    # reverse angle
    qtinv = rotatequaternion(v1, v2)
    qt = qtconjugate(qtinv)
    poscam4 = [0]
    poscam4.extend([originalposcam[i]-center[i] for i in range(3)])
    poscam4 = [num/poscamlen for num in poscam4]
    upvec4 = [0]
    upvec4.extend(upvec)
    upvec4 = [num/length(upvec) for num in upvec4]
    newqt = qtproduct(qt, qtproduct(poscam4, qtinv))
    newupvec = qtproduct(qt, qtproduct(upvec4, qtinv))
    newpos = newqt[1:4]
    #upvec = newupvec[1:4]
    poscam_ = [num/length(newpos)*poscamlen for num in newpos]
    poscam = [poscam_[i] + center[i] for i in range(3)]

def rotatescene(x, y):
    global oldx, oldy, poscam, originalposcam, axis, theta
    v1 = normalize(oldx, oldy)
    v2 = normalize(x, y)
    axis = crossproduct(v1, v2)
    theta = getangle(v1, v2)

def translatescene(x, y):
    global oldx, oldy, poscam, originalposcam, center, upvec
    rightvec = crossproduct([poscam[i]-center[i] for i in range(3)], upvec)
    theta = math.a
    


def doMouse(button, state, x, y):
    global mousepressed, oldx, oldy, poscam, originalposcam
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            mousepressed = True
            oldx, oldy = x, y
            #print('original coordinate: ', x, y)
            #print('normalized coordinate: ', normalize(x, y))
            originalposcam = poscam
            moving = True 
        elif state == GLUT_UP:
            mousepressed = False
            #print('original coordinate: ', x, y)
            #print('normalized coordinate: ', normalize(x, y))
            oldx, oldy = x, y
            originalposcam = poscam
            moving = False
    glutPostRedisplay()

def doMotion(x, y):
    global state
    # print('theta: ', getangle(normalize(oldx, oldy), normalize(x, y))/math.pi*180)
    if state == 0:
        # print(poscam)
        rotatecamera(x, y)
        # rotatescene(x, y)
    elif state == 1:
        pass
    glutPostRedisplay()

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
    gluLookAt(poscam[0], poscam[1], poscam[2], center[0], center[1], center[2], upvec[0], upvec[1], upvec[2])
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if moving:
        glRotatef(theta*10, axis[0], axis[1], axis[2])
    drawcube()

    glutSwapBuffers()

if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("Awesome Camera Viewer")

    print('Press [Q] to quit')
    print('Press [1] to rotate screen')
    print('Press [2] to translate screen/(Not Implemented yet)')
    print('Press [Z/X] to dolly in/out')
    print('Press [C/V] to zoom in/out')

    glutDisplayFunc(draw)
    glutKeyboardFunc(doKeyboard)
    glutMouseFunc(doMouse)
    glutMotionFunc(doMotion)
    glutPassiveMotionFunc(doPassiveMotion)
    glutIdleFunc(draw)
    glutMainLoop()
