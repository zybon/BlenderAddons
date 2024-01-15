__author__ = "zybon"
__date__ = "$2021.11.08. 11:12:05$"


import bpy
import bpy_extras
import os
import sys

    
def export_instances_to_android(objects_to_export):
    python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
    # ~ print(python_export_scripts_directory)
    if not python_export_scripts_directory in sys.path:
        sys.path.append(python_export_scripts_directory)

    import instances_export
    
    import importlib
    importlib.reload(instances_export)    
    return instances_export.save(bpy.context, objects_to_export)      
    
class Z3D_ExportInstances_Operator(bpy.types.Operator):
    bl_idname = "object.z3dexport_instances"
    bl_label = "Export instances with same z3d file"

    def execute(self, context):
        objects_to_export = []
        base_object = context.object
        for o in bpy.data.objects:
            if (o.z3dexport_settings.export and 
                    o.z3dexport_settings.datatype == "INSTANCE_GROUP" and
                    o.z3dexport_settings.export_projectdir == base_object.z3dexport_settings.export_projectdir and 
                    o.z3dexport_settings.instance_settings.instancegroup_export_file == base_object.z3dexport_settings.instance_settings.instancegroup_export_file
                    
                    ):
                objects_to_export.append(o)
                
        export_instances_to_android(objects_to_export)            
        
        return {'FINISHED'}           
        

        
class UpdateInstanceChildren(bpy.types.Operator):
    bl_idname = "object.z3dupdateinstancechildren"
    bl_label = "Update children"
    bl_description = "Update children name and mesh data share"

    def execute(self, context):
        i = 0
        base_object = bpy.data.objects[context.object.z3dexport_settings.instance_settings.base_object]
        if (context.object.z3dexport_settings.instance_settings.base_object is ''):
            raise Exception("['"+context.object.name+"'] has no instance parent")        
        for c in context.object.children:
            c.data = base_object.data
            c.name = base_object.name+"_"+str(i).rjust(4, "0")
            c.z3dexport_settings.datatype = 'PARTICLE'
            i += 1
        return {'FINISHED'}  
        
        
def clear_instacegroup_file_name(self, context):
    path = self.instancegroup_export_file
    if os.path.exists(path):
        self.instancegroup_export_file = os.path.splitext(os.path.basename(path))[0]     
  
class Z3D_InstanceSettings(bpy.types.PropertyGroup):
    
    def update_children_visiblity(self, context):
        hide = not context.object.z3dexport_settings.instance_settings.groupvisible
        for c in context.object.children:
            c.hide = hide   
            
    instancegroup_export_file = bpy.props.StringProperty(name="", subtype="FILE_PATH", default="", update=clear_instacegroup_file_name)        
    
    sector_columnsize = bpy.props.FloatProperty(name="Sector column size", default=100.0)
    sector_rowsize = bpy.props.FloatProperty(name="Sector row size", default=100.0)            
                
    base_object = bpy.props.StringProperty(name="Instance base object")
    groupvisible = bpy.props.BoolProperty(name="Visible group", default=False, update=update_children_visiblity)
    
    export_only_location = bpy.props.BoolProperty(name="Export only location", default=False) 
    save_names = bpy.props.BoolProperty(name="Save names", default=False) 
    
    
class Z3dInstanceGroupExportSettingsPanel():
   
    def draw_instance_options(export_panel, context):
        scene = context.scene
        instance_settings = context.object.z3dexport_settings.instance_settings
        layout = export_panel.layout

        box = layout.box()
        box.label("Instance options:")
        
        
        
        box.alert = bool(instance_settings.base_object == '')
        
        row = box.row()
        
        row = box.row()
        row.label("Export file name:")        
        
        row = box.row()
        row.prop(instance_settings, "instancegroup_export_file")

        row.label(".z3d")
        
        # ~ row.operator("object.getexistfilename") 
        
        row = box.row()
        row.prop_search(instance_settings, "base_object", scene, "objects") 
        
                    
        row = box.row()
        row.operator("object.z3dupdateinstancechildren")  
        
        row = box.row()
        row.prop(instance_settings, "groupvisible")  
        
        row = box.row()
        row.prop(instance_settings, "sector_columnsize")    
        row = box.row()
        row.prop(instance_settings, "sector_rowsize")   
            
        row = box.row()
        row.prop(instance_settings, "export_only_location")      
        
        row = box.row()
        row.prop(instance_settings, "save_names")         
            
        row = box.row()
        row.operator("object.z3dexport_instances")   
        
      
def register_instancegroup_export():
    bpy.utils.register_class(UpdateInstanceChildren)
    bpy.utils.register_class(Z3D_ExportInstances_Operator)
    bpy.utils.register_class(Z3D_InstanceSettings)
    print("register instancesgroup export")
    
     

def unregister_instancegroup_export():
    bpy.utils.unregister_class(UpdateInstanceChildren)
    bpy.utils.unregister_class(Z3D_ExportInstances_Operator)
    bpy.utils.unregister_class(Z3D_InstanceSettings)
    print("unregister instancesgroup export")
    

        
