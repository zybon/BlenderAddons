__author__ = "zybon"
__date__ = "$2018.02.05. 11:20:05$"

bl_info = {
    "name": "Camera settings",
    "category": "Object",
    "author": "zybon",
}

import bpy
from math import *

def change_fov(self, context):
    

    width = context.scene.render.resolution_x
    height = context.scene.render.resolution_y
    vfov = (self.opengl_angle)*pi/180.0
    hfov = 2 * atan((0.5 * width) / (0.5 * height / tan(vfov/2)))
    self.data.angle = hfov
#    print(hfov*180.0/pi)

class CameraSettings(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Camera settings"
    bl_idname = "OBJECT_PT_camera_settings"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
       return context.object.type == "CAMERA" 
   
    def draw(self, context):
        obj = context.object
        
        layout = self.layout        
#        row = layout.row()
#        row.label(text="Active object is: " + obj.name)
#        row = layout.row()
#        row.prop(obj, "name")

        row = layout.row()
        row.prop(obj, "opengl_angle")


def register():
    bpy.utils.register_class(CameraSettings)
    bpy.types.Object.opengl_angle = bpy.props.FloatProperty(name="OpenGl projDeg", default=40.0, update=change_fov)


def unregister():
    bpy.utils.unregister_class(CameraSettings)


if __name__ == "__main__":
    register()
     