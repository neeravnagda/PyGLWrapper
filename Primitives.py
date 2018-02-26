import math
import VAO
import OpenGL.GL as gl


class Primitives(object):
    """This class allows the creation of primitive shapes and stores them as VAOs"""

    # A dictionary of VAOs mapped to names
    s_VAOs = {}

    def __init__(self):
        """The constructor"""

        pass

    def draw(self, _name):
        if _name in Primitives.s_VAOs:
            Primitives.s_VAOs[_name].draw()
        else:
            print "Primitive does not exist"

    def createCube(self, _name, _length=1.0, _subdivisionsX=1, _subdivisionsY=1, _subdivisionsZ=1):
        '''Create a cube primitive'''

        if _name in Primitives.s_VAOs:
            print "VAO already exists"
            return

        minC = -_length / 2.0
        maxC = _length / 2.0

        # The net looks like:
        #    4      (top)
        #  3 1 2    (1 is front)
        #    5      (bottom)
        #    6      (at the back)

        #           Vertex            Normal
        face1 = [minC, minC, maxC, 0.0, 0.0, 1.0,
                 maxC, minC, maxC, 0.0, 0.0, 1.0,
                 maxC, maxC, maxC, 0.0, 0.0, 1.0,
                 maxC, maxC, maxC, 0.0, 0.0, 1.0,
                 minC, maxC, maxC, 0.0, 0.0, 1.0,
                 minC, minC, maxC, 0.0, 0.0, 1.0]

        face2 = [maxC, minC, maxC, -1.0, 0.0, 0.0,
                 maxC, minC, minC, -1.0, 0.0, 0.0,
                 maxC, maxC, minC, -1.0, 0.0, 0.0,
                 maxC, minC, maxC, -1.0, 0.0, 0.0,
                 maxC, maxC, minC, -1.0, 0.0, 0.0,
                 maxC, maxC, maxC, -1.0, 0.0, 0.0]

        face3 = [minC, minC, minC, 1.0, 0.0, 0.0,
                 minC, minC, maxC, 1.0, 0.0, 0.0,
                 minC, maxC, maxC, 1.0, 0.0, 0.0,
                 minC, minC, minC, 1.0, 0.0, 0.0,
                 minC, maxC, maxC, 1.0, 0.0, 0.0,
                 minC, maxC, minC, 1.0, 0.0, 0.0]

        face4 = [minC, maxC, maxC, 0.0, -1.0, 0.0,
                 maxC, maxC, maxC, 0.0, -1.0, 0.0,
                 maxC, maxC, minC, 0.0, -1.0, 0.0,
                 minC, maxC, maxC, 0.0, -1.0, 0.0,
                 maxC, maxC, minC, 0.0, -1.0, 0.0,
                 minC, maxC, minC, 0.0, -1.0, 0.0]

        face5 = [maxC, minC, minC, 0.0, 1.0, 0.0,
                 minC, minC, minC, 0.0, 1.0, 0.0,
                 minC, minC, maxC, 0.0, 1.0, 0.0,
                 maxC, minC, minC, 0.0, 1.0, 0.0,
                 minC, minC, maxC, 0.0, 1.0, 0.0,
                 maxC, minC, maxC, 0.0, 1.0, 0.0]

        face6 = [maxC, minC, minC, 0.0, 0.0, -1.0,
                 minC, minC, minC, 0.0, 0.0, -1.0,
                 maxC, maxC, minC, 0.0, 0.0, -1.0,
                 minC, minC, minC, 0.0, 0.0, -1.0,
                 minC, maxC, minC, 0.0, 0.0, -1.0,
                 maxC, maxC, minC, 0.0, 0.0, -1.0]

        vertices = face1 + face2 + face3 + face4 + face5 + face6

        # Create the VAO and assign data

        vao = VAO.VAO()
        vao.genArrayBuffer(vertices)
        vao.numVertices = len(vertices) / 6

        # Set the attrib pointers
        vao.setVertexAttrib(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, 0)
        vao.setVertexAttrib(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, 12)

        Primitives.s_VAOs[_name] = vao
