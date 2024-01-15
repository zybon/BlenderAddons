import bpy
import math
import mathutils
import numpy
import random


class BorderXY():
    
    def __init__(self):
        self.min_x = 1000000.0
        self.max_x = -1000000.0
        
        self.min_y = 1000000.0
        self.max_y = -1000000.0
        
    def contains(self, x, y):
        return self.min_x<=x and x<self.max_x and self.min_y<=y and y<self.max_y    
    
    def __str__(self):
        return "["+str(self.min_x)+","+str(self.max_x)+","+str(self.min_y)+","+str(self.max_y)+"]"    
    
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
 


class ZybTriangle():
    
    def __init__(self):
        self.vertices = []
        self.normal = []
        self.point_on_triangle = []
        self.D = 0
        self.border_xy = BorderXY()
        self.vertices_colors = []
        
    def set_index(self, index):
        self.index = index        
        
    def append_vertex_coord(self, vertex_coord):
        self.vertices.append(mathutils.Vector(vertex_coord))  
        
    def append_vertex_color(self, vertex_color):
        self.vertices_colors.append(mathutils.Color(vertex_color))                 
        
    def init_border_xy(self):
        for vertex in self.vertices:
            if vertex.x < self.border_xy.min_x:
                self.border_xy.min_x = vertex.x
                
            if vertex.x > self.border_xy.max_x:
                self.border_xy.max_x = vertex.x
                
            if vertex.y < self.border_xy.min_y:
                self.border_xy.min_y = vertex.y
                
            if vertex.y > self.border_xy.max_y:
                self.border_xy.max_y = vertex.y 
        
    def calc_constants(self):
        self.calc_normal()
        
        for vertex in self.vertices:
            if not self.isNullVertexCoord(vertex):
                self.point_on_triangle = vertex
                break      
        self.planeConstant = self.point_on_triangle.x*self.normal.x + self.point_on_triangle.y*self.normal.y + self.point_on_triangle.z*self.normal.z 

    def isNullVertexCoord(self, vertex):
        return ((abs(vertex.x) < 0.000001) and (abs(vertex.y) < 0.000001) and (abs(vertex.z) < 0.000001))

    def calc_normal(self):
        v1 = Vector3D()
        v1.set(self.vertices[0], self.vertices[1])
        v1.normalize()

        v2 = Vector3D()
        v2.set(self.vertices[0], self.vertices[2])  
        v2.normalize()
        
        self.normal = v1.crossProduct(v2)  
        if (self.normal.length() == 0):
            error = ("%s" % (self.vertices[:]))
            raise Exception(error)   
        self.normal.normalize()
        
        up = mathutils.Vector((0,0,1))
        dest = mathutils.Vector((self.normal.x, self.normal.y, self.normal.z))
        self.rotationMtxFromUp = up.rotation_difference(dest).to_matrix().to_4x4()               
                            
    def cross_2d(self, x1, y1, x2, y2):
        return y1*x2 - x1*y2
           
    def is_vertical_overlapped(self, x, y):
        if not self.border_xy.contains(x,y):
            return False
        else:
            c = self.vertices
            k1 = self.cross_2d(x-c[0][0], y-c[0][1], c[1][0]-c[0][0], c[1][1]-c[0][1])
            if (k1<0.0):
                return False
            k2 = self.cross_2d(x-c[1][0], y-c[1][1], c[2][0]-c[1][0], c[2][1]-c[1][1])
            if (k2<0.0):
                return False
            k3 = self.cross_2d(x-c[2][0], y-c[2][1], c[0][0]-c[2][0], c[0][1]-c[2][1])
            if (k3<0.0):
                return False
            return True  
            
    def is_vertical_overlapped_with_barycentric(self, x, y):
        if not self.border_xy.contains(x,y):
            return False
        else:
            v = self.vertices
            D = ((v[1][1]-v[2][1])*(v[0][0]-v[2][0])+(v[2][0]-v[1][0])*(v[0][1]-v[2][1]))
            C_W0_X = (v[1][1]-v[2][1]) / D
            C_W0_Y = (v[2][0]-v[1][0]) / D
            Wv0 = (x-v[2][0])*C_W0_X + (y-v[2][1])*C_W0_Y
            if (Wv0<0.0):
                return False
            
            C_W1_X = (v[2][1]-v[0][1]) / D
            C_W1_Y = (v[0][0]-v[2][0]) / D
            Wv1 = (x-v[2][0])*C_W1_X + (y-v[2][1])*C_W1_Y            
            if (Wv1<0.0):
                return False
            Wv2 = 1.0 - Wv0 - Wv1
            if (Wv2<0.0):
                return False            
            return True     
            
    def get_color_from_vertex_colors(self, x, y):
        v = self.vertices
        D = ((v[1][1]-v[2][1])*(v[0][0]-v[2][0])+(v[2][0]-v[1][0])*(v[0][1]-v[2][1]))
        C_W0_X = (v[1][1]-v[2][1]) / D
        C_W0_Y = (v[2][0]-v[1][0]) / D
        Wv0 = (x-v[2][0])*C_W0_X + (y-v[2][1])*C_W0_Y

        
        C_W1_X = (v[2][1]-v[0][1]) / D
        C_W1_Y = (v[0][0]-v[2][0]) / D
        Wv1 = (x-v[2][0])*C_W1_X + (y-v[2][1])*C_W1_Y            

        Wv2 = 1.0 - Wv0 - Wv1

        color = mathutils.Color((0, 0, 0))
        color.r = self.vertices_colors[0].r*Wv0 + self.vertices_colors[1].r*Wv1 + self.vertices_colors[2].r*Wv2
        color.r = max(min(color.r, 1.0), 0.0)
        color.g = self.vertices_colors[0].g*Wv0 + self.vertices_colors[1].g*Wv1 + self.vertices_colors[2].g*Wv2
        color.g = max(min(color.g, 1.0), 0.0)
        color.b = self.vertices_colors[0].b*Wv0 + self.vertices_colors[1].b*Wv1 + self.vertices_colors[2].b*Wv2
        color.b = max(min(color.b, 1.0), 0.0)
        return color
        
    def distance_from_point(self, p):
        return self.planeConstant-(p.x*self.normal.x+p.y*self.normal.y+p.z*self.normal.z);
        
    def intersection(self, v1, v2):
        e = Vector3D();
        e.set(v1, v2)
        A = v1.x*self.normal.x+v1.y*self.normal.y+v1.z*self.normal.z; 
        B = e.x*self.normal.x+e.y*self.normal.y+e.z*self.normal.z; 
        if (B == 0.0):
            return None
        t = (self.planeConstant-A)/B;
        return Vector3D(v1.x+e.x*t,v1.y+e.y*t,v1.z+e.z*t);        
        
    # ~ def pont_belul(self, x, y, z):
        # ~ c = self.vertices
        # ~ szog = 0
        # ~ v1 = Vector3D(c[0].x-x, c[0].y-y, c[0].z-z)
        # ~ v2 = Vector3D(c[1].x-x, c[1].y-y, c[1].z-z)
        # ~ v3 = Vector3D(c[2].x-x, c[2].y-y, c[2].z-z)        
        # ~ szog1= v1.angle(v2)
        # ~ print("szog1 %f" % szog1)
        # ~ szog2= v1.angle(v3)
        # ~ print("szog2 %f" % szog2)
        # ~ szog3= v2.angle(v3)
        # ~ print("szog3 %f" % szog3)
        # ~ szog = szog1+szog2+szog3
        # ~ print("szog %f" % (szog/(2*math.pi)))
        # ~ print("(szog-(2*math.pi) %f" % (szog-(2*math.pi)))
        # ~ return (abs(szog-(2*math.pi)) < 0.001)
    
    def z_value_on_xy(self, x, y):
        z = (self.planeConstant-self.normal.x*x-self.normal.y*y)/self.normal.z
        return z        

    def print_info(self):
        for c in self.vertices:
            print("vertices: %s" % (c))
        # ~ print("normal: %s" % self.normal)   
        # ~ print("point_on_triangle: %s" % self.point_on_triangle)     
        # ~ print("planeConstant: %s" % self.planeConstant)           
        # ~ print("border_xy: %s" % self.border_xy) 
        
