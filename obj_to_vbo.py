import numpy as np


def LoadOBJ(path, color):
    verts = []
    surfaces = []
    normals = []
    vbo = []
    textureVerts = []

    # open .obj file and read data
    f = open(path, 'r')
    for line in f:
        if line[0] == 'v':
            # if line starts with 'v ', its a vertex, and gets added to the vertex list
            if line[1] == ' ':
                vert = line[2:].split()
                verts.append([float(vert[0]), float(vert[1]), float(vert[2])])
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
            pass
            # remove the f from the line, and get the list of vertex/textureVert/normal
            # first number is the index of the vertex in verts[], starting at 1
            # second number is the index of the corresponding temp_textureVert[], starting at 1
            # third number is the index of the corresponding temp_normal[], starting at 1
            surface = line[2:].split()
            for vertex in surface:
                vertex = vertex.split('/')
                point=[]
                point.extend(verts[int(vertex[0]) - 1])
                point.extend(color)
                point.extend(normals[int(vertex[2]) - 1])
                point.append(textureVerts[int(vertex[1])-1][0])
                point.append(textureVerts[int(vertex[1])-1][1])

                vbo.append(tuple(point))
    f.close()

    return vbo


#print(LoadOBJ("resources/models/box_tetris_piece.obj", [0, 0, 1]))
