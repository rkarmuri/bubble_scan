from bubbleScan.domain.scantron import Scantron

class MemRepo:
    def __init__(self,data):
        self.data = data
        
    def list(self):
            return [Scantron.from_dict(i) for i in self.data]