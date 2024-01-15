__author__ = "zybon"
__date__ = "$2021.11.08. 11:02:05$"


import bpy
import bpy_extras
import os
import sys

def export_mesh_drawable_to_android(objects_to_export):
    python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
    # ~ print(python_export_scripts_directory)
    if not python_export_scripts_directory in sys.path:
        sys.path.append(python_export_scripts_directory)

    import mesh_drawable_export

    import importlib
    importlib.reload(mesh_drawable_export)     
    return mesh_drawable_export.save(bpy.context, objects_to_export)
    
def calc_optimized_sector_size(solid_object):
    python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
    # ~ print(python_export_scripts_directory)
    if not python_export_scripts_directory in sys.path:
        sys.path.append(python_export_scripts_directory)

    import mesh_solid_export

    import importlib
    importlib.reload(mesh_solid_export)     
    return mesh_solid_export.calc_optimized_sector_size(bpy.context, solid_object)     
    
def export_mesh_solid_to_android(object_to_export):
    python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
    # ~ print(python_export_scripts_directory)
    if not python_export_scripts_directory in sys.path:
        sys.path.append(python_export_scripts_directory)

    import mesh_solid_export

    import importlib
    importlib.reload(mesh_solid_export)     
    return mesh_solid_export.save(bpy.context, object_to_export) 
    
def export_animation_to_android(object_to_export):
    python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
    # ~ print(python_export_scripts_directory)
    if not python_export_scripts_directory in sys.path:
        sys.path.append(python_export_scripts_directory)

    import animation_export

    import importlib
    importlib.reload(animation_export)     
    return animation_export.save(bpy.context, object_to_export)      

class Z3D_ExportDrawableMeshes_Operator(bpy.types.Operator):
    bl_idname = "object.z3dexport_drawablemeshes"
    bl_label = "Export meshes with same z3d file"

    def execute(self, context):
        objects_to_export = []
        base_object = context.object
        for o in bpy.data.objects:
            if (o.z3dexport_settings.export and 
                    o.z3dexport_settings.datatype == "MESH" and
                    o.z3dexport_settings.mesh_settings.drawable and
                    o.z3dexport_settings.export_projectdir == base_object.z3dexport_settings.export_projectdir and 
                    o.z3dexport_settings.mesh_settings.drawable_export_file == base_object.z3dexport_settings.mesh_settings.drawable_export_file
                    ):
                objects_to_export.append(o)
                
        export_mesh_drawable_to_android(objects_to_export)
          
        return {'FINISHED'}   
        
class Z3D_AddVisibilitySphere_Operator(bpy.types.Operator):
    bl_idname = "object.z3d_add_visibilitysphere"
    bl_label = "Add visibility sphere"

    def execute(self, context):
        base_object = context.object
        
        bpy.ops.mesh.primitive_uv_sphere_add(view_align=False, enter_editmode=False, 
            location=context.scene.cursor_location, size=200.0, layers=base_object.layers[:])
        
        sp = context.selected_objects[0]
        sp.parent = base_object
        sp.name = base_object.name+"_visibilty_sphere"
        sp.draw_type = 'WIRE'

        base_object.z3dexport_settings.mesh_settings.visibility_sphere = sp.name
        sp.select = False
        
        base_object.select = True
        bpy.context.scene.objects.active = base_object
          
        return {'FINISHED'}   
        
class Z3D_CalcSolidOpimizedSectorSize_Operator(bpy.types.Operator):
    bl_idname = "object.z3d_calc_solidsectorsize"
    bl_label = "Calc optimized sector size"

    def execute(self, context):
                
        calc_optimized_sector_size(context.object)
          
        return {'FINISHED'}                 
        
class Z3D_ExportSolidMeshes_Operator(bpy.types.Operator):
    bl_idname = "object.z3dexport_solidmeshes"
    bl_label = "Export solid meshes"

    def execute(self, context):
                
        export_mesh_solid_to_android(context.object)
          
        return {'FINISHED'}      
        
