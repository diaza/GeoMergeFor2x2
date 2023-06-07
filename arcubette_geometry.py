from ROOT import TGeoManager, TGeoMaterial, TGeoElement, TGeoMixture, TGeoVolumeAssembly, TGeoMedium, TGeoVolume, TGeoBBox, TGeoCompositeShape
from array import array

## Make a very basic detector based around 30x30x60 cm box of LAr
## G10 bucket structure around it (6mm thick)
## Leave a ~few mm argon gap
## Double walled vacuum-insulated cryostat (aluminium? Steel?)
## Surround with air

def arcubette_maker():

    ## Define a manager to keep everything in
    manager = TGeoManager("world", "arcubette")

    ## Define basic elements
    vacuum    = TGeoMaterial("vacuum",0,0,0)
    hydrogen  = TGeoElement("H", "hydrogen", 1, 1.00794)
    boron     = TGeoElement("B", "boron", 5, 10.811)
    carbon    = TGeoElement("C", "carbon", 6, 12.0107)
    nitrogen  = TGeoElement("N", "nitrogen", 7, 14.0671) 
    oxygen    = TGeoElement("O", "oxygen", 8, 15.999)
    sodium    = TGeoElement("Na", "sodium", 11, 22.99)
    aluminum  = TGeoElement("Al", "aluminum", 13, 26.9815)
    silicon   = TGeoElement("Si", "silicon", 14, 28.0855)
    argon     = TGeoElement("Ar", "argon", 18, 39.948)
    potassium = TGeoElement("K", "potassium", 19, 39.0983)
    titanium  = TGeoElement("Ti", "titanium", 22, 47.867)
    chromium  = TGeoElement("Cr", "chromium", 24, 51.9961)
    iron      = TGeoElement("Fe", "iron", 26, 55.845)
    nickel    = TGeoElement("Ni", "nickel", 28, 58.6934)
    zinc      = TGeoElement("Zn64", "zinc", 30, 63.93)

    ## Need to get the density correct for LAr 1.3954 g cm^-3
    lar       = TGeoMaterial("lar", argon, 1.3954)

    ## Materials I need:
    ## - Steel
    ## - Aluminium (maybe)
    ## - G10 (ish)
    ## - LAr
    ## - Air

    ## This is the type of steel used in the MINERvA HCal
    steel = TGeoMixture("steel", 4, 7.93)
    steel .AddElement(iron, 0.7298)
    steel .AddElement(chromium, 0.1792)
    steel .AddElement(nickel, 0.09)
    steel .AddElement(carbon, 0.001)

    ## G10 is complex, epoxy and glass mixture
    glass = TGeoMixture("glass", 8, 2.7)
    glass .AddElement(silicon, 0.2743)
    glass .AddElement(boron, 0.0166)
    glass .AddElement(aluminum, 0.0207)
    glass .AddElement(sodium, 0.0449)
    glass .AddElement(potassium, 0.0821)
    glass .AddElement(zinc, 0.0882)
    glass .AddElement(titanium, 0.0292)
    glass .AddElement(oxygen, 0.444)
    
    epoxy = TGeoMixture("epoxy", 3, 1.25)
    epoxy .AddElement(carbon, 6)
    epoxy .AddElement(hydrogen, 6)
    epoxy .AddElement(oxygen, 1)
    
    g10   = TGeoMixture("g10", 2, 1.85)
    g10   .AddElement(epoxy, 0.206)
    g10   .AddElement(glass, 0.794)

    ## Air
    air   = TGeoMixture("air", 3, 0.001225)
    air   .AddElement(nitrogen, 0.781154)
    air   .AddElement(oxygen, 0.209476)
    air   .AddElement(argon, 0.00934)
    
    ## Media
    vacuum_med = TGeoMedium("vacuum_med", 0, vacuum)
    steel_med  = TGeoMedium("steel_med", 1, steel)
    lar_med    = TGeoMedium("lar_med", 2, lar)
    air_med    = TGeoMedium("air_med", 3, air)
    g10_med    = TGeoMedium("g10_med", 4, g10)
    
    top_vol = manager.MakeBox("top", air_med, 500, 500, 500)
    manager.SetTopVolume(top_vol)
    manager.SetTopVisible(0)

    ## Make a top level assembly volume
    arcubette = TGeoVolumeAssembly("arcubette_assembly")
    top_vol   .AddNode(arcubette, 1)

    ## Detector dimensions that can be modified (all cm)
    tile_z           = 31.5 ## The two dimensions of the larpix tile
    tile_y           = 31.5 
    drift            = 31.5 ## The drift length
    lar_pad          = 1    ## Padding around the 
    cryo_skin_width  = 0.5
    cryo_gap_width   = 0.5
    g10_width        = 0.6
    
    ## Make the cryostat skin
    ## (Everything is *0.5 because ROOT expects the half widths)
    cryo_outer_outer = TGeoBBox("cryo_outer_outer", \
                                0.5*(drift + 2*(lar_pad+g10_width + 2*cryo_skin_width + cryo_gap_width)), \
                                0.5*(tile_y + 2*(lar_pad+g10_width + 2*cryo_skin_width + cryo_gap_width)), \
                                0.5*(2*tile_z + 2*(lar_pad+g10_width + 2*cryo_skin_width + cryo_gap_width)))
    cryo_outer_inner = TGeoBBox("cryo_outer_inner", \
                                0.5*(drift + 2*(lar_pad+g10_width + cryo_skin_width + cryo_gap_width)), \
                                0.5*(tile_y + 2*(lar_pad+g10_width + cryo_skin_width + cryo_gap_width)), \
                                0.5*(2*tile_z + 2*(lar_pad+g10_width + cryo_skin_width + cryo_gap_width)))
    cryo_inner_outer = TGeoBBox("cryo_inner_outer", \
                                0.5*(drift + 2*(lar_pad+g10_width + cryo_skin_width)), \
                                0.5*(tile_y + 2*(lar_pad+g10_width + cryo_skin_width)), \
                                0.5*(2*tile_z + 2*(lar_pad+g10_width + cryo_skin_width)))
    cryo_inner_inner = TGeoBBox("cryo_inner_inner", \
                                0.5*(drift + 2*(lar_pad+g10_width)), \
                                0.5*(tile_y + 2*(lar_pad+g10_width)), \
                                0.5*(2*tile_z + 2*(lar_pad+g10_width)))

    cryo_outer_shp   = TGeoCompositeShape("cryo_outer_shp", "cryo_outer_outer - cryo_outer_inner")
    cryo_gap_shp     = TGeoCompositeShape("cryo_gap_shp", "cryo_outer_inner - cryo_inner_outer")
    cryo_inner_shp   = TGeoCompositeShape("cryo_inner_shp", "cryo_inner_outer - cryo_inner_inner")
    
    cryo_outer_vol   = TGeoVolume("cryo_outer_vol", cryo_outer_shp, steel_med)
    cryo_gap_vol     = TGeoVolume("cryo_gap_vol", cryo_gap_shp, vacuum_med)
    cryo_inner_vol   = TGeoVolume("cryo_inner_vol", cryo_inner_shp, steel_med)

    ## The cryostat belongs to the cubette assembly volume, but doesn't nest the bath
    cryostat         = TGeoVolumeAssembly("cryostat")
    cryostat         .AddNode(cryo_outer_vol, 1)
    cryostat         .AddNode(cryo_gap_vol, 2)
    cryostat         .AddNode(cryo_inner_vol, 3)
    
    ## Note that lar_bath has the same dimensons as cryo_inner_inner
    lar_bath         = TGeoVolume("lar_bath", cryo_inner_inner, lar_med)

    ## Now make the G10 box that actually forms the TPC
    ## This really should be separated into anode, cathode and other... but oh well
    ## Also, the LArPix tiles probably need a supporting plane, but again... a detail
    g10_box_outer     = TGeoBBox("g10_box_outer", \
                                 0.5*(drift + 2*g10_width),\
                                 0.5*(tile_y + 2*g10_width), \
                                 0.5*(2*tile_z + 2*g10_width))
    g10_box_inner     = TGeoBBox("g10_box_inner", \
                                 0.5*drift, 0.5*tile_y, 0.5*(2*tile_z))

    g10_box_shp       = TGeoCompositeShape("g10_box_shp", "g10_box_outer - g10_box_inner")
    g10_box_vol       = TGeoVolume("g10_box_vol", g10_box_shp, g10_med)
    
    ## Separate the LAr active volume for later convenience...
    lar_active        = TGeoVolume("lar_active", g10_box_inner, lar_med)

    ## Orient objects within the cryostat:
    lar_bath  .AddNode(g10_box_vol, 1)
    lar_bath  .AddNode(lar_active, 2)
    
    ## Add the high level volumes to the overall detector assembly volume
    arcubette .AddNode(cryostat, 1)
    arcubette .AddNode(lar_bath, 2)

    outFileName = "arcubette.gdml"
    manager .Export(outFileName)
    
if __name__ == '__main__':

    arcubette_maker()
    
