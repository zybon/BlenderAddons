__author__ = "zybon"
__date__ = "$2021.11.08. 11:02:05$"


import bpy
import bpy_extras
import os
import sys


class Z3D_ExportGuiMeshes_Operator(bpy.types.Operator):
    bl_idname = "object.z3dexport_guimeshes"
    bl_label = "Export gui meshes with same z3d file"

    def execute(self, context):
        objects_to_export = []
        base_object = context.object
        for o in bpy.data.objects:
            if (o.z3dexport_settings.export and 
                    o.z3dexport_settings.datatype == "GUI_MESH" and
                    o.z3dexport_settings.export_projectdir == base_object.z3dexport_settings.export_projectdir and 
                    o.z3dexport_settings.z3dfile == base_object.z3dexport_settings.z3dfile
                    ):
                objects_to_export.append(o)
                
        export_mesh_drawable_to_android(objects_to_export)
          
        return {'FINISHED'}                    
        

class Z3D_GuiMeshSettings(bpy.types.PropertyGroup):
    
    guimesh_export_file = bpy.props.StringProperty(name="", default="")
    
    virtual_screen = bpy.props.StringProperty(name="Virtual screen", default="virtual_screen") 
    squere = bpy.props.BoolProperty(name="Squere")
    squere_to = bpy.props.EnumProperty(
            name="Scale to",
            description="Squere scale",
            items = (
                    ("X", "X", "X"),
                    ("Y", "Y", "Y")
                    ),
            default = "X"
            )
            

    
    
class Z3dGuiMeshExportSettingsPanel():

        
    def draw_gui_mesh_options(export_panel, context):
        scene = context.scene
        gui_mesh_settings = context.object.z3dexport_settings.gui_mesh_settings
        
        box = export_panel.layout.box()
        box.label("GUI Mesh options:")
        
        box.alert = bool(gui_mesh_settings.virtual_screen == '')
        
        row = box.row()
        row.label("Export file name:")     
        
        row = box.row()
        row.prop(gui_mesh_settings, "guimesh_export_file")

        row.label(".z3d")
        
        row.operator("object.getexistfilename")             
        
        row = box.row()
        row.prop_search(gui_mesh_settings, "virtual_screen", scene, "objects")
        
        row = box.row()
        row.prop(gui_mesh_settings, "squere") 
        
        if (gui_mesh_settings.squere):
            row = box.row(align=True)
            row.prop(gui_mesh_settings, "squere_to", expand = True) 
            
        row = box.row()
        row.operator("object.z3dexport_guimeshes")            
           
                                                 
        
        
def register_guimesh_export():
    bpy.utils.register_class(Z3D_ExportGuiMeshes_Operator)
    bpy.utils.register_class(Z3D_GuiMeshSettings)
    print("register guimesh export")

def unregister_guimesh_export():
    bpy.utils.unregister_class(Z3D_ExportGuiMeshes_Operator)
    bpy.utils.unregister_class(Z3D_GuiMeshSettings)
    print("unregister guimesh export")
    

