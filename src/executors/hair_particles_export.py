# ##### ZYB3D creator #####
#
# 2018.02.27. 15:51
# 

import os

import bpy
import mathutils
import math
from time import localtime, strftime
import blend_to_z3d


class Particle():
    
    BLENDER_TO_ANDROID_OPENGL_MATRIX = mathutils.Matrix.Rotation(math.radians(-90.0), 4, 'X')
    
    def __init__(self, particle_object):
        self.object = particle_object
        self.read_basemesh_name()
        self.read_position()
        self.read_rotation()
        self.read_scale()
        
    def read_basemesh_name(self):
        point_index = self.object.name.rfind('.')
        self.basemesh_name = self.object.name[:point_index]
    
    def read_position(self):
        self.position = Particle.BLENDER_TO_ANDROID_OPENGL_MATRIX * self.object.location
    
    def read_rotation(self):
        # ~ self.object.rotation_mode = 'AXIS_ANGLE'
        # ~ self.rotation_angle = self.object.rotation_axis_angle[0]*180.0/math.pi
        # ~ self.rotation_axis = Particle.BLENDER_TO_ANDROID_OPENGL_MATRIX * mathutils.Vector(self.object.rotation_axis_angle[1:])  
        self.object.rotation_mode = 'XYZ'
        self.rotation_angle = self.object.rotation_euler[2]*180.0/math.pi
        self.rotation_axis = mathutils.Vector([0.0, 1.0, 0.0])
        
    def read_scale(self):    
        self.scale = self.object.scale[0]
        
    def write_to_bin(self, fw):    
        fw(blend_to_z3d.vector_to_bytes(self.position))
        fw(blend_to_z3d.float_to_bytes(self.rotation_angle))
        fw(blend_to_z3d.vector_to_bytes(self.rotation_axis))
        fw(blend_to_z3d.float_to_bytes(self.scale))        
        
    def write_to_txt(self, fw):
#        fw("basemesh name: "+self.basemesh_name+"\n")
        fw("position: "+(str(self.position))+"\n")
        fw("rotation angle: "+str(self.rotation_angle)+"°\n")
        fw("rotation axis: "+str(self.rotation_axis)+"\n")
        fw("scale: "+(str(self.scale))+"\n")
        

class ParticleGroup():
    
    def __init__(self, basemesh_name):
        self.basemesh_name = basemesh_name
        self.particles = []
        
    def add_particle(self, particle):   
        self.particles.append(particle)
        
    def write_to_bin(self, fw):
        particle_number = len(self.particles)
        fw(blend_to_z3d.int_to_bytes(particle_number))        
        for particle in self.particles:
            particle.write_to_bin(fw)
        
    def write_to_txt(self, fw):
        i = 0
        for particle in self.particles:
            fw("#"+str(i)+":\n")
            particle.write_to_txt(fw)
            i = i + 1

def copy_particles_to_meshes(context):
    print("\n*******  copy_particles_to_meshes  ******\n")
    source = context.object
    bpy.context.scene.objects.active = source
    source.select = True
    bpy.ops.object.duplicates_make_real()
    source.select = False
#    bpy.ops.object.make_single_user(obdata=True)
    return context.selected_objects

def read_particle_groups(particles):
    particle_groups = {}

    for particle_object in particles:
        particle = Particle(particle_object)  
        
        group_key = particle.basemesh_name
#        print("group_key "+group_key)
        if (group_key in particle_groups):
            particle_group = particle_groups.get(group_key)
        else:
            particle_group = ParticleGroup(group_key)
            particle_groups[group_key] = particle_group
           
        particle_group.add_particle(particle)    
    
    return particle_groups 

def write_particles_to_bin_z3d(resRawDirPath, filename, particle_groups):
    print("file mentes: "+resRawDirPath+filename)
    with open((resRawDirPath+filename), "wb") as f:
        fw = f.write
        for basemesh_name, particle_group in particle_groups.items():
            text_in_bytes = str.encode(basemesh_name)
