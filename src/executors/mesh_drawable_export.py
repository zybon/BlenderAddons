# ##### ZYB3D creator #####
#
# 2021.07.11. 12:00
# 

import os

import bpy
import mathutils
import math
import zyb_utils
from time import localtime, strftime

proj_dir = ""
image_errors = []


class FloatList():
    
    def __init__(self, name):
        self.name = name
        self.temp_dict = {}
        self.list = []
        self.indexed_list = {}
        self.unique_count = 0
        
    def add_float_to_indexed_list(self, value, index):
        dict_val = self.indexed_list.get(index)

        if dict_val is None:        
            self.indexed_list[index] = zyb_utils.float_round(value, 6)
            self.unique_count += 1 
        
    def add_float(self, value):
        dict_key = zyb_utils.float_round(value, 6)

        #az átmeneti tárolóban az index:
        dict_val = self.temp_dict.get(dict_key)

        if dict_val is None:
            #ha még nincs az átmeneti tárolóban
            dict_val = self.temp_dict[dict_key] = self.unique_count

            self.list.append(dict_key)

            self.unique_count += 1  
            
        return dict_val
            
        
    def write_to_txt(self, fw):  
        
        fw("%s (length: %s)\n" % (self.name, self.unique_count))
        
        if (len(self.indexed_list) > 0):
            for i, value in self.indexed_list.items():
                fw("\t%d. (%s)\n" % (i, str(value)))    
        else:
            for i, value in enumerate(self.list):
                fw("\t%d. (%s)\n" % (i, str(value)))    
        fw("\n")
        
    def write_to_bin(self, fw):  
        _length = self.unique_count
        fw(zyb_utils.int_to_bytes(_length))
        if (len(self.indexed_list) > 0):
            for i, value in self.indexed_list.items():
                fw(zyb_utils.float_to_bytes(value))  
        else:        
            for value in self.list:
                fw(zyb_utils.float_to_bytes(value))      
    
class VectorList():
    
    def __init__(self, name):
        self.name = name
        self.temp_dict = {}
        self.list = []
        self.indexed_list = {}
        self.unique_count = 0
        
    def add_vector_to_indexed_list(self, vector, index):
        dict_val = self.indexed_list.get(index)

        if dict_val is None:        
            self.indexed_list[index] = zyb_utils.vector_round(vector, 6)
            self.unique_count += 1 
        
    def add_vector(self, vector):
        dict_key = zyb_utils.vector_round(vector, 6)

        #az átmeneti tárolóban az index:
        dict_val = self.temp_dict.get(dict_key)

        if dict_val is None:
            #ha még nincs az átmeneti tárolóban
            dict_val = self.temp_dict[dict_key] = self.unique_count

            self.list.append(dict_key)

            self.unique_count += 1  
            
        return dict_val
        
    def write_to_txt(self, fw):  
        
        fw("%s (length: %s)\n" % (self.name, self.unique_count))
        
        if (len(self.indexed_list) > 0):
            for i, vector in self.indexed_list.items():
                fw("\t%d. (%s)\n" % (i, zyb_utils.vector_to_string(vector)))    
        else:
            for i, vector in enumerate(self.list):
                fw("\t%d. (%s)\n" % (i, zyb_utils.vector_to_string(vector)))    
        fw("\n")
        
    def write_to_bin(self, fw):  
        _length = self.unique_count
        fw(zyb_utils.int_to_bytes(_length))
        if (len(self.indexed_list) > 0):
            for i, vector in self.indexed_list.items():
                fw(zyb_utils.vector_to_bytes(vector))  
        else:        
            for vector in self.list:
                fw(zyb_utils.vector_to_bytes(vector))  
                
class IndexedVertexList():
    
    def __init__(self, name):
        self.name = name
        self.temp_dict = {}
        self.list = []
        self.indexed_list = {}
        self.unique_count = 0
        
    def add_vertex(self, vertex_coord, normal_vector, tex_coord, weight, vertex_color):
        dict_key = (zyb_utils.vector_round(vertex_coord, 6), 
            zyb_utils.vector_round(normal_vector, 6),
            zyb_utils.vector_round(tex_coord, 6),
            zyb_utils.float_round(weight, 6),
            zyb_utils.vector_round(vertex_color, 6)
            )

        #az átmeneti tárolóban az index:
        dict_val = self.temp_dict.get(dict_key)

        if dict_val is None:
            #ha még nincs az átmeneti tárolóban
            dict_val = self.temp_dict[dict_key] = self.unique_count

            self.list.append(dict_key)

            self.unique_count += 1  
            
        return dict_val
            
# ~ class WeightsDatas():
    
    # ~ def __init__(self):
        # ~ self.weights_lists = {}
        # ~ self.unique_count = 0
        
    # ~ def append_weight(self, name, weight_float):
        # ~ weight_list_index = self.weights_lists.get(name)

        # ~ if weight_list_index is None:
            # ~ self.weights_lists[name] = FloatList(name)
            # ~ weight_list_index = self.unique_count
            # ~ self.unique_count += 1
        # ~ weight_list =     
        # ~ weight_index = self.weights_lists[name].add_float(weight_float)
        # ~ return ()

    
            
class Rect():
    
    def __init__(self):
        self.minX = 1000000.0
        self.maxX = -1000000.0
        
        self.minZ = 1000000.0
        self.maxZ = -1000000.0
        
    def stretch_if_need(self, rect):
        if rect.minX<self.minX:
            self.minX = rect.minX
        if rect.minZ<self.minZ:
            self.minZ = rect.minZ  
            
        if rect.maxX>self.maxX:
            self.maxX = rect.maxX
        if rect.maxZ>self.maxZ:
            self.maxZ = rect.maxZ              
       
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

