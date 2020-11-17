import numpy as np


def LoadOBJ(path):
    verts = []
    surfaces = []
    normals = []
    textureVerts = []

    # open .obj file and read data
    f = open(path, 'r')
    for line in f:
        if line[0] == 'v':
            # if line starts with 'v ', its a vertex, and gets added to the vertex list
            if line[1] == ' ':
                vert = line[2:].split()
                verts.append((float(vert[0]), float(vert[1]), float(vert[2])))
            # if line starts with 'vn', its a normal, and gets added to the temp_normals list
            elif line[1] == 'n':
                normal = line[3:].split()
                normals.append((float(normal[0]), float(normal[1]), float(normal[2])))
            # if line starts with 'vt' it's a texture coordinate, and gets added to temp_textureVerts
            elif line[1] == 't':
                textureVert = line[3:].split()
                textureVerts.append((float(textureVert[0]), float(textureVert[1]), float(textureVert[2])))
        # if line starts with 'f', its a face/surface, and needs to be processed
        if line[0] == 'f':
            # create empty numpy arrays based off of the number of vertices, in try block as will fail if np array

            if normals == []:
                normals = [None] * len(verts)
            if textureVerts == []:
                textureVerts = [None] * len(verts)

            # remove the f from the line, and get the list of vertex/textureVert/normal
            # first number is the index of the vertex in verts[], starting at 1
            # second number is the index of the corresponding temp_textureVert[], starting at 1
            # third number is the index of the corresponding temp_normal[], starting at 1
            surface = line[2:].split()
            for vertex in surface:
                pair = []
                vertex = vertex.split('/')
                vertex_num = int(vertex[0]) - 1
                textureVert_num = int(vertex[1]) - 1
                normal_num = int(vertex[2]) - 1
                point = (int(vertex[0]) - 1, int(vertex[2]) - 1)
                pair.append(point)
                surfaces.append(pair)


    f.close()

    return {'verts': verts, 'surfs': surfaces, 'normals': normals}
