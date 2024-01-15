# ##### ZYB3D creator #####
#
# 2021.07.11. 12:00
# 

import os

import bpy
import mathutils
import math
import random

from time import localtime, strftime
import zyb_utils

class Instance():
    
    BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
    
    def __init__(self, context, instance_object):
        self.object = instance_object
        self.export_only_location = instance_object.parent.z3dexport_settings.instance_settings.export_only_location
        self.save_names = instance_object.parent.z3dexport_settings.instance_settings.save_names
        
        if (self.save_names):
            if (len(self.object.name)>32):
                raise Exception("['"+instance_object.name+"'] name length is longer than 32 character")  
                
        
        self.read_position()
        if (self.export_only_location is False):
            self.read_rotation()
            self.read_scale()
            self.read_modelmatrix()
          
        
    def read_position(self):
        self.position = Instance.BLENDER_TO_ANDROID_OPENGL_MATRIX * self.object.location
    
    def read_rotation(self):
        self.object.rotation_mode = 'AXIS_ANGLE'
        self.rotation_angle = self.object.rotation_axis_angle[0]*180.0/math.pi
        self.rotation_axis = Instance.BLENDER_TO_ANDROID_OPENGL_MATRIX * mathutils.Vector(self.object.rotation_axis_angle[1:])  
        # ~ self.object.rotation_mode = 'XYZ'
        # ~ self.rotation_angle = self.object.rotation_euler[2]*180.0/math.pi
        # ~ self.rotation_axis = mathutils.Vector([0.0, 1.0, 0.0])
        
    def set_rnd_rotation(self):
        self.rotation_angle = (360.0)*random.random()        
               
    def read_scale(self):    
        self.scale = self.object.scale[0]
        
    def set_rnd_scale(self, min, max):
        self.scale = min+(max-min)*random.random()
        
    def read_modelmatrix(self):    
        self.model_mtx = zyb_utils.createIdentityMatrix()
        self.model_mtx = zyb_utils.translateMatrix(self.model_mtx, self.position.x, self.position.y, self.position.z)
        self.model_mtx = zyb_utils.rotateMatrix(self.model_mtx, self.rotation_angle, self.rotation_axis[0], self.rotation_axis[1], self.rotation_axis[2])
        # self.model_mtx = zyb_utils.scaleMatrix(self.model_mtx, self.scale, self.scale, self.scale)       
        
    def write_to_bin(self, fw):    
        fw(zyb_utils.vector_to_bytes(self.position))
        if (self.export_only_location is False):
            fw(zyb_utils.float_to_bytes(self.rotation_angle))
            fw(zyb_utils.vector_to_bytes(self.rotation_axis))
            fw(zyb_utils.float_to_bytes(self.scale))  
            fw(zyb_utils.float_array_to_bytes(self.model_mtx)) 
        if (self.save_names is True):
            
            nameInBytes = str.encode(self.object.name.rjust(32, "#"))
            print(self.object.name.rjust(32, "#"), len(nameInBytes))
            # fw(bytes([len(nameInBytes)]))
            fw(nameInBytes)
        
    def write_to_txt(self, fw):
        # ~ fw("basemesh collector: "+self.basemesh_collector+"\n")
        # ~ fw("basemesh name: "+self.basemesh_name+"\n")
        fw("position: "+(str(self.position))+"\n")
        if (self.export_only_location is False):
            fw("rotation angle: "+str(self.rotation_angle)+"°\n")
            fw("rotation axis: "+str(self.rotation_axis)+"\n")
            fw("scale: "+(str(self.scale))+"\n")
            fw("model matrix:\n")
            fw("%s\n" % zyb_utils.matrixfloatarray_to_string(self.model_mtx)) 
        if (self.save_names is True):
            fw("%s\n" % self.object.name.rjust(32, "#")) 
        fw("\n******************************\n")         
        

