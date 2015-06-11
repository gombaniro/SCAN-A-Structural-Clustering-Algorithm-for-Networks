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
    
def similarity(G,v,u):
    """Compute similarity between pairwise vertices"""
    v_set = set(G.neighbors(v))
    u_set = set(G.neighbors(u))
    inter = v_set.intersection(u_set)
    if inter == 0:
        return 0
    #need to account for vertex itself, add 2(1 for each vertex)
    sim = (len(inter) + 2)/(math.sqrt((len(v_set) + 1 )*(len(u_set) + 1)))
    return sim
def neighborhood(G,v,eps):
    """Find neighborhood of v vertex"""
    eps_neighbors =[]
    v_list = G.neighbors(v)
    for u in v_list:
        print(similarity(G,u,v),u,v)
        if(similarity(G,u,v)) > eps:
            eps_neighbors.append(u)
    return eps_neighbors
    
class PregelScanVertex(Vertex):
    
    def update(self):
          if self.superstep < 30:
              
              for v,m in self.incoming_messages:
                  if m is not None and self.value == None:
                      self.value = m

                  """avoid labeling oscillation by id order """
                  if self.value is not None and v.id > self.id:
                      self.value = m

              if None not in [v.value for v in self.neighbors]:
                  self.active = False
              else:
                  self.outgoing_messages = []
                  """label propagation within neighborhood"""
                  for v in neighborhood(G,self,eps):
                      self.outgoing_messages.append((v,self.value))             
                         
          else:
              self.active = False

if __name__ == "__main__":
    main()
