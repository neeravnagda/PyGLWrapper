import numpy
import pyrr
from Camera import Camera
from Transformation import Transformation


class MVP(object):

    def __init__(self, _camera=None, _transformation=None):
        if _camera is None:
            self.m_camera = Camera()
        else:
            self.m_camera = _camera
        if _transformation is None:
            self.m_transfomation = Transformation()
        else:
            self.m_transfomation = _transformation

    @property
    def camera(self):
        return self.m_camera

    @camera.setter
    def camera(self, _camera):
        self.m_camera = _camera

    @property
    def transformation(self):
        return self.m_transfomation

    @transformation.setter
    def transformation(self, _transformation):
        self.m_transfomation = _transformation

    @property
    def M(self):
        return self.m_transfomation.openGL

    @property
    def MV(self):
        return numpy.array(self.m_transfomation.matrix * self.m_camera.viewMatrix)

    @property
    def MVP(self):
        return numpy.array(self.m_transfomation.matrix * self.m_camera.matrix)

    @property
    def N(self):
        n = pyrr.matrix33.create_from_matrix44(self.MV)
        return pyrr.matrix33.inverse(n)