class SectorXY_Info():
    
    x_min = -750.0
    x_max = 750.0
        
    y_min = -750.0
    y_max = 750.0
        
    dx = 50.0   
    dy = 50.0          


class BaseObjectToVerticalAlign():
    
    def __init__(self, instancegroup_creator_settings):
        self.instancegroup_creator_settings = instancegroup_creator_settings
        self.object = bpy.data.objects[instancegroup_creator_settings.object_to_aligned]
        self.name = self.object.name
        
        border = bpy.data.objects[self.instancegroup_creator_settings.border_object]
        self.border_x_min = border.location.x-border.dimensions.x*0.5
        self.border_y_min = border.location.y-border.dimensions.y*0.5
        self.border_z_min = border.location.z-border.dimensions.z*0.5
    
        self.border_x_max = border.location.x+border.dimensions.x*0.5
        self.border_y_max = border.location.y+border.dimensions.y*0.5
        self.border_z_max = border.location.z+border.dimensions.z*0.5    
        
        self.min_normal_z = instancegroup_creator_settings.min_normal_z
        self.max_normal_z = instancegroup_creator_settings.max_normal_z    
        
        self.init_sectors(self.object)
        
    def is_out_of_border(self, polygon):
               
        in_border =  (self.border_x_min < polygon.center.x) and (polygon.center.x < self.border_x_max) and \
                (self.border_y_min < polygon.center.y) and (polygon.center.y < self.border_y_max) and \
                (self.border_z_min < polygon.center.z) and (polygon.center.z < self.border_z_max)
                
        return not in_border
        
    def is_normal_not_ok(self, polygon): 
        return (polygon.normal.z < self.min_normal_z) or (polygon.normal.z > self.max_normal_z)        
        
        
    def init_sectors(self, obj):
        self.init_triangulated_mesh(obj)
        self.sectors = {}
        
        #read
        for blender_polygon in self.triangulated_mesh.polygons:
            if (self.is_out_of_border(blender_polygon)):
                continue
                
            if (self.is_normal_not_ok(blender_polygon)):
                continue                
            
            triangle = ZybTriangle()
            triangle.set_index(blender_polygon.index)
            
            for loop_index in blender_polygon.loop_indices:
                blender_vertex_index = self.triangulated_mesh.loops[loop_index].vertex_index
                triangle.append_vertex_coord(self.triangulated_mesh.vertices[blender_vertex_index].co)    
                triangle.append_vertex_color(self.triangulated_mesh.vertex_colors['Col'].data[loop_index].color)        
            
            triangle.init_border_xy()
            triangle.calc_constants()
            # ~ print(triangle.border_xy)
            
            columnMin = int((triangle.border_xy.min_x-SectorXY_Info.x_min)/SectorXY_Info.dx)
            columnMax = int((triangle.border_xy.max_x-SectorXY_Info.x_min)/SectorXY_Info.dx)
            rowMin = int((triangle.border_xy.min_y-SectorXY_Info.y_min)/SectorXY_Info.dy)
            rowMax = int((triangle.border_xy.max_y-SectorXY_Info.y_min)/SectorXY_Info.dy)
            for row in range(rowMin, rowMax+1):
                for column in range(columnMin, columnMax+1):
                    # ~ print(row, column)
                    index = (row, column)
                    dict_val = self.sectors.get(index)
                    if (dict_val is None):
                        self.sectors[index] = []
                    self.sectors[index].append(triangle)
                           
        # clean up
        bpy.data.meshes.remove(self.triangulated_mesh)    
        
        
    def init_triangulated_mesh(self, object):
        
        # temp mesh létrehozása úgy hogy modifiers-eket érvényesitik
        self.triangulated_mesh = object.to_mesh( bpy.context.scene, True, 'PREVIEW', calc_tessface=False)
        
        #háromszögelés, hogy minden face egy háromszög legyen
        # az elején meg kell csinálni mert ez újra képezi a loops tomboket
        import bmesh
        bm = bmesh.new()
        bm.from_mesh(self.triangulated_mesh)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        bm.to_mesh(self.triangulated_mesh)
        bm.free()     
         
    # ~ def get_vertical_overlapped_triangles(self, x, y):          
        # ~ vertical_overlapped_triangles = []
        
        # ~ column = int((x-SectorXY_Info.x_min)/SectorXY_Info.dx)
        # ~ row = int((y-SectorXY_Info.y_min)/SectorXY_Info.dy)
        # ~ index = (row, column)
        # ~ triangles_in_sector = self.sectors.get(index)
        # ~ if (triangles_in_sector is not None): 
            # ~ for zyb_triangle in triangles_in_sector:
                # ~ if (zyb_triangle.is_vertical_overlapped_with_barycentric(x,y)): 
                    # ~ vertical_overlapped_triangles.append(zyb_triangle)  
                    
        # ~ return vertical_overlapped_triangles
        
    def get_vertical_overlapped_triangles(self, location): 
        
        x = location[0]
        y = location[1]                 
        vertical_overlapped_triangles = []
        
        column = int((x-SectorXY_Info.x_min)/SectorXY_Info.dx)
        row = int((y-SectorXY_Info.y_min)/SectorXY_Info.dy)
        index = (row, column)
        triangles_in_sector = self.sectors.get(index)
        if (triangles_in_sector is not None): 
            for zyb_triangle in triangles_in_sector:
                if (zyb_triangle.is_vertical_overlapped_with_barycentric(x,y)): 
                    vertical_overlapped_triangles.append(zyb_triangle)  
                    
        return vertical_overlapped_triangles        
    
    def align_object(self, selected_object, modelmtx_align_to_object):
        x = selected_object.location[0]
        y = selected_object.location[1]
        
        # ~ print("x,y ",x,y)
                   
        align_error = 0           
        vertical_overlapped_triangles = self.get_vertical_overlapped_triangles(x,y)
        
        # ~ pols = self.object_to_vertical_align.polygons
        # ~ loops = self.object_to_vertical_align.loops           
        
        # ~ for p in pols:
            # ~ if (p.area > 0):
                # ~ zyb_triangle = ZybTriangle()
                # ~ zyb_triangle.vertices[0] = self.object_to_vertical_align.vertices[p.vertices[0]].co
                # ~ zyb_triangle.vertices[1] = self.object_to_vertical_align.vertices[p.vertices[1]].co
                # ~ zyb_triangle.vertices[2] = self.object_to_vertical_align.vertices[p.vertices[2]].co
                # ~ zyb_triangle.init_border_xy()
                # ~ if (zyb_triangle.is_vertical_overlapped(x,y)):
                    # ~ zyb_triangle.calc_constants()
                    # ~ vertical_overlapped_triangles.append(zyb_triangle)
            # ~ else:
                # ~ error_msg = ("This triangle area is zero: \n\t%s\n\t%s\n\t%s" % (self.object_to_vertical_align.vertices[p.vertices[0]].co,
                                                                        # ~ self.object_to_vertical_align.vertices[p.vertices[1]].co,
                                                                        # ~ self.object_to_vertical_align.vertices[p.vertices[2]].co))
                # ~ raise Exception(error_msg)            
        
        
        if (len(vertical_overlapped_triangles) == 0):
            
            print("No vertical overlap between ["+selected_object.name+"] and ["+self.name+"]") 
            align_error = align_error + 1

        else:            
            min_z = -10000 
            base_triangle = None
            for zyb_triangle in vertical_overlapped_triangles:
            #    h.print_info() 
                z = zyb_triangle.z_value_on_xy(x,y) 
                if (z>min_z):
                    min_z = z 
                    base_triangle = zyb_triangle   
              
            #selected_object.location = [0,0,0]
            if (modelmtx_align_to_object):
                selected_object.matrix_local = base_triangle.rotationMtxFromUp * selected_object.matrix_local
            selected_object.location = [x, y, min_z] 
        return align_error
             
            
    def align_object_Er(self, selected_object):
        x = selected_object.location[0]
        y = selected_object.location[1]
                   
        align_error = 0           
        vertical_overlapped_triangles = []
        for zyb_triangle in self.zyb_triangles:
            if zyb_triangle.is_vertical_overlapped(x,y):
                vertical_overlapped_triangles.append(zyb_triangle)
        #print("%s db talalt haromszog" % len(vertical_overlapped_triangles))       
        if (len(vertical_overlapped_triangles) == 0):
            
            print("No vertical overlap between ["+selected_object.name+"] and ["+self.name+"]") 
            align_error = align_error + 1

        else:            
            min_z = -10000 
            base_triangle = None
            for zyb_triangle in vertical_overlapped_triangles:
            #    h.print_info() 
                z = zyb_triangle.z_value_on_xy(x,y) 
                if (z>min_z):
                    min_z = z 
                    base_triangle = zyb_triangle   
              
            #selected_object.location = [0,0,0]
            selected_object.matrix_local = base_triangle.rotationMtxFromUp # * selected_object.matrix_local
            selected_object.location = [x, y, min_z] 
        return align_error
                 
            
    def print_info(self):
        for h in self.zyb_triangles:
            h.print_info()         


