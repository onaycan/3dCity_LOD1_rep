import buildings



class buildingblock:
    def __init__(self,_id):
        self.id=_id
        self.buildings=[]

    def append_building(self,_building):
        self.buildings.append(_building)