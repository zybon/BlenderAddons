__author__ = "zybon"
__date__ = "$2018.02.04. 23:12:05$"

bl_info = {
    "name": "ZybTools",
    "category": "Object",
    "author": "zybon",
    "location": "3D View > Porperties",
}

import bpy
import os
import sys
from bpy.types import Header, Menu, Panel
from math import pi as PI

class ZybTool_Instances_Groups(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="File Name")     
        
def update_instance_group(self, context):
    if (self.placement == "COPY_INSTANCE_GROUP"):
        self.instances_groups.clear()
        for o in bpy.data.objects:
            if (o.z3dexport_settings.datatype == "INSTANCE_GROUP"):
                self.instances_groups.add().name = o.name

class ZybTool_InstanceGroupCreatorSettings(bpy.types.PropertyGroup):   
    
    instancegroup_name = bpy.props.StringProperty(name="Instancegroup name", default = '')
    
    base_type = bpy.props.EnumProperty(
            name="Base type",
            description="Base type",
            items = (
                    ("OBJECT", "OBJECT", "OBJECT"),
                    ("GROUP", "GROUP", "GROUP")
                    ),
            default = "OBJECT"
            )     
    base_object = bpy.props.StringProperty(name="Base object", default = '')
    base_group = bpy.props.StringProperty(name="Base group", default = '')
    
    placement = bpy.props.EnumProperty(
            name="Placement",
            description="Placement type",
            items = (
                    ("RANDOM", "RANDOM", "RANDOM"),
                    ("TEXTURE_MASK", "TEXTURE_MASK", "TEXTURE_MASK"),
                    ("VERTEX_COLOR", "VERTEX_COLOR", "VERTEX_COLOR"),
                    ("COPY_INSTANCE_GROUP", "COPY_INSTANCE_GROUP", "COPY_INSTANCE_GROUP")
                    ),
            default = "RANDOM",
            update=update_instance_group
            )  
    image_for_mask = bpy.props.PointerProperty(type=bpy.types.Image)
    color_on_mask = bpy.props.FloatVectorProperty(
             name = "Color on mask",
             subtype = "COLOR",
             default = (1.0,1.0,1.0,1.0),
             min = 0.0,
             max = 1.0,             
             size = 4
             )    
    
    
    base_instance_group_to_copy = bpy.props.StringProperty(name="Base instance group")
    min_distance = bpy.props.FloatProperty(name="Minimum distance between instance", default=100.0, min=0.0, soft_min=0.0) 
    min_normal_z = bpy.props.FloatProperty(name="Minimum normal Z", default=0.0, min=-1.0, soft_min=-1.0, max=1.0, soft_max=1.0)
    max_normal_z = bpy.props.FloatProperty(name="Maximum normal Z", default=1.0, min=-1.0, soft_min=-1.0, max=1.0, soft_max=1.0)
    
    
    border_object = bpy.props.StringProperty(name="Border object", default = 'BORDER_GAME')
    
    vertical_align_to_object = bpy.props.BoolProperty(name="Vertical align to object", default=False)
    object_to_aligned = bpy.props.StringProperty(name="Object to alignment")
    modelmtx_align_to_object = bpy.props.BoolProperty(name="Model matrix align to object", default=False)  
    
    instances_groups = bpy.props.CollectionProperty(type=ZybTool_Instances_Groups)

