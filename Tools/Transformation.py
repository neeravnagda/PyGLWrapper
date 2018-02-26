import math
import numpy
import pyrr


class Transformation(object):
    """This class is used to create, store and retrieve a transformation matrix"""

    def __init__(self):
        """The constructor"""

        # A translation vector
        self.m_translate = pyrr.vector3.create()
        self.m_translateMatrix = numpy.matrix(pyrr.matrix44.create_identity())
        # A rotation quaternion
        self.m_rotation = pyrr.quaternion.create()
        self.m_rotationMatrix = numpy.matrix(pyrr.matrix44.create_identity())
        # A scale vector
        self.m_scale = pyrr.vector3.create()
        self.m_scaleMatrix = numpy.matrix(pyrr.matrix44.create_identity())
        # The output matrix
        self.m_matrix = numpy.matrix(pyrr.matrix44.create_identity())
        # If the matrices are dirty and need to be recomputed
        self.m_isDirty = [False, False, False]

    def addTranslation(self, _translation):
        """Perform a relative transformation

        Args:
            _translation: A vector for translation as [dx, dy, dz]
        """

        self.m_translate += _translation
        self.m_isDirty[0] = True

    def setTranslation(self, _translation):
        """Set the transformation

        Args:
            _translation: A vector translation as [x, y, z]
        """

        self.m_translate = pyrr.vector3.create(_translation[0], _translation[1], _translation[2])
        self.m_isDirty[0] = True

    def addRotation(self, _axis, _angle, _radians=False):
        """Add a relative rotation

        Args:
            _axis: The axis to rotate around
            _angle: The angle to rotate by
            _radians: A bool if the value is in radians
        """

        # Make sure the values in the axis are floats
        axis = [float(i) for i in _axis]

        angle = _angle
        # If the angle is in degrees, convert to radians
        if _radians is not True:
            angle = math.radians(angle)

        q = pyrr.quaternion.create_from_axis_rotation(axis, angle)
        r = self.m_rotation

        # Multiply the two quaternions
        t3 = (q[3] * r[3]) - (r[0] * q[0]) - (r[1] * q[1]) - (r[2] * q[2])
        t0 = (r[3] * q[0]) + (r[0] * q[3]) - (r[1] * q[2]) + (r[2] * q[1])
        t1 = (r[3] * q[1]) + (r[0] * q[2]) + (r[1] * q[3]) - (r[2] * q[0])
        t2 = (r[3] * q[2]) - (r[0] * q[1]) + (r[1] * q[0]) + (r[2] * q[3])

        newQuat = pyrr.quaternion.create(t0, t1, t2, t3)
        self.m_rotation = pyrr.quaternion.normalize(newQuat)
        self.m_isDirty[1] = True

    def setRotation(self, _axis, _angle, _radians=False):
        """Set the rotation

        Args:
            _axis: The axis to rotate around
            _angle: The angle to rotate by
            _radians: A bool if the value is in radians
        """

        # Make sure the values in the axis are floats
        axis = [float(i) for i in _axis]

        angle = _angle
        # If the angle is in degrees, convert to radians
        if _radians is not True:
            angle = math.radians(angle)

        self.m_rotation = pyrr.quaternion.create_from_axis_rotation(axis, angle)
        self.m_isDirty[1] = True

    def addScale(self, _scale):
        """Add a relative scale

        Args:
            _scale: A vector representing the scale as [sx, sy, sz]
        """

        scale = []

        if type(_scale) is float:
            scale = [_scale] * 3

        elif type(_scale) is int:
            scale = [float(_scale)] * 3

        elif len(_scale) < 3:
            scale = [float(i) for i in _scale]

            while len(scale) < 3:
                scale.append(1.0)

        else:
            scale = [_scale[i] for i in range(3)]

        self.m_scale *= scale
        self.m_isDirty[2] = True

    def setScale(self, _scale):
        """Set the scale

        Args:
            _scale: A vector representing the scale as [sx, sy, sz]
        """

        scale = []

        if type(_scale) is float:
            scale = [_scale] * 3

        elif type(_scale) is int:
            scale = [float(_scale)] * 3

        elif len(_scale) < 3:
            scale = [float(i) for i in _scale]

            while len(scale) < 3:
                scale.append(1.0)

        else:
            scale = [_scale[i] for i in range(3)]

        self.m_scale = pyrr.vector3.create(scale[0], scale[1], scale[2])
        self.m_isDirty[2] = True

    @property
    def matrix(self):
        """Get the matrix
        This function recomputes the matrix if the translation, rotation or scale have changed.

        Returns:
            The matrix equal to the translate * rotate * scale
        """

        recompute = False
        if self.m_isDirty[0] is True:
            translateMatrix = pyrr.matrix44.create_from_translation(self.m_translate)
            self.m_translateMatrix = numpy.matrix(translateMatrix)
            recompute = True
            self.m_isDirty[0] = False
        if self.m_isDirty[1] is True:
            rotateMatrix = pyrr.matrix44.create_from_quaternion(self.m_rotation)
            self.m_rotationMatrix = numpy.matrix(rotateMatrix)
            recompute = True
            self.m_isDirty[1] = False
        if self.m_isDirty[2] is True:
            scaleMatrix = pyrr.matrix44.create_from_scale(self.m_scale)
            self.m_scaleMatrix = numpy.matrix(scaleMatrix)
            recompute = True
            self.m_isDirty[2] = False

        if recompute is True:
            self.m_matrix = self.m_scaleMatrix * self.m_rotationMatrix * self.m_translateMatrix

        return self.m_matrix

    @property
    def openGL(self):
        """Get the matrix as a numpy array, which is compatible with OpenGL

        Returns:
            self.m_matrix converted to a numpy array
        """

        return numpy.array(self.m_matrix)
