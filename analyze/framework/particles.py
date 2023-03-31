class lepton_obj:
   def __init__(self, pt, eta, phi, pdgId, hasTauAnc):
     self.pt = pt
     self.eta = eta
     self.phi = phi
     self.pdgId    = pdgId
     self.hasTauAnc = hasTauAnc
     return

class jet_obj:
   def __init__(self, pt, eta, phi, partonFlavour, hadronFlavor):
     self.pt = pt
     self.eta = eta
     self.phi = phi     
     self.partonFlavour = partonFlavour
     self.hadronFlavour = hadronFlavor
     return
