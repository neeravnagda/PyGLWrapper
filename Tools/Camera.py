import math
import pyrr
from VPMatrix import VPMatrix


class Camera(object):
    """This class provides methods for transforming a first person camera"""

    def __init__(self, _position=[0.0, 0.0, 0.0], _target=[0.0, 0.0, -2.0], _up=[0.0, 1.0, 0.0]):
        """The constructor

        Args:
            _position: The position of the camera
            _target: The target position to look at
            _up: The up vector
        """

        # Global coordinate frames
        # The position of the camera
        self.m_position = pyrr.vector3.create(_position[0], _position[1], _position[2])
        # The point to look at
        self.m_target = pyrr.vector3.create(_target[0], _target[1], _target[2])
        # The up direction
        self.m_up = pyrr.vector3.create(_up[0], _up[1], _up[2])

        # Local coordinate frames
        # The direction of the camera
        self.m_n = None
        # The local vertical direction
        self.m_u = None
        # The local horizontal direction
        self.m_v = None
        # Calculate the values for m_n, m_u, m_v
        self.calculateLocal()

        # Create the view component of the VP matrix
        self.m_vpMatrix = VPMatrix()
        self.m_vpMatrix.createViewMatrix(self.m_position, self.m_target, self.m_up)

    def perspectiveProjection(self, _fov, _aspect, _near, _far):
        self.m_vpMatrix.createPerspectiveMatrix(_fov, _aspect, _near, _far)

    def orthographicProjection(self, _left, _right, _top, _bottom, _near, _far):
        self.m_vpMatrix.createOrthogonalMatrix(_left, _right, _top, _bottom, _near, _far)

    @property
    def viewMatrix(self):
        return self.m_vpMatrix.viewMatrix

    @property
    def projectionMatrix(self):
        return self.m_vpMatrix.projectionMatrix

    @property
    def matrix(self):
        return self.m_vpMatrix.matrix

    @property
    def openGL(self):
        return self.m_vpMatrix.openGL

    def calculateLocal(self):
        """Calculate the local coordinate frame"""

        # Calculate the vectors
        n = self.m_target - self.m_position
        u = pyrr.vector3.cross(self.m_up, n)
        v = pyrr.vector3.cross(n, u)

        # Normalise and set the vectors
        self.m_n = pyrr.vector3.normalize(n)
        self.m_u = pyrr.vector3.normalize(u)
        self.m_v = pyrr.vector3.normalize(v)

    @property
    def position(self):
        """Get the position of the camera

        Returns:
            The position of the camera
        """

        return self.m_position

    @position.setter
    def position(self, _pos):
        """Set the position of the camera

        Args:
            _pos: A new camera position as [x,y,z]
        """

        self.m_position = pyrr.vector3.create(_pos[0], _pos[1], _pos[2])
        self.calculateLocal()

    @property
    def target(self):
        """Get the target position

        Returns:
            The target position
        """

        return self.m_target

    @target.setter
    def target(self, _pos):
        """Set the target position

        Args:
            _pos: A new camera target as [x,y,z]
        """

        self.m_target = pyrr.vector3.create(_pos[0], _pos[1], _pos[2])
        self.calculateLocal()

    @property
    def n(self):
        """Return the direction of the camera

        Returns:
            The n vector
        """

        return self.m_n

    @property
    def u(self):
        """Return the local up direction of the camera

        Returns:
            The u vector
        """

        return self.m_u

    @property
    def v(self):
        """Return the local horizontal direction of the camera

        Returns:
            The v vector
        """

        return self.m_v

    def move(self, _pos):
        """Move both the position and the target

        Args:
            _pos: A relative offset to move by
        """

        x, y, z = [i + j for i, j in zip(self.m_position, _pos)]
        self.m_position = pyrr.vector3.create(x, y, z)
        x, y, z = [i + j for i, j in zip(self.m_target, _pos)]
        self.m_target = pyrr.vector3.create(x, y, z)

    def rotateHorizontal(self, _angle, _radians=False):
        """Rotate the camera about the Y axis

        Args:
            _angle: The angle to rotate about
            _radians: A boolean if the angle is already specified in radians
        """

        # Move the position to the origin and maintain a relative target
        relativeTarget = self.m_target - self.m_position

        # Calculate the angle to rotate
        angle = _angle
        if _radians is not True:
            angle = math.radians(angle)

        # Compute cos and sin of the angle
        cosTheta = math.cos(angle)
        sinTheta = math.sin(angle)

        # Rotate using a 2D rotation matrix
        # [x'] = [cos(a)  -sin(a)] [x]
        # [y'] = [sin(a)   cos(a)] [y]
        # Then translate back
        x = cosTheta * relativeTarget[0] - sinTheta * relativeTarget[2] + self.m_position[0]
        z = sinTheta * relativeTarget[0] + cosTheta * relativeTarget[2] + self.m_position[2]

        self.m_target = pyrr.vector3.create(x, self.m_target[1], z)
        self.calculateLocal()

    def rotateVertical(self, _angle, radians=False):
        """Rotate the camera vertically in screen space

        Args:
            _angle: The angle to rotate about
            _radians: A boolean if the angle is already specified in radians

        """
        angle = _angle
        if radians is not True:
            angle = math.radians(angle)

        quat = pyrr.quaternion.create_from_axis_rotation(self.m_u, angle)

        # Move the position to the origin and maintain a relative target
        relativeTarget = self.m_target - self.m_position

        # Rotate the relative target using the quaternion
        # Then translate back
        self.m_target = pyrr.quaternion.apply_to_vector(quat, relativeTarget) + self.m_position
