import glfw


class Window(object):
    """This class is used to manage the window"""

    def __init__(self, _width, _height, _title, _monitor=None, _share=None):
        """Construct the Window class

        This function stores all the information for the window, but does not create the window

        Args:
            _width: The width of the window
            _height: The height of the window
            _title: The title for the window
            _monitor: The monitor to display on
            _share: For context object sharing
        """

        self.m_width = _width
        self.m_height = _height
        self.m_title = _title
        self.m_monitor = _monitor
        self.m_share = _share
        self.m_window = None

    def createWindow(self):
        """Create the GLFW window

        Returns:
            True if the window was successfuly created
            False if the window was not created
        """

        self.m_window = glfw.create_window(self.m_width, self.m_height, self.m_title, self.m_monitor, self.m_share)
        if not Window:
            return False
        else:
            return True

    def makeCurrent(self):
        """Make the window context current"""

        glfw.make_context_current(self.m_window)

    @property
    def shouldClose(self):
        """Check if the window should close

        Returns:
            Bool if the window should close
        """

        return glfw.window_should_close(self.m_window)

    def swapBuffers(self):
        """Swap the OpenGL buffers"""

        glfw.swap_buffers(self.m_window)

    @property
    def window(self):
        """Return the window"""

        return self.m_window
