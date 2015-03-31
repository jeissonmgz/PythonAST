class Elements(object):
        def insert(self, data,idElement,idSuprasystem):
                self.data=data
                self.idElement=idElement
                self.idSuprasystem=idSuprasystem

class Systems(object):
	elements=[]
	def existSuprasystemById(self,idSuprasystem):
		for element in self.elements:
			if element.idElement==idSuprasystem:
				return True
		return False
        def searchById(self,idElement):
                index=0
                while index < len(self.elements):
                        if self.elements[index].idElement==idElement:
                                return index
                        index += 1
                return -1
        def insert(self,data,idElement,idSuprasystem):
                if (not self.existSuprasystemById(idSuprasystem) and len(self.elements)!=0) or self.searchById(idElement)!=-1:
                        return False
                else:
			self.elements.append(Elements())
	                self.elements[len(self.elements)-1].insert(data,idElement,idSuprasystem)
                return True
        def getSubsystemsById(self,idElement):
		subsystems=[]
                for element in self.elements:
                        if element.idSuprasystem==idElement:
                                subsystems.append(element)
                return subsystems
        def getAllSubsystemsById(self,idElement):
		subsystems=[]
                for element in self.elements:
                        if element.idSuprasystem==idElement:
				subsystems=self.getAllSubsystemsById(element.idElement)+subsystems
				subsystems.append(element)
                return subsystems
        def getSuprasystemById(self,idElement):
		index=self.searchById(idElement)
		if index==-1 :
			return -1
		elif self.elements[index].idSuprasystem is None:
			return None
		return self.elements[index].idSuprasystem
        def getLevelById(self,idElement):
		level=0
		idElement=self.getSuprasystemById(idElement)
		if idElement==-1:
			return None
		while not (idElement is None):
			idElement=self.getSuprasystemById(idElement)
			level+=1
                return level
