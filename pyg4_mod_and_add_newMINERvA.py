#!/usr/bin/env python3

# XXX fix vertical offset (move planes up a bit)

import pyg4ometry

def add_sens_to_file(inFile, outFile):

    r1 = pyg4ometry.gdml.Reader(inFile)
    reg1 = r1.getRegistry()

    print("Looping over volumes")
    for volname, volume in reg1.logicalVolumeDict.items():
        aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
        volume .addAuxiliaryInfo(aux_tag)

    # gdml output
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg1)
    w.write(outFile)
        
def merge_files(inFileArC, inFileMin, outFile):
    
    r1 = pyg4ometry.gdml.Reader(inFileArC)
    reg1 = r1.getRegistry()
    
    r2 = pyg4ometry.gdml.Reader(inFileMin)
    reg2 = r2.getRegistry()
    
    ## Want to loop over the logical volumes, and add an auxiliary field to them
    print("Looping over ArC volumes")
    for volname, volume in reg1.logicalVolumeDict.items():
        if volname == 'volLArActive':
            aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
            volume .addAuxiliaryInfo(aux_tag)

    print("Looping over MINERvA volumes")
    for volname, volume in reg2.logicalVolumeDict.items():
        if "AssemblyVolume" in str(type(volume)): continue
        if "Fiber" in volname: continue
        aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
        volume .addAuxiliaryInfo(aux_tag)

    print("Merging volumes")
    lv = reg2.logicalVolumeDict["MINERvA_components"]
    
    # create physical volume with placement
    # see geonotes.txt
    pv = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,430,-6548.65], lv, "MINERvA", reg1.logicalVolumeDict["volMinosNDHall"], reg1)
    
    reg1.addVolumeRecursive(pv)
    
    # gdml output
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg1)
    w.write(outFile)

if __name__ == "__main__":

    inFileArC = "input/arc2x2.gdml"
    inFileMin = "input/minerva_hacked.gdml"
    outFile   = "output/Merged2x2newMINERvA.gdml"
    merge_files(inFileArC, inFileMin, outFile)
