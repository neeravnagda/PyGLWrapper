import numpy
import pyrr


class VPMatrix(object):
    """This class is used to create, store and retrieve the view projection matrix"""

    def __init__(self):
        """The constructor"""

        # The view matrix
        self.m_view = numpy.matrix(pyrr.matrix44.create_identity())
        # The projection matrix
        self.m_projection = numpy.matrix(pyrr.matrix44.create_identity())
        # The output view-projection matrix
        self.m_matrix = numpy.matrix(pyrr.matrix44.create_identity())
        # Whether the VP matrix needs to be recomputed
        self.m_isDirty = False

    def createViewMatrix(self, _eye, _target, _up):
        """Create the view matrix from a lookat function

        Args:
            _eye: The eye position as a list [x,y,z]
            _target: The target position as a list [x,y,z]
            _up: The up vector as a list [x,y,z]
        """

        eye = [float(i) for i in _eye]
        eye = numpy.array(eye)
        target = [float(i) for i in _target]
        target = numpy.array(target)
        up = [float(i) for i in _up]
        up = numpy.array(up)

        viewMat = pyrr.matrix44.create_look_at(eye, target, up)
        self.m_view = numpy.matrix(viewMat)
        self.m_isDirty = True

    def createOrthogonalMatrix(self, _left, _right, _top, _bottom, _near, _far):
        """Create an orthogonal projection matrix

        Args:
            _left: The left coordinate of the frustum
            _right: The right coordinate of the frustum
            _top: The top coordinate of the frustum
            _bottom: The bottom coordinate of the frustum
            _near: The near clipping plane
            _far: The far clipping plane
        """

        projMat = pyrr.matrix44.create_orthogonal_projection_matrix(_left, _right, _top, _bottom, _near, _far)
        self.m_projection = numpy.matrix(projMat)
        self.m_isDirty = True

    def createPerspectiveMatrix(self, _fov, _aspect, _near, _far):
        """Create a perspective projection matrix

        Args:
            _fov: The field of view
            _aspect: The aspect ratio for the window
            _near: The near clipping plane
            _far: The far clipping plane
        """

        projMat = pyrr.matrix44.create_perspective_projection(_fov, _aspect, _near, _far)
        self.m_projection = numpy.matrix(projMat)
        self.m_isDirty = True

    @property
    def viewMatrix(self):
        return self.m_view

    @property
    def projectionMatrix(self):
        return self.m_projection

    @property
    def matrix(self):
        """Get the matrix
        This function recomputes the matrix if the view or perspective matrices have changed.

        Returns:
            The matrix equal to the projection * view as a numpy matrix
        """

        if self.m_isDirty is True:
            # Recompute the matrix
            self.m_matrix = self.m_view * self.m_projection
            self.m_isDirty = False

        return self.m_matrix

    @property
    def openGL(self):
        """Get the matrix as a numpy array, which is compatible with OpenGL

        Returns:
            self.m_matrix converted to a numpy array
        """

        return numpy.array(self.m_matrix)
