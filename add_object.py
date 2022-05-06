from time import sleep
import bpy
from bpy.types import Mesh, Object, Collection
from typing import Tuple, List


def mesh_new(name : str) -> Mesh:
    if name in bpy.data.meshes:
        mesh = bpy.data.meshes[name]
        mesh.clear_geometry()
    else:
        mesh = bpy.data.meshes.new(name)

    return mesh
    
def obj_new(mesh_name : str, mesh : Mesh, material="") -> Object:
    
    if mesh_name in bpy.data.objects:
        obj = bpy.data.objects[mesh_name]
        obj.data = mesh
    else:
        obj = bpy.data.objects.new(mesh_name, mesh)

    obj.data.materials.clear()
    obj.data.materials.append(material)
    # obj.data.materials.insert(material)
    return obj

def obj_to_col(obj : Object, col : Collection) -> None:
    for c in bpy.data.collections:
        if obj.name in c.objects:
            col.objects.unlink(obj)
    for sc in bpy.data.scenes:
        if obj.name in sc.collection.objects:
            sc.collection.objects.unlink(obj)

    col.objects.link(obj)

def house(number_of_walls):
    build_mesh(number_of_walls)

def build_mesh(x, y, z, start_x, start_y, start_z) -> Tuple[List[Tuple]]:
    # z = 1
    # start = -1,0
    x_right = start_x + y
    y_outer = start_y + x
    z_max = start_z + z
    print(f'start_x: {start_x}')
    print(f'start_y: {start_y}')

    vertices = [
        ( start_y, start_x, start_z), # 1
        ( y_outer, start_x, start_z), # 2
        ( y_outer, x_right, start_z), # 3 
        ( start_y, x_right, start_z), # 4
        ( start_y, start_x, z_max), # 1
        ( y_outer, start_x, z_max), # 2
        ( y_outer, x_right, z_max), # 3 
        ( start_y, x_right, z_max), # 4
    ]
    edges = [
        ()
    ]
    faces = [
        (3, 2, 1, 0),
        (1, 2, 6, 5),
        (4, 5, 6, 7),
        (3, 7, 6, 2),
        (1, 5, 4, 0),
        (0, 4, 7, 3)
    ]

    return vertices, edges, faces

def build_house():
    house_size_x = 10
    house_size_y = 8
    house_size_z = 2
    wall_width = 0.1
    covering_width = 0.2
    columns_width = 0.2
    assert house_size_y >= 2

    create_basement(house_size_x, house_size_y)
    create_covering(house_size_x, house_size_y, house_size_z, covering_width)
    create_colums(house_size_x, house_size_y, house_size_z, columns_width)
    create_floor()
    create_walls2(house_size_x, house_size_y, house_size_z, wall_width, covering_width, covering_width)
    # create_walls(width, depth, height, number_of_parts)

def create_basement(house_size_x, house_size_y):
    material = bpy.data.materials['basement']
    z = 1
    start_x = 0
    start_y = 0
    start_z = -1
    name = "basement"
    create_mesh(name, material, house_size_x, z, house_size_y, start_x, start_y, start_z)

def create_covering(house_size_x, house_size_y, house_size_z, covering_width):
    material = bpy.data.materials['wood']
    # name = "covering"
    wall_x = covering_width
    wall_y = 1
    wall_z = covering_width
    start_x = 0
    start_y = 0
    start_z = 0
    offset = 0
    otstup = covering_width
    
    for floor in range(0, 2):
        name = f'covering_{floor}'
        create_y_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup)
        wall_x = 1
        wall_y = covering_width
        create_x_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup)
        start_z = house_size_z + covering_width
        wall_x = covering_width
        wall_y = 1

def create_walls2(house_size_x, house_size_y, house_size_z, wall_width, start_z, otstup):
    material = bpy.data.materials['wall']
    name = "wall"
    wall_x = wall_width
    wall_y = 2
    wall_z = house_size_z
    offset = 0.05
    # wall_count = house_size_y / wall_y
    start_x = offset
    start_y = 0
    #otstup = 0.2
    
    create_y_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup)
    wall_x = 2
    wall_y = wall_width
    start_x = 0
    start_y = offset
    create_x_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup)

