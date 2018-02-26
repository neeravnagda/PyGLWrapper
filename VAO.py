import OpenGL.GL as gl
import numpy


class VAO(object):
    """This class stores a vertex data object"""

    def __init__(self):
        """The constructor"""

        self.m_vao = gl.glGenVertexArrays(1)
        self.m_numVertices = 0
        self.m_numElements = 0

    @property
    def numVertices(self):
        return self.m_numVertices

    @numVertices.setter
    def numVertices(self, _numVertices):
        self.m_numVertices = _numVertices

    @property
    def numElements(self):
        return self.m_numElements

    @numElements.setter
    def numElements(self, _numElements):
        self.m_numElements = _numElements

    def draw(self):
        self.bind()
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.m_numVertices)
        self.unbind()

    def bind(self):
        """Bind the VAO"""

        gl.glBindVertexArray(self.m_vao)

    def unbind(self):
        """Unbind the VAO"""

        gl.glBindVertexArray(0)

    def genArrayBuffer(self, _data, _drawType=gl.GL_STATIC_DRAW):
        """Generate a vertex buffer object and initialise the data

        Args:
            _data: The data to pass to the GPU
            _drawType: The type of drawing, either gl.GL_STATIC_DRAW, gl.GL_DYNAMIC_DRAW or gl.GL_STREAM_DRAW
        """

        data = _data
        if type(_data) is list:
            data = numpy.array(_data, dtype=numpy.float32)

        self.bind()
        self.m_vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.m_vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, data.itemsize * len(data), data, _drawType)
        self.unbind()

    def genElementBuffer(self, _indices, _drawType=gl.GL_STATIC_DRAW):
        """Generate an element buffer object and initialise the data

        Args:
            _indices: The indices to pass to the GPU
            _drawType: The type of drawing, either gl.GL_STATIC_DRAW, gl.GL_DYNAMIC_DRAW or gl.GL_STREAM_DRAW
        """

        indices = _indices
        if type(_indices) is list:
            indices = numpy.array(_indices, dtype=numpy.uint32)

        self.bind()
        self.m_ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.m_ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, _drawType)
        self.unbind()

    def setVertexAttrib(self, _id, _numValues, _type, _normalise, _size, _offset):
        """Set a vertex attribute

        Args:
            _id: The location of the attribute
            _numValues: The number of values for the attribute
            _type: The type of data
            _normalise: A bool if the data should be normalised
            _size: The size of the data
            _offset: The number of bytes to offset
        """

        self.bind()
        gl.glVertexAttribPointer(_id, _numValues, _type, _normalise, _size, gl.ctypes.c_void_p(_offset))
        gl.glEnableVertexAttribArray(_id)
        self.unbind()
