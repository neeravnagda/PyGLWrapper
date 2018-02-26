import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders


class ShaderStore(object):
    """This class stores all of the shaders"""

    # A dictionary of shader programs
    m_shaders = {}
    # Currently active shader
    m_currentShader = None

    @staticmethod
    def createShader(_name, _vertexShader, _fragmentShader):
        """Create a shader

        Args:
            _vertexShader: The vertex shader file name
            _fragmentShader: The fragment shader file name
        """

        # Check if the shader does not already exist
        if _name not in ShaderStore.m_shaders:
            # Load and compile the vertex shader
            vs = file(_vertexShader).read()
            compiledVS = shaders.compileShader(vs, gl.GL_VERTEX_SHADER)
            # Load and compile the fragment shader
            fs = file(_fragmentShader).read()
            compiledFS = shaders.compileShader(fs, gl.GL_FRAGMENT_SHADER)
            # Create the shader program and store in the dictionary
            ShaderStore.m_shaders[_name] = shaders.compileProgram(compiledVS, compiledFS)

    @staticmethod
    def use(_name):
        """Use the specified shader

        Args:
            _name: The name of the shader to use

        Returns:
            True if the shader exists
            False if the shader does not exist
        """

        # Check if the shader exists
        if _name in ShaderStore.m_shaders:
            gl.glUseProgram(ShaderStore.m_shaders[_name])
            ShaderStore.m_currentShader = _name
            return True
        elif _name == 0:
            gl.glUseProgram(0)
            ShaderStore.m_currentShader = None
            return True
        else:
            return False

    @staticmethod
    def getShader(_name):
        """Get a shader with the specified name

        Args:
            _name: The name of the shader to get

        Returns:
            The shader if it exists
            None if the shader does not exist
        """

        # Check if the shader exists
        if _name in ShaderStore.m_shaders:
            return ShaderStore.m_shaders[_name]
        else:
            return None

    @staticmethod
    def getCurrentShader():
        """Get the shader currently in use"""

        if ShaderStore.m_currentShader is not None:
            return ShaderStore.m_shaders[ShaderStore.m_currentShader]
        else:
            return None
