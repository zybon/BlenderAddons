

def items_file():
    items = []
    # open file
    dir = "/home/zybon/NetBeansProjects/android"
    lista = sorted(next(os.walk(dir))[1])
    for file in lista:
        if file[0] == '_':
            continue
        items.append((file, file, file)) 
    # construct a tuple
    # append to items
    return items 

def getlastsavedplace():
    path = "/home/zybon/BlenderProjects/temp/last_androidproject.txt"
    if not os.path.exists(path):
        print("nincs")
        dir = "/home/zybon/NetBeansProjects/android"
        return sorted(next(os.walk(dir))[1])[0]
    file = open(path)
    l_ap = file.read()
    file.close()
    return l_ap

def clear_filename(self, context):
    self.filename = self.exist_files

def set_filename(self, context):
    self.filename = self.exist_files

def savelastsavedplace(saved):
    with open(("/home/zybon/BlenderProjects/temp/last_androidproject.txt"), "w") as f:
        f.write(saved)


class AnimationExportOperator(bpy.types.Operator):
    bl_idname = "object.animationexport"
    bl_label = "Export animation"
    
    def items_file_names(self, context):
        items = []
        # open file
        dir = "/home/zybon/NetBeansProjects/android/"+self.projdir+"/res/raw/"
        if not os.path.exists(dir):
            items.append(("", "", "")) 
            return items
        lista = sorted(next(os.walk(dir))[2])
        for file in lista:
            indexOf = file.find('.anim')
            if indexOf != -1:
                name = file[:indexOf]
                items.append((name, name, name)) 
        # construct a tuple
        # append to items
        return items
 
    
    projdir = bpy.props.EnumProperty(
            name="Android Projects",
            description="Android Projects",
            items = items_file(),
            default = None,
            update = clear_filename
            )
            
    exist_files = bpy.props.EnumProperty(
            name="Exist anim files",
            description="Exist anim files in projects",
            items = items_file_names,
            default = None,
            update = set_filename
            )            
            
    filename = bpy.props.StringProperty(name="anim file name", default="animation")        
          
    objects_select_option = bpy.props.EnumProperty(
            name="Export objects",
            description="Export objects",
            items = [('ALL','ALL','ALL'),
                    ('SELECTED','SELECTED','SELECTED')],
            default = None
            )  
            
    def export_animation(self):
        python_export_script = os.path.dirname("/home/zybon/NetBeansProjects/python/BlenderToAndroid/src/executors/animation_export.py")
        if not python_export_script in sys.path:
            sys.path.append(python_export_script)

        import animation_export

        import importlib
        importlib.reload(animation_export)     
        projdir_fullpath = "/home/zybon/NetBeansProjects/android/"+self.projdir+"/"
        res_raw_dir =projdir_fullpath+"res/raw/"
        if not os.path.exists(res_raw_dir):
            return "Ebben a projectben ["+projdir+"] nincs 'raw' konyvtar"    
        return animation_export.save(bpy.context, projdir_fullpath, self.objects_select_option, self.filename)             

    def execute(self, context):
        if (self.filename == ""):
            self.report({'ERROR'}, "File name is empty")
            return {'CANCELLED'}            
        eredmeny = self.export_animation()
        print(eredmeny)
        if eredmeny == {'FINISHED'}:
            self.report({'INFO'}, self.projdir+"-ba mentve")
            savelastsavedplace(self.projdir)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, eredmeny)
            return {'CANCELLED'}
        
    def check(self, context):
        return True        
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "projdir") 
        row = layout.row()
        row.prop(self, "exist_files")         
        row = layout.row()
        row.prop(self, "filename")   
        row = layout.row()
        row.prop(self, "objects_select_option")          

    def invoke(self, context, event):
        self.projdir = getlastsavedplace()
        self.filepath = "/home/zybon/NetBeansProjects/android/"+self.projdir+"/res/raw/"
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
#        context.window_manager.fileselect_add(self)
#        return {'RUNNING_MODAL'}  
    