class Triangle():

    def __init__(self):
        self.vertices_indices = []
        self.vertices_coords = []
        
        self.normal_indices = []
        self.normal_vectors = []
        
        self.has_texture_coords = False
        self.texture_coords_indices = [] 
        self.texture_coords = []
        
        self.rect = Rect()
        
        self.parent_is_indexed = False
        
        self.has_weights = False
        self.weights_indices = []         
        self.weights = []        
        
        self.has_vertex_colors = False
        self.vertex_colors_indices = []         
        self.vertex_colors = []
        
    def set_index(self, index):
        self.index = index
        
    def set_parent_is_indexed(self, parent_is_indexed):
        self.parent_is_indexed = parent_is_indexed        
        
    def set_material_index(self, material_index):
        self.material_index = material_index    
        
    def set_center(self, center):
        self.center = center    
       
    def append_vertex(self, vertex_coord, vertex_index):
        self.vertices_coords.append(mathutils.Vector(vertex_coord))  
        self.vertices_indices.append(vertex_index)   
        
    def get_vertex_coord(self, index):
        return self.vertices_coords[index]
        
    def append_normal(self, normal_vector, normal_index):
        self.normal_vectors.append(mathutils.Vector(normal_vector)) 
        self.normal_indices.append(normal_index)
        
    def get_normal_vector(self, index):
        return self.normal_vectors[index]        
        
    def set_has_texture_coords(self, has_texture_coords):
        self.has_texture_coords = has_texture_coords
        
    def append_texture_coord(self, texture_coords, texture_coords_index):
        self.texture_coords.append(mathutils.Vector(texture_coords))
        self.texture_coords_indices.append(texture_coords_index) 
        
    def get_texture_coord(self, index):
        return self.texture_coords[index]  
        
    def set_has_weights(self, has_weights):
        self.has_weights = has_weights        
        
    def append_weight(self, weight, weight_index):
        self.weights.append(weight)
        self.weights_indices.append(weight_index) 
        
    def get_weight(self, index):
        return self.weights[index]                   
        
    def set_has_vertex_colors(self, has_vertex_colors):
        self.has_vertex_colors = has_vertex_colors        
        
    def append_vertex_color(self, vertex_color, vertex_color_index):
        self.vertex_colors.append(mathutils.Vector([vertex_color[0],vertex_color[1],vertex_color[2]]))
        self.vertex_colors_indices.append(vertex_color_index)   
        
    def get_vertex_color(self, index):
        return self.vertex_colors[index]                          
        
    def init_rect(self):
        rect = self.rect
        for co in self.vertices_coords:
            if co.x < rect.minX:
                rect.minX = co.x
            if co.z < rect.minZ:
                rect.minZ = co.z
                
            if co.x > rect.maxX:
                rect.maxX = co.x
            if co.z > rect.maxZ:
                rect.maxZ = co.z
                
    def __str__(self):
        txt = str(self.vertices_indices)
        txt = txt + ", "+str(self.normal_indices)
        txt = txt + ", "+str(vec3d_round(self.center, 6))
#        txt = txt + ", "+str(self.rect)
        if (self.has_texture_coords):
            return txt+", "+str(self.texture_coords_indices)
        else:
            return txt
        
    def write_to_txt(self, fw):
        fw("\t%d. triangle" % (self.index))
        fw(" [material_index: %d]" % (self.material_index))
        fw("\n\t\t{")
        for i in range(3):
            fw("%d" % (self.vertices_indices[i]))
            if (self.parent_is_indexed is False):
                fw(", %d" % (self.normal_indices[i]))
                if (self.has_texture_coords):
                    fw(", %d" % (self.texture_coords_indices[i]))
                if (self.has_weights):
                    fw(", %d" % (self.weights_indices[i]))
                if (self.has_vertex_colors):
                    fw(", %d" % (self.vertex_colors_indices[i]))                                        
            
            if (i<2):
                fw(" # ")
        fw("}\n")
        
    def write_coords_to_txt(self, fw):
        fw("\t%d. triangle\n" % (self.index))
        fw("\t\t{")
        
        fw("vertices:\n%s\n" % str(self.vertices_coords))
        fw("normals:\n%s\n" % str(self.normal_vectors))
        if (self.has_texture_coords):
            fw("texture_coords:\n%s\n" % str(self.texture_coords))        
        
        fw("}\n")        
        
    # ~ def write_to_txt_indexed(self, fw):
        # ~ fw("\t%d. " % (self.index))
        # ~ fw("[material_index: %d]" % (self.material_index))
        # ~ fw("\t\t{")
        # ~ for i in range(3):
            # ~ fw("%d " % (self.vertices_indices[i]))
            # ~ if (i<2):
                # ~ fw(" # ")
        # ~ fw("}\n")        
                
    def write_to_bin(self, fw):
        for i in range(3):
            fw(zyb_utils.int_to_bytes(self.vertices_indices[i]))
            if (self.parent_is_indexed is False):
                fw(zyb_utils.int_to_bytes(self.normal_indices[i]))
                if (self.has_texture_coords):
                    fw(zyb_utils.int_to_bytes(self.texture_coords_indices[i]))  
                if (self.has_weights):
                    fw(zyb_utils.int_to_bytes(self.weights_indices[i]))  
                if (self.has_vertex_colors):
                    fw(zyb_utils.int_to_bytes(self.vertex_colors_indices[i]))       
                    
    def write_to_bin_raw(self, fw):
        for i in range(3):
            fw(zyb_utils.vector_to_bytes(self.vertices_coords[i]))
            if (self.parent_is_indexed is False):
                fw(zyb_utils.vector_to_bytes(self.normal_vectors[i]))
                if (self.has_texture_coords):
                    fw(zyb_utils.vector_to_bytes(self.texture_coords[i]))  
                if (self.has_weights):
                    fw(zyb_utils.float_to_bytes(self.weights[i]))  
                if (self.has_vertex_colors):
                    fw(zyb_utils.vector_to_bytes(self.vertex_colors[i]))                                                           
                      
                
    # ~ def write_to_bin_indexed(self, fw):
        # ~ for i in range(3):
            # ~ fw(int_to_bytes(self.vertices_indices[i]))



        
class Sector():
    
    def __init__(self, index, row_column):
        self.index = index
        self.name = "R%d_C%d" % row_column
        # ~ self.parentMeshData = parentMeshData;
        self.vertex_list = VectorList("vertices")
        self.normal_list = VectorList("normals")  
        self.texture_coord_list = VectorList("texture_coods")        
        self.triangles = []
        
    def add_triangle(self, triangle):
        self.triangles.append(triangle)
        
#    def add_triangle(self, parent_triangle):
#        triangle = Triangle(parent_triangle.index)
#        triangle.set_center(parent_triangle.center) 
#        triangle.set_has_texture_coords(parent_triangle.has_texture_coords)
#        for i in range(3):
#            vertex_coord = parent_triangle.vertices_coords[i]
#            vertex_index = self.vertex_list.add_vector(vertex_coord)
#            triangle.append_vertex(vertex_coord, vertex_index)
#
#            normal_vector = parent_triangle.normal_vectors[i]
#            normal_index = self.normal_list.add_vector(normal_vector)
#            triangle.append_normal(normal_vector, normal_index)
#
#            if (triangle.has_texture_coords):
#                tex_coord = parent_triangle.texture_coords[i]
#                texture_coord_index = self.texture_coord_list.add_vector(tex_coord)
#                triangle.append_texture_coord(tex_coord, texture_coord_index)
#
##        triangle.init_rect()        
#        self.triangles.append(triangle) 
        
    def num_of_triangles(self):    
        return len(self.triangles)
    
