import bpy

import mathutils

import zyb_utils

class Frame():
    
    def __init__(self, frame_index, mesh_data):
        self.frame_index = frame_index
        self.mesh_data = mesh_data
        
class Frames():  
    
    def __init__(self, frame_start, frame_end):
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.frames = {}
        
    def add_frame(self, frame):    
        self.frames[frame.index] = frame

class AnimatedMesh():
    
    def __init__(self, context):
        self.context = context
        self.blender_object = context.object
        self.name = self.blender_object.name
        self.orig_vertices = self.blender_object.data.vertices
        self.vertices_count = len(self.orig_vertices)
#        self.frames = Frames(frame_start, frame_end)

        self.init_indices()

    def init_indices(self):
        self.indices = []
        
        for blender_polygon in self.blender_object.data.polygons:
            for loop_index in blender_polygon.loop_indices:
                blender_vertex_index = self.blender_object.data.loops[loop_index].vertex_index
                if (blender_vertex_index not in self.indices):
                    self.indices.append(blender_vertex_index)
        
        print(self.indices)
        
    def read_positions(self, scene):
        obj = self.blender_object
        mesh = obj.to_mesh(scene, True, 'PREVIEW') # apply modifiers with preview settings
        
        positions = []
        
        for index in self.indices:
            current_vertex = mesh.vertices[index]
            vector = current_vertex.co.xzy
            vector.z = -vector.z
            positions.append(vector.x)            
            positions.append(vector.y)
            positions.append(vector.z)
            positions.append(1.0)
        
        bpy.data.meshes.remove(mesh) # remove 'posed' mesh 
        
        return positions       
        

    def write_frame_to_bin(self, scene, fw):
#        name_in_bytes = str.encode(self.name)
#        fw(bytes([len(name_in_bytes)]))
#        fw(name_in_bytes)    
        
        obj = self.blender_object
        mesh = obj.to_mesh(scene, True, 'PREVIEW') # apply modifiers with preview settings
        # mesh.transform(obj.matrix_world) # apply loc/rot/scale
        
        for index in self.indices:
            current_vertex = mesh.vertices[index]
            # ~ vector = current_vertex.co-self.orig_vertices[index].co
            vector = current_vertex.co.xzy
            vector.z = -vector.z
            fw(zyb_utils.vector_to_bytes(vector))            
        
#         Iterate over vertices
        # ~ for v in mesh.vertices:
            # ~ vector = v.co-self.orig_vertices[v.index].co
            # ~ vector = vector.xzy
            # ~ vector.z = -vector.z
            # ~ fw(zyb_utils.vector_to_bytes(vector))
        bpy.data.meshes.remove(mesh) # remove 'posed' mesh
#        fw("\n")

    def write_frame_to_txt(self, scene, fw):
#        fw("OBJECT: %s\n" % self.name)
        obj = self.blender_object
        mesh = obj.to_mesh(scene, True, 'PREVIEW') # apply modifiers with preview settings
        # mesh.transform(obj.matrix_world) # apply loc/rot/scale
        for index in self.indices:
            current_vertex = mesh.vertices[index]
            # ~ vector = current_vertex.co-self.orig_vertices[index].co
            vector = current_vertex.co.xzy
            vector.z = -vector.z
            fw("%d. vertex: %s\n" % (index, vector))  
        
# ~ #         Iterate over vertices
        # ~ for v in mesh.vertices:
            # ~ #for g in v.groups:
            # ~ #    print(G[g.group].name)
            # ~ vector = v.co-self.orig_vertices[v.index].co
            # ~ vector = vector.xzy
            # ~ vector.z = -vector.z
            # ~ fw("%d. vertex: %s\n" % (v.index, vector))
        bpy.data.meshes.remove(mesh) # remove 'posed' mesh
        fw("\n")
        
def export_frames_to_bin(context, path, filename, animated_mesh):
    anim_file = path+filename+"_"+animated_mesh.name+".anim"
    print("file mentes: "+anim_file)
    with open(anim_file, "wb") as f:
        fw = f.write
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end   
        frame_step = bpy.context.scene.frame_step

        fw(zyb_utils.int_to_bytes(animated_mesh.vertices_count))
        fw(zyb_utils.int_to_bytes(frame_start))
        fw(zyb_utils.int_to_bytes(frame_end))
        fw(zyb_utils.int_to_bytes(frame_step))

        frame_index = frame_start
        while (frame_index<=frame_end): 
            fw(zyb_utils.int_to_bytes(frame_index))
            bpy.context.scene.frame_set(frame_index)
            animated_mesh.write_frame_to_bin(context.scene, fw)
            frame_index = frame_index + frame_step
            
