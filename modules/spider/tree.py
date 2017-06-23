import urlparse
def path_list(url):
    r = urlparse.urlsplit(url.encode('utf-8'))
    path = r.path.split('/')
    tree = []
    
    for i in range(len(path)):
        node = {}
        if i == 0:
            u = r.scheme + '://' + r.netloc + '/' + path[i]
            node['id'] = u
            node['text'] = u
            node['parent'] = '#'
        elif i == len(path)-1:
            if path[i] == '':
                continue
            node['parent'] = u
            u = u.rstrip('/') + '/' + path[i]
            if r.query != '':
                u = u + '?' + r.query
                node['text'] = path[i] + '?' + r.query
            else:
                node['text'] = path[i]
            node['id'] = u
            
        else:
            node['parent'] = u
            u = u.rstrip('/') + '/' + path[i] + '/'
            node['id'] = u
            node['text'] = path[i]         
        tree.append(node)
    
    return tree

class tree():
    def __init__(self):
        self.tree  = []
    
    def append(self,url):
        path = path_list(url)
        for p in path:
            if p not in self.tree:
                self.tree.append(p)
    #def append(self,url):
        #start = self.find(url)
        #if start == -1:
            #return
        #path = path_list(url)
        #self.tree.extend(path[start:])
    
    #def find(self,url):
        #exist = 0
        #path = path_list(url)
        #for t in self.tree:
            #for i in range(len(path)):
                #if t == path[i]:
                    #if i == 0:
                        #exist = 1
                        #continue
                    #elif i != len(path) -1:
                        #return i + 1
                    #else:
                        #return -1
        #return exist
    
    def set(self,url,**kwargs):
        for t in self.tree:
            if t['id'] == url:
                for k,v in kwargs.items():
                    t[k] = v
                return True
        return False
    
    def printj(self):
        f = open('tree.json','w')
        f.write(str(self.tree))
        f.close()
    
    
    