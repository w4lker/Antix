from urllibs import path_list

class tree():
    def __init__(self):
        self.tree  = []
    
    def append(self,url):
        path = path_list(url)
        for p in path:
            if p not in self.tree:
                self.tree.append(str(p))
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
    
    
    