def vertical_align():    
    object_to_vertical_align = BaseObjectToVerticalAlign(bpy.context.active_object)
    align_error = 0
    for o in bpy.context.selected_objects: 
        if (o != bpy.context.active_object):
            align_error = align_error + object_to_vertical_align.align_object(o, True)
            
    import os

    infoText = ""
    if (align_error == 0):
        infoText = "Done!"
        # ~ sh = "zenity --info --text=\""+infoText+"\" --title=\"Vertical align\" --width=200"
    else:
        infoText = str(align_error)+" error with some objects, look at the console!"           
        # ~ sh = "zenity --warning --text=\""+infoText+"\" --title=\"Vertical align\" --width=400"
         
    os.system("msg zybon "+infoText) 
    
    # ~ print(infoText)
    return {'FINISHED'}
    
def rotate_objects():
    
    zyb_tools_prop = bpy.context.scene.zyb_tools_properties
    
    import random
    for o in bpy.context.selected_objects: 
        o.rotation_mode = 'XYZ'
        R = o.rotation_euler
        if (zyb_tools_prop.rotation_aroundX):
            if (zyb_tools_prop.rotation_rnd_aroundX):
                R[0] = random.uniform(-math.pi, math.pi)
            else:
                R[0] = zyb_tools_prop.rotation_angle_aroundX 
            
        if (zyb_tools_prop.rotation_aroundY):    
            if (zyb_tools_prop.rotation_rnd_aroundY):
                R[1] = random.uniform(-math.pi, math.pi)
            else:
                R[1] = zyb_tools_prop.rotation_angle_aroundY
        
        if (zyb_tools_prop.rotation_aroundZ):     
            if (zyb_tools_prop.rotation_rnd_aroundZ):
                R[2] = random.uniform(-math.pi, math.pi)
            else:
                R[2] = zyb_tools_prop.rotation_angle_aroundZ            
        
    return {'FINISHED'}
    
