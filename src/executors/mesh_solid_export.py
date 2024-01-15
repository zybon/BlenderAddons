# ##### ZYB3D creator #####
#
# 2021.07.14. 18:08
# 

import os

import bpy
import mathutils
import math
import zyb_utils
import zyb_tools
from time import localtime, strftime, time, gmtime


import bpy, bmesh
from bpy import context as C

def cut_to_chunk():

    C.object.select = False
    
    triangulated_mesh = C.object.to_mesh(
                    C.scene, True, 'PREVIEW', calc_tessface=False)
                    
    BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')

    triangulated_mesh.transform(BLENDER_TO_ANDROID_OPENGL_MATRIX)
    
    zyb_utils.mesh_triangulate(triangulated_mesh)    
    
    temp_obj = bpy.data.objects.new("Temp object", triangulated_mesh)
    
    C.scene.objects.link(temp_obj)
    
    temp_obj.select = True
    C.scene.objects.active = temp_obj

    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(triangulated_mesh)

    edges = []
    
    chunk_size = 4

    chunk_x_size = chunk_size

    x_min = round(-temp_obj.dimensions.x*0.5)
    x_min = x_min - x_min % chunk_x_size
    x_max = round(temp_obj.dimensions.x*0.5)
    x_max = x_max + (chunk_x_size-(x_max % chunk_x_size))    
    # ~ print("x_min: %s, x_max: %s" % (x_min, x_max))
    
    for i in range(x_min, x_max, chunk_x_size):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(-1,0,0))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])   
            
             
            
    # ~ chunk_y_size = chunk_size

    # ~ y_min = round(-temp_obj.dimensions.y*0.5)
    # ~ y_min = y_min - y_min % chunk_y_size
    
    # ~ y_max = round(temp_obj.dimensions.y*0.5)
    # ~ y_max = y_max + (chunk_y_size-(y_max % chunk_y_size))       
    # ~ print("y_min: %s, y_max: %s" % (y_min, y_max))


    # ~ for i in range(y_min, y_max, chunk_y_size):
            # ~ ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,i,0), plane_no=(0,1,0))
            # ~ bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])        
            
                
    
    chunk_z_size = chunk_size

    z_min = round(-temp_obj.dimensions.z*0.5)
    z_min = z_min - z_min % chunk_z_size
    
    z_max = round(temp_obj.dimensions.z*0.5)
    z_max = z_max + (chunk_z_size-(z_max % chunk_z_size))       
    # ~ print("z_min: %s, z_max: %s" % (z_min, z_max))


    for i in range(z_min, z_max, chunk_z_size):
            ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(0,0,i), plane_no=(0,0,1))
            bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

    bmesh.update_edit_mesh(triangulated_mesh)

    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # ~ column = 0
    # ~ row = 0
    # ~ for o in C.selected_objects:
        # ~ o.name = str(column)+"_"+str(row)
        # ~ column = column + 1
        # ~ row = row + 1
    
def cut_to_sector():
    C.object.select = False
    
    triangulated_mesh = C.object.to_mesh(
                    C.scene, True, 'PREVIEW', calc_tessface=False)
                    
    BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')

    triangulated_mesh.transform(BLENDER_TO_ANDROID_OPENGL_MATRIX)
    
    zyb_utils.mesh_triangulate(triangulated_mesh)    
    
    temp_obj = bpy.data.objects.new("Temp object", triangulated_mesh)
    
    C.scene.objects.link(temp_obj)
    temp_obj.parent = bpy.data.objects['terrain_parent']
    temp_obj.select = True
    C.scene.objects.active = temp_obj   
    
    bpy.ops.object.mode_set(mode='EDIT')

    bm = bmesh.from_edit_mesh(triangulated_mesh)
    
    bpy.ops.mesh.select_all(action='DESELECT')

    chunk_x_size = 50

    x_min = 250
    # ~ x_min = x_min - x_min % chunk_x_size + chunk_x_size
    
    x_max = 300
    # ~ x_max = x_max + (chunk_x_size-(x_max % chunk_x_size)) + chunk_x_size
    
    chunk_z_size = 50

    z_min = 150
    # ~ z_min = z_min - z_min % chunk_z_size + chunk_z_size
    
    z_max = 200
    # ~ z_max = z_max + (chunk_z_size-(z_max % chunk_z_size))  + chunk_z_size 
    
    # ~ c = 0
    # ~ for x in range(x_min, x_max, chunk_x_size):
        # ~ r = 0
        # ~ for z in range(z_min, z_max, chunk_z_size):
    s = 0
    for face in bm.faces:
        for loop in face.loops:
            vert = loop.vert
            if (vert.co.x>=x_min-10 and vert.co.x<x_max+10 and
                vert.co.z>=z_min-10 and vert.co.z<z_max+10):
                face.select = True
                s = s+1
            # ~ print("Loop Vert: (%f,%f,%f)" % vert.co[:])
        
    
    # ~ bmesh.update_edit_mesh(triangulated_mesh)
    if (s>0):
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')      
        temp_obj.select = False
        C.selected_objects[0].name = "0_cutted"#str(r)+"_"+str(c)
        C.selected_objects[0].parent = bpy.data.objects['terrain_parent']
        temp_obj.select = True
        C.scene.objects.active = temp_obj   
        
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(triangulated_mesh)
        
        bpy.ops.mesh.select_all(action='DESELECT')                                
                
            # ~ r = r + 1 
        # ~ c = c + 1
    bpy.ops.object.mode_set(mode='OBJECT')    

            