class Z3D_ExportAnimation_Operator(bpy.types.Operator):
    bl_idname = "object.z3dexport_animation"
    bl_label = "Export animation"

    def execute(self, context):
                
        export_animation_to_android(context.object)
          
        return {'FINISHED'}               
        
        
def clear_drawable_file_name(self, context):
    path = self.drawable_export_file
    if os.path.exists(path):
        self.drawable_export_file = os.path.splitext(os.path.basename(path))[0] 
    
def clear_solid_file_name(self, context):
    path = self.solid_export_file
    if os.path.exists(path):
        self.solid_export_file = os.path.splitext(os.path.basename(path))[0] 
    
def clear_animated_file_name(self, context):
    path = self.animated_export_file
    if os.path.exists(path):
        self.animated_export_file = os.path.splitext(os.path.basename(path))[0] 
        
class Z3D_MeshSettings(bpy.types.PropertyGroup):
    
    drawable = bpy.props.BoolProperty(name="Drawable", default=False)
    drawable_export_file = bpy.props.StringProperty(name="", subtype="FILE_PATH", default="", update=clear_drawable_file_name)
    drawable_sector = bpy.props.BoolProperty(name="Split into sectors", default=False)
    drawable_sector_columnsize = bpy.props.FloatProperty(name="sector column size", default=100.0)
    drawable_sector_rowsize = bpy.props.FloatProperty(name="sector row size", default=100.0)    
    
    solid = bpy.props.BoolProperty(name="Solid", default=False)
    solid_export_file = bpy.props.StringProperty(name="", subtype="FILE_PATH", default="", update=clear_solid_file_name)
    solid_optimized_sectorsize = bpy.props.BoolProperty(name="Optimized sector size", default=False)
    solid_sector_columnsize = bpy.props.FloatProperty(name="sector column size", default=50.0)
    solid_sector_rowsize = bpy.props.FloatProperty(name="sector row size", default=50.0)    
    
    animated = bpy.props.BoolProperty(name="Animated", default=False)
    animated_export_file = bpy.props.StringProperty(name="", subtype="FILE_PATH", default="", update=clear_animated_file_name)
            
    minvisibilitydistance = bpy.props.FloatProperty(name="Min visibility distance", default=0.0)
    maxvisibilitydistance = bpy.props.FloatProperty(name="Max visibility distance", default=500.0)
    visibility_sphere = bpy.props.StringProperty(name="Visibility sphere")
    
    

    
    indexedmesh = bpy.props.BoolProperty(name="Export as indexed mesh", default=False)            
    export_weight = bpy.props.BoolProperty(name="Export weight", default=False)  
    export_vertexcolor = bpy.props.BoolProperty(name="Export vertex color", default=False)  
        

    

    
    