#    def write_to_txt(self, fw):
#        fw("\n################  "+self.name+"  ###################\n") 
#        fw("name: %s\n" % self.name)    
#        fw("position %s\n" % vector_to_string((0,0,0)))
#        fw("rotation_angle: %s\n" % 0)
#        fw("rotation_axis: %s\n" % vector_to_string((0,0,0)))        
#        fw("scale: %s\n" % vector_to_string((1,1,1)))
#        fw("dimensions: %s\n" % vector_to_string((1,1,1)))
#        fw("color: %s\n" % vector_to_string(self.parentMeshData.color))
#        fw("has_texture_coords: %s\n" % self.parentMeshData.has_texture_coords)
#
#        if self.parentMeshData.has_texture_coords:
#            fw("texture kep: %s\n" % self.parentMeshData.texture_image)            
#        
#        fw("\n")
#        
#        self.vertex_list.write_to_txt(fw)    
#        self.normal_list.write_to_txt(fw)
#        if self.parentMeshData.has_texture_coords:
#            self.texture_coord_list.write_to_txt(fw)  
#            
#        fw("triangles: \n")
#        fw("length: %d\n" % (len(self.triangles)))
#        for triangle in self.triangles:
#            triangle.write_to_txt(fw)     
        
    def write_to_txt(self, fw):
        fw("(index: %d)" % self.index)
        fw(" [num of triangles: %d]\n" % self.num_of_triangles())
        for triangle in self.triangles:
            triangle.write_to_txt(fw)
            fw("\n")
        
    def write_to_bin(self, fw):
        fw(zyb_utils.int_to_bytes(self.index))
        fw(zyb_utils.int_to_bytes(self.num_of_triangles()))
        for triangle in self.triangles:
            triangle.write_to_bin(fw)
        
class Sectors():
    
    def __init__(self, column_size, row_size):
        self.rect = Rect()
        self.column_size = column_size
        self.row_size = row_size  
        self.sectors = {}

            
    def load_triangles(self, triangles):
        for triangle in triangles:
            self.rect.stretch_if_need(triangle.rect)  
            
        size_x = self.rect.x_size()    
        size_z = self.rect.z_size()
        # ~ print(size_x, size_z)
        self.column_number = math.ceil(size_x/self.column_size) 
        self.row_number = math.ceil(size_z/self.row_size)
        
        for row in range(self.row_number):
            for column in range(self.column_number):    
                self.sectors[(row, column)] = Sector(row*self.column_number+column, (row, column))   
        
        for triangle in triangles:
            self.append_to_sector(triangle)             
            
    def append_to_sector(self, triangle):
        #x = triangle.center[0]
        #z = triangle.center[2]
        x = triangle.rect.minX;
        z = triangle.rect.minZ;
        column = (int)((x-self.rect.minX)/self.column_size);
        row = (int)((z-self.rect.minZ)/self.row_size);
        self.sectors[(row, column)].add_triangle(triangle)              
    
    def write_to_txt(self, fw):
        fw("sectors\n")    
        fw("rect %s\n" % self.rect)
        fw("row_size: %.5f\n" % self.row_size)
        fw("column_size: %.5f\n" % self.column_size)        
        fw("row_number: %d\n" % self.row_number)
        fw("column_number: %d\n" % self.column_number)
        for row in range(self.row_number):
            for column in range(self.column_number):  
                sector = self.sectors[(row, column)]
                fw("(row: %d, column: %d) " % (row, column))
                sector.write_to_txt(fw)
#                if ((row)%2==0 and (column+1)%2==0):
#                    for t in sector.triangles:
#                        bpy.context.object.data.polygons[t.index].select = True
#                else:        
#                    if ((row+1)%2==0 and (column)%2==0):
#                        for t in sector.triangles:
#                            bpy.context.object.data.polygons[t.index].select = True         
                
    def write_to_bin(self, fw):        
        self.rect.write_to_bin(fw)
        fw(zyb_utils.float_to_bytes(self.column_size))
        fw(zyb_utils.int_to_bytes(self.column_number))
        fw(zyb_utils.float_to_bytes(self.row_size))
        fw(zyb_utils.int_to_bytes(self.row_number))
        
        for row in range(self.row_number):
            for column in range(self.column_number):  
                sector = self.sectors[(row, column)]
                sector.write_to_bin(fw) 
 
      