class BorderXZ():
    
    def __init__(self):
        self.minX = 1000000.0
        self.maxX = -1000000.0
        
        self.minZ = 1000000.0
        self.maxZ = -1000000.0
        
    def stretch_if_need(self, border_xz):
        if border_xz.minX<self.minX:
            self.minX = border_xz.minX
        if border_xz.minZ<self.minZ:
            self.minZ = border_xz.minZ  
            
        if border_xz.maxX>self.maxX:
            self.maxX = border_xz.maxX
        if border_xz.maxZ>self.maxZ:
            self.maxZ = border_xz.maxZ              
       
    def x_size(self):   
        return self.maxX-self.minX
    
    def z_size(self):   
        return self.maxZ-self.minZ  
    
    def write_to_bin(self, fw):
        fw(zyb_utils.float_to_bytes(self.minX))
        fw(zyb_utils.float_to_bytes(self.minZ))
        fw(zyb_utils.float_to_bytes(self.maxX))
        fw(zyb_utils.float_to_bytes(self.maxZ))
        
    def __str__(self):
        return "["+str(self.minX)+","+str(self.minZ)+","+str(self.maxX)+","+str(self.maxZ)+"]"
        
class Vector3D:
        
    def __init__(self,x=0,y=0,z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def create(self, v1, v2):
        return Vector3D(v2.x-v1.x, v2.y-v1.y, v2.z-v1.z)
        
    def set(self, vectorFrom, vectorTo):
        self.x = vectorTo.x - vectorFrom.x   
        self.y = vectorTo.y - vectorFrom.y 
        self.z = vectorTo.z - vectorFrom.z     
        
    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)  
    
    def tostring(self):
        return ("[%f, %f, %f]" % (self.x, self.y, self.z))  
    
    def dot_product(self, other):
        return self.x*other.x+self.y*other.y+self.z*other.z;
        
    def crossProduct(self, other):
        return Vector3D(
                self.y*other.z - self.z*other.y, 
                self.z*other.x - self.x*other.z, 
                self.x*other.y - self.y*other.x
        )  
        
    def normalize(self):
        length = self.length()
        self.x = self.x / length           
        self.y = self.y / length
        self.z = self.z / length
    
    def angle(self, other):
        return math.acos(self.dot_product(other) / (self.length() * other.length()));   
    
    def __str__(self):
        return self.tostring()
        

