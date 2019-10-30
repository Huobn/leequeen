# -*- coding:utf-8 -*-
# author: Bingnan Huo

import re

from .interface import Cif,Atom
# const regular expression varibles

CELL_LENGTH_A = 'cell_length_a';
CELL_LENGTH_B = 'cell_length_b';
CELL_LENGTH_C = 'cell_length_c';

ALPHA = 'cell_angle_alpha';
BETA = 'cell_angle_beta';
GAMMA = 'cell_angle_gamma';

SPACE_GROUP = 'symmetry_space_group_name';

ATOM_POSITION_STD = "[ ]*[A-Z][a-z]*[0-9]+[ ]+[0-9][.][0-9]+[ ]+[0-9][.][0-9]+";

def _readFileStream(file:str, encoding:str="utf-8")-> "Cif":
    
    # cif structure define
    cif = Cif();
    
    try:
        f = open(file, 'r', encoding=encoding);
        content = f.readline();
        while( content ):
            r = re.split("[ ]+", content);
            i = 0;
            while( i < len(r) ):
                r[i] = r[i].replace("\r", "");
                r[i] = r[i].replace("\n", "");
                i += 1;
            
            if( re.search(CELL_LENGTH_A, content) ):
                cif.a = float(r[-1]);
            elif( re.search(CELL_LENGTH_B, content) ):
                cif.b = float(r[-1]);
            elif( re.search(CELL_LENGTH_C, content) ):
                cif.c = float(r[-1]);
            elif( re.search(ALPHA, content) ):
                cif.alpha = float(r[-1]);
            elif( re.search(BETA, content) ):
                cif.beta = float(r[-1]);
            elif( re.search(GAMMA, content) ):
                cif.gamma = float(r[-1]);
            elif( re.search(SPACE_GROUP, content) ):
                cif.spaceGroup = r[-1];
            elif( re.search(ATOM_POSITION_STD, content) ):
                rf = [];
                for i in r:
                    if( i ):
                        rf.append(i);
                # atom structure define
                '''
                atom = {
                  "id":rf[0],
                  "component":rf[-1],
                  "x":float(rf[2]),
                  "y":float(rf[3]),
                  "z":float(rf[4])
                };
                '''
                atom = Atom();
                atom.x = float(rf[2]);
                atom.y = float(rf[3]);
                atom.z = float(rf[4]);
                atom.component = rf[-1];
                atom.id = rf[0];
                cif.atoms.append(atom);
                
                
            
            content = f.readline();
    except:
        raise Exception("file open error. please check the file's path and the file's format");
    finally:
        f.close();
    return cif;

def _readFileOnce(file:str, encoding:str = "utf-8"):
    # TODO
    pass;

def cifp(file:str, encoding:str="utf-8", openType:str="stream") -> "dict":
    
    if openType == "stream":
        return _readFileStream(file, encoding);
    elif openType == "once":
        return _readFileOnce(file, encoding);
    else:
        raise Exception("parameter openType must be 'stream' or 'once'");
        