#                print("texture: "+object_data['texture'])
            fw(bytes([len(text_in_bytes)]))
            fw(text_in_bytes) 
#            fw(basemesh_name+" particles\n")
            particle_group.write_to_bin(fw)
#            fw("\n")
            

                
def write_particles_to_txt(filename, particle_groups):
    print("file save: /home/zybon/BlenderProjects/temp/"+filename+".txt")
    with open(("/home/zybon/BlenderProjects/temp/"+filename+".txt"), "w") as f:
        fw = f.write
        for basemesh_name, particle_group in particle_groups.items():
            fw(basemesh_name+" particles\n")
            particle_group.write_to_txt(fw)
            fw("\n")

def save_particles(proj_dir, filename, context):
#    particles = copy_particles_to_meshes(context)

#    particles_groups = read_particle_groups(particles)
#    bpy.ops.object.delete(use_global=False)
#    write_particles_to_bin_z3d(proj_dir+"res/raw/", filename+".z3d", particles_groups)

#    write_particles_to_txt(filename, particles_groups)
#    write_to_txt_z3d(filename, particles_datas)
    print("particle_export.save_particles() executor")
    return {'FINISHED'}

#
#def create_empty_mesh_for_join():
#    bpy.ops.object.select_all(action='DESELECT')
#    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
#    bpy.ops.object.editmode_toggle()
#    bpy.ops.mesh.select_all(action='SELECT')
#    bpy.ops.mesh.delete(type='VERT')
#    bpy.ops.object.editmode_toggle()
#    return bpy.context.scene.objects.active
#    
#    
#
#def place_particles_to_cells(particles):
#    print("\n*******  place_particles_to_cells  ******\n")
#    tableSizeX = 3000.0
#    tableSizeZ = 3000.0
#    min_cellX = -1500.0
#    min_cellZ = -1500.0
#    cellSizeX = 50.0
#    cellSizeZ = 50.0
#    columnNumber = int((tableSizeX/cellSizeX)+1)
#    rowNumber = int((tableSizeZ/cellSizeZ)+1)
#    cells = {}
#    for row in range(rowNumber):
#        for column in range(columnNumber):    
#            cells[(row, column)] = []
#    
#    for particle in particles:
#        x = particle.location.x
#        z = -particle.location.y
#        column = (int)((x-min_cellX)/cellSizeX);
#        row = (int)((z-min_cellZ)/cellSizeZ);
#        cells[(row, column)].append(particle)
#        
#    cell_objects = []    
#    for cellIndex in cells:
#        if len(cells[cellIndex])>0:
#
#            empty = create_empty_mesh_for_join()
#            empty.name = "cell_%d_%d" % (cellIndex[0], cellIndex[1])               
#            bpy.ops.object.select_all(action='DESELECT')
#
#            for p in cells[cellIndex]:
#                p.select = True
##                bpy.ops.object.make_single_user(obdata=True)
#            empty.select = True
#            bpy.context.scene.objects.active = empty
#            bpy.ops.object.join()
#            cell_objects.append(empty)
#            print(empty.name+" added to cell_objects")        
#        
##        print("cell_%d_%d" % (cell[0] ,cell[1]))
##    for row in range(rowNumber):
##        for column in range(columnNumber):    
##            if len(cells[(row, column)])>0:
##                
##                empty = create_empty_mesh_for_join()
##                empty.name = "cell_%d_%d" % (row, column)               
##                bpy.ops.object.select_all(action='DESELECT')
##                
##                for p in cells[(row, column)]:
##                    p.select = True
###                bpy.ops.object.make_single_user(obdata=True)
##                empty.select = True
##                bpy.context.scene.objects.active = empty
##                bpy.ops.object.join()
##                cell_objects.append(empty)
##                print(empty.name+" added to cell_objects")
#    return cell_objects