def create_y_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup = 0.0):
    wall_count = house_size_y / wall_y
    for xxx in range(0, 2):
        # height = house_size_z / column_z
        for yyy in range(0, int(wall_count)):
            if yyy == 0:
                _wall_y = wall_y - otstup
                _start_y = start_y + otstup
            elif yyy == int(wall_count) -1:
                _wall_y = wall_y - otstup
            else:
                _wall_y = wall_y
            for zzz in range(0, 1):
                name = f'{name}_{xxx}_{yyy}_{zzz}_y'
                # print(name, start_z, wall_z)
                _start_z = start_z
                create_mesh(name, material, wall_x, wall_z, _wall_y, _start_y, start_x, _start_z)
                _start_z += wall_z
            _start_z = start_z
            _start_y += _wall_y
        start_x = house_size_x - wall_x - offset
        _start_y = 0

def create_x_axes(name, material, house_size_x, house_size_y, wall_x, wall_y, wall_z, start_x, start_y, start_z, offset, otstup = 0.0):
    wall_count = house_size_x / wall_x
    for xxx in range(0, 2):
        # height = house_size_z / column_z
        for yyy in range(0, int(wall_count)):
            if yyy == 0:
                _wall_x = wall_x - otstup
                _start_x = start_x + otstup
            elif yyy == int(wall_count) -1:
                _wall_x = wall_x - otstup
            else:
                _wall_x = wall_x
            for zzz in range(0, 1):
                name = f'{name}_{xxx}_{yyy}_{zzz}_x'
                # print(name, start_z, wall_z)
                _start_z = start_z
                create_mesh(name, material, _wall_x, wall_z, wall_y, start_y, _start_x, _start_z)
                _start_z += wall_z
            _start_z = start_z
            _start_x += _wall_x
        start_y = house_size_y - wall_y - offset
        _start_x = 0

def create_floor():
    pass

def create_colums(house_size_x, house_size_y, house_size_z, columns_width):
    material = bpy.data.materials['wood']
    column_x = columns_width
    column_z = 1
    column_y = columns_width
    start_x = 0
    start_y = 0
    start_z = columns_width

    for xxx in range(0, 2):
        # height = house_size_z / column_z
        for yyy in range(0, 2):
            height = house_size_z / column_z
            for zzz in range(0, int(height)):
                if zzz == 0:
                    _start_z = start_z - columns_width
                    _column_z = column_z + columns_width
                elif zzz == int(height) - 1:
                    _column_z = column_z + columns_width
                else:
                    # _start_z = start_z
                    _column_z = column_z
                name = f'column_{xxx}_{yyy}_{zzz}'
                create_mesh(name, material, column_x, _column_z, column_y, start_y, start_x, _start_z)
                _start_z += _column_z
            #_start_z = 0.2
            start_y = house_size_y - column_y
        start_y = 0
        start_x = house_size_x - column_x

def create_walls(width, depth, height, number_of_parts):
    material = bpy.data.materials['wall']
    start_y = 0
    start_z = 0
    for wall in range(0, 2):
        start_x = depth

        for part in range(0, number_of_parts):
            name = f"wall_{wall}_{part}"
            create_mesh(name, material, depth, height, width, start_x, start_y, start_z)
            start_x += width

        start_y = (width * number_of_parts) + depth

    start_x = 0
    for wall in range(0, 2):
        start_y = depth

        for part in range(0, number_of_parts):
            name = f"wall2_{wall}_{part}"
            create_mesh(name, material, width, height, depth, start_x, start_y, start_z)
            start_y += width

        start_x = (width * number_of_parts) + depth

def create_mesh(mesh_name, material, x, z, y, start_x, start_y, start_z):
    mesh = mesh_new(mesh_name)
    col_name = "Collection"    
    col = bpy.data.collections[col_name]
    obj = obj_new(mesh_name, mesh, material)
    obj_to_col(obj, col)
    pydata = build_mesh(x, y, z, start_x, start_y, start_z)
    mesh.from_pydata(vertices=pydata[0], edges=pydata[1], faces=pydata[2])

# def create_mesh():
#     mesh_name = "Test"
#     mesh = mesh_new(mesh_name)
#     col_name = "col"    
#     col = bpy.data.collections[col_name]
#     obj = obj_new(mesh_name, mesh)
#     obj_to_col(obj, col)
#     pydata = wall()
#     mesh.from_pydata(vertices=pydata[0], edges=pydata[1], faces=pydata[2])

if __name__ == "__main__":
    materials = {
        "wood": (0.12,0.03,0, 1),
        "basement": (0.3,0.3,0.3, 1),
        "wall": (0.6,0.54,0.296, 1),
        }

    for material in materials:
        if material in bpy.data.materials:
            mat = bpy.data.materials[material]
            bpy.data.materials.remove(mat)

        mat = bpy.data.materials.new(material)
        mat.diffuse_color = materials[material]
    build_house()



