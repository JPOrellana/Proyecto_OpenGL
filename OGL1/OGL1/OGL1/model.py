from numpy import array, float32
from OpenGL.GL import *
import pygame
import glm
from obj import Obj

class Model(object):

	def __init__(self, file):

		self.obj = Obj(file)
		self.data = self.obj.data

		self.vertexBuffer = array(self.data, dtype = float32)

		self.VBO = glGenBuffers(1)

		self.VAO = glGenVertexArrays(1)

		self.position = glm.vec3(0,0,0)
		self.rotation = glm.vec3(0,0,0)
		self.scale = glm.vec3(1,1,1)


	def loadTexture(self, texturePath):
		self.textureSurface = pygame.image.load(texturePath)
		self.textureData	= pygame.image.tostring(self.textureSurface, "RGB", True)
		self.textureBuffer	= glGenTextures(1)


	def getModelMatrix(self):
		identity = glm.mat4(1)

		translationMatrix = glm.translate(identity, self.position)

		pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))		
		yaw	  = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))		
		roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))	

		rotationMatrix = pitch * yaw * roll

		scaleMatrix = glm.scale(identity, self.scale)

		return translationMatrix * rotationMatrix * scaleMatrix


	def render(self):

		glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
		glBindVertexArray(self.VAO)

		glBufferData(target = GL_ARRAY_BUFFER,				
					 size = self.vertexBuffer.nbytes,		
					 data = self.vertexBuffer,				
					 usage = GL_STATIC_DRAW)              



		glVertexAttribPointer(index = 0,						
							  size	= 3,							
							  type	= GL_FLOAT,					
							  normalized = GL_FALSE,			
							  stride = 4 * 8,					
							  pointer = ctypes.c_void_p(0))		

		glEnableVertexAttribArray(0)


		glVertexAttribPointer(index = 1,						
							  size	= 2,								
							  type	= GL_FLOAT,					
							  normalized = GL_FALSE,			
							  stride = 4 * 8,					
							  pointer = ctypes.c_void_p(4 * 3))	
		glEnableVertexAttribArray(1)



		glVertexAttribPointer(index = 2,						
							  size	= 3,								
							  type	= GL_FLOAT,					
							  normalized = GL_FALSE,			
							  stride = 4 * 8,					
							  pointer = ctypes.c_void_p(4 * 5))	
		glEnableVertexAttribArray(2)

		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.textureBuffer)
		glTexImage2D(GL_TEXTURE_2D,							
					 0,										
					 GL_RGB,								
					 self.textureSurface.get_width(),		
					 self.textureSurface.get_height(),		
					 0,										
					 GL_RGB,								
					 GL_UNSIGNED_BYTE,						
					 self.textureData)						

		glGenerateTextureMipmap(self.textureBuffer)

		glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertexBuffer / 8)))