def export_frames_to_bin_and_png(context, path, animated_mesh):
    anim_file = path+animated_mesh.name+".anim"
    print("file mentes: "+anim_file)
    
    frame_start = bpy.context.scene.frame_start
    frame_end = bpy.context.scene.frame_end   
    frame_step = bpy.context.scene.frame_step    

    print("frame_start: %s, frame_end: %s, frame_step: %s" % (frame_start, frame_end, frame_step))

    all_frame_positions = []

    frame_index = frame_start
    while (frame_index<=frame_end): 
        bpy.context.scene.frame_set(frame_index)
        all_frame_positions.append(animated_mesh.read_positions(context.scene))
        # ~ print("%d. frame: %s" % (frame_index, positions))
        frame_index = frame_index + frame_step     
        
    max_positions = mathutils.Vector((-100.0, -100.0, -100.0))    
    min_positions = mathutils.Vector((100.0, 100.0, 100.0))
        
    for positions in all_frame_positions:
        i = 0
        while (i<len(positions)):
            if (positions[i] > max_positions.x ):
                max_positions.x = positions[i]
            if (positions[i] < min_positions.x ):
                min_positions.x = positions[i]  
                
            if (positions[i+1] > max_positions.y ):
                max_positions.y = positions[i+1]
            if (positions[i+1] < min_positions.y ):
                min_positions.y = positions[i+1]  
                
            if (positions[i+2] > max_positions.z ):
                max_positions.z = positions[i+2]
            if (positions[i+2] < min_positions.z ):
                min_positions.z = positions[i+2]   
            i = i+4
                              
    print("max_positions: %s" % max_positions)
    print("min_positions: %s" % min_positions)
    
    png_file_name = animated_mesh.name
            
    imagepath = "C:\\Users\\zybon\\BlenderProjects\\zybonotopia\\game_textures\\"+png_file_name+".png"
    
    im_w = 128
    im_h = 128
    
    image = bpy.data.images.new("Sprite", alpha=True, width=im_w, height=im_h)
    image.use_alpha = True
    image.alpha_mode = 'STRAIGHT'
    image.filepath_raw = imagepath
    image.file_format = 'PNG'
    
    row_as_frame = 0
    for positions in all_frame_positions:
        column_as_vertex_position = 0
        while (column_as_vertex_position < len(positions)):
            
            image.pixels[row_as_frame*im_w*4 + column_as_vertex_position] = (positions[column_as_vertex_position]-min_positions.x)/(max_positions.x-min_positions.x)
            image.pixels[row_as_frame*im_w*4 + column_as_vertex_position+1] = (positions[column_as_vertex_position+1]-min_positions.y)/(max_positions.y-min_positions.y)
            image.pixels[row_as_frame*im_w*4 + column_as_vertex_position+2] = (positions[column_as_vertex_position+2]-min_positions.z)/(max_positions.z-min_positions.z)
            image.pixels[row_as_frame*im_w*4 + column_as_vertex_position+3] = 1.0   
                 
            column_as_vertex_position = column_as_vertex_position + 4   
        row_as_frame = row_as_frame + 1                  
              
                
    image.save() 
    bpy.data.images.remove(image)      
    
    
    with open(anim_file, "wb") as f:
        fw = f.write
        fw(zyb_utils.int_to_bytes(animated_mesh.vertices_count))
        fw(zyb_utils.int_to_bytes(frame_start))
        fw(zyb_utils.int_to_bytes(frame_end))
        fw(zyb_utils.int_to_bytes(frame_step))    
        
        png_file_name_in_byte = str.encode(png_file_name)
        fw(bytes([len(png_file_name_in_byte)]))
        fw(png_file_name_in_byte)   
        
        fw(zyb_utils.vector_to_bytes(max_positions))  
        fw(zyb_utils.vector_to_bytes(min_positions))  
        
def export_frames_to_txt(context, path, filename, animated_mesh):
    anim_file = path+filename+"_"+animated_mesh.name+"_anim.txt"
    print("file mentes: "+anim_file)
    with open(anim_file, "w") as f:
        fw = f.write
        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end   
        frame_step = bpy.context.scene.frame_step

        fw("VERTICES_COUNT: %d\n" % animated_mesh.vertices_count)
        fw("FRAME_START: %d\n" % frame_start)
        fw("FRAME_END: %d\n" % frame_end)
        fw("FRAME_STEP: %d\n" % frame_step)
        fw("\n")

        frame_index = frame_start
        while (frame_index<=frame_end): 
        #        print("FRAME: %d" % frame_index)
            bpy.context.scene.frame_set(frame_index)
            fw("********** FRAME: %d **********\n" % frame_index)
            animated_mesh.write_frame_to_txt(context.scene, fw)
            fw("\n")  
            frame_index = frame_index + frame_step
        


def save(context, objects):
    print("save animation")


    animated_mesh = AnimatedMesh(context)
    
    projdir_fullpath = context.object.z3dexport_settings.export_projectdir
    export_frames_to_bin_and_png(context, projdir_fullpath+"assets\\animations\\", animated_mesh)
    
    import os
    os.system("msg zybon \"Export is complete\"") 
    # ~ export_frames_to_txt(context, "C:\\Users\\zybon\\BlenderProjects\\temp\\", context.object.name, animated_mesh)
    return {"FINISHED"}
 
    
