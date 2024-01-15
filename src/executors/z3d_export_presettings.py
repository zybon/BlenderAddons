import bpy
from mathutils import *
from math import *



def changeProjDir():
    for o in bpy.data.objects:
        if (o.z3dexport_settings.export):
            o.z3dexport_settings.export_projectdir = 'C:\\Users\\User\\AndroidStudioProjects\\Zybotopia\\app\\src\\main\\' 
            
def setDrawables():
    for o in bpy.data.objects:
        if (o.z3dexport_settings.export):
            o.z3dexport_settings.mesh_settings.drawable = True
            o.z3dexport_settings.mesh_settings.drawable_export_file = "walker"

changeProjDir()            
setDrawables()