def resize_objects():
    
    zyb_tools_prop = bpy.context.scene.zyb_tools_properties
    
    import random
    for o in bpy.context.selected_objects: 
        value = 0.0
        if (zyb_tools_prop.resize_type != "FIX"):
            value = random.uniform(zyb_tools_prop.resize_value, zyb_tools_prop.resize_value_2)
        else:
            value = zyb_tools_prop.resize_value 
        o.scale[0] = value
        o.scale[1] = value
        o.scale[2] = value
                
        
    return {'FINISHED'}    
    
def switch_texture(visibility=False):
    
    for o in bpy.context.selected_objects:
        for m in o.data.materials:
            m.texture_slots[0].use = visibility
    
    return {'FINISHED'}  

    
    
def create_random_instance_group(context):
    print("create_random_instance_group")
    
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings
    
    instancegroup_parent = bpy.data.objects[instancegroup_creator_settings.instancegroup_name]
    
    print(instancegroup_parent.name)
    
    base_object = bpy.data.objects[instancegroup_creator_settings.base_object]
    
    print(base_object.name)
    
    border = bpy.data.objects[instancegroup_creator_settings.border_object]
    
    print(border.dimensions)
    
    offset = instancegroup_creator_settings.min_distance
    
    x_min = border.location.x-border.dimensions.x*0.5+offset*0.5
    x_max = border.location.x+border.dimensions.x*0.5
    
    y_min = border.location.y-border.dimensions.y*0.5+offset*0.5
    y_max = border.location.y+border.dimensions.y*0.5
    
    # import random
    
    # i = 0
    # x = x_min
    # j = 0
    # while (x<x_max):
        # y = y_min
        # while (y<y_max):        
            # instance = bpy.data.objects.new(instancegroup_parent.name+"_"+str(i).rjust(10, "0"), base_object.data)
            # # ~ instance.hide = True
            # instance.location = [x+(random.random()-0.5)*offset, y+(random.random()-0.5)*offset, 0] 
            # bpy.context.scene.objects.link(instance)
            # instance.parent = instancegroup_parent 
            # instance.select = True
            # bpy.context.scene.objects.active = instance
            # # ~ j = j + 1
            # # ~ if (j == 50):
                # # ~ bpy.ops.object.join()
                # # ~ j = 0
                # # ~ return
            # i = i+1
            # y = y + offset    
        # x = x + offset
    # # ~ if (j>0):
        # # ~ bpy.ops.object.join()   
    # # ~ bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

def get_rnd_picked_object(base_objects):
    object_count = len(base_objects)
    if (object_count == 1):
        return base_objects[0]
    else:
        picked_index = random.randint(0, object_count-1)
        return base_objects[picked_index]
        
    
