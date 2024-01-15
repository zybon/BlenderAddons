import bpy
from mathutils import *
from math import *

def renamer():

    X = -1.0
    Z = 1.0

    LETTERS = []
    LETTERS.append("ÁÉÍÓÖŐÚÜŰáéí")
    LETTERS.append("óöőúüűABCDEFG")
    LETTERS.append("HIJKLMNOPRS")
    LETTERS.append("TUVWXYZbdfhk")
    LETTERS.append("acemnorsuvwxz+")
    LETTERS.append("ilt!?/01234567")
    LETTERS.append("89*[]{}()%#&Q")
    LETTERS.append("gjpqy.,-:=<>")
    
    OBJ = [[],[],[],[],[],[],[],[]]
    for o in bpy.context.selected_objects:
        o.name = "_text_"
        S = int(-(o.location.z-Z)/o.dimensions.z)
        o.name = "text_"+str(S)
        if (len(OBJ[S]) == 0):
            OBJ[S].append(o)
        else:
            inserted = False
            for i, s in enumerate(OBJ[S]):
                if (o.location.x<s.location.x):
                    OBJ[S].insert(i, o)
                    inserted = True                
                    break
            if (inserted == False):
                OBJ[S].append(o)    

    for row_index, ROW in enumerate(OBJ):
        for col_index, o in enumerate(ROW):
            print("%s, %s" % (row_index, col_index))
            o.name = LETTERS[row_index][col_index]
            o.data.name = o.name
            o.z3dexport = True
            
def mov_origins():
    bpy.ops.object.select_all(action='DESELECT')
    scene = bpy.context.scene  
    for o in bpy.data.objects:
        if o.hide is False:   
            o.select = True
            pos = o.location + Vector((-o.dimensions.x/2.0, 0, -o.dimensions.z/2.0))      
            scene.cursor_location = pos
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
            o.select = False
    
#mov_origins()
#renamer()

def rnem():

    row = []
    for o in bpy.context.selected_objects:
        if (len(row) == 0):
            row.append(o)
        else:
            inserted = False
            for i, s in enumerate(row):
                if (o.location.x<s.location.x):
                    row.insert(i, o)
                    inserted = True                
                    break
            if (inserted == False):
                row.append(o)  
                  
    for i, o in enumerate(row):   
        o.name = "char_7_"+str(i)
        
#rnem()       

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
            calc_tex_coord.x = (vertex_coord.x+5.0)/10.0
            calc_tex_coord.y = (vertex_coord.z+5.0)/10.0
            
            # print("vertex coord: %s" % vertex_coord)
            # print("tex_coord coord: %s" % tex_coord)
            # print("calc_tex_coord coord: %s" % calc_tex_coord)
            # print()
            
    
            uv_data[loop_index].uv = calc_tex_coord    


def textmap_creator():
    print("\n\ntextmap_creator")
    
    LETTERS = []
    LETTERS.append("ÁÉÍÓÖŐÚÜŰáéí")
    LETTERS.append("óöőúüűABCDEFG")
    LETTERS.append("HIJKLMNOPRS")
    LETTERS.append("TUVWXYZbdfhk")
    LETTERS.append("acemnorsuvwxz+")
    LETTERS.append("ilt!?/01234567")
    LETTERS.append("89*[]{}()%#&Q")
    LETTERS.append("gjpqy.,-:=<>")
    
    for o in bpy.data.objects:
        if (o.name[:5] == 'char_' or o.name[:7] == 'symbol_' ):
            set_uvs(o)
        if (o.name[:6] == 'wchar_' or o.name[:8] == 'wsymbol_' ):
            set_uvs(o)            
        
    

    
textmap_creator()    
































    