class ZybToolProperties(bpy.types.PropertyGroup):
    
    rotation_aroundX = bpy.props.BoolProperty(name="Rotation around X", default=False)
    rotation_aroundY = bpy.props.BoolProperty(name="Rotation around Y", default=False)
    rotation_aroundZ = bpy.props.BoolProperty(name="Rotation around Z", default=False)  
    
    rotation_angle_aroundX = bpy.props.FloatProperty(name="", min=0.0, max=2*PI, soft_min=0.0, soft_max=2*PI, step=100, subtype='ANGLE')
    rotation_angle_aroundY = bpy.props.FloatProperty(name="", min=0.0, max=2*PI, soft_min=0.0, soft_max=2*PI, step=100, subtype='ANGLE')
    rotation_angle_aroundZ = bpy.props.FloatProperty(name="", min=0.0, max=2*PI, soft_min=0.0, soft_max=2*PI, step=100, subtype='ANGLE')
    
    rotation_rnd_aroundX = bpy.props.BoolProperty(name="random", default=False)
    rotation_rnd_aroundY = bpy.props.BoolProperty(name="random", default=False)
    rotation_rnd_aroundZ = bpy.props.BoolProperty(name="random", default=False)
    
    resize_X = bpy.props.BoolProperty(name="X ", default=False)
    resize_Y = bpy.props.BoolProperty(name="Y", default=False)
    resize_Z = bpy.props.BoolProperty(name="Z", default=False)    
    
    resize_value = bpy.props.FloatProperty(name="", min=0.0, soft_min=0.0, step=100)
    
    resize_value_2 = bpy.props.FloatProperty(name="", min=0.0, soft_min=0.0, step=100)
    
    resize_type =  bpy.props.EnumProperty(
        name="Type",
        # ~ description="Export data type",
        items = (
                ("FIX", "FIX", "FIX"),
                ("RANDOM BETWEEN", "RANDOM BETWEEN", "RANDOM BETWEEN")
                ),
        default = "FIX",
        )  
        
    instancegroup_creator_settings = bpy.props.PointerProperty(type=ZybTool_InstanceGroupCreatorSettings)
    
    low_poly_mesh_decimate = bpy.props.FloatProperty(name="", default=0.01, min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)
    
    
################### PANEL #####################

class VIEW3D_PT_zybtools:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'    

class ZybTool_VerticalAlignOperator(bpy.types.Operator):
    bl_idname = "zybtool.vertical_align"
    bl_label = "Vertical align"
    bl_description = "Selected objects align to active object"

    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.vertical_align()

        
