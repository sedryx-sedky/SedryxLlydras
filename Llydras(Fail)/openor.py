import sqlalchemy as sql
from pathlib import Path
from treelib import Tree
import sys

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

FOLDER_ICON = '📁'
FILE_ICON = '📄'

def name(path):
    if path.is_dir():
        icon = FOLDER_ICON
    elif path.is_file():
        icon = FILE_ICON
    else:
        icon = '?'
        
    return f'{icon} {path.name}'
    
def create_struct(Dir, depth = 1, current_depth = 0, hidden = False, func = None):
    if Dir.is_file():
        return name(Dir)
    elif depth <= current_depth:
        return name(Dir)
    else:
        children = [
            create_struct(p, depth, current_depth + 1,
                          hidden = hidden, func = func)
            
            for p in Dir.iterdir()
            if (hidden or not p.name.startswith('.')) and
            (p.is_dir() or func is None or func(p))
            ]
        return [name(Dir), *children]

def create_tree(struct, parent = ''):
    tree = Tree()
    folder_name = struct[0]
    root = f'{parent}/{folder_name}'
    children = struct[1:]
    tree.create_node(folder_name, root)
    for child in children:
        if isinstance(child, list):
            sub = create_tree(child, parent = root)
            tree.paste(root, sub)
        else:
            tree.create_node(child, parent = root)
    return tree

def show_directory(Dir, depth = 3, hidden = False, func = None):
    struct = create_struct(Dir, depth, hidden = hidden, func = func)
    directory = create_tree(struct)
    directory.show()
    return directory

def show(depth = 3, hidden = False, func = None):
    folder['hidden'] = hidden
    folder['depth'] = depth
    p = folder['path']
    return show_directory(p, depth, hidden, func) 

def write(Dir, depth = 3, hidden = False, func = None):
    directory = show_directory(Dir, depth = depth, hidden = hidden, func = func)
    tree = str(directory)
    txt = Dir / 'project_structure.txt'
    with open(txt, 'w') as file:
        file.write(tree)

def directory(depth = 3, hidden = False):
    struct = create_struct(folder['path'], depth, hidden = hidden, func = lambda p: False)
    q = create_tree(struct)
    i = -1
    for n in q.expand_tree():
        i += 1
        if i == 0: continue
        q[n].tag = f'[{i}] {q[n].tag}'
    q.show()
    

def count(path):
    f = d = 0
    for p in path.iterdir():
        if p.name.startswith('.'): continue
        if p.is_file():
            f += 1
        elif p.is_dir():
            d += 1
    return (d, f)

def _new_directory(path):
    folder['path'] = path
    print(f'Current directory {path.name}')
    d, f = count(path)
    print(f'{d}x{FOLDER_ICON}, {f}x{FILE_ICON}')

def parent():
    p = folder['path'].parent
    _new_directory(p)

def re(path, depth = 1, current_depth = 1):
    hidden = folder['hidden']
    K = []
    if folder['depth'] < current_depth:
        return K
        
    sub_dir = [p for p in path.iterdir()
               if p.is_dir() and
                   (hidden or not p.name.startswith('.'))
              ]
    sub_dir.sort(key = lambda p: p.name)
    for dir_ in sub_dir:
        K.append(dir_)
        K.extend(re(dir_, depth, current_depth + 1))
    return K

def enter(i):
    #_new_directory(m[0])
    k = re(folder['path'])
    _new_directory(k[i - 1])

def file_browser(cmd):
    Cmds = cmd.split(' ')
    command = Cmds[0]

    if command == 'show':
        pass
    elif command == 'parent':
        pass
    elif command == 'enter':
        pass

folder = {'path': Path.cwd(), 'hidden': False, 'depth': 3}
while True:
    Name = input('Database name> ')
    path = Path(Name)
    if Name.startswith('>'):
        eval(Name[1:])
        continue
    if not path.is_file():
        print('No such file could be found.')
        sys.exit()