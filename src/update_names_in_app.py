import os
import sys
from time import localtime, strftime

__author__ = "zybon"
__date__ = "2021.06.17. 15:33:57"


     
def read_package_name(projdirpath):
     file = open(projdirpath+"..\\..\\namespace.txt")
     fileContent = file.read()
     return fileContent    
    # from xml.dom import minidom

    # parse an xml file by name
#     mydoc = minidom.parse(projdirpath+'AndroidManifest.xml')

#     manifest = mydoc.getElementsByTagName('manifest')[0]
#     return manifest.attributes['package'].value
# #    mainDir = package.replace(".","/")
#    print(mainDir)

def get_alapfile_es_dirpath(projdirpath, java_file_name, package): 
    file = open(os.path.dirname(os.path.realpath(__file__))+"\\objectsnames.temp")
    ido = strftime("%Y.%m.%d %H:%M:%S", localtime())
    fileContent = file.read()
    fileContent = fileContent.replace("IDO", ido)
#    fileContent = fileContent.replace("NEV", filenev)
    dirpath = projdirpath+"java\\"+(package.replace(".", "\\"))+"\\"
    fileContent = fileContent.replace("PACKAGE", package, 1)
    fileContent = fileContent.replace("NAME", java_file_name, 1)
#    file.close()
    return (fileContent , dirpath)
    
def write_animationsnev_tojava(projdirpath):
    print("\n*******  write_animationsnev_tojava  ******\n")
    if not os.path.exists(projdirpath+"assets\\animations"):
        return    
   
    package = read_package_name(projdirpath)+".names"
    java_file_name = "AnimationsNames"
    fileContent, dirpath = get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    solidsFiles = os.listdir(projdirpath+"assets\\animations")
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent)  
        for solidsFile in solidsFiles:
            fw("    public static final String ")
            fw(os.path.splitext(solidsFile)[0]+" = ")
            fw('"')
            fw("animations/"+solidsFile)
            fw('";')
            fw('\n')
        
        #file lezáró
        fw("\n}")      
    
def write_solidsnev_tojava(projdirpath):
    print("\n*******  write_solidsnev_tojava  ******\n")
    if not os.path.exists(projdirpath+"assets\\solids"):
        return    
   
    package = read_package_name(projdirpath)+".names"
    java_file_name = "SolidsNames"
    fileContent, dirpath = get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    solidsFiles = os.listdir(projdirpath+"assets\\solids")
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent)  
        for solidsFile in solidsFiles:
            fw("    public static final String ")
            fw(os.path.splitext(solidsFile)[0]+" = ")
            fw('"')
            fw("solids/"+solidsFile)
            fw('";')
            fw('\n')
        
        #file lezáró
        fw("\n}")    

def write_musicsnev_tojava(projdirpath):
    print("\n*******  write_musics_names_tojava  ******\n")
    if not os.path.exists(projdirpath+"assets\\musics"):
        return
        
   
    package = read_package_name(projdirpath)+".names"
    java_file_name = "MusicsNames"
    fileContent, dirpath = get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    musicFiles = os.listdir(projdirpath+"assets\\musics")
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent)  
        for musicFile in musicFiles:
            fw("    public static final String ")
            fw(os.path.splitext(musicFile)[0]+" = ")
            fw('"')
            fw("musics/"+musicFile)
            fw('";')
            fw('\n')
        
        #file lezáró
        fw("\n}")
        
def write_shadersnev_tojava(projdirpath):
    print("\n*******  write_shaders_names_tojava  ******\n")
   
    package = read_package_name(projdirpath)+".names"
    java_file_name = "ShadersNames"
    fileContent, dirpath = get_alapfile_es_dirpath(projdirpath, java_file_name, package)
    if not os.path.exists(dirpath):
        print(dirpath+" created")
        os.makedirs(dirpath)      
    
    shaderFiles = os.listdir(projdirpath+"assets\\shaders")
    vertex_shaders = []
    fragment_shaders = []
    for shaderFile in shaderFiles:
        if ("vertex" in shaderFile):
            vertex_shaders.append(shaderFile)
        if ("fragment" in shaderFile):
            fragment_shaders.append(shaderFile)            
    
    
    with open((dirpath+java_file_name+".java"), "w", encoding="utf8", newline="\n") as f:
        fw = f.write
        fw(fileContent)  
        
        fw("    public static final class VertexShaders {\n")
        for shaderFile in vertex_shaders:
            fw("        public static final String ")
            fw(os.path.splitext(shaderFile)[0].replace("_vertex_shader", "")+" = ")
            fw('"')
            fw("shaders/"+shaderFile)
            fw('";')
            fw('\n')
        fw("    }\n") 
        fw('\n')
        fw("    public static final class FragmentShaders {\n")
        for shaderFile in fragment_shaders:
            fw("        public static final String ")
            fw(os.path.splitext(shaderFile)[0].replace("_fragment_shader", "")+" = ")
            fw('"')
            fw("shaders/"+shaderFile)
            fw('";')
            fw('\n')
        fw("    }\n")         
        
        #file lezáró
        fw("\n}")        
    
def start_rename():
    print(str(sys.argv))
    projdirpath = sys.argv[1]+"\\"
    # ~ print(projdirpath)
    
    write_musicsnev_tojava(projdirpath)
    write_shadersnev_tojava(projdirpath)
    # ~ write_solidsnev_tojava(projdirpath)
    write_animationsnev_tojava(projdirpath)
    # answer = input("Press any button...")


    
    
def go():
    print("go")
    
    

if __name__ == "__main__":
#    blender_extract()
#    read_xml(
    start_rename()

        
