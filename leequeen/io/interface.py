# -*- coding:utf-8 -*-
# author : Bingnan Huo
# version : 1.0.0

from math import cos,sin
from numpy import array, zeros, matrix

class File:
    
    def __init__(self):
        self.path = "";
        self.encoding = "";
        

class Atom:
    
    def __init__(self):
        self.x = None;
        self.y = None;
        self.z = None;
        self.component = None;
        self.id = None;
        
    def smell(self) -> "bool":
        flag = True;
        if( self.x and self.y and self.z ):
            pass;
        else:
            flag = False;
        return flag;
    

class Cif:
    
    def __init__(self):
        self.a = None;
        self.b = None;
        self.c = None;
        self.alpha = None;
        self.beta = None;
        self.gamma = None;
        self.spaceGroup = None;
        self.atoms = [];
        
    def smell(self) -> "bool":
        flag = True;
        if(self.a and self.b and self.c
           and self.alpha and self.beta and self.gamma):
            pass;
        else:
            flag = False;
        return flag;
    
    def fractionalMatrix(self) -> "matrix":
        
        c = len(self.atoms);
        
        m = zeros((3,c));
        
        i = 0;
        while( i < c ):
            atom = self.atoms[i];
            a = array([atom.x, atom.y, atom.z]);
            m[:, i] = a;
            i+=1;
        m = matrix(m);
        return m;
    
    def cellMatrix(self) -> "matrix":
        PI = 3.1415926;
        if self.smell():
            # 统一单位，将角度转换为弧度制
            alpha = self.alpha / 180 * PI;
            beta = self.beta / 180 * PI;
            gamma = self.gamma / 180 * PI;
            # 创建晶胞向量集
            cellVectors = zeros((3,3));
    
            # 计算晶胞向量坐标
            z1 = self.a * cos(beta);
            z2 = self.b * cos(alpha);
            z3 = self.c;
    
            # y1 = (cos(gamma) - cos(alpha) * cos(beta)) / (b * sin(alpha))
            y1 = self.a * (cos(gamma) - cos(alpha) * cos(beta)) / sin(alpha);
            y2 = self.b * sin(alpha);
            y3 = 0;
    
            x1 = ((self.a ** 2) * (sin(beta) ** 2) - (y1 ** 2)) ** 0.5;
            x2 = 0;
            x3 = 0;
            
            cellVectors[:,0] = array([x1, y1, z1]);
            cellVectors[:,1] = array([x2, y2, z2]);
            cellVectors[:,2] = array([x3, y3, z3]);
            
            cellVectors = matrix(cellVectors);
            return cellVectors;
        else:
            raise Exception("bad file input");
            
      