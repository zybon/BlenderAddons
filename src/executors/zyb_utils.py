# ##### ZYB3D creator #####
#
# 2021.07.11. 12:00
# 
import os
import math
import mathutils
from time import localtime, strftime





def mesh_triangulate(mesh):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()  

def float_round(value, rounder):
    k = round(value, rounder)
    if abs(k)<0.0001:
        return 0.0
    else:
        return k
        
    
def rgb_color_round(color, rounder):
    return (float_round(color[0], rounder), float_round(color[1], rounder), float_round(color[2], rounder))    
    
def vector_round(vector, rounder):
    if (len(vector)==2):
        return (float_round(vector[0], rounder), float_round(vector[1], rounder)) 
    else:
        return (float_round(vector[0], rounder), float_round(vector[1], rounder), float_round(vector[2], rounder))     

def name_compat(name):
    if name is None:
        return 'None'
    else:
        return name.replace('.', '_')


    
def vector_to_bytes(vector):
    t = []
    for coord in vector:
        i = int(coord*100000)#int(float_round(coord,5)*100000)
        t.append((i>>24)&0xff)
        t.append((i>>16)&0xff)
        t.append((i>>8)&0xff)
        t.append((i)&0xff)
        
    return bytes(t)   
    
    

def vector_to_string(vector):        
    t = ""
    length = len(vector)
    for i in range(length):
        t = t+str(vector[i]) #float_round(coo[i],5))
        if (i<length-1):
            t = t+", "
        #t = t+str(int(float_round(c,5)*100000))+" "
    return t   
    
def matrix4x4_to_string(matrix):        
    t = "float[] modelMatrix = float[]{\n\t\t"+str(matrix[0][0])+", "+str(matrix[1][0])+", "+str(matrix[2][0])+", "+str(matrix[3][0])+",\n\t\t"
    t = t+str(matrix[0][1])+", "+str(matrix[1][1])+", "+str(matrix[2][1])+", "+str(matrix[3][1])+",\n\t\t"
    t = t+str(matrix[0][2])+", "+str(matrix[1][2])+", "+str(matrix[2][2])+", "+str(matrix[3][2])+",\n\t\t"
    t = t+str(matrix[0][3])+", "+str(matrix[1][3])+", "+str(matrix[2][3])+", "+str(matrix[3][3])+"}\n"
    
    return t      

def int_to_bytes(ertek):
    return bytes([
        ((ertek>>24)&0xff),
        ((ertek>>16)&0xff),
        ((ertek>>8)&0xff),
        ((ertek)&0xff)
    ])
    
def float_to_bytes(ertek):
    return int_to_bytes(int(float_round(ertek,5)*100000)) 
    
def read_int_from_bytes(int_in_bytes):
    return int.from_bytes(bytes_in_file[byte_index:byte_index+4], byteorder='big', signed=True)
    
def read_float_from_bytes(float_in_bytes):
    float(read_int_from_bytes(float_in_bytes))/100000.0

#-21474 - 21474 között lehet az érték
def float_array_to_bytes(float_array):
    t = []
    for floatValue in float_array:
        float_in_integer = int(float_round(floatValue,5)*100000)
        t.append((float_in_integer>>24)&0xff)
        t.append((float_in_integer>>16)&0xff)
        t.append((float_in_integer>>8)&0xff)
        t.append((float_in_integer)&0xff)
        
    return bytes(t)

def int_array_to_bytes(int_array):
    t = []
    for intValue in int_array:
        t.append((intValue>>24)&0xff)
        t.append((intValue>>16)&0xff)
        t.append((intValue>>8)&0xff)
        t.append((intValue)&0xff)
        
    return bytes(t)        

def matrixfloatarray_to_string(matrix):
    text = ""
    for r in range(0,4):
        for c in range(0,4):
            text = text + str(float_round(matrix[r*4+c],4))
            if (c<3):
                text = text + ", "
        text = text + "\n"
    return text
    
def matrixfloatarray_to_bytes(matrix):
    text = ""
    for r in range(0,4):
        for c in range(0,4):
            text = text + str(float_round(matrix[r*4+c],4))
            if (c<3):
                text = text + ", "
        text = text + "\n"
    return text    
       
def matrixfloatarray_to_Matrix4x4(matrix):
    return mathutils.Matrix((matrix[0:4],matrix[4:8],matrix[8:12],matrix[12:16]))
    
def Matrix4x4_to_matrixfloatarray(matrix4x4):
    matrix = []
    for i in range(0,16):
        matrix.append(0.0)  
    for r in range(0,4):
        for c in range(0,4):
            matrix[r*4+c] = matrix4x4[r][c]
    return matrix
       

def createIdentityMatrix():
    matrix = []
    for i in range(0,16):
        matrix.append(0.0)
    matrix[0] = 1.0
    matrix[5] = 1.0
    matrix[10] = 1.0
    matrix[15] = 1.0
    return matrix
    
