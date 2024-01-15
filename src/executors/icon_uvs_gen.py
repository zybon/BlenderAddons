import bpy
from mathutils import *
from math import *

def changeProjDir():
    for o in bpy.data.objects:
        if (o.z3dexport_settings.export):
            o.z3dexport_settings.export_projectdir = 'C:\\Users\\User\\AndroidStudioProjects\\Zybotopia\\app\\src\\main\\' 

#changeProjDir()

def set_uvs(blender_object):
    print(blender_object.name)
    position = blender_object.location
    
    mesh_loops = blender_object.data.loops
    mesh_vertices = blender_object.data.vertices[:]  
    uv_data = blender_object.data.uv_layers[0].data[:]
    
    for blender_polygon in blender_object.data.polygons:
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_index = mesh_loops[loop_index].vertex_index
            _vertex = mesh_vertices[blender_vertex_index]
            vertex_coord = blender_object.matrix_local * _vertex.co
            
            tex_coord = uv_data[loop_index].uv
            
            calc_tex_coord = tex_coord
            calc_tex_coord.x = (vertex_coord.x+16.0)/32.0
            calc_tex_coord.y = (vertex_coord.z+16.0)/32.0
            
            # print("vertex coord: %s" % vertex_coord)
            # print("tex_coord coord: %s" % tex_coord)
            # print("calc_tex_coord coord: %s" % calc_tex_coord)
            # print()
            
    
            uv_data[loop_index].uv = calc_tex_coord    


def textmap_creator():
    print("\n\ntextmap_creator")
    i = 0
#    set_uvs(bpy.context.object)
    for o in bpy.data.objects:
        if (o.type == 'MESH' and o.name[:5] == 'icon_'):
            #o.z3dexport_settings.export = False
            set_uvs(o)
            #o.name = 'icon_'+str(i).rjust(4, '0')
            #i = i+1
            #o.hide_render = True
#            if (o.name[5:6] == '0'):
#                o.z3dexport_settings.export = False
        
    

    
textmap_creator()    
































    