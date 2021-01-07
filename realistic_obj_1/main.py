from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame


class Dice(object):

    def __init__(self):
        self.__init_cube()
        self.__init_env()

    def __init_cube(self):
        self.__vertices = [
            (1, 1, -1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
            (1, -1, -1),
            (1, -1, 1),
            (-1, -1, 1),
            (-1, -1, -1),
        ]
        self.__normals = [
            (0, 1, 0),
            (0, 0, -1),
            (-1, 0, 0),
            (1, 0, 0),
            (0, 0, 1),
            (0, -1, 0),
        ]
        self.__surfaces = {
            1: [1, 2, 3, 4],
            2: [1, 5, 8, 4],
            3: [4, 8, 7, 3],
            4: [1, 5, 6, 2],
            5: [2, 6, 7, 3],
            6: [5, 6, 7, 8]
        }

    def __init_env(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 480/480, 0.1, 200)
        gluLookAt(3, 4, 5, 0, 0, 0, 0, 1, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        # 设置光照
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.3, 0.3, 0.3, 1.0])  # 环境光强度
        glLightfv(GL_LIGHT0, GL_POSITION, [4, 4, -4, 1])  # 光照方向
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [4, 4, 4, 1])   # 漫反射光强度

        # 材质
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def __load_texture(self, filename):
        surface = pygame.image.load(filename)
        img = pygame.image.tostring(surface, "RGBA", 1)
        width, height = surface.get_width(), surface.get_height()
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        return ID

    def __render_texture(self, num):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.__load_texture(f"./texture/{num}.png"))
        glBegin(GL_QUADS)
        normal = self.__normals[num-1]
        glNormal3fv(normal)
        for tex, vertice_idx in zip([(1, 1), (1, 0), (0, 0), (0, 1)], self.__surfaces[num]):
            glTexCoord2fv(tex)
            glVertex3fv(self.__vertices[vertice_idx-1])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def flush(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, -1, -1, 1)   # (角度,x,y,z)
        for num in range(1, 7):
            self.__render_texture(num)
        glutSwapBuffers()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(480, 480)  # 窗口大小
    glutCreateWindow('Dice')      # 窗口名
    _ = Dice()
    glutDisplayFunc(_.flush)
    glutIdleFunc(_.flush)       # 产生动画函数
    glutMainLoop()
