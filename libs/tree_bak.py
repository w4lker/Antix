from collections import defaultdict
import json
import urlparse
import urllibs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def tree():
    return defaultdict(tree)

def path_tree(tree,domain,**kwargs):
    split_result = urlparse.urlsplit(kwargs['url'])
    if domain != split_result.netloc or split_result.path == u'' or split_result.path == u'/':
        return tree
    tree = tree_append(tree,[split_result.netloc],{})
    path = split_result.path.split('/')
    path.pop(0)
    path[-1] = str(path[-1]) + split_result.query
    depth = len(path)
    
    tree = tree_append(tree,path,kwargs)
    return tree

def tree_append(tree,path,kwargs):       #路径树查找及插入
    if len(path) == 0 :
        return tree
    else:
        if tree.has_key(path[0]) == False:
            if path[0] != '':
                if len(path) == 1:
                    for key,arg in kwargs.items():
                        tree[path[0]][key] = arg
                else:
                    tree[path[0]]

        v = path.pop(0)
        tree_append(tree.get(v),path,kwargs)

        return tree

f = open('path.txt','w')
def tree_print(depth,tree):       #路径树查找    
    if type(tree) != defaultdict:
        for i in range(depth):
                    print ' '
                    f.write(' ')        
        print tree + '\n'
        f.write(tree + '\n')
        return
    if len(tree.items()) == 0:
        print '\n'
        return
    
    for k,v in tree.items():
        for i in range(depth):
            print ' '
            f.write(' ')           
        print k + '\n'
        f.write(k + '\n')
        tree_print(depth+1,v)

def tree_json(tree):       #路径树查找
    
    if type(tree) != defaultdict:
        for i in range(depth):
            print ' '
            f.write(' ')
        print tree + '\n'
        f.write(tree + '\n')
        return
    if len(tree.items()) == 0:
        print '\n'
        return
    
    for k,v in tree.items():
        for i in range(depth):
            print ' '
            f.write(' ')           
        print k + '\n'
        f.write(k + '\n')
        tree_print(depth+1,v)
#def tree_append(tree,url):
    

if __name__ == '__main__':
    #t = [{'text':'a.com','url':'http://www.a.com/'},{'text':'b.com','url':'http://www.b.com/',''},{'text':'c.com','url':'http://www.c.com/'}]
    t = {'a':'L1','b':{'b1':'b'}}
    print json.dumps(path2tree(url_tree,'123.com','http://123.com/a/b/c/ad/b1/c.123.php?a=1&b=2'))
   