class ZybMeshObject():
    
    def __init__(self):
        self.vertex_list = VectorList("vertex vector list")
        self.normal_list = VectorList("normal vector list")  
        self.texture_coord_list = VectorList("texture_coord vector list")
        self.weight_list = FloatList("weight list")
        self.vertex_color_list = VectorList("vertexcolor list")
        self.indexed_vertex_list = IndexedVertexList("indexed list")
        self.sectored = False
        self.indexed = False
        self.has_weights = False
        self.has_vertex_colors = False      
        self.triangles = []
        
        self.from_index = 0
        self.data_length = 0        
        # ~ if (self.blender_object.z3dexport_settings.mesh_settings.sector):
            # ~ self.sectors = Sectors(self) 
            
    def set_name(self, name):
        self.name = name                 
            
    def set_geometry(self, geometry):
        self.geometry = geometry            
            
    def set_material(self, material):
        self.material = material
        
    def set_has_texture_coords(self, has_texture_coords):
        self.has_texture_coords = has_texture_coords  
        
    def set_has_weights(self, has_weights):
        self.has_weights = has_weights 
        
    def set_has_vertex_colors(self, has_vertex_colors):
        self.has_vertex_colors = has_vertex_colors                   
        
    def set_indexed(self, indexed):
        self.indexed = indexed           
        
    def append_triangles(self, blender_triangles):
        print("---- append_triangles()")
        size = len(blender_triangles)
        p = 0        
        for blender_triangle in blender_triangles:
            zyb_triangle = Triangle()
            zyb_triangle.set_index(blender_triangle.index)
            zyb_triangle.set_material_index(blender_triangle.material_index)
            zyb_triangle.set_center(blender_triangle.center)
            zyb_triangle.set_has_texture_coords(blender_triangle.has_texture_coords)
            zyb_triangle.set_has_weights(blender_triangle.has_weights)
            zyb_triangle.set_has_vertex_colors(blender_triangle.has_vertex_colors)
            zyb_triangle.set_parent_is_indexed(self.indexed)
            for i in range(3):
                vertex_coord = blender_triangle.get_vertex_coord(i)
                # ~ print("vertex_coord %s" % (zyb_utils.vector_to_string(vertex_coord)))
                vertex_index = self.vertex_list.add_vector(vertex_coord)
                zyb_triangle.append_vertex(vertex_coord, vertex_index)
                
                normal_vector = blender_triangle.get_normal_vector(i)
                normal_index = self.normal_list.add_vector(normal_vector)
                zyb_triangle.append_normal(normal_vector, normal_index)
                
                if (blender_triangle.has_texture_coords):
                    tex_coord = blender_triangle.get_texture_coord(i)
                    
                    if (math.isnan(tex_coord[0])):
                        raise Exception("tex_coord0 is None:" + str(vertex_coord)) 
                    if (math.isnan(tex_coord[1])):
                        raise Exception("tex_coord1 is None:" + str(vertex_coord)+""+str(tex_coord)+" #"+str(i)) 
                        
                    tex_coord_index = self.texture_coord_list.add_vector(tex_coord)                                 
                    zyb_triangle.append_texture_coord(tex_coord, tex_coord_index)
                    
                if (blender_triangle.has_weights):
                    weight = blender_triangle.get_weight(i)
                    # ~ print(weight)
                    weight_index = self.weight_list.add_float(weight)                                 
                    zyb_triangle.append_weight(weight, weight_index)   
                    
                if (blender_triangle.has_vertex_colors):
                    vertex_color = blender_triangle.get_vertex_color(i)
                    # ~ print(vertex_color)
                    vertex_color_index = self.vertex_color_list.add_vector(vertex_color)                                 
                    zyb_triangle.append_vertex_color(vertex_color, vertex_color_index)                                      
                    
                    
            zyb_triangle.init_rect()
            self.triangles.append(zyb_triangle)
            p = p+1
            percent = int((p/size)*100)
            print('----- triangles added: %s%%' % (percent), end="\r")     
        print()            
            
    def create_index_to_indexed_list(self, blender_triangle, i):
        vertex_coord = blender_triangle.get_vertex_coord(i)
        normal_vector = blender_triangle.get_normal_vector(i)
        tex_coord = mathutils.Vector([0.0, 0.0])
        if (blender_triangle.has_texture_coords):
            tex_coord = blender_triangle.get_texture_coord(i)
            
            if (math.isnan(tex_coord[0])):
                raise Exception("tex_coord0 is None:" + str(vertex_coord)) 
            if (math.isnan(tex_coord[1])):
                raise Exception("tex_coord1 is None:" + str(vertex_coord)+""+str(tex_coord)+" #"+str(i))
        
        weight = 0.0
        if (blender_triangle.has_weights):  
            weight = blender_triangle.get_weight(i)  
            
        vertex_color = mathutils.Vector([0.0, 0.0, 0.0, 0.0])
        if (blender_triangle.has_vertex_colors):  
            vertex_color = blender_triangle.get_vertex_color(i)                     
                
        return self.indexed_vertex_list.add_vertex(vertex_coord, normal_vector, tex_coord, weight, vertex_color)
                
                        
            
    def append_indexed_triangles(self, blender_triangles):
        print("---- append_indexed_triangles()") 
        size = len(blender_triangles)
        p = 0
        for blender_triangle in blender_triangles:
            
            zyb_triangle = Triangle()
            zyb_triangle.set_index(blender_triangle.index)
            zyb_triangle.set_material_index(blender_triangle.material_index)
            zyb_triangle.set_center(blender_triangle.center)
            zyb_triangle.set_has_texture_coords(blender_triangle.has_texture_coords)
            zyb_triangle.set_parent_is_indexed(self.indexed)
            for i in range(3):
                
                vertex_index = self.create_index_to_indexed_list(blender_triangle, i)
                
                vertex_coord = blender_triangle.get_vertex_coord(i)
                self.vertex_list.add_vector_to_indexed_list(vertex_coord, vertex_index)
                zyb_triangle.append_vertex(vertex_coord, vertex_index)
                
                normal_vector = blender_triangle.get_normal_vector(i)
                self.normal_list.add_vector_to_indexed_list(normal_vector, vertex_index)
                zyb_triangle.append_normal(normal_vector, vertex_index)
                
                if (blender_triangle.has_texture_coords):
                    tex_coord = blender_triangle.get_texture_coord(i)
                    
                    if (math.isnan(tex_coord[0])):
                        raise Exception("tex_coord0 is None:" + str(vertex_coord)) 
                    if (math.isnan(tex_coord[1])):
                        raise Exception("tex_coord1 is None:" + str(vertex_coord)+""+str(tex_coord)+" #"+str(i)) 
                                            
                    self.texture_coord_list.add_vector_to_indexed_list(tex_coord, vertex_index)
                    zyb_triangle.append_texture_coord(tex_coord, vertex_index)
                    
                if (blender_triangle.has_weights):
                    weight = blender_triangle.get_weight(i)
                    self.weight_list.add_float_to_indexed_list(weight, vertex_index)                                 
                    zyb_triangle.append_weight(weight, vertex_index)   
                    
                if (blender_triangle.has_vertex_colors):
                    vertex_color = blender_triangle.get_vertex_color(i)
                    self.vertex_color_list.add_vector_to_indexed_list(vertex_color, vertex_index)                                 
                    zyb_triangle.append_vertex_color(vertex_color, vertex_index)                      
                    
            zyb_triangle.init_rect()
            self.triangles.append(zyb_triangle) 
            p = p+1
            percent = int((p/size)*100)
            print('----- triangles added: %s%%' % (percent), end="\r")     
        print()
            
            
    def init_sectors(self, column_size, row_size):
        self.sectored = True
        self.sectors = Sectors(column_size, row_size)
        self.sectors.load_triangles(self.triangles)
            
    def write_to_txt(self, fw):

        fw("\n############### ZybMeshObject #######################\n")
        fw("name: %s\n" % self.name)    
        self.geometry.write_to_txt(fw)
        
        self.material.write_to_txt(fw)
        fw("has_texture_coords: %s\n" % self.has_texture_coords) 
        fw("indexed: %s\n" % self.indexed) 
        fw("sectored: %s\n" % self.sectored)        
        fw("\n")
        
        
        self.vertex_list.write_to_txt(fw) 
        self.normal_list.write_to_txt(fw)
        
        if self.has_texture_coords:
            self.texture_coord_list.write_to_txt(fw)    
            
        if self.has_weights:
            self.weight_list.write_to_txt(fw) 
            
        if self.has_vertex_colors:
            self.vertex_color_list.write_to_txt(fw)                          
            
        if(self.sectored):
            self.sectors.write_to_txt(fw)
        else:
            fw("triangles:  (length: %d)\n" % (len(self.triangles)))
            # ~ if (self.indexed):
                # ~ for triangle in self.triangles:
                    # ~ triangle.write_to_txt_indexed(fw)   
            # ~ else:
            for triangle in self.triangles:
                triangle.write_to_txt(fw)   
        fw("\n#################################################\n")
        
    def write_to_bin(self, fw):
        nevb = str.encode(self.name)
        fw(bytes([len(nevb)]))
        fw(nevb)
        
        self.geometry.write_to_bin(fw)
        
        self.material.write_to_bin(fw)        

        if (self.indexed):
            fw(bytes([1]))
        else:
            fw(bytes([0]))
            
        self.vertex_list.write_to_bin(fw)
        self.normal_list.write_to_bin(fw)
        if self.has_texture_coords:
            fw(bytes([1]))
            self.texture_coord_list.write_to_bin(fw)  
        else:
            fw(bytes([0]))
            
        if self.has_weights:
            fw(bytes([1]))
            self.weight_list.write_to_bin(fw)  
        else:
            fw(bytes([0]))
            
        if self.has_vertex_colors:
            fw(bytes([1]))
            self.vertex_color_list.write_to_bin(fw)  
        else:
            fw(bytes([0]))                        

        if(self.sectored):
            fw(bytes([1]))
            self.sectors.write_to_bin(fw)
        else:            
            fw(bytes([0]))
            fw(zyb_utils.int_to_bytes(len(self.triangles)))    
            for triangle in self.triangles:
                triangle.write_to_bin(fw)         
               
    def write_to_bin_raw(self, fw):
        nevb = str.encode(self.name)
        fw(bytes([len(nevb)]))
        fw(nevb)
        
        self.geometry.write_to_bin(fw)
        
        self.material.write_to_bin(fw)        

        if (self.indexed):
            fw(bytes([1]))
        else:
            fw(bytes([0]))
            
        if self.has_texture_coords:
            fw(bytes([1]))
        else:
            fw(bytes([0]))
            
        if self.has_weights:
            fw(bytes([1]))
        else:
            fw(bytes([0]))
            
        if self.has_vertex_colors:
            fw(bytes([1]))
        else:
            fw(bytes([0]))                        

        if(self.sectored):
            fw(bytes([1]))
        else:            
            fw(bytes([0]))
            fw(zyb_utils.int_to_bytes(len(self.triangles)))    
            for triangle in self.triangles:
                triangle.write_to_bin_raw(fw)       