def create_texture_masked_instance_group(context):
    print("create_textured_instance_group")
    
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings
    
    instancegroup_parent = bpy.data.objects[instancegroup_creator_settings.instancegroup_name]
    instancegroup_parent.select = False
    
    
    base_objects = []
    
    if (instancegroup_creator_settings.base_type == 'OBJECT'):
        base_objects.append(bpy.data.objects[instancegroup_creator_settings.base_object])
        
    if (instancegroup_creator_settings.base_type == 'GROUP'):  
        base_group = bpy.data.groups[instancegroup_creator_settings.base_group].objects  
        for o in base_group:
            base_objects.append(o)
    
    align = False
    modelmtx_align_to_object = False
    if (instancegroup_creator_settings.vertical_align_to_object):   
        object_to_vertical_align = BaseObjectToVerticalAlign(instancegroup_creator_settings)
        align = True
        modelmtx_align_to_object = instancegroup_creator_settings.modelmtx_align_to_object
        
    image = instancegroup_creator_settings.image_for_mask
    w = image.size[0]
    h = image.size[1]
    
    # ~ print(w, h)
    
    color_on_mask = instancegroup_creator_settings.color_on_mask
    
    border = bpy.data.objects[instancegroup_creator_settings.border_object]
    border_x_min = border.location.x-border.dimensions.x*0.5
    border_y_min = border.location.y-border.dimensions.y*0.5
    border_z_min = border.location.z-border.dimensions.z*0.5
    
    border_x_size = border.dimensions.x
    border_y_size = border.dimensions.y
    border_z_size = border.dimensions.z
    
    offset = instancegroup_creator_settings.min_distance
    
    x_min = border.location.x-border.dimensions.x*0.5+offset*0.5
    x_max = border.location.x+border.dimensions.x*0.5
    
    y_min = border.location.y-border.dimensions.y*0.5+offset*0.5
    y_max = border.location.y+border.dimensions.y*0.5
    
    
    
    instance_location = [0, 0, 0]
    pixel = [0, 0, 0, 0]
    
    pixels = image.pixels[:]
    
    # ~ print("0 %s" % ("%"))
    
    x_offset = (int((x_max-x_min)/offset))
    y_offset = (int((y_max-y_min)/offset))
    
    i = 0
    x = x_min
    j = 0
    while (x<x_max):
        y = y_min
        while (y<y_max): 
            # ~ print(x, y)
            instance_location[0] = x +(random.random()*2.0-1.0)*offset*0.25
            instance_location[1] = y +(random.random()*2.0-1.0)*offset*0.25 
            # ~ print("instance_location %s" % instance_location)
            x_value = (instance_location[0]+2000.0)/(4000.0)
            y_value = (instance_location[1]+2000.0)/(4000.0)
            # ~ print("x_value = %s, y_value = %s" % (x_value, y_value))
            if (x_value<0.0 or x_value>=1.0):
                y = y + offset
                # ~ print("continue x")
                continue
            if (y_value<0.0 or y_value>=1.0):
                y = y + offset
                # ~ print("continue y")
                continue                
            
            pixel_x = int(w*x_value)
            pixel_y = int(h*y_value)
                  
            pixel_pos_in_image = (pixel_y*w+pixel_x)*4  
                  
            pixel[0] = pixels[pixel_pos_in_image]      
            pixel[1] = pixels[pixel_pos_in_image+1]      
            pixel[2] = pixels[pixel_pos_in_image+2]      
            pixel[3] = pixels[pixel_pos_in_image+3]      
            # ~ print(pixel)
            if (abs(pixel[0]-color_on_mask[0]) < 0.1 and
                abs(pixel[1]-color_on_mask[1]) < 0.1 and
                abs(pixel[2]-color_on_mask[2]) < 0.1
                ):
                # ~ print("ok")  
                if (align):
                    # ~ print("add_aligned_object")
                    vertical_overlapped_triangles = object_to_vertical_align.get_vertical_overlapped_triangles(instance_location)
                    if (len(vertical_overlapped_triangles) > 0):
                        for zyb_triangle in vertical_overlapped_triangles:
                            base_object = get_rnd_picked_object(base_objects)
                            instance = bpy.data.objects.new(base_object.name+"_"+str(i).rjust(4, "0"), base_object.data.copy())
                            # ~ instance.hide = True
                            i = i+1
                            # ~ instance = base_object.copy()
                            instance.data = base_object.data
                            # ~ instance.name = instancegroup_parent.name+"_"+str(i).rjust(10, "0")
                            instance.location = instance_location
                            instance.z3dexport_settings.datatype = 'PARTICLE'
                            bpy.context.scene.objects.link(instance)
                            
                            if (instancegroup_creator_settings.base_type == 'OBJECT'):
                                instance.parent = instancegroup_parent 
                            if (instancegroup_creator_settings.base_type == 'GROUP'):
                                instance.parent = bpy.data.objects[base_object.name+"_parent"]
                            
                            instance.select = True
                            instance.hide = False
                            instance.hide_render = True
                            bpy.context.scene.objects.active = instance
                            
                            location_x = instance_location[0]
                            location_y = instance_location[1]                            
                            location_z = zyb_triangle.z_value_on_xy(location_x,location_y) 
                            if (modelmtx_align_to_object):
                                instance.matrix_local = zyb_triangle.rotationMtxFromUp * instance.matrix_local
                            instance.location = [location_x, location_y, location_z] 
                    # ~ object_to_vertical_align.align_object(instance, modelmtx_align_to_object)
                else:
                    instance = bpy.data.objects.new(instancegroup_parent.name+"_"+str(i).rjust(10, "0"), base_object.data.copy())
                    # ~ instance.hide = True
                    i = i+1
                    # ~ instance = base_object.copy()
                    # ~ instance.data = base_object.data
                    instance.name = instancegroup_parent.name+"_"+str(i).rjust(10, "0")
                    instance.location = instance_location
                    bpy.context.scene.objects.link(instance)
                    instance.parent = instancegroup_parent 
                    instance.select = True
                    instance.hide = False
                    bpy.context.scene.objects.active = instance
                    
                j = j + 1
                # ~ if (j == 100):
                    # ~ bpy.ops.object.join()
                    # ~ bpy.ops.object.select_all(action='DESELECT')
                    # ~ j = 0
                    # ~ print("blablabla")
                    # ~ return "BLABLA"
                
                # ~ print(i)
            y = y + offset   
            # ~ print("x: %s, y: %s" % (x, y))
        percent = (x-x_min)/(x_max-x_min) 

        print("%s %s" % (int(percent*100), "%"))
        x = x + offset
        
    # ~ if (j>0):
        # ~ bpy.ops.object.join()   
    # ~ bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    print("DONE\n")
    