class Z3dMeshExportSettingsPanel():

        
    def draw_mesh_options(export_panel, context):
        mesh_settings = context.object.z3dexport_settings.mesh_settings
        
        box = export_panel.layout.box()
        box.label("Mesh options")
        
        row = box.row()
        row.prop(mesh_settings, "drawable") 
        
        if (mesh_settings.drawable):
            Z3dMeshExportSettingsPanel.draw_mesh_drawable_options(context, box)    
        
        row = box.row()
        row.prop(mesh_settings, "solid")  
        
        if (mesh_settings.solid):
            Z3dMeshExportSettingsPanel.draw_mesh_solid_options(context, box) 
            
        row = box.row()
        row.prop(mesh_settings, "animated")  
        
        if (mesh_settings.animated):
            Z3dMeshExportSettingsPanel.draw_mesh_animated_options(context, box)             
        
        
    def draw_mesh_drawable_options(context, box):
        scene = context.scene
        mesh_settings = context.object.z3dexport_settings.mesh_settings
        
        box = box.box()
        box.label("Drawable options") 
        
        row = box.row()
        row.label("Export file name:")        
        
        row = box.row()
        row.prop(mesh_settings, "drawable_export_file")
        row.label(".z3d")
        
        # ~ row.operator("object.getexistfilename")        
        
        row = box.row()
        row.prop(mesh_settings, "indexedmesh") 
        
        row = box.row()
        row.prop(mesh_settings, "export_weight") 
        
        row = box.row()
        row.prop(mesh_settings, "export_vertexcolor")  
        
        visibility_box = box.box() 
        visibility_box.label("Visibility settings")              
        
        row = visibility_box.row()
        row.prop(mesh_settings, "minvisibilitydistance") 
        
        row = visibility_box.row()
        row.prop(mesh_settings, "maxvisibilitydistance")
        
        if (mesh_settings.visibility_sphere == ""):  
            row = visibility_box.row()
            row.operator("object.z3d_add_visibilitysphere")
        else:
            row = visibility_box.row()
            row.prop_search(mesh_settings, "visibility_sphere", scene, "objects")   
        
               

        row = box.row()
        row.prop(mesh_settings, "drawable_sector") 
        
        if (mesh_settings.drawable_sector):
            row = box.row()
            row.prop(mesh_settings, "drawable_sector_columnsize")    
            row = box.row()
            row.prop(mesh_settings, "drawable_sector_rowsize")    
            
        row = box.row()
        row.operator("object.z3dexport_drawablemeshes")                    
        
    def draw_mesh_solid_options(context, box):
        mesh_settings = context.object.z3dexport_settings.mesh_settings
        
        box = box.box()
        box.label("Solid options") 
        
        # row = box.row()
        # row.label("Export file name:")        
        
        # row = box.row()
        # row.prop(mesh_settings, "solid_export_file")

        # row.label(".z3d")      
        
        row = box.row()
        row.operator("object.z3d_calc_solidsectorsize")  
        
        # ~ if not (mesh_settings.solid_optimized_sectorsize):
        row = box.row()
        row.prop(mesh_settings, "solid_sector_columnsize")    
        row = box.row()
        row.prop(mesh_settings, "solid_sector_rowsize")           
        
        row = box.row()
        row.operator("object.z3dexport_solidmeshes")    
        
    def draw_mesh_animated_options(context, box):
        mesh_settings = context.object.z3dexport_settings.mesh_settings
        
        box = box.box()
        box.label("Animated options") 
        
        row = box.row()
        row.label("Export file name:")        
        
        row = box.row()
        row.prop(mesh_settings, "animated_export_file")

        row.label(".z3d")        
        
        row = box.row()
        row.operator("object.z3dexport_animation")        
        
         
                                                 
def register_mesh_export():
    bpy.utils.register_class(Z3D_AddVisibilitySphere_Operator)
    bpy.utils.register_class(Z3D_CalcSolidOpimizedSectorSize_Operator)
    bpy.utils.register_class(Z3D_ExportDrawableMeshes_Operator)
    bpy.utils.register_class(Z3D_ExportSolidMeshes_Operator)
    bpy.utils.register_class(Z3D_ExportAnimation_Operator)
    
    bpy.utils.register_class(Z3D_MeshSettings)
    print("register mesh export")
    
    
     

def unregister_mesh_export():
    bpy.utils.unregister_class(Z3D_AddVisibilitySphere_Operator)
    bpy.utils.unregister_class(Z3D_CalcSolidOpimizedSectorSize_Operator)
    bpy.utils.unregister_class(Z3D_ExportDrawableMeshes_Operator)
    bpy.utils.unregister_class(Z3D_ExportSolidMeshes_Operator)
    bpy.utils.unregister_class(Z3D_ExportAnimation_Operator)
    
    bpy.utils.unregister_class(Z3D_MeshSettings)
    
    print("unregister mesh export")
    