class InstanceGroup():
    
    def __init__(self, instance_group_parent):
        self.name = instance_group_parent.name
        self.instance_group_parent = instance_group_parent
        
        self.export_only_location = instance_group_parent.z3dexport_settings.instance_settings.export_only_location
        self.save_names = instance_group_parent.z3dexport_settings.instance_settings.save_names
        
        self.from_index = 0
        self.data_length = 0          
        
        self.x_min = 100000
        self.x_max = -100000
            
        self.z_min = 10000
        self.z_max = -10000
        self.sector_column_size = instance_group_parent.z3dexport_settings.instance_settings.sector_columnsize
        self.sector_row_size = instance_group_parent.z3dexport_settings.instance_settings.sector_rowsize
        self.instances = []
        
        self.int_size_in_bytes = 4
        self.vector_size_in_bytes = 3*self.int_size_in_bytes
        
        self.onlylocation_info_size_in_bytes = 1*self.int_size_in_bytes
        self.savename_info_size_in_bytes = 1*self.int_size_in_bytes
        
        
        self.sector_info_size_in_bytes = 6*self.int_size_in_bytes
        self.header_index_size_in_byte = 1*self.int_size_in_bytes
        
        self.instance_counter_size_in_bytes = 1*self.int_size_in_bytes
        
        self.positions_size_in_bytes = 1*self.vector_size_in_bytes
        
        self.rotation_angle_size_in_bytes = 1*self.int_size_in_bytes
        self.rotation_axis_size_in_bytes = 1*self.vector_size_in_bytes        
        
        self.scale_size_in_bytes = 1*self.int_size_in_bytes
        
        self.modelmtx_size_in_bytes = 16*self.int_size_in_bytes
        
        self.name_size_in_bytes = 32
        
        self.instance_size_in_bytes = self.positions_size_in_bytes 
        if (self.export_only_location is False):
            self.instance_size_in_bytes = self.instance_size_in_bytes + self.rotation_angle_size_in_bytes + self.rotation_axis_size_in_bytes + self.scale_size_in_bytes + self.modelmtx_size_in_bytes       
            
        if (self.save_names is True):  
            self.instance_size_in_bytes = self.instance_size_in_bytes + self.name_size_in_bytes
        
            
        
    def add_instance(self, instance):   
        self.instances.append(instance)
        if (self.x_min > instance.position.x):
            self.x_min = instance.position.x
        if (self.x_max < instance.position.x):
            self.x_max = instance.position.x
        if (self.z_min > instance.position.z):
            self.z_min = instance.position.z
        if (self.z_max < instance.position.z):
            self.z_max = instance.position.z
            
    def get_sectored_instances(self):            
        sectors = {} 
        for instance in self.instances:
            column = int((instance.position.x-self.x_min)/self.sector_column_size)
            row = int((instance.position.z-self.z_min)/self.sector_row_size)
            index = (row, column)
            dict_val = sectors.get(index)
            if (dict_val is None):
                sectors[index] = []
            sectors[index].append(instance)     
        return sectors
        
    def write_to_bin(self, fw):
        #write group is export_only_location
        if (self.export_only_location is False):
            fw(zyb_utils.int_to_bytes(0))
        else:
            fw(zyb_utils.int_to_bytes(1))       
            
        if (self.save_names is False):
            fw(zyb_utils.int_to_bytes(0))
        else:
            fw(zyb_utils.int_to_bytes(1))               
        

        column_number = int((self.x_max-self.x_min)/self.sector_column_size)+1
        row_number = int((self.z_max-self.z_min)/self.sector_row_size)+1          
        sectors = self.get_sectored_instances()
        
        #write border data
        fw(zyb_utils.float_to_bytes(self.x_min)) 
        fw(zyb_utils.float_to_bytes(self.x_max))        
        fw(zyb_utils.float_to_bytes(self.z_min)) 
        fw(zyb_utils.float_to_bytes(self.z_max))         
        
        #write sector data
        fw(zyb_utils.float_to_bytes(self.sector_column_size)) 
        fw(zyb_utils.float_to_bytes(self.sector_row_size)) 
        
        print("self.instance_size_in_bytes", self.instance_size_in_bytes)
        
        header_size_in_bytes = self.onlylocation_info_size_in_bytes + \
                                self.savename_info_size_in_bytes + \
                                self.sector_info_size_in_bytes + \
                                row_number*column_number*self.header_index_size_in_byte
        
        #write header data
        #4 byte to every sector start index (max 4,3 Gb)
        sector_start_index = header_size_in_bytes
        for row in range(row_number):
            for column in range(column_number):  
                index = (row, column)
                instances_in_sector = sectors.get(index)
                if (instances_in_sector is not None):
                    print(" sector_start_index:", sector_start_index) 
                    print(index, " instances count:", len(instances_in_sector)) 
                    fw(zyb_utils.int_to_bytes(sector_start_index)) 
                    instances_count_in_sector = len(instances_in_sector) 
                    sector_start_index = sector_start_index + self.instance_counter_size_in_bytes + instances_count_in_sector*self.instance_size_in_bytes        
                else:
                    fw(zyb_utils.int_to_bytes(0))        
        
        #body write only sector with instances
        for row in range(row_number):
            for column in range(column_number):  
                index = (row, column)
                instances_in_sector = sectors.get(index)
                if (instances_in_sector is not None): 
                    fw(zyb_utils.int_to_bytes(len(instances_in_sector)))
                    for instance in instances_in_sector:
                        instance.write_to_bin(fw)  
        
    def write_to_txt(self, fw):
        fw("group name: "+self.name+"\n")
        
        fw("export_only_location: "+str(self.export_only_location)+"\n")
        fw("save_names: "+str(self.save_names)+"\n")
        
        column_number = int((self.x_max-self.x_min)/self.sector_column_size)+1
        row_number = int((self.z_max-self.z_min)/self.sector_row_size)+1          
        sectors = self.get_sectored_instances()
        
        fw("x_min: "+str(self.x_min)+"\n")
        fw("x_max: "+str(self.x_max)+"\n")  
        fw("z_min: "+str(self.z_min)+"\n")
        fw("z_max: "+str(self.z_max)+"\n")          
        fw("sector_column_size: "+str(self.sector_column_size)+"\n")
        fw("sector_row_size: "+str(self.sector_row_size)+"\n")
        fw("\n")
        for row in range(row_number):
            for column in range(column_number):  
                index = (row, column)
                instances_in_sector = sectors.get(index)
                if (instances_in_sector is not None): 
                    fw("sector ["+str(row)+", "+str(column)+"]: \n")
                    fw("instance_number in sector: "+str(len(instances_in_sector))+"\n")
                    for instance in instances_in_sector:
                        instance.write_to_txt(fw)         




