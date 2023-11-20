
# To use this, you must:
# - Use MeshPlayerGen.cs
# - Add `ShaderMotion` & `ShaderMotion2` UV maps to every affected mesh
# - Run the script

import collections
import math
import pathlib

import bpy


PATH = r"C:\Users\user\Unity Projects\Your project\whereveryourmeshis.mesh.dump.txt"
PATH = pathlib.Path(PATH)

with open(PATH, 'r', encoding='utf-8') as fp:
    data = fp.read().replace('\r\n', '\n').strip().split('\n')

markers = []
vertices = []
normals = []
tangents = []
uv0s = []
uv1s = []

mapp = {
    'vertex': vertices,
    'normal': normals,
    'tangent': tangents,
    'uv0': uv0s,
    'uv1': uv1s,
}

for line in data:
    inst, *parts = line.split(" ")

    if inst == "mesh":
        markers.append((int(parts[0]), parts[1]))
        continue

    mapp[inst].append([float(x) for x in parts])

print(f"{len(vertices)=} {len(normals)=} {len(tangents)=} {len(uv0s)=} {len(uv1s)=}")
markers = [(index, bpy.data.objects[name]) for index, name in markers]
print(markers)

# this prevents it from going on forever if i made a mistake :)
stop_after = 1_000_000_000
vertex_count = len(vertices)

# first we're going to make a terrible lookup table using bands of Z coordinates
# this just reduces the amount of vertices we have to check when finding a match
loop_bands = collections.defaultdict(lambda: collections.defaultdict(list))

for _, b_object in markers:
    mesh = b_object.data

    if 'ShaderMotion' not in mesh.uv_layers:
        mesh.uv_layers.new(name='ShaderMotion')
    if 'ShaderMotion2' not in mesh.uv_layers:
        mesh.uv_layers.new(name='ShaderMotion2')

    for polygon in mesh.polygons:
        for loopindex in polygon.loop_indices:
            meshloop = mesh.loops[loopindex]
            meshvertex = mesh.vertices[meshloop.vertex_index]
            vertex_coord = b_object.matrix_world @ meshvertex.co

            loop_bands[mesh][int(vertex_coord[2] * 100)].append(loopindex)

# now try to match every unity vert to a blender vert
for index, (vertex, normal, tangent, uv0, uv1) in enumerate(zip(vertices, normals, tangents, uv0s, uv1s)):
    b_object = max([m for m in markers if m[0] <= index], key=lambda p: p[0])[1]
    mesh = b_object.data

    target_uv = mesh.uv_layers['ShaderMotion']
    target_uv2 = mesh.uv_layers['ShaderMotion2']

    blender_vertex = [-vertex[0], -vertex[2], vertex[1]]

    matches_found = set()

    lut_index = int(blender_vertex[2] * 100)

    # make sure we check adjacent bands in case we're on a boundary
    for band_index in range(lut_index - 1, lut_index + 2):
        band = loop_bands[mesh][band_index]
        for loopindex in band:
            meshloop = mesh.loops[loopindex]
            meshvertex = mesh.vertices[meshloop.vertex_index]
            meshuvloop = target_uv.data[loopindex]
            meshuvloop2 = target_uv2.data[loopindex]

            vertex_coord = b_object.matrix_world @ meshvertex.co

            x_diff = vertex_coord[0] - blender_vertex[0]
            y_diff = vertex_coord[1] - blender_vertex[1]
            z_diff = vertex_coord[2] - blender_vertex[2]

            total_dist = math.sqrt(pow(x_diff, 2.0) + pow(y_diff, 2.0) + pow(z_diff, 2.0))

            if total_dist < 0.0001:
                matches_found.add(meshloop.vertex_index)
                meshuvloop.uv.x = uv1[0]
                meshuvloop.uv.y = uv1[1]
                meshuvloop2.uv.x = uv1[2]
                meshuvloop2.uv.y = uv1[3]

    if index > stop_after:
        break

    print(f"{index}/{len(vertices)} {mesh=} {blender_vertex=} {len(matches_found)}")