class VIEW3D_PT_zybtool_vertical_align(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Vertical align"   

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("zybtool.vertical_align")    


            
class ZybTool_RotateObjectsOperator(bpy.types.Operator):
    bl_idname = "zybtool.rotate_objects"
    bl_label = "Rotate"
    bl_description = "Rotate selected objects"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.rotate_objects()    
        
           
        
class VIEW3D_PT_zybtool_rotation(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Rotate selected objects"  


    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        zyb_tools_prop = context.scene.zyb_tools_properties
        layout = self.layout
        
        row = layout.row()
        row.prop(zyb_tools_prop, "rotation_aroundX")
        if (zyb_tools_prop.rotation_aroundX):
            row = layout.row()
            column = row.column()
            column.enabled = not zyb_tools_prop.rotation_rnd_aroundX
            column.prop(zyb_tools_prop, "rotation_angle_aroundX")
            column = row.column()
            column.prop(zyb_tools_prop, "rotation_rnd_aroundX")
        
        row = layout.row()
        row.prop(zyb_tools_prop, "rotation_aroundY")
        if (zyb_tools_prop.rotation_aroundY):
            row = layout.row()
            column = row.column()
            column.enabled = not zyb_tools_prop.rotation_rnd_aroundY
            column.prop(zyb_tools_prop, "rotation_angle_aroundY")
            column = row.column()
            column.prop(zyb_tools_prop, "rotation_rnd_aroundY")
        
        row = layout.row()
        row.prop(zyb_tools_prop, "rotation_aroundZ")
        if (zyb_tools_prop.rotation_aroundZ):
            row = layout.row()
            column = row.column()
            column.enabled = not zyb_tools_prop.rotation_rnd_aroundZ
            column.prop(zyb_tools_prop, "rotation_angle_aroundZ")
            column = row.column()
            column.prop(zyb_tools_prop, "rotation_rnd_aroundZ")        
        
        row = layout.row()
        row.operator("zybtool.rotate_objects")   
        
         
        
class ZybTool_ResizeObjectsOperator(bpy.types.Operator):
    bl_idname = "zybtool.resize_objects"
    bl_label = "Resize"
    bl_description = "Resize selected objects"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.resize_objects()    
        
           
        
class VIEW3D_PT_zybtool_resize(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Resize selected objects"  

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        zyb_tools_prop = context.scene.zyb_tools_properties
        layout = self.layout
        
        row = layout.row()
        row.prop(zyb_tools_prop, "resize_type")
        row = layout.row()
        row.prop(zyb_tools_prop, "resize_value")  
        if (zyb_tools_prop.resize_type != "FIX"):
            row = layout.row()
            row.prop(zyb_tools_prop, "resize_value_2")            
                
        row = layout.row()
        row.operator("zybtool.resize_objects")     
        
class ZybTool_LowPolyObjectCreatOperator(bpy.types.Operator):
    bl_idname = "zybtool.lowpoly_creator"
    bl_label = "Low poly object creator"
    bl_description = "Create low poly from active object"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.create_lowpoly()    
        
           
        
class VIEW3D_PT_zybtool_lowpolycreator(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Create low poly from active object"  

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        zyb_tools_prop = context.scene.zyb_tools_properties
        layout = self.layout
        
        row = layout.row()
        row.prop(zyb_tools_prop, "low_poly_mesh_decimate") 
                
        row = layout.row()
        row.operator("zybtool.lowpoly_creator")             
        
class ZybTool_TurnOnTextureOperator(bpy.types.Operator):
    bl_idname = "zybtool.switch_texture_on"
    bl_label = "On"
    bl_description = "Turn on texture"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.switch_texture(visibility=True)    
        
class ZybTool_TurnOffTextureOperator(bpy.types.Operator):
    bl_idname = "zybtool.switch_texture_off"
    bl_label = "Off"
    bl_description = "Turn off texture"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.switch_texture(visibility=False)            
        
           
        
class VIEW3D_PT_zybtool_texture_switch(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Switch texture visibility in materials"  
    bl_description = "Switch texture visibility in materials"

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        column = row.column()
        column.operator("zybtool.switch_texture_on")     
        column = row.column()
        column.operator("zybtool.switch_texture_off") 
        
        
class ZybTool_ImpostorCreatorOperator(bpy.types.Operator):
    bl_idname = "zybtool.create_impostors"
    bl_label = "Create impostor"
    bl_description = "Start impostor creator"
    
    def execute(self, context):
        zyb_tool_script = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\zyb_tools.py")
        if not zyb_tool_script in sys.path:
            sys.path.append(zyb_tool_script)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.create_impostors(context)          
        
class VIEW3D_PT_zybtool_impostor_creator(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Impostor creator"  
    bl_description = "Create impostor images"

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        column = row.column()
        column.operator("zybtool.create_impostors")   
        # ~ column.operator("render.render", text="Animation", icon='RENDER_ANIMATION').animation = True  
        
class ZybTool_InstanceCreatorOperator(bpy.types.Operator):
    bl_idname = "object.z3dinstancecreator"
    bl_label = "Create instance group"
    bl_description = "Create instance group"

    def execute(self, context):
        python_export_scripts_directory = os.path.dirname("C:\\Users\\User\\BlenderAddons\\executors\\")
        # ~ print(python_export_scripts_directory)
        if not python_export_scripts_directory in sys.path:
            sys.path.append(python_export_scripts_directory)

        import zyb_tools

        import importlib
        importlib.reload(zyb_tools)     
        return zyb_tools.create_instance_group(context)    
        
                       

            
        
     
    
class VIEW3D_PT_zybtool_instancegroup_creator(VIEW3D_PT_zybtools, Panel):
    bl_category = "ZybTools"
    bl_context = "objectmode"
    bl_label = "Instancegroup creator"  
    bl_description = "Instancegroup creator"

    @classmethod
    def poll(cls, context):
        view = context.space_data
        return (view)
        
    def draw(self, context):
        instancegroup_creator_settings = context.scene.zyb_tools_properties.instancegroup_creator_settings      
        scene = context.scene
        
        enabled = True
        
        box = self.layout.box()
        
        row = box.row()
        row.prop(instancegroup_creator_settings, "instancegroup_name") 
        
        if (instancegroup_creator_settings.instancegroup_name == ''):
            enabled = False   
        
        row = box.row()
        row.prop(instancegroup_creator_settings, "base_type", expand=True)     
        
        if (instancegroup_creator_settings.base_type == 'OBJECT'):
            row = box.row()
            row.prop_search(instancegroup_creator_settings, "base_object", scene, "objects")   
            
            if (instancegroup_creator_settings.base_object == ''):
                enabled = False                 
            
        if (instancegroup_creator_settings.base_type == 'GROUP'):
            row = box.row()
            row.prop_search(instancegroup_creator_settings, "base_group", bpy.data, "groups")   
            
            if (instancegroup_creator_settings.base_group == ''):
                enabled = False                     
        
        row = box.row()
        row.prop(instancegroup_creator_settings, "placement")   
        
        if (instancegroup_creator_settings.placement == "COPY_INSTANCE_GROUP"):
            row = box.row()
            row.prop_search(instancegroup_creator_settings, "base_instance_group_to_copy", instancegroup_creator_settings, "instances_groups", icon='OUTLINER_OB_EMPTY')     
                   
            row = box.row()
            row.operator("object.z3dinstancecreator")            
            return
            
        if (instancegroup_creator_settings.placement == "TEXTURE_MASK"):
            row = box.row()
            row.template_ID(instancegroup_creator_settings, "image_for_mask", new="image.new", open="image.open")   
            
            row = box.row()
            row.prop(instancegroup_creator_settings, "color_on_mask")       
            
        row = box.row()
        row.prop_search(instancegroup_creator_settings, "border_object", scene, "objects", icon='MESH_CUBE')                     
            
        row = box.row()
        row.prop(instancegroup_creator_settings, "min_distance")             
        
        row = box.row()
        row.prop(instancegroup_creator_settings, "vertical_align_to_object")        
        
        if (instancegroup_creator_settings.vertical_align_to_object):
            box = box.box()
            row = box.row()
              
            row.prop_search(instancegroup_creator_settings, "object_to_aligned", scene, "objects")
            
            row = box.row()
            row.prop(instancegroup_creator_settings, "min_normal_z") 
        
            row = box.row()
            row.prop(instancegroup_creator_settings, "max_normal_z") 
            
            row = box.row()
            row.prop(instancegroup_creator_settings, "modelmtx_align_to_object")      
            
        row = box.row()
        row.enabled = enabled
        row.operator("object.z3dinstancecreator")     
        
        
classes = (
    ZybTool_Instances_Groups,
    ZybTool_InstanceGroupCreatorSettings,
    ZybToolProperties,
    
    ZybTool_VerticalAlignOperator,
    VIEW3D_PT_zybtool_vertical_align,
    
    ZybTool_RotateObjectsOperator,
    VIEW3D_PT_zybtool_rotation,
    
    ZybTool_ResizeObjectsOperator,
    VIEW3D_PT_zybtool_resize, 
    
    ZybTool_LowPolyObjectCreatOperator,
    VIEW3D_PT_zybtool_lowpolycreator,    
    
    ZybTool_TurnOnTextureOperator,
    ZybTool_TurnOffTextureOperator,
    VIEW3D_PT_zybtool_texture_switch,
    
    
    ZybTool_ImpostorCreatorOperator,
    VIEW3D_PT_zybtool_impostor_creator,
    
    ZybTool_InstanceCreatorOperator,
    VIEW3D_PT_zybtool_instancegroup_creator
    
  
)             

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.zyb_tools_properties = \
        bpy.props.PointerProperty(type=ZybToolProperties)     
        
    # ~ bpy.utils.register_class(Z3D_Instances_Groups)
    # ~ bpy.types.Scene.z3d_instances_groups = bpy.props.CollectionProperty(type=Z3D_Instances_Groups)    
    # ~ bpy.utils.register_class(Z3D_InstanceGroupCreatorSettings)
    # ~ bpy.utils.register_class(Z3D_InstanceCreatorOperator)          
    
    
def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        unregister_class(cls)
        
    del bpy.types.Scene.zyb_tools_properties 
    
    # ~ bpy.utils.unregister_class(Z3D_Instances_Groups)
    # ~ bpy.utils.unregister_class(Z3D_InstanceGroupCreatorSettings)
    # ~ bpy.utils.unregister_class(Z3D_InstanceCreatorOperator)    
    # ~ del bpy.types.Scene.z3d_instances_groups    
    
# ~ if __name__ == "__main__":  # only for live edit.
    # ~ from bpy.utils import register_class
    # ~ register_class(VIEW3D_PT_zybtool)            
