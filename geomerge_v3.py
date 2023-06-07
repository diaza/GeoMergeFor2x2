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
        
def merge_files(inFileHall, inFileArC, inFileMin, outFile):
    r0 = pyg4ometry.gdml.Reader(inFileHall)
    reg0 = r0.getRegistry()
    
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
    lvHall = reg0.logicalVolumeDict["volMinosNDHall"]
    lvArC = reg1.logicalVolumeDict["volArgonCubeDetector"]
    lvMin = reg2.logicalVolumeDict["MINERvA_components"]
    
    zoffset = 4000

    pvArC = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,zoffset],
                                             lvArC, "TheArgonCube", lvHall, reg0)
    pvMin = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0, 420, -6548.65 + zoffset],
                                             lvMin, "MINERvA", lvHall, reg0)
    
    reg0.addVolumeRecursive(pvArC)
    reg0.addVolumeRecursive(pvMin)
    
    # gdml output
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg0)
    w.write(outFile)

if __name__ == "__main__":

    # XXX fix rock composition!
    inFileHall = "input/New_2x2_Hall.gdml"
    inFileArC = "input/arc2x2.gdml"
    inFileMin = "input/minerva_hacked.gdml"
    outFile   = "output/Merged2x2MINERvA_v3.gdml"
    merge_files(inFileHall, inFileArC, inFileMin, outFile)
