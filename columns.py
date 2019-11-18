
import vertices
import trusses

class column:
    def __init__(self,_id, _femid):
        self.id=_id
        self.femid=_femid
        
    def define_truss(self,_truss):
        self.truss=_truss        
    