def create_texture_masked_instance_group_to_directfile(context):
    print("create_texture_masked_instance_group_to_directfile")
    
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings
    
    instancegroup_parent = bpy.data.objects[instancegroup_creator_settings.instancegroup_name]
    instancegroup_parent.select = False
    
    
    base_objects = []
    
    if (instancegroup_creator_settings.base_type == 'OBJECT'):
        base_objects.append(bpy.data.objects[instancegroup_creator_settings.base_object])
        
    if (instancegroup_creator_settings.base_type == 'GROUP'):  
        base_group = bpy.data.groups[instancegroup_creator_settings.base_group].objects  
        for o in base_group:
            base_objects.append(o)
    
    align = False
    modelmtx_align_to_object = False
    if (instancegroup_creator_settings.vertical_align_to_object):   
        object_to_vertical_align = BaseObjectToVerticalAlign(instancegroup_creator_settings)
        align = True
        modelmtx_align_to_object = instancegroup_creator_settings.modelmtx_align_to_object
        
    image = instancegroup_creator_settings.image_for_mask
    w = image.size[0]
    h = image.size[1]
    
    # ~ print(w, h)
    
    color_on_mask = instancegroup_creator_settings.color_on_mask
    
    border = bpy.data.objects[instancegroup_creator_settings.border_object]
    border_x_min = border.location.x-border.dimensions.x*0.5
    border_y_min = border.location.y-border.dimensions.y*0.5
    border_z_min = border.location.z-border.dimensions.z*0.5
    
    border_x_size = border.dimensions.x
    border_y_size = border.dimensions.y
    border_z_size = border.dimensions.z
    
    offset = instancegroup_creator_settings.min_distance
    
    x_min = border.location.x-border.dimensions.x*0.5+offset*0.5
    x_max = border.location.x+border.dimensions.x*0.5
    
    y_min = border.location.y-border.dimensions.y*0.5+offset*0.5
    y_max = border.location.y+border.dimensions.y*0.5
    
    
    
    instance_location = [0, 0, 0]
    pixel = [0, 0, 0, 0]
    
    pixels = image.pixels[:]
    
    # ~ print("0 %s" % ("%"))
    
    x_offset = (int((x_max-x_min)/offset))
    y_offset = (int((y_max-y_min)/offset))
    
    i = 0
    x = x_min
    j = 0
    
    instance_for_matrix = bpy.data.objects.new("instance_base_for_matrix", base_objects[0].data.copy())
    
    instance = bpy.data.objects.new("instance_base", base_objects[0].data.copy())
    bpy.context.scene.objects.link(instance)
    
    instance.z3dexport_settings.datatype = 'PARTICLE'


    if (instancegroup_creator_settings.base_type == 'OBJECT'):
        instance.parent = instancegroup_parent 
    if (instancegroup_creator_settings.base_type == 'GROUP'):
        instance.parent = bpy.data.objects[base_object.name+"_parent"]
        
    instance.select = True
    instance.hide = True
    bpy.context.scene.objects.active = instance    
    
    import instances_export
    
    import importlib
    importlib.reload(instances_export)      
    
    
    instance_group = instances_export.InstanceGroup(instancegroup_parent)
    
    while (x<x_max):
        y = y_min
        while (y<y_max): 
            # ~ print(x, y)
            instance_location[0] = x +(random.random()*2.0-1.0)*offset*0.25
            instance_location[1] = y +(random.random()*2.0-1.0)*offset*0.25 
            # ~ print("instance_location %s" % instance_location)
            x_value = (instance_location[0]+2000.0)/(4000.0)
            y_value = (instance_location[1]+2000.0)/(4000.0)
            # ~ print("x_value = %s, y_value = %s" % (x_value, y_value))
            if (x_value<0.0 or x_value>=1.0):
                y = y + offset
                # ~ print("continue x")
                continue
            if (y_value<0.0 or y_value>=1.0):
                y = y + offset
                # ~ print("continue y")
                continue                
            
            pixel_x = int(w*x_value)
            pixel_y = int(h*y_value)
                  
            pixel_pos_in_image = (pixel_y*w+pixel_x)*4  
                  
            pixel[0] = pixels[pixel_pos_in_image]      
            pixel[1] = pixels[pixel_pos_in_image+1]      
            pixel[2] = pixels[pixel_pos_in_image+2]      
            pixel[3] = pixels[pixel_pos_in_image+3]      
            # ~ print(pixel)
            if (abs(pixel[0]-color_on_mask[0]) < 0.1 and
                abs(pixel[1]-color_on_mask[1]) < 0.1 and
                abs(pixel[2]-color_on_mask[2]) < 0.1
                ):
                # ~ print("ok")  
                if (align):
                    # ~ print("add_aligned_object")
                    vertical_overlapped_triangles = object_to_vertical_align.get_vertical_overlapped_triangles(instance_location)
                    if (len(vertical_overlapped_triangles) > 0):
                        for zyb_triangle in vertical_overlapped_triangles:
                            base_object = get_rnd_picked_object(base_objects)
                            # ~ instance = bpy.data.objects.new(base_object.name+"_"+str(i).rjust(4, "0"), base_object.data.copy())
                            # ~ instance.hide = True
                            i = i+1
                            # ~ instance = base_object.copy()
                            instance.data = base_object.data
                            # ~ instance.name = instancegroup_parent.name+"_"+str(i).rjust(10, "0")
                            instance.location = instance_location


                            
                            location_x = instance_location[0]
                            location_y = instance_location[1]                            
                            location_z = zyb_triangle.z_value_on_xy(location_x,location_y) 
                            if (modelmtx_align_to_object):
                                instance.matrix_local = zyb_triangle.rotationMtxFromUp * instance_for_matrix.matrix_local
                            instance.location = [location_x, location_y, location_z] 
                            
                            myInstance = instances_export.Instance(context, instance)  
                            
                            myInstance.set_rnd_scale(2.0, 3.0)
                            # ~ myInstance.set_rnd_rotation()
                            myInstance.read_modelmatrix()
                            
                            instance_group.add_instance(myInstance)                            
                            
                    # ~ object_to_vertical_align.align_object(instance, modelmtx_align_to_object)
                else:
                    instance = bpy.data.objects.new(instancegroup_parent.name+"_"+str(i).rjust(10, "0"), base_object.data.copy())
                    # ~ instance.hide = True
                    i = i+1
                    # ~ instance = base_object.copy()
                    # ~ instance.data = base_object.data
                    instance.name = instancegroup_parent.name+"_"+str(i).rjust(10, "0")
                    instance.location = instance_location
                    bpy.context.scene.objects.link(instance)
                    instance.parent = instancegroup_parent 
                    instance.select = True
                    instance.hide = False
                    bpy.context.scene.objects.active = instance
                    
                j = j + 1
                # ~ if (j == 100):
                    # ~ bpy.ops.object.join()
                    # ~ bpy.ops.object.select_all(action='DESELECT')
                    # ~ j = 0
                    # ~ print("blablabla")
                    # ~ return "BLABLA"
                
                # ~ print(i)
            y = y + offset   
            # ~ print("x: %s, y: %s" % (x, y))
        percent = (x-x_min)/(x_max-x_min) 

        print("%s %s" % (int(percent*100), "%"))
        x = x + offset
        
    # ~ if (j>0):
        # ~ bpy.ops.object.join()   
    # ~ bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    
    instances_groups = {}
    instances_groups[instancegroup_parent.name] = instance_group
    
    proj_dir = instancegroup_parent.z3dexport_settings.export_projectdir 
    
    filename = instancegroup_parent.z3dexport_settings.instance_settings.instancegroup_export_file     
    
    instances_export.write_instances_to_bin_z3d(proj_dir+"assets\\instances\\", filename+".z3d", instances_groups)

    instances_export.write_instancesgroupsnames_to_txt(filename, instances_groups)
    instances_export.write_instancesgroupsnames_to_java(proj_dir)
    
    instances_export.write_instances_to_txt("direct_instance_test", instances_groups)
    
    print("DONE\n")    
    
