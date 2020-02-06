from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from math import *

IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
SCALE_K = np.array([1.0, 1.0, 1.0])  # 模型缩放比例
EYE = np.array([-1.5, 2, 4.0])  # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.8, 0, 0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 640, 480  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置

# --------------------
divisor = 10.0
PI = 3.14159
l1 = 10
l2 = 3
l3 = 15
l4 = 15
l5 = 5
X = 0.0
Y = 23.0
Z = 0.0


def inverse_kinematics(x, y, z):
    global l1, l2, l3, l4, l5, PI
    d1 = sqrt(pow(x, 2) + pow(y, 2))
    d2 = d1 - l2
    d3 = sqrt(pow(l1, 2) + pow(d2, 2))
    b1 = atan(l1 / d2) / PI * 180
    b2 = 90 - b1
    d4 = z + l5
    d5 = sqrt(pow(d3, 2) + pow(d4, 2) - 2 * d3 * d4 * cos(b2 / 180 * PI))

    a1 = (atan(d2 / l1) / PI * 180) + (acos((pow(d3, 2) + pow(d5, 2) - pow(d4, 2)) / (2 * d3 * d5)) / PI * 180) + (
            acos((pow(d5, 2) + pow(l3, 2) - pow(l4, 2)) / (2 * d5 * l3)) / PI * 180) - 90

    a2 = 180 - (acos((pow(l3, 2) + pow(l4, 2) - pow(d5, 2)) / (2 * l3 * l4)) / PI * 180)
    a3 = 180 - ((acos((pow(d4, 2) + pow(d5, 2) - pow(d3, 2)) / (2 * d4 * d5)) / PI * 180) +
                (acos((pow(l4, 2) + pow(d5, 2) - pow(l3, 2)) / (2 * l4 * d5)) / PI * 180))
    a4 = atan(x / y) / PI * 180
    # print("d1:%d" % d1)
    # print("d2:%d" % d2)
    # print("d3:%d" % d3)
    # print("d4:%d" % d4)
    # print("d5:%d" % d5)
    # print("a1:%d" % a1)
    # print("a2:%d" % a2)
    # print("a3:%d" % a3)
    # print("a4:%d" % a4)
    print("X:%.2f   Y:%.2f   Z:%.2f" % (X, Y, Z))

    return d1, d2, d3, d4, d5, a1, a2, a3, a4


D1, D2, D3, D4, D5, A1, A2, A3, A4 = inverse_kinematics(X, Y, Z)


# --------------------

def getposture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta


DIST, PHI, THETA = getposture()  # 眼睛与观察目标之间的距离、仰角、方位角


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # 设置画布背景色。注意：这里必须是4个参数
    glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    glDepthFunc(GL_LEQUAL)  # 设置深度测试函数（GL_LEQUAL只是选项之一）


def draw():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H

    # 清除屏幕及深度缓存
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 设置投影（透视投影）
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])

    # 设置模型视图
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 几何变换
    glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])

    # 设置视点
    gluLookAt(
        EYE[0], EYE[1], EYE[2],
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )

    # 设置视口
    glViewport(0, 0, WIN_W, WIN_H)

    # ---------------------------------------------------------------
    glBegin(GL_LINES)  # 开始绘制线段（世界坐标系）

    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)  # 设置当前颜色为红色不透明
    glVertex3f(-0.8, 0.0, 0.0)  # 设置x轴顶点（x轴负方向）
    glVertex3f(0.8, 0.0, 0.0)  # 设置x轴顶点（x轴正方向）

    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)  # 设置当前颜色为绿色不透明
    glVertex3f(0.0, -0.8, 0.0)  # 设置y轴顶点（y轴负方向）
    glVertex3f(0.0, 0.8, 0.0)  # 设置y轴顶点（y轴正方向）

    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)  # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.0, -0.8)  # 设置z轴顶点（z轴负方向）
    glVertex3f(0.0, 0.0, 0.8)  # 设置z轴顶点（z轴正方向）

    glEnd()  # 结束绘制线段

    # ---------------------------------------------------------------
    glBegin(GL_LINES)

    glColor3f(1, 1, 1)

    # l1
    glVertex(0, 0, 0)
    glVertex(0, l1 / divisor, 0)

    # l2
    glVertex(0, l1 / divisor, 0)
    glVertex(sin(A4/180*PI) * l2 / divisor, l1 / divisor, cos(A4/180*PI) * l2 / divisor)

    # l3
    glVertex(sin(A4/180*PI) * l2 / divisor, l1 / divisor, cos(A4/180*PI) * l2 / divisor)
    glVertex(sin(A4/180*PI) * (cos(A1 / 180 * PI) * l3 + l2) / divisor, (sin(A1 / 180 * PI) * l3 + l1) / divisor,
             cos(A4/180*PI) * (cos(A1 / 180 * PI) * l3 + l2) / divisor)

    # l4
    glVertex(sin(A4/180*PI) * (cos(A1 / 180 * PI) * l3 + l2) / divisor, (sin(A1 / 180 * PI) * l3 + l1) / divisor,
             cos(A4/180*PI) * (cos(A1 / 180 * PI) * l3 + l2) / divisor)
    glVertex((sin(A4/180*PI) * D1) / divisor, D4 / divisor, (cos(A4/180*PI) * D1) / divisor)

    # l5
    glVertex((sin(A4/180*PI) * D1) / divisor, D4 / divisor, (cos(A4/180*PI) * D1) / divisor)
    glVertex((sin(A4/180*PI) * D1) / divisor, Z / divisor, (cos(A4/180*PI) * D1) / divisor)

    glEnd()
    # ---------------------------------------------------------------
    glutSwapBuffers()  # 切换缓冲区，以显示绘制内容


def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()


def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()


def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()


def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW
    global D1, D2, D3, D4, D5, A1, A2, A3, A4
    global X, Y, Z

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z', b'd', b'a', b's', b'w', b'e', b'q']:
        if key == b'x':  # 瞄准参考点 x 减小
            LOOK_AT[0] -= 0.01
        elif key == b'X':  # 瞄准参考 x 增大
            LOOK_AT[0] += 0.01
        elif key == b'y':  # 瞄准参考点 y 减小
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  # 瞄准参考点 y 增大
            LOOK_AT[1] += 0.01
        elif key == b'z':  # 瞄准参考点 z 减小
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  # 瞄准参考点 z 增大
            LOOK_AT[2] += 0.01
        elif key == b'd':
            Y += 0.3
        elif key == b'a':
            Y -= 0.3
        elif key == b's':
            X -= 0.3
        elif key == b'w':
            X += 0.3
        elif key == b'e':
            Z += 0.3
        elif key == b'q':
            Z -= 0.3
        D1, D2, D3, D4, D5, A1, A2, A3, A4 = inverse_kinematics(X, Y, Z)
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\r':  # 回车键，视点前进
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\x08':  # 退格键，视点后退
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b' ':  # 空格键，切换投影模式
        IS_PERSPECTIVE = not IS_PERSPECTIVE
        glutPostRedisplay()


if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Quidam Of OpenGL')

    init()  # 初始化画布
    glutDisplayFunc(draw)  # 注册回调函数draw()
    glutReshapeFunc(reshape)  # 注册响应窗口改变的函数reshape()
    glutMouseFunc(mouseclick)  # 注册响应鼠标点击的函数mouseclick()
    glutMotionFunc(mousemotion)  # 注册响应鼠标拖拽的函数mousemotion()
    glutKeyboardFunc(keydown)  # 注册键盘输入的函数keydown()

    glutMainLoop()  # 进入glut主循环