class ImageError():
    
    def __init__(self, blender_object_name, material_name, image):
        self.blender_object_name = blender_object_name
        self.material_name = material_name
        self.image = image
        
    def __str__(self):
        text = ("'%s'\n" % bpy.path.basename(self.image.filepath))
        text += ("\t['%s' object, " % self.blender_object_name)
        text += ("'%s' material]\n" % self.material_name)
        return text
        
class Materials():
    
    def __init__(self, blender_object):
        self.materials = []
        self.count = len(blender_object.data.materials)
        if (self.count == 0):
            raise Exception("'"+blender_object.name+"' has no material")            
        
        for material in blender_object.data.materials:
            
            # ~ if (material.users == 0):
                # ~ raise Exception("'"+blender_object.name+"' has no texture_slots[0]"+
                                    # ~ " in material: ["+material.name+"]")   
            self.materials.append(Material(blender_object, material))
            
    def write_to_txt(self, fw):  
        fw("\n#* Materials: #****\n")
        fw("length: %s\n" % self.count)
        
        for i, material in enumerate(self.materials):
            fw("%d. material\n" % (i))  
            material.write_to_txt(fw)
        fw("\n####***\n")
        
    def write_to_bin(self, fw):  
        _length = self.count
        fw(zyb_utils.int_to_bytes(_length))
        for material in self.materials:
            material.write_to_bin(fw) 
            

    
      
class Material():

    
    def __init__(self, blender_object, blender_material):
        self.blender_object = blender_object
        self.name = blender_material.name
        self.diffuse_color = blender_material.diffuse_color
        self.diffuse_intensity = blender_material.diffuse_intensity
        self.texture = blender_material.texture_slots[0]
        if (self.texture is not None):
            self.check_image_in_projdir(self.texture.texture.image)
            
    def check_image_in_projdir(self, image):
        global proj_dir  
        global image_errors
        drawable_path = proj_dir+"res\\drawable-nodpi\\"
        
        image_name = bpy.path.basename(image.filepath)
        path = drawable_path+image_name
        if (os.path.exists(path) == False):  
            not_reported = True
            for i, e in enumerate(image_errors):
                if (e.image == image):
                    not_reported = False
                    break 
            if (not_reported):        
                image_errors.append(ImageError(self.blender_object.name, 
                                        self.name,
                                        image))    
            # ~ image_errors.append("{"+self.blender_object.name+"} object ["+self.name+"] material '"+image_name+"' image is not in '"+drawable_path+"'")            
                
    def write_to_txt(self, fw):  
        
        fw("\tname: %s\n" % self.name)
        fw("\tdiffuse_color: %s\n" % zyb_utils.vector_to_string(self.diffuse_color))
        fw("\tdiffuse_intensity: %s\n" % str(self.diffuse_intensity))
        if (self.texture is None):
            fw("\tno texture\n")
        else:
            fw("\ttexture_image file name: %s\n" % 
                bpy.path.display_name_from_filepath(self.texture.texture.image.filepath))
            # ~ fw("\timage_tex_coords: %s\n" % self.texture.texture_coords)
            # ~ if (self.texture.texture_coords == 'UV'):
                # ~ fw("\tuv_layer: %s\n" % self.texture.uv_layer)
                
            fw("\timage_tex_coords_scale: %s\n" % zyb_utils.vector_to_string(self.texture.scale))
            fw("\timage_diffuse_mix: %s\n" % str(self.texture.blend_type == 'MULTIPLY'))
             
        fw("\n")
        
    def write_to_bin(self, fw):  
        
        nevb = str.encode(self.name)
        fw(bytes([len(nevb)]))
        fw(nevb)  
        
        fw(zyb_utils.vector_to_bytes(self.diffuse_color))
        fw(zyb_utils.float_to_bytes(self.diffuse_intensity))
        if (self.texture is None):
            fw(bytes([0]))
        else:
            fw(bytes([1]))
            image_filename = bpy.path.display_name_from_filepath(self.texture.texture.image.filepath)
            image_filename_in_bytes = str.encode(image_filename)
            fw(bytes([len(image_filename_in_bytes)]))
            fw(image_filename_in_bytes) 
            fw(zyb_utils.vector_to_bytes(self.texture.scale))
            diffuse_mix_with_image = (self.texture.blend_type == 'MULTIPLY')
            if (diffuse_mix_with_image):
                fw(bytes([1]))
            else:
                fw(bytes([0]))  
        

          
