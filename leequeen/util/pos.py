# -*- coding:utf-8 -*-
# author : Bingnan Huo

from math import cos,sin
from numpy import array,zeros,matrix,cross
from numpy.linalg import norm

# const varible used in this moudle

PI:float = 3.1416926


# function defined

def getCellVectorByCellProperties(a:float, b:float, c:float,
                                  alpha:float, beta:float, gamma:float) -> "matrix":
    
     # 统一单位，将角度转换为弧度制
        alpha = alpha / 180 * PI;
        beta = beta / 180 * PI;
        gamma = gamma / 180 * PI;
        # 创建晶胞向量集
        cellVectors = zeros((3,3));

        # 计算晶胞向量坐标
        z1 = a * cos(beta);
        z2 = b * cos(alpha);
        z3 = c;

        # y1 = (cos(gamma) - cos(alpha) * cos(beta)) / (b * sin(alpha))
        y1 = a * (cos(gamma) - cos(alpha) * cos(beta)) / sin(alpha);
        y2 = b * sin(alpha);
        y3 = 0;

        x1 = ((a ** 2) * (sin(beta) ** 2) - (y1 ** 2)) ** 0.5;
        x2 = 0;
        x3 = 0;
        
        cellVectors[:,0] = array([x1, y1, z1]);
        cellVectors[:,1] = array([x2, y2, z2]);
        cellVectors[:,2] = array([x3, y3, z3]);
        
        cellVectors = matrix(cellVectors);
        return cellVectors;
    
def baseTransform(b1, b2) -> "matrix":
    
    if( b1.shape != b2.shape ):
        raise Exception("dimension error");
    else:
        return b1 ** -1 * b2;
    
def containerBaseFind(m, b:matrix=None, hl=0.05) -> "matrix":
    if( m.shape  and len(m) >= 2  and m.shape[0] == 3 
       and m.shape[1] >= 4):
        
        obase = matrix([1,0,0,0,1,0,0,0,1]).reshape((3,3));
        limit = 1000000;
        cbase = None;
        
        if( b and b.shape == (3,3)):
            obase = b;
        
        # axis
        a1 = m[:, 0];
        a2 = m[:, 1];
        # loop and find high quality base
        i = 2;
        while( i < m.shape[0]):
            a3 = m[:, i];
            
            b1 = a3 - a1;
            b2 = a3 - a2;
            b3 = cross(b1.T, b2.T).T;
            if(  not b3.any() ):
                i += 1;
                break;
            # create a new base;
            nbase = matrix(zeros((3,3)));
            nbase[:, 0] = b1;
            nbase[:, 1] = b2;
            nbase[:, 2] = b3;
            
            #t = baseTransform(obase, nbase);
            t = nbase ** -1 * obase;
            # coordinate transform
            nm = t * m;
            
            # coordinate analyse
            ref = nm[2,:] * norm(b3);
            lref = (ref >= hl);
            pl = lref.sum() / ref.shape[1];
            
            cref = pl * ref.std();
            if( cref <= limit ):
                limit = cref;
                cbase = nbase;
            i += 1;
        print(limit);
        return cbase;
            
    else:
        raise Exception("dimension error");
    