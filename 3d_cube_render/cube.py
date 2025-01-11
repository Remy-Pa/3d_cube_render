import OpenGL
import numpy as np

class Cube:
    def __init__(self, coords = (0,0,0)):
        self.coords = x, y, z = coords
        self.vertices = np.array((
            (x,  y,  z), (x, y+1, z),
            (x+1, y+1,  z), (x+1, y, z), 
            (x,  y, z+1), (x, y+1, z+1),
            (x+1, y+1, z+1), (x+1, y, z+1)
            ))
        self.edges = ( # the index of the vertices which are connected
            (0,1),
            (0,3),
            (0,4),
            (1,2),
            (1,5),
            (2,3),
            (2,6),
            (3,7),
            (4,5),
            (4,7),
            (5,6),
            (6,7)
        )
        self.faces = ( # the index of the vertices which makeup the faces
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 3, 7, 4),
            (1, 2, 6, 5)
        )
        self.normals = (
            (0,0,-1),
            (0,0,1),
            (-1,0,0),
            (1,0,0),
            (0,-1,0),
            (0,1,0),
        )
    
    def draw_cube(self):
        '''Draws cube onto an opengl window. Can be pretty slow, consider using a display list'''
        contour_color = (0.0, 0.0, 0.3)
        face_color = (0.5, 0.5, 0.5)

        OpenGL.GL.glBegin(OpenGL.GL.GL_QUADS)
        OpenGL.GL.glColor3f(*face_color)
        for face in self.faces: # take the surfaces one by one
            for vertex in face: # take the coordinates of each vertex in this face
                OpenGL.GL.glVertex3f(*self.vertices[vertex]) 
        OpenGL.GL.glEnd()

        # draw darker contours
        OpenGL.GL.glBegin(OpenGL.GL.GL_LINES)
        OpenGL.GL.glColor3f(*contour_color)
        for edge in self.edges: # take the edges one by one
            for vertex in edge: # take the coordinates of each vertex in this edge
                OpenGL.GL.glVertex3f(*self.vertices[vertex]) # feed each vertex to the OpenGL.GL.GL_LINES environment so it draws the vertices

        OpenGL.GL.glEnd()