def copy_instances_to_meshes(context):
    print("\n*******  copy_instances_to_meshes  ******\n")
    source = context.object
    bpy.context.scene.objects.active = source
    source.select = True
    bpy.ops.object.duplicates_make_real()
    source.select = False
#    bpy.ops.object.make_single_user(obdata=True)
    return context.selected_objects

def read_instance_groups(context, instance_group_parents):
    print("\n- read_instance_groups()")
    instance_groups = {}

    for instance_group_parent in instance_group_parents:
        print("-- Create InstanceGroup ["+instance_group_parent.name+"]")
        instance_group = InstanceGroup(instance_group_parent)
        
        for instance_object in instance_group_parent.children:
            print("--- Create Instance ["+instance_object.name+"] and to group")
            instance = Instance(context, instance_object)  
            instance_group.add_instance(instance)    
            
        instance_groups[instance_group_parent.name] = instance_group
    return instance_groups 

def write_instances_to_bin_z3d(assetsParticlesDirPath, filename, instance_groups):
    print("\n- write_instances_to_bin_z3d()")
    print("-- Instances data export to: ["+assetsParticlesDirPath+filename+"]")
    with open((assetsParticlesDirPath+filename), "wb") as f:
        fw = f.write
        from_index = 0
        data_length = 0           
        for instance_group_name, instance_group in instance_groups.items():
            from_index = f.tell()
            print("--- Export ["+instance_group_name+"]")
            instance_group.write_to_bin(fw)
            data_length = f.tell() - from_index
            instance_group.from_index = from_index
            instance_group.data_length = data_length
            print(from_index, data_length)             
#            fw("\n")
            

                
def write_instances_to_txt(filename, instance_groups):
    print("\n- write_instances_to_txt()")
    print("-- Temp file save to [C:\\Users\\user\\BlenderProjects\\temp\\"+filename+".txt]")
    with open(("C:\\Users\\user\\BlenderProjects\\temp\\"+filename+".txt"), "w") as f:
        fw = f.write
        for instance_group_name, instance_group in instance_groups.items():

            instance_group.write_to_txt(fw)
            fw("\n")
            
