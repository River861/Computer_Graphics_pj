from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame


class Rubik(object):

    def __init__(self):
        self.__rubik_id = self.__load_texture("rubik.png")
        self.__init_env()
        self.__init_cube()

    def __init_env(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 480/480, 0.1, 200)
        gluLookAt(-1.5, 4, -2.5, 0, 0, 0, 0, 1, 0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        # 设置光照
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])  # 环境光强度
        glLightfv(GL_LIGHT0, GL_POSITION, [4, 8, 1, 1])  # 光照方向
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [2, 2, 2, 1])   # 漫反射光强度

        # 材质
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    def __init_cube(self):
        self.vertices = [
            (1, -1, -1),
            (1, -1, 1),
            (-1, -1, 1),
            (-1, -1, -1),
            (1, 1, -1),
            (1, 1, 1),
            (-1, 1, 1),
            (-1, 1, -1),
        ]
        self.normals = [
            (0, -1, 0),
            (0, 1, 0),
            (1, 0, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, 0, -1)
        ]
        self.quad_faces = {
            1: [1, 2, 3, 4],
            2: [5, 8, 7, 6],
            3: [1, 5, 6, 2],
            4: [2, 6, 7, 3],
            5: [3, 7, 8, 4],
            6: [5, 1, 4, 8]
        }

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

    def __render_texture(self, texcoord):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.__rubik_id)
        glBegin(GL_QUADS)
        for normal_idx, face in self.quad_faces.items():
            normal = self.normals[normal_idx-1]
            glNormal3fv(normal)
            for tex, vertice_idx in zip(texcoord, face):
                glTexCoord2fv(tex)
                glVertex3fv(self.vertices[vertice_idx-1])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def display(self):
        glClearColor(255, 255, 255, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.__render_texture([(0, 0), (1, 0), (1, 1), (0, 1)])
        glutSwapBuffers()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(480, 480)  # 窗口大小
    glutCreateWindow('Rubik')     # 窗口名
    glutDisplayFunc(Rubik().display)
    glutMainLoop()
