class Obj(object):
	def __init__(self, filename):

		with open(filename,"r") as file:
			self.lines = file.read().splitlines()

		self.vertices = []
		self.texcoords = []
		self.normals = []
		self.faces = []

		for line in self.lines:

			try:
				prefix, value = line.split(" ",1)
			except: 
				continue

			if prefix == "v":
				self.vertices.append(list(map(float,value.split(" "))))
			elif prefix == "vt":
				uvw = list(map(float,value.split(" ")))
				self.texcoords.append(uvw[:2])
			elif prefix == "vn": 
				self.normals.append(list(map(float,value.split(" "))))
			if prefix == "f":
				self.faces.append([list(map(int, vert.split("/"))) for vert in value.split(" ")])

		self.data = self.get_model_data()

	def get_model_data(self):

		data = []

		for face in self.faces:
			for vert in face:

				vertex_index = vert[0] - 1
				vertex_coords = self.vertices[vertex_index]

				texture_coords = (0, 0) 
				normal_coords = (0, 0, 0) 

				if len(vert) > 1 and vert[1] > 0:
					texture_coords = self.texcoords[vert[1] - 1]

				if len(vert) > 2 and vert[2] > 0:
					normal_coords = self.normals[vert[2] - 1]

				data.extend(vertex_coords)
				data.extend(texture_coords)
				data.extend(normal_coords)

		return data