def write_instancesgroupsnames_to_txt(filename, instances_groups):
    print("\n- write_instancesgroupsnames_to_txt()")
   
    dirpath = os.path.dirname(bpy.data.filepath)+"\\game_extra\\names\\instancesystems\\"
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
   
    file_name = filename #.capitalize()
    print("-- Write instances_groups names to \n\t["+dirpath+file_name+".txt]")
    with open((dirpath+file_name+".txt"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        for instance_group_name, instance_group in instances_groups.items():
            print("--- Write ["+instance_group_name+"]")
#            fw("        public static final String ")
#            fw(object_data.name+" = ")
#            fw('"')
            fw(instance_group_name)
            fw("#")
            fw(str(instance_group.from_index))
            fw("#")
            fw(str(instance_group.data_length))
            fw("#")
            if (instance_group.save_names):
                fw(str(len(instance_group.instances)))
                fw("#")
                for instance in instance_group.instances:
                    fw(instance.object.name)
                    fw("#")
            else:
                fw("0")
            fw('\n')
        
        #file lezáró
#        fw("\n    }")      

def write_instancesgroupsnames_to_java(projdirpath):
    print("\n-  write_objectsnames_to_java()")
    
    names_dir = os.path.dirname(bpy.data.filepath)+"\\game_extra\\names\\instancesystems\\"
   
    package = zyb_utils.read_package_name(projdirpath)+".names"
    java_file_name = "InstanceSystemsNames"
    fileContent, dirpath = zyb_utils.get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    
    print("-- Write intsance names from ["+names_dir+"] \n\tto ["+ dirpath+java_file_name+".java]")
    
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent) 
        file_list = sorted(next(os.walk(names_dir))[2])
        for filename in file_list:
            print("--- Instance name: ["+filename+"]")
            write_instancesgroupsname_from_txt_file_to_java(fw, names_dir, filename)
            fw("\n") 
        #file lezáró
        fw("\n}")     
    
        
def write_instancesgroupsname_from_txt_file_to_java(fw, names_dir, filename):
    collector_name = filename[:len(filename)-4]
    fw("    public static final class "+collector_name.capitalize()+" {\n")   
    fw("        public static final String ")
    fw("collector_file_name = ")
    fw('"')
    fw("instances/"+collector_name)
    fw('.z3d";\n\n')    
    
    with open(names_dir+filename) as fp:
        for cnt, line in enumerate(fp):
            lineContent = line.strip()
            lineContentArray = lineContent.split("#")
            name = lineContentArray[0]
            fw("        public static final String ")
            fw(name+" = ")
            fw('"instances/')
            fw(collector_name)
            fw(".z3d#")
            fw(lineContentArray[0]+"#"+lineContentArray[1]+"#"+lineContentArray[2])
            fw('";\n')
            savedNames = int(lineContentArray[3])
            if (savedNames>0):
                for i in range(0, savedNames):
                    fw("        public static final String ")
                    fw(lineContentArray[4+i]+" = \""+lineContentArray[4+i]+"\";\n")
                
    fw("    }\n")         

def save(context, objects):
    print("\n------------------------\n")
    print("INSTANCE DATA EXPORT START ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")
    import importlib
    importlib.reload(zyb_utils)     
    
    
    global proj_dir
    proj_dir = objects[0].z3dexport_settings.export_projectdir 
    
    filename = objects[0].z3dexport_settings.instance_settings.instancegroup_export_file 
    
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')     
    
#    instances = copy_instances_to_meshes(context)
#    print("objects_select_option: "+objects_select_option)
    # ~ if (objects_select_option == "ACTIVE_AND_SIBLINGS"):
        # ~ bpy.ops.object.select_grouped(type='SIBLINGS')
    instance_group_parents = objects
    if (len(instance_group_parents)==0):
        error_message = 'Context.selected_objects is empty.\n'
        error_message += 'Maybe they are in an invisble layer'
        return error_message
    
    instances_groups = read_instance_groups(context, instance_group_parents)
#    bpy.ops.object.delete(use_global=False)
    write_instances_to_bin_z3d(proj_dir+"assets\\instances\\", filename+".z3d", instances_groups)

    write_instancesgroupsnames_to_txt(filename, instances_groups)
    write_instancesgroupsnames_to_java(proj_dir)

    write_instances_to_txt(filename, instances_groups)
    # ~ sh = "zenity --info --text=\"Export is complete\" --title=\"Finish\" --width=222"
    # ~ os.system(sh)  
    os.system("msg user \"Export is complete\"")    
    print("EXPORT FINISHED ["+strftime("%Y.%m.%d %H:%M:%S", localtime())+"]")    
    print("------------------------\n")
    return {'FINISHED'}


