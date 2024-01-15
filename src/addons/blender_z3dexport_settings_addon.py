__author__ = "zybon"
__date__ = "$2018.02.04. 23:12:05$"

bl_info = {
    "name": "Z3d Export settings",
    "category": "Object",
    "author": "zybon",
    "location": "Properties > Object",
}

import bpy
import bpy_extras
import os
import sys
import importlib

export_classes_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\classes\\")
# ~ print(python_export_scripts_directory)
if not export_classes_directory in sys.path:
    sys.path.append(export_classes_directory)
    
import blender_z3d_mesh_export_settings
importlib.reload(blender_z3d_mesh_export_settings)     
from blender_z3d_mesh_export_settings import *

import blender_z3d_instancegroup_export_settings
importlib.reload(blender_z3d_instancegroup_export_settings)     
from blender_z3d_instancegroup_export_settings import *

import blender_z3d_guimesh_export_settings
importlib.reload(blender_z3d_guimesh_export_settings)     
from blender_z3d_guimesh_export_settings import *

class SameNameOperator(bpy.types.Operator):
    bl_idname = "object.samename"
    bl_label = "Object name to data name"

    def execute(self, context):
        context.object.data.name = context.object.name
        return {'FINISHED'}
        
class SameZ3dInfoOperator(bpy.types.Operator):
    bl_idname = "object.same_exportinfo"
    bl_label = "Copy info to selected"

    def execute(self, context):
        base_object = context.object
        for o in context.selected_objects:
            o.z3dexport_settings.export = base_object.z3dexport_settings.export
            o.z3dexport_settings.export_projectdir = base_object.z3dexport_settings.export_projectdir
            o.z3dexport_settings.datatype = base_object.z3dexport_settings.datatype
            o.z3dexport_settings.mesh_settings.drawable = base_object.z3dexport_settings.mesh_settings.drawable
            o.z3dexport_settings.mesh_settings.drawable_export_file = base_object.z3dexport_settings.mesh_settings.drawable_export_file
        return {'FINISHED'}    
        
# ~ class GetExistFileName(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    # ~ bl_idname = "object.getexistfilename" 
    # ~ bl_label = "Get exist file"

    # ~ def invoke(self, context, event):
        # ~ print(self)
        # ~ datatype = context.object.z3dexport_settings.datatype
        # ~ if (datatype == 'INSTANCE_GROUP'):
            # ~ self.filepath = context.object.z3dexport_settings.export_projectdir+"assets\\instances\\"
        # ~ if (datatype == 'MESH' or datatype == 'GUI_MESH'):
            # ~ self.filepath = context.object.z3dexport_settings.export_projectdir+"assets\\meshes\\"
        # ~ wm = context.window_manager.fileselect_add(self)
        # ~ return {'RUNNING_MODAL'}

    # ~ def execute(self, context):
        # ~ datatype = context.object.z3dexport_settings.datatype
        # ~ if (datatype == 'INSTANCE_GROUP'):
            # ~ context.object.z3dexport_settings.instance_settings.instancegroup_export_file = os.path.splitext(os.path.basename(self.filepath))[0]     
        # ~ if (datatype == 'MESH'):
            # ~ context.object.z3dexport_settings.mesh_settings.drawable_export_file = os.path.splitext(os.path.basename(self.filepath))[0]
        # ~ return {'FINISHED'}                  
        
 
            
class Z3D_ExportSettings(bpy.types.PropertyGroup):
    
    export = bpy.props.BoolProperty(name="", default=False)
                
    export_projectdir = bpy.props.StringProperty(name="", subtype="DIR_PATH", default="") 
     
    
    datatype = bpy.props.EnumProperty(
            name="data type",
            description="Export data type",
            items = (
                    ("MESH", "MESH", "MESH"),
                    ("INSTANCE_GROUP", "INSTANCE_GROUP", "INSTANCE_GROUP"),
                    ("PARTICLE", "PARTICLE", "PARTICLE"),
                    ("GUI_MESH", "GUI_MESH", "GUI_MESH")
                    ),
            default = "MESH"
            ) 
            
    mesh_settings = bpy.props.PointerProperty(type=Z3D_MeshSettings)  
    
    instance_settings = bpy.props.PointerProperty(type=Z3D_InstanceSettings) 
    
    gui_mesh_settings = bpy.props.PointerProperty(type=Z3D_GuiMeshSettings)
        
    
    

    
    
class Z3dExportSettingsPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Z3d Export"
    bl_idname = "OBJECT_PT_z3dexport_settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    
    # ~ @classmethod
    # ~ def poll(cls, context):
        # ~ if (context.object.type == "MESH"):
            # ~ return context.object.parent.z3dexport
        # ~ if (context.object.type == "EMPTY"):
            # ~ return True
        # ~ return False    

    # ~ def check(self, context):
        # ~ return True   
   
    def draw_header(self, context):
        layout = self.layout   
        obj = context.object
        row = layout.row()
        row.prop(obj.z3dexport_settings, "export")
        
    def draw(self, context):
        z3dexport_settings = context.object.z3dexport_settings
        
        if (not z3dexport_settings.export):
            return
            
        layout = self.layout
        # ~ layout.enabled = obj.export  
        
        self.draw_blender_options(context)
            
        row = layout.row()
        row.prop(z3dexport_settings, "datatype")              
            
        if (z3dexport_settings.datatype == "PARTICLE"):
            return              
        
        self.draw_file_options(context)
        
        if (z3dexport_settings.datatype == "INSTANCE_GROUP"):
            Z3dInstanceGroupExportSettingsPanel.draw_instance_options(self, context)
            
        elif (z3dexport_settings.datatype == "MESH"):
            Z3dMeshExportSettingsPanel.draw_mesh_options(self, context)
            
        elif (z3dexport_settings.datatype == "GUI_MESH"):
            Z3dGuiMeshExportSettingsPanel.draw_gui_mesh_options(self, context)
        
        # ~ row = layout.row()
        # ~ row.operator("object.export_all_to_z3d")  
        
    def draw_blender_options(self, context):
        box = self.layout.box()
        box.label("Blender options")        
        
        row = box.row()
        row.operator("object.same_exportinfo")   
        
        row = box.row()
        row.operator("object.samename")  
        
    def draw_file_options(self, context):
        z3dexport_settings = context.object.z3dexport_settings
        
        box = self.layout.box()
        box.label("File options")
        
        row = box.row()
        row.label("Android project dir:")
        
        row = box.row()
        row.prop(z3dexport_settings, "export_projectdir")
        
          
                                                 
        
        
def register():
    bpy.utils.register_class(SameNameOperator)
    bpy.utils.register_class(SameZ3dInfoOperator)
    # ~ bpy.utils.register_class(GetExistFileName)
    
    register_mesh_export()
    register_instancegroup_export()
    register_guimesh_export()
    
    
    bpy.utils.register_class(Z3dExportSettingsPanel)
    bpy.utils.register_class(Z3D_ExportSettings)
    
    bpy.types.Object.z3dexport_settings = bpy.props.PointerProperty(type=Z3D_ExportSettings)
    
    
    
     

def unregister():
    bpy.utils.unregister_class(SameNameOperator)
    bpy.utils.unregister_class(SameZ3dInfoOperator)
    # ~ bpy.utils.unregister_class(GetExistFileName)
    
    register_mesh_export()
    register_instancegroup_export()
    register_guimesh_export()
    
    bpy.utils.unregister_class(Z3dExportSettingsPanel)
    bpy.utils.unregister_class(Z3D_ExportSettings)
    


if __name__ == "__main__":
    register()
   
     
