"""scan.py illustrates how to use the pregel.py library and test
    that model works
"""
from pregel import Vertex,Pregel
import threading

num_workers =  2
num_vertices =  14
threadLock = threading.Lock()
def main():
    edges = [[6,4,5,1],[0,5,2],[1,3,5],[2,6,4,5],[3,6,0,5],
                [2,3,4,0,1],[3,4,0,10,11,7],[6,11,12,8],[7,12,9],
                [8,12,13,10],[6,9,11,12],[6,7,10,12],[11,10,7,8,9],
                [9]]

    
    
    vertice_ids  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
    communities = []
    for i in range(14):
        v = ScanVertex(i,None,edges[i])
        communities.append(v)

    for i in range(14):
        neighbors = []
        for j in edges[i]:
            neighbors.append(communities[j])
        communities[i].neighbors = neighbors
            

    #initialize
    communities[12].value = 'A'
    communities[5].value = 'B'
    print(id(communities))
    '''for v in vertices:
        print(v.id,v.value)'''
    print('running scan pregel')
    p = Pregel(communities,num_workers)
    p.run()
    print(id(communities))
    for v in communities:
        print(v.id,v.value)
    



class ScanVertex(Vertex):
    
    def update(self):
          if self.superstep < 2:
            
              for v,m in self.incoming_messages:
                  if m is not None:
                      self.value = m
                          
              self.outgoing_messages = []
              for v in self.neighbors:
                 self.outgoing_messages.append((v,self.value))
                 
                 
                         
          else:
              self.active = False

if __name__ == "__main__":
    main()