class Geometry():
    
    def __init__(self, blender_object):
        # ez a mátrix forgatja a Blender worldből az OpenGl worldbe
        # Blender = X:jobb, Y:előre, Z:fel
        # OpenGl = X:jobb, Y:fel, Z:hátra
        self.BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
        
        self.position = self.BLENDER_TO_ANDROID_OPENGL_MATRIX * blender_object.location

        #rotation
        self.rotation_angle = blender_object.rotation_axis_angle[0]*180.0/math.pi
        self.rotation_axis = zyb_utils.vector_round(self.BLENDER_TO_ANDROID_OPENGL_MATRIX * mathutils.Vector(blender_object.rotation_axis_angle[1:]), 6)
    #    print(self.'rotation'])
    
        self.scale = zyb_utils.vector_round(self.BLENDER_TO_ANDROID_OPENGL_MATRIX * blender_object.scale, 6)
        self.scale = (self.scale[0], self.scale[1], -self.scale[2])
    
        #meret
        self.dimensions = zyb_utils.vector_round(self.BLENDER_TO_ANDROID_OPENGL_MATRIX * blender_object.dimensions, 6)
        self.dimensions = (self.dimensions[0], self.dimensions[1], abs(-self.dimensions[2])) 
        
        self.model_mtx = zyb_utils.createIdentityMatrix()
        self.model_mtx = zyb_utils.translateMatrix(self.model_mtx, self.position.x, self.position.y, self.position.z)
        self.model_mtx = zyb_utils.rotateMatrix(self.model_mtx, self.rotation_angle, self.rotation_axis[0], self.rotation_axis[1], self.rotation_axis[2])
        self.model_mtx = zyb_utils.scaleMatrix(self.model_mtx, self.scale[0], self.scale[1], self.scale[2])
        
        # ~ self.visibility_center = blender_object.z3dexport_settings.mesh_settings.
        
    def write_to_txt(self, fw):  
        fw("\n#* Geometry: #****\n")
        fw("position %s\n" % zyb_utils.vector_to_string(self.position))
        fw("rotation_angle: %s\n" % self.rotation_angle)
        fw("rotation_axis: %s\n" % zyb_utils.vector_to_string(self.rotation_axis))        
        fw("scale: %s\n" % zyb_utils.vector_to_string(self.scale))
        fw("dimensions: %s\n" % zyb_utils.vector_to_string(self.dimensions))  
        fw("model matrix:\n")
        fw("%s\n" % zyb_utils.matrixfloatarray_to_string(self.model_mtx)) 
        fw("\n####**\n") 

        
    def write_to_bin(self, fw):
        fw(zyb_utils.vector_to_bytes(self.position))

        fw(zyb_utils.float_to_bytes(self.rotation_angle))
        fw(zyb_utils.vector_to_bytes(self.rotation_axis))
        
        fw(zyb_utils.vector_to_bytes(self.scale))

        fw(zyb_utils.vector_to_bytes(self.dimensions))        
        
                     
class BlenderTriangles():
    
    def __init__(self, blender_mesh_object):
        # ~ print(blender_mesh_object.name)
        self.blender_mesh_object = blender_mesh_object
        
        self.has_weights = blender_mesh_object.blender_object.z3dexport_settings.mesh_settings.export_weight
        if (self.has_weights):
            self.weight_group_index = blender_mesh_object.blender_object.vertex_groups['weights'].index
        self.has_vertex_colors = blender_mesh_object.blender_object.z3dexport_settings.mesh_settings.export_vertexcolor
        
        self.init_triangulated_mesh()
        
        self.mesh_loops = self.triangulated_mesh.loops
        self.mesh_vertices = self.triangulated_mesh.vertices[:]          
        
        # UV ellenőrzés, hogy van e UV texture
        self.has_texture_coords = len(self.triangulated_mesh.uv_layers) > 0
        if self.has_texture_coords:
            self.blender_active_uv_layer_datas = self.triangulated_mesh.uv_layers.active.data[:] 

        self.read_triangles()
           
        # clean up
        bpy.data.meshes.remove(self.triangulated_mesh)    

        
    def init_triangulated_mesh(self):
        
        # temp mesh létrehozása úgy hogy modifiers-eket érvényesitik
        self.triangulated_mesh = self.blender_mesh_object.blender_object.to_mesh(
                        self.blender_mesh_object.context.scene, True, 'PREVIEW', calc_tessface=False)

        self.triangulated_mesh.transform(self.blender_mesh_object.geometry.BLENDER_TO_ANDROID_OPENGL_MATRIX)
        
        #háromszögelés, hogy minden face egy háromszög legyen
        # az elején meg kell csinálni mert ez újra képezi a loops tomboket
        zyb_utils.mesh_triangulate(self.triangulated_mesh)    
          
        #normálok számítása face-enként a vertexekhez
        self.triangulated_mesh.calc_normals_split()  
        
           
        
    def read_triangles(self):
        self.triangles_by_material_index = {}
        size = len(self.triangulated_mesh.polygons)
        p = 0
        for blender_polygon in self.triangulated_mesh.polygons:
            self.read_triangle(blender_polygon)
            p = p+1
            percent = int((p/size)*100)
            print('--- Polygons read: %s%%' % (percent), end="\r")
        print()
            
            
    def read_triangle(self, blender_polygon):
        triangle = Triangle()
        triangle.set_index(blender_polygon.index)
        triangle.set_material_index(blender_polygon.material_index)
        triangle.set_center(blender_polygon.center)
        triangle.set_has_texture_coords(self.has_texture_coords)
        triangle.set_has_weights(self.has_weights)
        triangle.set_has_vertex_colors(self.has_vertex_colors)
        for loop_index in blender_polygon.loop_indices:
            blender_vertex_index = self.mesh_loops[loop_index].vertex_index
            # ~ print("blender_vertex_index: %s" % (blender_vertex_index))
            _vertex = self.mesh_vertices[blender_vertex_index]
            vertex_coord = _vertex.co
            triangle.append_vertex(vertex_coord, 0)            

            normal_vector = self.mesh_loops[loop_index].normal
            triangle.append_normal(normal_vector, 0)

            if (self.has_texture_coords):
                tex_coord = self.blender_active_uv_layer_datas[loop_index].uv
                tex_coord[1] = -tex_coord[1]
                triangle.append_texture_coord(tex_coord, 0)
                
            if (self.has_weights):
                for group in _vertex.groups:
                    if (group.group == self.weight_group_index):
                        triangle.append_weight(group.weight, 0)
                        # ~ print(group.weight)
                
            if (self.has_vertex_colors):
                color = self.triangulated_mesh.vertex_colors[0].data[loop_index].color 
                triangle.append_vertex_color(color, 0)  
                # ~ print(color) 
                
        triangle.init_rect()      
        
        dictval = self.triangles_by_material_index.get(triangle.material_index)
        if (dictval is None):
            self.triangles_by_material_index[triangle.material_index] = []
          
        self.triangles_by_material_index[triangle.material_index].append(triangle)  
        
    def get_triangles_by_material_index(self, material_index):
        dictval = self.triangles_by_material_index.get(material_index)
        if (dictval is None):
            return None
        return self.triangles_by_material_index[material_index]    
        
    def write_to_txt(self, fw):  
        for i, triangles_by_material in self.triangles_by_material_index.items():
            fw("%d. material:\n" % (i))  
            fw("\t%d triangles\n" % len(triangles_by_material))
            for i, triangle in enumerate(triangles_by_material):
                triangle.write_coords_to_txt(fw)
       
            