def create_vertex_colored_instance_group(context):
    print("create_vertex_colored_instance_group")
    
    for o in context.object.children:
        bpy.data.objects.remove(o)
    
    context.object.select = False    
    
    base_object = bpy.data.objects[context.object.z3dexport_settings.instance_settings.base_object]
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings
    
    align = False
    mod_mtx_align = False
    if (instancegroup_creator_settings.vertical_align_to_object):   
        object_to_vertical_align = BaseObjectToVerticalAlign(bpy.data.objects[instancegroup_creator_settings.object_to_aligned])
        align = True
        mod_mtx_align = instancegroup_creator_settings.modelmtx_align_to_object
        
    border = bpy.data.objects[instancegroup_creator_settings.border_object]
    border_x_min = border.location.x-border.dimensions.x*0.5
    border_y_min = border.location.x-border.dimensions.x*0.5
    
    border_x_size = border.dimensions.x
    border_y_size = border.dimensions.x
    
    offset = instancegroup_creator_settings.min_distance
    
    x_min = border.location.x-border.dimensions.x*0.5+offset*0.5
    x_max = border.location.x+border.dimensions.x*0.5
    
    y_min = border.location.y-border.dimensions.y*0.5+offset*0.5
    y_max = border.location.y+border.dimensions.y*0.5
    
    import random
    
    instance_location = [0, 0, 0]
    pixel = [0, 0, 0, 0]

    
    x_offset = (int((x_max-x_min)/offset))
    y_offset = (int((y_max-y_min)/offset))
    
    i = 0
    x = x_min
    j = 0
    while (x<x_max):
        y = y_min
        while (y<y_max): 
            instance_location[0] = x +(random.random()-0.5)*offset
            instance_location[1] = y +(random.random()-0.5)*offset 
            
            vertical_overlapped_triangles = object_to_vertical_align.get_vertical_overlapped_triangles(instance_location[0], instance_location[1])
            
            for triangle in vertical_overlapped_triangles:
                if (triangle.normal.z<0.9):
                    continue
                color = triangle.get_color_from_vertex_colors(instance_location[0], instance_location[1])
                if color.g>0.7:
                    i = i+1
                    # ~ instance = base_object.copy()
                    # ~ instance.data = base_object.data.copy()
                    # ~ instance.name = context.object.name+"_"+str(i).rjust(10, "0")
                    instance = bpy.data.objects.new(context.object.name+"_"+str(i).rjust(10, "0"), base_object.data)
                    
                    # ~ instance.location = instance_location
                    bpy.context.scene.objects.link(instance)
                    instance.parent = context.object 
                    instance.select = True
                    instance.hide = False
                    bpy.context.scene.objects.active = instance 

                    fw = mathutils.Vector((1,0,0))
                    dest_v3D = Vector3D(random.random()*2.0-1.0, random.random()*2.0-1.0, 0.0)
                    dest_v3D.normalize()
                    dest = mathutils.Vector((dest_v3D.x, dest_v3D.y, dest_v3D.z))
                    randomRotationMtxAroundZ = fw.rotation_difference(dest).to_matrix().to_4x4() 
                    instance.matrix_local = triangle.rotationMtxFromUp * randomRotationMtxAroundZ *  instance.matrix_local

                    z = triangle.z_value_on_xy(instance_location[0],instance_location[1]) 
                    instance.location = [instance_location[0],instance_location[1], z] 
            y = y + offset   
            # ~ print("x: %s, y: %s" % (x, y))
        percent = (x-x_min)/(x_max-x_min) 

        print("%s %s" % (int(percent*100), "%"))
        x = x + offset
        
    # ~ if (j>0):
        # ~ bpy.ops.object.join()   
    # ~ bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)    
    print("DONE\n")
    
      
    
def copy_instance_group(context, instance_settings):
    print("copy_instance_group")   
    
def prepare_instance_group(context):
    bpy.ops.object.select_all(action='DESELECT')

    
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings
    
    instancegroup_name = instancegroup_creator_settings.instancegroup_name
    
    if (bpy.data.objects.get(instancegroup_name) is None):
        instancegroup_parent = bpy.data.objects.new(instancegroup_name, None)
        bpy.context.scene.objects.link(instancegroup_parent)   
    else:
        instancegroup_parent = bpy.data.objects[instancegroup_name] 
        for o in instancegroup_parent.children:
            for ch in o.children:
                bpy.data.objects.remove(ch)
            bpy.data.objects.remove(o)
            
    if (instancegroup_creator_settings.base_type == 'OBJECT'):   
        instancegroup_parent.z3dexport_settings.export = True
        instancegroup_parent.z3dexport_settings.datatype = "INSTANCE_GROUP"
        instancegroup_parent.z3dexport_settings.instance_settings.base_object = instancegroup_creator_settings.base_object
        instancegroup_parent.z3dexport_settings.instance_settings.groupvisible = True
        
        return
        
    if (instancegroup_creator_settings.base_type == 'GROUP'):  
        instancegroup_parent.z3dexport_settings.export = False
        base_group = bpy.data.groups[instancegroup_creator_settings.base_group].objects  
        for o in base_group:
            instancegroup_subparent = bpy.data.objects.new(o.name+"_parent", None)
            bpy.context.scene.objects.link(instancegroup_subparent) 
            instancegroup_subparent.parent = instancegroup_parent
            instancegroup_subparent.z3dexport_settings.export = True
            instancegroup_subparent.z3dexport_settings.export_projectdir = instancegroup_parent.z3dexport_settings.export_projectdir
            instancegroup_subparent.z3dexport_settings.instance_settings.instancegroup_export_file = instancegroup_parent.z3dexport_settings.instance_settings.instancegroup_export_file
            instancegroup_subparent.z3dexport_settings.datatype = "INSTANCE_GROUP"
            instancegroup_subparent.z3dexport_settings.instance_settings.base_object = o.name
            instancegroup_subparent.z3dexport_settings.instance_settings.groupvisible = True        
    
    
