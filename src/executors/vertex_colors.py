import bpy
from mathutils import Color



# ~ selected_verts = []
# ~ for v in terrain.data.vertices:
    # ~ if (v.select == True):
        # ~ selected_verts.append(v)
            
       
def set_vertex_colors_to_black(object):                
    for p in object.data.polygons:
        for i, index in enumerate(p.vertices):
            loop_index = p.loop_indices[i]
            
            color = Color((0.0, 0.0, 0.0))
            #vertex_posZ = object.data.vertices[index].co.z
#            if (vertex_posZ<10.0):
#                color = Color((0.0, 0.0, 0.0))
#            else:
#                color = Color((0.0, 1.0, 0.0))
                
            #vertex_normal = object.data.vertices[index].normal.z
            
            #if (vertex_normal<0.8):
            #    color = Color((1.0, 0.0, 0.0))
            #else:
            #    color = Color((1.0, 0.0, 0.0))            
                
            object.data.vertex_colors['Col'].data[loop_index].color = color   
            
def set_vertex_colors_to_weight(object):                
    for p in object.data.polygons:
        for i, index in enumerate(p.vertices):
            loop_index = p.loop_indices[i]
            
            head = object.data.vertices[index].groups[0].weight
            body = object.data.vertices[index].groups[1].weight
            tail = object.data.vertices[index].groups[2].weight            
            
            color = Color((head, body, tail))         
                
            object.data.vertex_colors['Col'].data[loop_index].color = color               

obj_to_color = bpy.context.object #bpy.data.objects['terrain_long_island_vert_col']
set_vertex_colors_to_weight(obj_to_color)