class BlenderMeshDrawableObject():
    
    def __init__(self, context, blender_object):
        self.context = context
        self.blender_object = blender_object
        
        self.name = zyb_utils.name_compat(blender_object.name)
        # ~ print("-- Create BlenderMeshDrawableObject: "+blender_object.name)
        print("-- Create BlenderMeshDrawableObject ["+self.name+"]") 
        
        self.geometry = Geometry(blender_object)
        
        self.materials = Materials(blender_object)
        
        self.blender_triangles = BlenderTriangles(self) 
        

        
        self.zyb_meshobjects = []
        for material_index, material in enumerate(self.materials.materials):
            triangles_by_material = self.blender_triangles.get_triangles_by_material_index(material_index)
            if (triangles_by_material is None):
                continue
            zybmeshobject = ZybMeshObject()
            print("--- Create ZybMeshObject ["+self.name+"]")
            zybmeshobject.set_name(self.name)#+"__"+zyb_utils.name_compat(material.name))
            zybmeshobject.set_geometry(self.geometry)
            zybmeshobject.set_material(material)
            zybmeshobject.set_has_texture_coords(self.blender_triangles.has_texture_coords)
            zybmeshobject.set_has_weights(self.blender_triangles.has_weights)
            zybmeshobject.set_has_vertex_colors(self.blender_triangles.has_vertex_colors)
            if (self.blender_object.z3dexport_settings.mesh_settings.indexedmesh):
                zybmeshobject.set_indexed(True)
                zybmeshobject.append_indexed_triangles(triangles_by_material)
            else:
                zybmeshobject.set_indexed(False)
                zybmeshobject.append_triangles(triangles_by_material)
                
#            if (blender_object.z3dexport_settings.mesh_settings.sector):
#                column_size = blender_object.z3dexport_settings.mesh_settings.sector_columnsize  
#                row_size = blender_object.z3dexport_settings.mesh_settings.sector_rowsize                 
            self.zyb_meshobjects.append(zybmeshobject)
        
    def write_to_txt(self, fw):

        # ~ fw("\n----------------BlenderMeshDrawableObject-----------------\n")
        # ~ fw("name: %s\n" % self.name)    
        # ~ self.geometry.write_to_txt(fw)
        
        # ~ self.materials.write_to_txt(fw)
        
        # ~ fw("\n")
        
        # ~ self.blender_triangles.write_to_txt(fw)
        
        # ~ fw("\n--------------------------------------------------\n")
        
        for index, zybmeshobject in enumerate(self.zyb_meshobjects):
            zybmeshobject.write_to_txt(fw)
        
    def write_to_bin(self, f): 
        fw = f.write
        from_index = 0
        data_length = 0        
        for index, zybmeshobject in enumerate(self.zyb_meshobjects):
            from_index = f.tell()
            zybmeshobject.write_to_bin(fw)   
            data_length = f.tell() - from_index
            zybmeshobject.from_index = from_index
            zybmeshobject.data_length = data_length
            print(from_index, data_length)            
            
    def write_to_bin_raw(self, fw): 
        for index, zybmeshobject in enumerate(self.zyb_meshobjects):
            zybmeshobject.write_to_bin_raw(fw)      
            
                         
def write_to_bin_z3d(targetDirPath, filename, blender_mesh_objects):
    print("\n- write_to_bin_z3d()")
    if not os.path.exists(targetDirPath):
        print(targetDirPath+" created")
        os.makedirs(targetDirPath)    
    
    print("-- Objects data export to: "+targetDirPath+filename)
    with open((targetDirPath+filename), "wb") as f:
        

        for blender_mesh_object in blender_mesh_objects:
            print("--- Export "+blender_mesh_object.name)
            blender_mesh_object.write_to_bin(f)

            
            
            
            
def write_to_bin_raw_z3d(targetDirPath, filename, blender_mesh_objects):
    print("\n- write_to_bin_raw_z3d()")
    
    print("-- Objects raw data export to: "+targetDirPath+filename)
    with open((targetDirPath+filename), "wb") as f:
        fw = f.write
        for blender_mesh_object in blender_mesh_objects:
            print("--- Export "+blender_mesh_object.name)
            blender_mesh_object.write_to_bin_raw(fw)            
              