def create_instance_group(context):
    
    prepare_instance_group(context)
    
    instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings    
        
    if (instancegroup_creator_settings.placement == 'RANDOM'):
        create_random_instance_group(context)
        
    elif (instancegroup_creator_settings.placement == 'TEXTURE_MASK'):
        create_texture_masked_instance_group(context)
        # ~ create_texture_masked_instance_group_to_directfile(context)
        
    # ~ elif (instancegroup_creator_settings.placement == 'VERTEX_COLOR'):
        # ~ create_vertex_colored_instance_group(context)        
        
    # ~ elif (instancegroup_creator_settings.placement == 'COPY_INSTANCE_GROUP'):
        # ~ copy_instance_group(context)     
        
    instancegroup_parent = bpy.data.objects[instancegroup_creator_settings.instancegroup_name]
    instancegroup_parent.select = True   
    bpy.context.scene.objects.active = instancegroup_parent    
        
    return {'FINISHED'}      
    
   
def create_impostors(context): 
    image_folder = "C:\\Users\\User\\BlenderProjects\\temp\\impostor_test\\"
    bpy.data.scenes["Scene"].render.filepath = image_folder
    bpy.ops.render.render(animation=True)    
    
    
    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end   
    frame_step = bpy.context.scene.frame_step   
    
    sprite_w = bpy.context.scene.render.resolution_x    
    sprite_h = bpy.context.scene.render.resolution_y
    
    W = sprite_w*frame_end
    H = sprite_h     
    
    impostors = bpy.data.images.new("Sprite", alpha=True, width=W, height=H)
    impostors.use_alpha = True
    impostors.alpha_mode = 'STRAIGHT'
    impostors.filepath_raw = image_folder+"in_one.png"
    impostors.file_format = 'PNG'  
    
    num_pixels = len(impostors.pixels)

    pix_array = [(0.5) for cp in range(num_pixels)] 
    
      
    P = 0
    while P<frame_end:
        
        imp_path = image_folder+str(P+1).rjust(4, "0")+".png"
        imp_img = bpy.data.images.new("sp", sprite_w, sprite_h)
        imp_img.source = "FILE"        
        # ~ imp_img.use_alpha = True
        # ~ imp_img.alpha_mode = 'STRAIGHT'
        imp_img.filepath_raw = imp_path
        # ~ imp_img.file_format = 'PNG'      
        # ~ imp_img.update()
        imp_img_pixels = imp_img.pixels[:]    
            
        y = 0
        while (y<sprite_h):
            x = 0
            while (x<sprite_w):
                pix_array[y*W*4 + (x+sprite_w*P)*4] = imp_img_pixels[y*sprite_w*4 + x*4]
                pix_array[y*W*4 + (x+sprite_w*P)*4+1] = imp_img_pixels[y*sprite_w*4 + x*4+1]
                pix_array[y*W*4 + (x+sprite_w*P)*4+2] = imp_img_pixels[y*sprite_w*4 + x*4+2]
                pix_array[y*W*4 + (x+sprite_w*P)*4+3] = imp_img_pixels[y*sprite_w*4 + x*4+3]   
                x = x + 1
                # ~ print(x)
            y = y+1
            print(y)
            
        bpy.data.images.remove(imp_img)
            
        P = P+1
      
    impostors.pixels = pix_array
    impostors.save() 
    bpy.data.images.remove(impostors)  
    
    
    return {'FINISHED'} 

def create_lowpoly():
    zyb_tools_prop = bpy.context.scene.zyb_tools_properties
    percent = zyb_tools_prop.low_poly_mesh_decimate
    
    base_object = bpy.context.object  
    
    low_object = bpy.data.objects.new(base_object.name+"_low", base_object.data.copy())
    low_object.parent = base_object.parent
    low_object.z3dexport_settings.export = base_object.z3dexport_settings.export
    low_object.z3dexport_settings.export_projectdir = base_object.z3dexport_settings.export_projectdir
    low_object.z3dexport_settings.datatype = base_object.z3dexport_settings.datatype
    low_object.z3dexport_settings.mesh_settings.drawable = base_object.z3dexport_settings.mesh_settings.drawable
    low_object.z3dexport_settings.mesh_settings.indexedmesh = base_object.z3dexport_settings.mesh_settings.indexedmesh
    low_object.z3dexport_settings.mesh_settings.drawable_export_file = base_object.z3dexport_settings.mesh_settings.drawable_export_file+"_low"
    bpy.context.scene.objects.link(low_object)
    
    base_object.select = False
    low_object.select = True
    low_object.hide = False
    bpy.context.scene.objects.active = low_object
    
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = percent
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")
    
    return {'FINISHED'} 

# ~ import bpy
# ~ from math import *
# ~ from mathutils import *

# ~ ob = bpy.context.object

# ~ #vertex colors are in fact stored per loop-vertex -&gt; MeshLoopColorLayer
# ~ if ob.type == 'MESH':
    
    # ~ #how many loops do we have ?
    # ~ loops = len(ob.data.loops)
    # ~ verts = len(ob.data.vertices)
   
    # ~ #go through each vertex color layer
    # ~ for vcol in ob.data.vertex_colors:
        # ~ # look into each loop's vertex ? (need to filter out double entries)
        # ~ visit = verts * [False]
        # ~ colors = {}
        
        # ~ for l in range(loops):
            # ~ v = ob.data.loops[l].vertex_index
            # ~ c = vcol.data[l].color
            # ~ vcol.data[l].color = Vector([0.0, 0.0, 0.0])
            # ~ #if not visit[v]:
            # ~ #    colors[v] = c
            # ~ #    visit[v] = True
                
        # ~ #sorted(colors)
        # ~ #print("Vertex-Colors of Layer:", vcol.name)
        # ~ #print(colors)
        # ~ #for v, c in colors.items():
        # ~ #    print("Vertex {0} has Color {1}".format(v, (c.r, c.g, c.b)))
            
        # ~ print("")
                


 