def scaleMatrix(matrix, x, y, z):
    for i in range(0,4):
        matrix[     i] = matrix[i] * x
        matrix[ 4 + i] = matrix[ 4 + i] * y
        matrix[ 8 + i] = matrix[ 8 + i] * z
    return matrix
    
def translateMatrix(matrix, x, y, z):
    for i in range(0,4):
        matrix[12 + i] += matrix[i] * x + matrix[4 + i] * y + matrix[8 + i] * z
    return matrix    
    
    
def vector_length(x, y, z):
    return math.sqrt(x * x + y * y + z * z)

def createRotateMatrix(angleInDegress, x, y, z):
    # ~ print("%s, %s, %s" % (x,y,z))
    matrix = []
    for i in range(0,16):
        matrix.append(0.0)
    matrix[15]= 1.0
    a = math.radians(angleInDegress)
    s = math.sin(a)
    c = math.cos(a)
    if (1.0 == x and 0.0 == y and 0.0 == z):
        matrix[5] = c   
        matrix[10]= c
        matrix[6] = s   
        matrix[9] = -s
        matrix[1] = 0.0   
        matrix[2] = 0.0
        matrix[4] = 0.0   
        matrix[8] = 0.0
        matrix[0] = 1.0
    elif (0.0 == x and 1.0 == y and 0.0 == z):
        matrix[0] = c   
        matrix[10]= c
        matrix[8] = s   
        matrix[2] = -s
        matrix[1] = 0.0   
        matrix[4] = 0.0
        matrix[6] = 0.0   
        matrix[9] = 0.0
        matrix[5] = 1.0
    elif (0.0 == x and 0.0 == y and 1.0 == z):
        matrix[0] = c   
        matrix[5] = c
        matrix[1] = s   
        matrix[4] = -s
        matrix[2] = 0.0   
        matrix[6] = 0.0
        matrix[8] = 0.0   
        matrix[9] = 0.0
        matrix[10]= 1.0
    else:
        rotate_vector_length = vector_length(x, y, z)
        if (1.0 != rotate_vector_length):
            recipLen = 1.0 / rotate_vector_length
            x *= recipLen
            y *= recipLen
            z *= recipLen
        nc = 1.0 - c
        xy = x * y
        yz = y * z
        zx = z * x
        xs = x * s
        ys = y * s
        zs = z * s
        matrix[ 0] = x*x*nc +  c
        matrix[ 4] =  xy*nc - zs
        matrix[ 8] =  zx*nc + ys
        matrix[ 1] =  xy*nc + zs
        matrix[ 5] = y*y*nc +  c
        matrix[ 9] =  yz*nc - xs
        matrix[ 2] =  zx*nc - ys
        matrix[ 6] =  yz*nc + xs
        matrix[10] = z*z*nc +  c
    return matrix
    
def rotateMatrix(matrix, a, x, y, z):
        rot4x4 = matrixfloatarray_to_Matrix4x4(createRotateMatrix(a, x, y, z))
        matrix4x4 = matrixfloatarray_to_Matrix4x4(matrix)
        return Matrix4x4_to_matrixfloatarray(rot4x4 * matrix4x4)
        
def read_package_name(projdirpath):
#    from xml.dom import minidom
#
#    # parse an xml file by name
#    mydoc = minidom.parse(projdirpath+'AndroidManifest.xml')
#
#    manifest = mydoc.getElementsByTagName('manifest')[0]
#    return manifest.attributes['package'].value
     file = open(projdirpath+"..\\..\\namespace.txt")
     fileContent = file.read()
     return fileContent


def get_alapfile_es_dirpath(projdirpath, java_file_name, package): 
    file = open(os.path.dirname(os.path.realpath(__file__))+"\\..\\objectsnames.temp")
    ido = strftime("%Y.%m.%d %H:%M:%S", localtime())
    fileContent = file.read()
    fileContent = fileContent.replace("IDO", ido)
#    fileContent = fileContent.replace("NEV", filenev)
    dirpath = projdirpath+"java\\"+(package.replace(".", "\\"))+"\\"
    fileContent = fileContent.replace("PACKAGE", package, 1)
    fileContent = fileContent.replace("NAME", java_file_name, 1)
#    file.close()
    return (fileContent , dirpath)        
    
def teszt():
    m = createIdentityMatrix()
    print("identity matrix\n%s" % matrixfloatarray_to_string(m))

    m2 = translateMatrix(m, 2.2, 1.2, 2.0)
    print("translateMatrix(matrix, 2.2, 1.2, 2.0)\n%s" % matrixfloatarray_to_string(m2))

    m3 = rotateMatrix(m, 90.0, 0.0, 1.0, 0.0)
    print("rotateMatrix(matrix, 90.0, 0.0, 1.0, 0.0)\n%s" % matrixfloatarray_to_string(m3))

