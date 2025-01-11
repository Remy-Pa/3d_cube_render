import pygame as pg
import OpenGL.GL
import OpenGL.GLU
import numpy as np
from cube import Cube

class App:

    def __init__(self, coords_lists = [], colors_list = [], win_size = (1728, 972), background_color = (0.1,0.1,0.1)):

        pg.init()
        width, height = win_size
        pg.display.set_caption('cube display')
        self.window = pg.display.set_mode(win_size, pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        self.coords_lists = coords_lists
        if self.coords_lists == []:
            print('No cubes to be rendered')
            quit()
        self.colors_list = colors_list

        if len(coords_lists) > len(colors_list):
            print('Colors list should be of same length as coords list')
            while len(coords_lists) > len(colors_list):
                colors_list.append((np.random.random(), np.random.random(), np.random.random()))

        # setup opengl
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
        OpenGL.GLU.gluPerspective(45, width/height, 1, 250.0)
        OpenGL.GL.glEnable(OpenGL.GL.GL_LIGHTING)
        OpenGL.GL.glEnable(OpenGL.GL.GL_LIGHT0)
        OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)

        self.background_color = background_color
        OpenGL.GL.glClearColor(*self.background_color, 1)

        # setup vertex transformations
        self.rotation = [0,0,0]
        self.zoom = 0
        self.wanna_rotate = 0
        self.wanna_zoom = 0

        # create a dummy cube to make a display list
        dummy_cube = Cube()
        
        ### create display list ###
        self.cube_display_list = OpenGL.GL.glGenLists(1)
        OpenGL.GL.glNewList(self.cube_display_list, OpenGL.GL.GL_COMPILE)

        OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)

        for face, normal in zip(dummy_cube.faces, dummy_cube.normals): # take the surfaces one by one
            OpenGL.GL.glNormal3f(*normal)
            for vertex in face: # take the coordinates of each vertex in this face
                OpenGL.GL.glVertex3f(*dummy_cube.vertices[vertex]) 
        OpenGL.GL.glEnd()

        OpenGL.GL.glEndList()

        ### calculate center of all cubes ###
        all_cubes = []
        for cubes_list in self.coords_lists:
            all_cubes += cubes_list
        number_of_cubes = len(all_cubes)
        self.all_xs = np.empty(number_of_cubes, dtype = np.float32)
        self.all_ys = np.empty(number_of_cubes, dtype = np.float32)
        self.all_zs = np.empty(number_of_cubes, dtype = np.float32)

        # gather coordinates to calculate center
        for i, cube_instance in enumerate(all_cubes):
            self.all_xs[i] = cube_instance[0]
            self.all_ys[i] = cube_instance[1]
            self.all_zs[i] = cube_instance[2]

        self.center = np.array(((self.all_xs.max()+self.all_xs.min())/2, (self.all_ys.max()+self.all_ys.min())/2, (self.all_zs.max()+self.all_zs.min())/2))
        self.center += 0.5

        x_spread = max(abs(self.center[0]-max(self.all_xs)), abs(self.center[0]-min(self.all_xs)))
        y_spread = max(abs(self.center[1]-max(self.all_ys)), abs(self.center[1]-min(self.all_ys)))
        z_spread = max(abs(self.center[2]-max(self.all_zs)), abs(self.center[2]-min(self.all_zs)))
        self.initial_zoom = -(max((x_spread, y_spread, z_spread))*3+4)
        self.zoom = self.initial_zoom

        self.mainloop()

    def mainloop(self):
        while True:
            
            ### manage user input
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.wanna_rotate = -10
                    if event.key == pg.K_RIGHT:
                        self.wanna_rotate = 10
                    if event.key == pg.K_UP:
                        self.wanna_zoom = 2
                    if event.key == pg.K_DOWN:
                        self.wanna_zoom = -2

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.wanna_rotate = 0
                    if event.key == pg.K_DOWN or event.key == pg.K_UP:
                        self.wanna_zoom = 0

            self.rotation[2] += self.wanna_rotate
            if self.rotation[2] < 0:
                self.rotation[2] += 360
            if self.rotation[2] > 360:
                self.rotation[2] -= 360
            if not self.zoom + self.wanna_zoom > 0: # make it impossible to zoom past the object
                self.zoom += self.wanna_zoom 
            else:
                self.zoom = 0 # if we would make it past the object, bring the zoom to zero 
                if self.wanna_zoom < 0: # if we're trying to zoom back out make it possible
                    self.zoom += self.wanna_zoom
            ### manage user input ^ 

            OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
            OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)

            ### Generate transformation matrix
            OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
            OpenGL.GL.glLoadIdentity()

            OpenGL.GL.glEnable(OpenGL.GL.GL_COLOR_MATERIAL)

            pos = [0,0,1,0]
            diff = [1,1,1,0.2]
            amb = [1,1,1,0.2]

            OpenGL.GL.glLightfv(OpenGL.GL.GL_LIGHT0, OpenGL.GL.GL_POSITION, pos)
            OpenGL.GL.glLightfv(OpenGL.GL.GL_LIGHT0, OpenGL.GL.GL_DIFFUSE, diff)
            OpenGL.GL.glLightfv(OpenGL.GL.GL_LIGHT0, OpenGL.GL.GL_AMBIENT, amb)

            # push the objects back
            OpenGL.GL.glTranslate(0,0,self.zoom)
            # rotate objects around origin
            OpenGL.GL.glRotate(self.rotation[2], 0, 1, 0)
            # center objects around origin
            OpenGL.GL.glTranslate(-self.center[0], -self.center[1], -self.center[2])
            ### Generate transformation matrix ^

            # render the cubes
            for color, cubes_list in zip(self.colors_list, self.coords_lists): # take one list at a time
                OpenGL.GL.glColor3f(*color) # set the color
                
                for cube_pos in cubes_list:
                    OpenGL.GL.glPushMatrix()
                    OpenGL.GL.glTranslatef(*cube_pos)
                    OpenGL.GL.glCallList(self.cube_display_list)
                    OpenGL.GL.glPopMatrix()

            pg.display.flip()

            self.clock.tick(60)

    def quit(self):
        pg.quit()
        quit()