def write_to_txt_z3d(filename, blender_mesh_objects):
    print("\n- write_to_txt_z3d()")
    print("-- Temp file save to [C:\\Users\\User\\BlenderProjects\\temp\\"+filename+".txt]")
    with open(("C:\\Users\\User\\BlenderProjects\\temp\\"+filename+".txt"), "w") as f:
        fw = f.write
        for blender_mesh_object in blender_mesh_objects:
            blender_mesh_object.write_to_txt(fw)                  

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
        for blender_mesh_object in blender_mesh_objects:
            for index, zybmeshobject in enumerate(blender_mesh_object.zyb_meshobjects):
                fw(zybmeshobject.name)
                fw("#")
                fw(str(zybmeshobject.from_index))
                fw("#")
                fw(str(zybmeshobject.data_length))
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
            lineContent = line.strip()
            name = lineContent.split("#")[0]
            fw("        public static final String ")
            fw(name+" = ")
            fw('"meshes/')
            fw(collector_name)
            fw(".z3d#")
            fw(lineContent)
            fw('";\n')
    fw("    }\n")             

def read_blender_mesh_drawable_objects(context, objects):
    print("\n- read_blender_mesh_drawable_objects()")
    blender_mesh_objects = []

    if (len(objects) == 0):
        raise Exception("Some object is maybe in inactive scene layer")        

    # Get all meshes
    for object in objects:

        # ~ if (object.z3dexport_settings.mesh_settings.indexedmesh):
            # ~ raise Exception("az indexed mesh most még nem támogatott!!")
        # ~ print("-- Create BlenderMeshDrawableObject ["+object.name+"]") 
        blender_mesh_object = BlenderMeshDrawableObject(context, object)    
        blender_mesh_objects.append(blender_mesh_object)
        print("-- ["+blender_mesh_object.name+"] added to blender_mesh_objects")
    
    return blender_mesh_objects 
        
    
def save(context, objects):
    
    
    print("\n------------------------\n")
    print("MESH DRAWABLE DATA EXPORT START ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")
    import importlib
    importlib.reload(zyb_utils)     
    
    
    global proj_dir
    proj_dir = objects[0].z3dexport_settings.export_projectdir 
    
    filename = objects[0].z3dexport_settings.mesh_settings.drawable_export_file 
    
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT') 

    no_write = False

    blender_mesh_objects = read_blender_mesh_drawable_objects(context, objects)
    
    if (no_write):
        return {'FINISHED'}
    
    
    write_to_bin_z3d(proj_dir+"assets\\meshes\\", filename+".z3d", blender_mesh_objects)
    
    #write_to_bin_raw_z3d("C:\\Users\\zybon\\BlenderProjects\\zybonotopia\\game_extra\\datas\\", filename+"_raw.z3d", blender_mesh_objects)
     
    write_objectsnames_to_txt(filename, blender_mesh_objects)
    write_objectsnames_to_java(proj_dir)
    
    #write_to_txt_z3d(filename, blender_mesh_objects)
    
    global image_errors
    
    if (len(image_errors) > 0):
        proj_drawable_folder_path = proj_dir+"res\\drawable-nodpi"
        error_list = "This images are missing from '"+proj_drawable_folder_path+"'\n\n"
        for i, e in enumerate(image_errors):
            error_list += str(e) + "\n"
        os.system("msg user Missing file, look at the console...")
         
        print(error_list)
        
        answer = input("Copy now? [y/n] ")
        if answer == 'y':
            import shutil
            for i, error in enumerate(image_errors):
                result = shutil.copy2(bpy.path.abspath(error.image.filepath), proj_drawable_folder_path)             
                print(bpy.path.basename(error.image.filepath)+" copy to project")            
        os.system("msg user \"Export is complete\"")
    else:
        os.system("msg user \"Export is complete\"")
    print("EXPORT FINISHED ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")   
    print("------------------------\n") 
    return {'FINISHED'}
    
# def save_on_LINUX(context, objects):
    # print("\n------------------------\n")
    # print("MESH DRAWABLE DATA EXPORT START ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")
    # import importlib
    # importlib.reload(zyb_utils)     
    
    
    # global proj_dir
    # proj_dir = objects[0].z3dexport_settings.export_projectdir 
    
    # filename = objects[0].z3dexport_settings.mesh_settings.drawable_export_file 
    
    # if bpy.ops.object.mode_set.poll():
        # bpy.ops.object.mode_set(mode='OBJECT') 

    # no_write = False

    # blender_mesh_objects = read_blender_mesh_drawable_objects(context, objects)
    
    # if (no_write):
        # return {'FINISHED'}
    
    
    # # ~ write_to_bin_z3d(proj_dir+"assets\\meshes\\", filename+".z3d", blender_mesh_objects)
     
    # # ~ write_objectsnames_to_txt(filename, blender_mesh_objects)
    # # ~ write_objectsnames_to_java(proj_dir)
    
    # write_to_txt_z3d(filename, blender_mesh_objects)
    
    # global image_errors
    
    # if (len(image_errors) > 0):
        # proj_drawable_folder_path = proj_dir+"res\\drawable-nodpi"
        # error_list = "This images are missing from '"+proj_drawable_folder_path+"'\n\n"
        # for i, e in enumerate(image_errors):
            # error_list += str(e) + "\n"
        # os.system("msg zybon Missing file, look at the console...")    
         
        # print(error_list)
        
        # answer = input("Copy now? [y/n] ")
        # if answer == 'y':
            # import shutil
            # for i, error in enumerate(image_errors):
                # result = shutil.copy2(bpy.path.abspath(error.image.filepath), proj_drawable_folder_path)             
                # print(bpy.path.basename(error.image.filepath)+" copy to project")            
        # os.system("msg zybon \"Export is complete\"")    
        # # ~ error_list += "Copy now?"    
            
        # # ~ sh = "zenity --question --text=\""+error_list+"\" --title=\"Images\" --width=600"
        # # ~ answer = os.system(sh)
        # # ~ if (answer == 0):
            # # ~ import shutil
            # # ~ for i, error in enumerate(image_errors):
                # # ~ result = shutil.copy2(bpy.path.abspath(error.image.filepath), proj_drawable_folder_path)             
                # # ~ print(bpy.path.basename(error.image.filepath)+" copy to project")
    # else:
        # # ~ sh = "zenity --info --text=\"Export is complete\" --title=\"Finish\" --width=222"
        # os.system("msg zybon \"Export is complete\"") 
    # print("EXPORT FINISHED ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")   
    # print("------------------------\n") 
    # return {'FINISHED'}  
    
    