class SolidTriangle():

    def __init__(self):
        self.vertices_coords = []
        self.vertices_colors = []
        
    def set_index(self, index):
        self.index = index
        
    def set_center(self, center):
        self.center = center    
       
    def append_vertex_coord(self, vertex_coord):
        self.vertices_coords.append(mathutils.Vector(vertex_coord))  
        
    def append_vertex_color(self, vertex_color):
        self.vertices_colors.append(mathutils.Color(vertex_color))          
        
    def get_vertex_coord(self, index):
        return self.vertices_coords[index]
        
        
    def init_border_xz(self):
        self.border_xz = BorderXZ()
        for co in self.vertices_coords:
            if co.x < self.border_xz.minX:
                self.border_xz.minX = co.x
            if co.z < self.border_xz.minZ:
                self.border_xz.minZ = co.z
                
            if co.x > self.border_xz.maxX:
                self.border_xz.maxX = co.x
            if co.z > self.border_xz.maxZ:
                self.border_xz.maxZ = co.z
                
    def calc_constants(self):
        self.calc_normal()
        
        for vertex in self.vertices_coords:
            if not self.isNullVertexCoord(vertex):
                self.point_on_triangle = vertex
                break    

        self.plane_constant = self.point_on_triangle.x * self.normal.x + self.point_on_triangle.y * self.normal.y + self.point_on_triangle.z * self.normal.z 

    def isNullVertexCoord(self, vertex):
        return ((abs(vertex.x) < 0.000001) and (abs(vertex.y) < 0.000001) and (abs(vertex.z) < 0.000001))
        
    def calc_normal(self):
        v1 = Vector3D()
        v1.set(self.vertices_coords[0], self.vertices_coords[1])
        v1.normalize()

        v2 = Vector3D()
        v2.set(self.vertices_coords[0], self.vertices_coords[2])  
        v2.normalize()
        
        self.normal = v1.crossProduct(v2)     
        self.normal.normalize()
                        
        
    def write_to_txt(self, fw):
        fw("\t%d. triangle" % (self.index))
        fw("\n\t\t{")
        fw("\n\t\t\tvertices_coords[0]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_coords[0], 6)))
        fw("\n\t\t\tvertices_coords[1]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_coords[1], 6)))
        fw("\n\t\t\tvertices_coords[2]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_coords[2], 6)))
        fw("\n\t\t\tnormal: %s" % self.normal)
        fw("\n\t\t\tplane_constant: %s" % (self.plane_constant))
        fw("\n\t\t\tpoint_on_triangle: %s, %s, %s" % (zyb_utils.vector_round(self.point_on_triangle, 6)))
        fw("\n\t\t\tvertex_colors[0]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_colors[0], 6)))
        fw("\n\t\t\tvertex_colors[1]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_colors[1], 6)))
        fw("\n\t\t\tvertex_colors[2]: %s, %s, %s" % (zyb_utils.vector_round(self.vertices_colors[2], 6)))
        fw("}\n")
        
    def write_coords_to_txt(self, fw):
        fw("\t%d. triangle\n" % (self.index))
        fw("\t\t{")
        
        fw("vertices:\n%s\n" % str(self.vertices_coords))
        fw("normals:\n%s\n" % str(self.normal_vectors))
        if (self.has_texture_coords):
            fw("texture_coords:\n%s\n" % str(self.texture_coords))        
        
        fw("}\n")        
              
                
    def write_to_bin(self, fw):
        fw(zyb_utils.int_to_bytes(self.index))
        fw(zyb_utils.vector_to_bytes(self.vertices_coords[0]))
        fw(zyb_utils.vector_to_bytes(self.vertices_coords[1]))
        fw(zyb_utils.vector_to_bytes(self.vertices_coords[2]))
        fw(zyb_utils.float_to_bytes(self.normal.x))
        fw(zyb_utils.float_to_bytes(self.normal.y))
        fw(zyb_utils.float_to_bytes(self.normal.z))
        fw(zyb_utils.vector_to_bytes(self.vertices_colors[0]))
        fw(zyb_utils.vector_to_bytes(self.vertices_colors[1]))
        fw(zyb_utils.vector_to_bytes(self.vertices_colors[2]))        

                      
                
    # ~ def write_to_bin_indexed(self, fw):
        # ~ for i in range(3):
            # ~ fw(int_to_bytes(self.vertices_indices[i]))



class BlenderMeshSolidObject():
    
    def __init__(self, context, blender_object):
        self.context = context
        self.blender_object = blender_object
        
        self.name = zyb_utils.name_compat(blender_object.name)+"_solid"
        
        self.init_triangulated_mesh()
        
        self.triangles = []
        
        self.read_triangles()
           
        # clean up
        bpy.data.meshes.remove(self.triangulated_mesh)    
        
    def init_triangulated_mesh(self):
        
        BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
        
        # temp mesh létrehozása úgy hogy modifiers-eket érvényesitik
        self.triangulated_mesh = self.blender_object.to_mesh(
                        self.context.scene, True, 'PREVIEW', calc_tessface=False)

        self.triangulated_mesh.transform(BLENDER_TO_ANDROID_OPENGL_MATRIX)
        
        #háromszögelés, hogy minden face egy háromszög legyen
        # az elején meg kell csinálni mert ez újra képezi a loops tomboket
        zyb_utils.mesh_triangulate(self.triangulated_mesh)    
          
        #normálok számítása face-enként a vertexekhez
        self.triangulated_mesh.calc_normals_split()             
                
        
    def read_triangles(self):
        for blender_polygon in self.triangulated_mesh.polygons:
            self.read_triangle(blender_polygon)
            
    def read_triangle(self, blender_polygon):
        
        triangle = SolidTriangle()
        triangle.set_index(blender_polygon.index)
        triangle.set_center(blender_polygon.center)
        
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_index = self.triangulated_mesh.loops[loop_index].vertex_index
            triangle.append_vertex_coord(self.triangulated_mesh.vertices[blender_vertex_index].co)            

        triangle.init_border_xz()     
        triangle.calc_constants() 
        self.triangles.append(triangle)
            

    def write_solid_to_txt(self, fw):

        fw("\n----------------BlenderMeshSolidObject-----------------\n")
        fw("name: %s\n" % self.name)    
        
        for triangle in self.triangles:
            triangle.write_to_txt(fw)
        
    def write_to_bin(self, fw): 
        fw(zyb_utils.int_to_bytes(len(self.triangles)))
        for triangle in self.triangles:
            triangle.write_to_bin(fw)   
            

                         
def write_solid_to_bin_z3d(blender_mesh_solid_object):
    print("\n- write_solid_to_bin_z3d()")
    # ~ if not os.path.exists(targetDirPath):
        # ~ print(targetDirPath+" created")
        # ~ os.makedirs(targetDirPath)    
        
    dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids\\"
    if not os.path.exists(dirpath):
        print("\n\t[[[ "+dirpath+" created ]]]\n")
        os.makedirs(dirpath)   
        
    filename = blender_mesh_solid_object.name+".z3d"         
    
    print("-- Objects data export to: "+dirpath+filename)
    with open((dirpath+filename), "wb") as f:
        fw = f.write
        print("--- Export "+blender_mesh_solid_object.name)
        blender_mesh_solid_object.write_to_bin(fw)
              
def write_solid_to_txt_z3d(blender_mesh_solid_object):
    print("\n- write_to_txt_z3d()")
    filename = blender_mesh_solid_object.name
    tempfile_path = "C:\\Users\\zybon\\BlenderProjects\\temp\\"+filename+".txt"
    print("-- Temp file save to ["+tempfile_path+"]")
    with open((tempfile_path), "w") as f:
        fw = f.write
        blender_mesh_solid_object.write_solid_to_txt(fw)                  

def write_objectsnames_to_txt(filename, blender_mesh_objects):
    print("\n- write_objectsname_to_txt()")
    
   
    dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\names\\meshes\\"
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
   
    file_name = filename #.capitalize()
    print("-- Write blender_mesh_objects names to \n\t["+dirpath+file_name+".txt]")
    with open((dirpath+file_name+".txt"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        for blender_mesh_solid_object in blender_mesh_objects:
            for index, zybmeshobject in enumerate(blender_mesh_solid_object.zyb_meshobjects):
                fw(zybmeshobject.name)
                fw('\n')
        
    
def write_objectsnames_to_java(projdirpath):
    print("\n-  write_objectsnames_to_java()")
    
    names_dir = os.path.dirname(bpy.data.filepath)+"\\game_extra\\names\\meshes\\"
   
    package = zyb_utils.read_package_name(projdirpath)+".names"
    java_file_name = "MeshesNames"
    fileContent, dirpath = zyb_utils.get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    
    print("-- Write mesh names from ["+names_dir+"] \n\tto ["+ dirpath+java_file_name+".java]")
    
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent) 
        file_list = sorted(next(os.walk(names_dir))[2])
        for filename in file_list:
            print("--- Mesh name: ["+filename+"]")
            write_objectsname_from_txt_file_to_java(fw, names_dir, filename)
            fw("\n") 
        #file lezáró
        fw("\n}")     
    
        
def write_objectsname_from_txt_file_to_java(fw, names_dir, filename):
    collector_name = filename[:len(filename)-4]
    fw("    public static final class "+collector_name.capitalize()+" {\n")   
    fw("        public static final String ")
    fw("collector_file_name = ")
    fw('"')
    fw("meshes/"+collector_name)
    fw('.z3d";\n\n')    
    
    with open(names_dir+filename) as fp:
        for cnt, line in enumerate(fp):
            name = line.strip()
            fw("        public static final String ")
            fw(name+" = ")
            fw('"')
            fw(name)
            fw('";\n')
    fw("    }\n")             

def read_blender_mesh_solid_object(context, object):
    print("\n- read_blender_mesh_solid_object()")

    blender_mesh_solid_object = BlenderMeshSolidObject(context, object)    

    print("-- Create BlenderMeshSolidObject ["+blender_mesh_solid_object.name+"]")
    
    return blender_mesh_solid_object 
    
    
class BlenderToSolidObject():
    
    def __init__(self, context, blender_object):
        self.context = context
        self.blender_object = blender_object
        
        self.name = zyb_utils.name_compat(blender_object.name)+"_solid"
        
        self.init_triangulated_mesh()
        
        triNumber = len(self.triangulated_mesh.polygons)
        self.triangles = [None]*triNumber
        
        self.read_triangles()
           
        # clean up
        bpy.data.meshes.remove(self.triangulated_mesh)    
        
    def init_triangulated_mesh(self):
        
        BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
        
        # temp mesh létrehozása úgy hogy modifiers-eket érvényesitik
        self.triangulated_mesh = self.blender_object.to_mesh(
                        self.context.scene, True, 'PREVIEW', calc_tessface=False)

        self.triangulated_mesh.transform(BLENDER_TO_ANDROID_OPENGL_MATRIX)
        
        #háromszögelés, hogy minden face egy háromszög legyen
        # az elején meg kell csinálni mert ez újra képezi a loops tomboket
        zyb_utils.mesh_triangulate(self.triangulated_mesh)    
          
        #normálok számítása face-enként a vertexekhez
        self.triangulated_mesh.calc_normals_split()             
                
        
    def read_triangles(self):
        for blender_polygon in self.triangulated_mesh.polygons:
            self.read_triangle(blender_polygon)
            
    def read_triangle(self, blender_polygon):
        
        triangle = SolidTriangle()
        triangle.set_index(blender_polygon.index)
        triangle.set_center(blender_polygon.center)
        
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_index = self.triangulated_mesh.loops[loop_index].vertex_index
            triangle.append_vertex_coord(self.triangulated_mesh.vertices[blender_vertex_index].co)            

        triangle.init_border_xz()     
        triangle.calc_constants() 
        self.triangles.append(triangle)
            

    def write_solid_to_txt(self, fw):

        fw("\n----------------BlenderMeshSolidObject-----------------\n")
        fw("name: %s\n" % self.name)    
        
        for triangle in self.triangles:
            triangle.write_to_txt(fw)
        
    def write_to_bin(self, fw): 
        fw(zyb_utils.int_to_bytes(len(self.triangles)))
        for triangle in self.triangles:
            triangle.write_to_bin(fw)   
            

            
            
def init_triangulated_mesh(context, blender_object):
    
    BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
    
    # temp mesh létrehozása úgy hogy modifiers-eket érvényesitik
    triangulated_mesh = blender_object.to_mesh(
                    context.scene, True, 'PREVIEW', calc_tessface=False)

    triangulated_mesh.transform(blender_object.matrix_local)

    triangulated_mesh.transform(BLENDER_TO_ANDROID_OPENGL_MATRIX)
    
    #háromszögelés, hogy minden face egy háromszög legyen
    # az elején meg kell csinálni mert ez újra képezi a loops tomboket
    zyb_utils.mesh_triangulate(triangulated_mesh)    
      
    return triangulated_mesh        
                            
      
    
def read_and_write_triangles_er(context, blender_object):
    print("\n- read_and_write_triangles()")
    
    triangulated_mesh = init_triangulated_mesh(context, blender_object)
    
    name = zyb_utils.name_compat(blender_object.name)
        
    dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids\\"
    if not os.path.exists(dirpath):
        print("\n\t[[[ "+dirpath+" created ]]]\n")
        os.makedirs(dirpath)   
        
    filename = name+".z3d"       
    
    print("-- ["+name+"] data export to: "+dirpath+filename)
    with open((dirpath+filename), "wb") as f:
        fw = f.write
        fw(zyb_utils.int_to_bytes(len(triangulated_mesh.polygons)))
        triangle = None
        for blender_polygon in triangulated_mesh.polygons:
            triangle = SolidTriangle()
            
            for loop_index in blender_polygon.loop_indices:
                blender_vertex_index = triangulated_mesh.loops[loop_index].vertex_index
                triangle.append_vertex_coord(triangulated_mesh.vertices[blender_vertex_index].co)            
     
            triangle.calc_constants() 
            triangle.write_to_bin(fw) 
    
       
    # clean up
    bpy.data.meshes.remove(triangulated_mesh)     
    

    
def read_mesh_to_sectors(context, sectorInfo, blender_object):
    print("-- read_mesh_to_sectors")
    triangulated_mesh = init_triangulated_mesh(context, blender_object)
    # calc sector info
    sectorInfo.calc_data(triangulated_mesh)
    
    sectors = {}      
    
    
    #read
    for blender_polygon in triangulated_mesh.polygons:
        triangle = SolidTriangle()
        triangle.set_index(blender_polygon.index)
        
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_coord_index = triangulated_mesh.loops[loop_index].vertex_index
            triangle.append_vertex_coord(triangulated_mesh.vertices[blender_vertex_coord_index].co)
            if (len(triangulated_mesh.vertex_colors)>0):
                triangle.append_vertex_color(triangulated_mesh.vertex_colors[0].data[loop_index].color)            
            
                     
        
        triangle.init_border_xz()
        triangle.calc_constants()
        
        columnMin = int((triangle.border_xz.minX-sectorInfo.x_min)/sectorInfo.dx)
        columnMax = int((triangle.border_xz.maxX-sectorInfo.x_min)/sectorInfo.dx)
        rowMin = int((triangle.border_xz.minZ-sectorInfo.z_min)/sectorInfo.dz)
        rowMax = int((triangle.border_xz.maxZ-sectorInfo.z_min)/sectorInfo.dz)
        for row in range(rowMin, rowMax+1):
            for column in range(columnMin, columnMax+1):
                # print(row, column)
                index = (row, column)
                dict_val = sectors.get(index)
                if (dict_val is None):
                    sectors[index] = []
                sectors[index].append(triangle)
                       
    # clean up
    bpy.data.meshes.remove(triangulated_mesh)                         
    return sectors
    
def read_and_write_triangles(context, blender_object):
    
    
    print("\n- read_and_write_triangles()")
    
    sectorInfo = Solid_Sector_Info(blender_object)
    

    
    
    name = zyb_utils.name_compat(blender_object.name)
        
    dirpath = blender_object.z3dexport_settings.export_projectdir+"assets\\solids\\"
    # ~ dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids\\"
    if not os.path.exists(dirpath):
        print("\n\t[[[ "+dirpath+" created ]]]\n")
        os.makedirs(dirpath) 
        
    
    sectors = read_mesh_to_sectors(context, sectorInfo, blender_object)
    
    print("sectorX: %f - %f" % (sectorInfo.x_min, sectorInfo.x_max))
    print("sectorZ: %f - %f" % (sectorInfo.z_min, sectorInfo.z_max))
    
    print("sector dx: %f" % (sectorInfo.dx))
    print("sector dz: %f" % (sectorInfo.dz)) 
    
    print("sector column number: %f" % (sectorInfo.column_number)) 
    print("sector row number: %f" % (sectorInfo.row_number))     
    
    filename = name+"_"+str(int(sectorInfo.dx))+"x"+str(int(sectorInfo.dz))+".z3d" 
    
    print()
          
    print("-- ["+name+"] data export to: "+dirpath+filename)                

    #write            
    with open((dirpath+filename), "wb") as f:
        fw = f.write
        
        
        #header 
        fw(zyb_utils.float_to_bytes(sectorInfo.x_min))
        fw(zyb_utils.float_to_bytes(sectorInfo.x_max))
        
        fw(zyb_utils.float_to_bytes(sectorInfo.z_min))
        fw(zyb_utils.float_to_bytes(sectorInfo.z_max))

        fw(zyb_utils.float_to_bytes(sectorInfo.dx)) 
        fw(zyb_utils.float_to_bytes(sectorInfo.dz)) 
        
        
        #4 byte to every sector start index (max 4,3 Gb)
        sector_start_index = sectorInfo.header_size_in_bytes
        for row in range(sectorInfo.row_number):
            for column in range(sectorInfo.column_number):  
                index = (row, column)
                triangles_in_sector = sectors.get(index)
                if (triangles_in_sector is not None):
                    #print(index, len(triangles_in_sector)) 
                    fw(zyb_utils.int_to_bytes(sector_start_index)) 
                    triangles_count_in_sector = len(triangles_in_sector) 
                    sector_start_index = sector_start_index + sectorInfo.triangle_counter_size_in_bytes + triangles_count_in_sector*sectorInfo.triangle_size_in_bytes        
                else :
                    fw(zyb_utils.int_to_bytes(0))
                    
        #body write only sector with triangles
        for row in range(sectorInfo.row_number):
            for column in range(sectorInfo.column_number):  
                index = (row, column)
                triangles_in_sector = sectors.get(index)
                if (triangles_in_sector is not None): 
                    fw(zyb_utils.int_to_bytes(len(triangles_in_sector)))
                    for triangle in triangles_in_sector:
                        triangle.write_to_bin(fw)  
     
                  
    filename = name+"_"+str(int(sectorInfo.dx))+"x"+str(int(sectorInfo.dz))+".txt"      
    exported = {}
    with open(("C:\\Users\\User\\BlenderProjects\\temp\\"+filename), "w") as f:
        fw = f.write 
        for row in range(sectorInfo.row_number):
            for column in range(sectorInfo.column_number):  
                index = (row, column)
                triangles_in_sector = sectors.get(index)
                if (triangles_in_sector is not None): 
                    # ~ fw(zyb_utils.int_to_bytes(len(triangles_in_sector)))
                    for triangle in triangles_in_sector:
                        exportet_tri = exported.get(triangle.index)
                        if (exportet_tri is None):
                            triangle.write_to_txt(fw)
                            exported[triangle.index] = True
       
    
        
                  
class Sector():
    
    def __init__(self, sector_info, x, z):
        self.sector_info = sector_info
        self.x_min = x
        self.z_min = z
        self.x_max = x + sector_info.dx
        self.z_max = z + sector_info.dz       
                
        r = (z-sector_info.z_min)/sector_info.dz
        c = (x-sector_info.x_min)/sector_info.dx
        self.name = ("%03d_%03d" % (r,c))   
        
        self.empty = True
        
        self.sector_file_path =  os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids_temp\\"+self.name+".z3d"    
        with open((self.sector_file_path), "wb") as fww:
            self.fw = fww.write  
            self.read_insector_solids()      
        
        if (self.empty):
            os.remove(self.sector_file_path)
        
        
    def read_insector_solids(self):
        # ~ print(self.name)    
        dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids\\"
        file_list = sorted(next(os.walk(dirpath))[2])

        for filename in file_list: 
            self.read_insector_solid(dirpath, filename)        

            
    def read_insector_solid(self, dirpath, filename):
        # ~ filepath = dirpath+filename
        # ~ print(filepath)
        # ~ file_size = os.path.getsize(filepath) 
        # ~ print("file size %s" % file_size)  
    
        with open(dirpath+filename, "rb") as f: 
            num_in_byte = f.read(4)
            tri_number = int.from_bytes(num_in_byte, byteorder='big', signed=True)
            i = 0
            while i<tri_number:
                v0x_byte = f.read(4)
                v0x = float(int.from_bytes(v0x_byte, byteorder='big', signed=True))/100000
                v0y_byte = f.read(4)
                # ~ v0y = float(int.from_bytes(v0y_byte, byteorder='big', signed=True))/100000
                v0z_byte = f.read(4)
                v0z = float(int.from_bytes(v0z_byte, byteorder='big', signed=True))/100000
                # ~ print("v0: [%s, %s, %s]" % (v0x,v0y,v0z))
            
                v1x_byte = f.read(4)
                v1x = float(int.from_bytes(v1x_byte, byteorder='big', signed=True))/100000
                v1y_byte = f.read(4)
                # ~ v1y = float(int.from_bytes(v1y_byte, byteorder='big', signed=True))/100000
                v1z_byte = f.read(4)
                v1z = float(int.from_bytes(v1z_byte, byteorder='big', signed=True))/100000
                # ~ print("v1: [%s, %s, %s]" % (v1x,v1y,v1z))
                
                v2x_byte = f.read(4)
                v2x = float(int.from_bytes(v2x_byte, byteorder='big', signed=True))/100000
                v2y_byte = f.read(4)
                # ~ v2y = float(int.from_bytes(v2y_byte, byteorder='big', signed=True))/100000
                v2z_byte = f.read(4)
                v2z = float(int.from_bytes(v2z_byte, byteorder='big', signed=True))/100000 
                # ~ print("v2: [%s, %s, %s]" % (v2x,v2y,v2z))    
                
                nx_byte = f.read(4)
                # ~ nx = float(int.from_bytes(nx_byte, byteorder='big', signed=True))/100000
                ny_byte = f.read(4)
                # ~ ny = float(int.from_bytes(ny_byte, byteorder='big', signed=True))/100000
                nz_byte = f.read(4)
                # ~ nz = float(int.from_bytes(nz_byte, byteorder='big', signed=True))/100000  
                # ~ print("n: [%s, %s, %s]" % (nx,ny,nz))
                # ~ print("\n")
                i = i + 1    
                
                if (self.is_in_sector(v0x, v0z, v1x, v1z, v2x, v2z)):
                    self.empty = False
                    self.fw(v0x_byte)   
                    self.fw(v0y_byte)
                    self.fw(v0z_byte)
                    
                    self.fw(v1x_byte)
                    self.fw(v1y_byte)
                    self.fw(v1z_byte)
                    
                    self.fw(v2x_byte)
                    self.fw(v2y_byte)
                    self.fw(v2z_byte)
                    
                    self.fw(nx_byte)
                    self.fw(ny_byte)
                    self.fw(nz_byte) 

    def is_in_sector(self, v0x, v0z, v1x, v1z, v2x, v2z):
        if (v0x >= self.x_min and 
            v0x < self.x_max and
            v0z >= self.z_min and 
            v0z < self.z_max):
            return True 
            
        if (v1x >= self.x_min and 
            v1x < self.x_max and
            v1z >= self.z_min and 
            v1z < self.z_max):
            return True 
            
        if (v2x >= self.x_min and 
            v2x < self.x_max and
            v2z >= self.z_min and 
            v2z < self.z_max):
            return True                               
        
        return False
                    
    
    
      
    
    

def export_all_solid_to_sectored_z3d(proj_dir):
    print("\nexport_all_solid_to_sectored_z3d()")
    dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\solids\\"
    file_list = sorted(next(os.walk(dirpath))[2])

    filename = file_list[0]
    
    cursor = bpy.context.scene.cursor_location
    cursor_x = cursor.x
    cursor_z = -cursor.y
    cursor_column = int((cursor_x-Solid_Sector_Info.x_min)/Solid_Sector_Info.dx)
    cursor_row = int((cursor_z-Solid_Sector_Info.z_min)/Solid_Sector_Info.dz)
    
    cursor_index = (cursor_row*Solid_Sector_Info.column_number)+cursor_column
    
    print("cursor_row: %s, cursor_column: %s " % (cursor_row, cursor_column))
    print("cursor_index: %s" % cursor_index)
    
    with open(dirpath+filename, "rb") as f:
        bytes_in_file = f.read()
        
    cursor_index_start_in_header = cursor_index*Solid_Sector_Info.header_index_size_in_byte
    # ~ print("cursor_index_start_in_header %s" % (cursor_index_start_in_header))
    sector_start_index_in_bytes = bytes_in_file[cursor_index_start_in_header:cursor_index_start_in_header+4]
    # ~ print("sector_start_index_in_bytes %s" % (sector_start_index_in_bytes))
    sector_start_index = int.from_bytes(sector_start_index_in_bytes, byteorder='big', signed=True)
    # ~ print("sector_start_index %s" % (sector_start_index))              
    triangle_number_in_sector = int.from_bytes(bytes_in_file[sector_start_index:sector_start_index+4], byteorder='big', signed=True)
    if (triangle_number_in_sector == 0):
        print("In this sector triangle_number_in_sector = 0")
        return
    
    print("triangle_number_in_sector = %s" % triangle_number_in_sector)
    
    byte_index = sector_start_index+4
    for i in range(triangle_number_in_sector):
        tri_index_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        tri_index = float(int.from_bytes(tri_index_byte, byteorder='big', signed=True))   
        # ~ print("tri_index: %s" % (tri_index))    
        
        v0x_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v0x = float(int.from_bytes(v0x_byte, byteorder='big', signed=True))/100000
        v0y_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v0y = float(int.from_bytes(v0y_byte, byteorder='big', signed=True))/100000
        v0z_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v0z = float(int.from_bytes(v0z_byte, byteorder='big', signed=True))/100000
        # ~ print("v0: [%s, %s, %s]" % (v0x,v0y,v0z))
    
        v1x_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v1x = float(int.from_bytes(v1x_byte, byteorder='big', signed=True))/100000
        v1y_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v1y = float(int.from_bytes(v1y_byte, byteorder='big', signed=True))/100000
        v1z_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v1z = float(int.from_bytes(v1z_byte, byteorder='big', signed=True))/100000
        # ~ print("v1: [%s, %s, %s]" % (v1x,v1y,v1z))
        
        v2x_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v2x = float(int.from_bytes(v2x_byte, byteorder='big', signed=True))/100000
        v2y_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v2y = float(int.from_bytes(v2y_byte, byteorder='big', signed=True))/100000
        v2z_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        v2z = float(int.from_bytes(v2z_byte, byteorder='big', signed=True))/100000 
        # ~ print("v2: [%s, %s, %s]" % (v2x,v2y,v2z))    
        
        nx_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        nx = float(int.from_bytes(nx_byte, byteorder='big', signed=True))/100000
        ny_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        ny = float(int.from_bytes(ny_byte, byteorder='big', signed=True))/100000
        nz_byte = bytes_in_file[byte_index:byte_index+4]
        byte_index = byte_index+4
        nz = float(int.from_bytes(nz_byte, byteorder='big', signed=True))/100000  
        # ~ print("n: [%s, %s, %s]" % (nx,ny,nz))
        # ~ print("\n")   
        
        zyb_triangle = zyb_tools.ZybTriangle()    
        zyb_triangle.vertices[0] = mathutils.Vector((v0x, -v0z, v0y))
        zyb_triangle.vertices[1] = mathutils.Vector((v1x, -v1z, v1y))
        zyb_triangle.vertices[2] = mathutils.Vector((v2x, -v2z, v2y))
        zyb_triangle.init_border_xy()
        if (zyb_triangle.is_vertical_overlapped(cursor_x,-cursor_z)):
            zyb_triangle.print_info()
            break
            
def getX(vertex):
    return vertex.co.x    
    
def getZ(vertex):
    return vertex.co.z              
        
class Solid_Sector_Info():
    
    def __init__(self, blender_object):
        self.dx = blender_object.z3dexport_settings.mesh_settings.solid_sector_columnsize
        self.dz = blender_object.z3dexport_settings.mesh_settings.solid_sector_rowsize          
        
    
    def calc_data(self, triangulated_mesh):
        self.x_min = min(triangulated_mesh.vertices, key=getX).co.x
        self.x_max = max(triangulated_mesh.vertices, key=getX).co.x
            
        self.z_min = min(triangulated_mesh.vertices, key=getZ).co.z
        self.z_max = max(triangulated_mesh.vertices, key=getZ).co.z
            
        self.column_number = int((self.x_max-self.x_min)/self.dx)+1
        self.row_number = int((self.z_max-self.z_min)/self.dz)+1
        
        self.int_size_in_bytes = 4
        
        self.sector_info_size_in_bytes = 6*self.int_size_in_bytes
        self.header_index_size_in_byte = 1*self.int_size_in_bytes
        
        self.triangle_counter_size_in_bytes = 1*self.int_size_in_bytes
        
        self.index_size_in_bytes = 1*self.int_size_in_bytes
        self.vector_size_in_bytes = 3*self.int_size_in_bytes
        self.vertices_coords_size_in_bytes = 3*self.vector_size_in_bytes
        
        self.normal_size_in_bytes = self.vector_size_in_bytes
        
        self.vertices_colors_size_in_bytes = 3*self.vector_size_in_bytes        
        
        self.header_size_in_bytes = self.sector_info_size_in_bytes+self.row_number*self.column_number*self.header_index_size_in_byte
        
        self.triangle_size_in_bytes = self.index_size_in_bytes + self.vertices_coords_size_in_bytes + self.normal_size_in_bytes + self.vertices_colors_size_in_bytes
    
def read_package_name(projdirpath):
    from xml.dom import minidom

    # parse an xml file by name
    mydoc = minidom.parse(projdirpath+'AndroidManifest.xml')

    manifest = mydoc.getElementsByTagName('manifest')[0]
    return manifest.attributes['package'].value
#    mainDir = package.replace(".","/")
#    print(mainDir)

def get_alapfile_es_dirpath(projdirpath, java_file_name, package):
    file = open(os.path.dirname(os.path.realpath(__file__))+"\\..\\objectsnames.temp")

    ido = strftime("%Y.%m.%d %H:%M:%S", localtime())
    fileContent = file.read()
    fileContent = fileContent.replace("IDO", ido)
#    fileContent = fileContent.replace("NEV", filenev)
    dirpath = projdirpath+"java\\"+(package.replace(".", "\\"))+"\\"
    fileContent = fileContent.replace("PACKAGE", package, 1)
    fileContent = fileContent.replace("NAME", java_file_name, 1)
#    file.close()
    return (fileContent , dirpath)    
    
def write_solidsnev_tojava(projdirpath):
    print("\n*******  write_solidsnev_tojava  ******\n")
    if not os.path.exists(projdirpath+"assets\\solids"):
        print(projdirpath+"assets\\solids is not exist")
        return    
   
    package = zyb_utils.read_package_name(projdirpath)+".names"
    print("package: "+package)
    java_file_name = "SolidsNames"
    fileContent, dirpath = get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    solidsFiles = os.listdir(projdirpath+"assets\\solids")
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent)  
        for solidsFile in solidsFiles:
            fw("    public static final String ")
            fw(os.path.splitext(solidsFile)[0]+" = ")
            fw('"')
            fw("solids/"+solidsFile)
            fw('";')
            fw('\n')
        
        #file lezáró
        fw("\n}")       
    
     
def save_2(context, object):   
    cut_to_sector()  

def save(context, base_object):

    
    print("\n------------------------\n")
    start_time = time()
    print("MESH SOLID DATA EXPORT START ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")
    import importlib
    importlib.reload(zyb_utils) 
    importlib.reload(zyb_tools)    
    
    
    # ~ global proj_dir
    proj_dir = base_object.z3dexport_settings.export_projectdir 
    
    # ~ print(Solid_Sector_Info.header_size_in_bytes) 
    
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT') 


    # object_copied = bpy.data.objects.new(base_object.name+"_copied", base_object.data.copy())
    # object_copied.z3dexport_settings.export = base_object.z3dexport_settings.export
    # object_copied.z3dexport_settings.export_projectdir = base_object.z3dexport_settings.export_projectdir
    # object_copied.z3dexport_settings.datatype = base_object.z3dexport_settings.datatype
    # object_copied.z3dexport_settings.mesh_settings.solid = base_object.z3dexport_settings.mesh_settings.drawable
    # bpy.context.scene.objects.link(object_copied)
    
    # base_object.select = False
    # object_copied.select = True
    # object_copied.hide = False
    # bpy.context.scene.objects.active = object_copied
    # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    

    read_and_write_triangles(context, base_object)
    
    
    # ~ blender_mesh_solid_object = read_blender_mesh_solid_object(context, base_object)

    # ~ write_solid_to_bin_z3d(blender_mesh_solid_object)
    
    # ~ write_solid_to_txt_z3d(blender_mesh_solid_object)

    # ~ export_all_solid_to_sectored_z3d(proj_dir)
    
     
    write_solidsnev_tojava(proj_dir)

    os.system("msg user \"Export is complete\"")
    end_time = localtime()
    print("\nEXPORT FINISHED ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")   
    
    process_time = gmtime(time()-start_time)
    print("\n\tPROCESS TIME ["+strftime("%H:%M:%S", process_time)+"]") 
    print("------------------------\n") 
    return {'FINISHED'}
    
  
def calc_optimized_sector_size(context, blender_object):
    triangulated_mesh = init_triangulated_mesh(context, blender_object)
    
    sectorInfo = Solid_Sector_Info(blender_object)
    
    sectorInfo.calc_data(triangulated_mesh)
    
    print("sectorX: %f - %f" % (sectorInfo.x_min, sectorInfo.x_max))
    print("sectorZ: %f - %f" % (sectorInfo.z_min, sectorInfo.z_max))
    
    print("sector dx: %f" % (sectorInfo.dx))
    print("sector dz: %f" % (sectorInfo.dz))
    
    
    x_size_min = 100000.0
    x_size_max = -100000.0
    
    z_size_min = 100000.0
    z_size_max = -100000.0   
    
    x_0_25 = 0 
    x_25_50 = 0
    x_50_75 = 0
    x_75_ = 0
    
    z_0_25 = 0 
    z_25_50 = 0
    z_50_75 = 0
    z_75_ = 0    
    
    for blender_polygon in triangulated_mesh.polygons:
        
        x_min = 100000.0
        x_max = -100000.0
        z_min = 100000.0
        z_max = -100000.0
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_coord_index = triangulated_mesh.loops[loop_index].vertex_index
            co = triangulated_mesh.vertices[blender_vertex_coord_index].co
            x_min = min(x_min, co.x)         
            x_max = max(x_max, co.x)         
            z_min = min(z_min, co.z)         
            z_max = max(z_max, co.z)         
           
        x_size = x_max-x_min             
        z_size = z_max-z_min    
        x_size_min = min(x_size_min, x_size)         
        x_size_max = max(x_size_max, x_size)         
        z_size_min = min(z_size_min, z_size)         
        z_size_max = max(z_size_max, z_size)  
        if (x_size<25):
            x_0_25 = x_0_25 + 1               
        elif (x_size<50):
            x_25_50 = x_25_50 + 1    
        elif (x_size<75):
            x_50_75 = x_50_75 + 1
        else:
            x_75_ = x_75_ + 1
            
        if (z_size<25):
            z_0_25 = z_0_25 + 1               
        elif (z_size<50):
            z_25_50 = z_25_50 + 1    
        elif (z_size<75):
            z_50_75 = z_50_75 + 1
        else:
            z_75_ = z_75_ + 1            
        
    bpy.data.meshes.remove(triangulated_mesh)  
    
    print("x_size_min: %f" % x_size_min)
    print("x_size_max: %f" % x_size_max)
    print("z_size_min: %f" % z_size_min)
    print("z_size_max: %f" % z_size_max)
    
    print("x_0_25: %d" % x_0_25)
    print("x_25_50: %d" % x_25_50)
    print("x_50_75: %d" % x_50_75)
    print("x_75_: %d" % x_75_)    
    
    print("z_0_25: %d" % z_0_25)
    print("z_25_50: %d" % z_25_50)
    print("z_50_75: %d" % z_50_75)
    print("z_75_: %d" % z_75_)     
