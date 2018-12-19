#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu October 04 11:27:23 2018

@author: kavisha
"""

#CityGML2infraGML converter
#Facilities(buildings) + LandSurface(terrain) + LandElement(landForm)

from lxml import etree
import time
import argparse
import sys
import uuid

dxlinks = {}
def infragml2citygml(inputfile,outputfile):
    tree = etree.parse(inputfile)
    root = tree.getroot()
#    print (root)
    ns="http://www.opengis.net/citygml/2.0"
    ns_gml  = "http://www.opengis.net/gml"
    ns_xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
    ns_xsi="http://www.w3.org/2001/XMLSchema-instance"
    ns_xlink="http://www.w3.org/1999/xlink"
    ns_dem="http://www.opengis.net/citygml/relief/2.0"
    ns_bldg="http://www.opengis.net/citygml/building/2.0"
    ns_core="http://www.opengis.net/citygml/base/2.0"                  
    nsmap = {None : ns,
        'gml' : ns_gml,
        'xAL':ns_xAL,
        'xsi':ns_xsi,
        'xlink':ns_xlink ,
        'dem':ns_dem,
        'bldg':ns_bldg,
        'core':ns_core
    }

    nsinfra="http://www.opengis.net/infragml/core/1.0"
    ns_gml32  = "http://www.opengis.net/gml/3.2"
    ns_xlink2="http://www.w3.org/1999/xlink"
    ns_xsi2="http://www.w3.org/2001/XMLSchema-instance"
    ns_xAL2="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
    ns_lilf = "http://www.opengis.net/infragml/landfeature/1.0"
    ns_gmllr = "http://www.opengis.net/gml/3.3/lr"
    ns_tin = "http://www.opengis.net/gml/3.3/tin"
    ns_li = "http://www.opengis.net/infragml/core/1.0"
    ns_lif = "http://www.opengis.net/infragml/facility/1.0"
    nsmap2 = {None : nsinfra,
        'gml' : ns_gml32,
        'xAL':ns_xAL2,
        'xsi':ns_xsi2,
        'xlink':ns_xlink2,
        'lilf' : ns_lilf,
        'gmllr': ns_gmllr,
        'tin' : ns_tin,
        'li' : ns_li,
        'lif' : ns_lif
    }
        
    citymodel = etree.Element("CityModel", nsmap=nsmap)
    citymodel.attrib['{%s}schemaLocation' %ns_xsi] = "http://www.opengis.net/citygml/relief/2.0 \
    http://schemas.opengis.net/citygml/relief/2.0/relief.xsd \
    http://www.opengis.net/citygml/building/2.0 \
    http://schemas.opengis.net/citygml/building/2.0/building.xsd"
    featureCountDict = {"facility":0, "landSurface": 0, "landElement":0, "surfacesLayer":0}
    
    searchId = []
    d = {}
    for obj in root.getiterator('{%s}feature' % nsinfra):          
        if obj.find('{%s}Facility' %ns_lif) is not None:
            lf = obj.find('{%s}Facility' %ns_lif)
            featureCountDict["facility"] =  featureCountDict["facility"] + 1
            if lf.get('{%s}id' %ns_gml32) is not None:
                lfid = lf.get('{%s}id' %ns_gml32)
            else:
                lfid = "GML_"+str(uuid.uuid4())

            searchId1 = []  
            ftype = lf.find('{%s}type' %ns_lif)
            if ftype.text == "Building":
                for lfps in lf.findall("{%s}part" %ns_lif):
                    partId = lfps.get('{%s}href' %ns_xlink2)
                    
                    if partId.startswith("#"):
                        searchId.append(partId[1:])
                        searchId1.append(partId[1:])
                    else:
                        searchId.append(partId)
                        searchId1.append(partId)
                d[lfid] = searchId1
            
        elif obj.find('{%s}LandSurface' %ns_lilf) is not None:
            ls = obj.find('{%s}LandSurface' %ns_lilf)
            featureCountDict["landSurface"] =  featureCountDict["landSurface"] + 1
            
            cityObjectMember = etree.SubElement(citymodel, "cityObjectMember")
            reliefFeature = etree.SubElement(cityObjectMember, "{%s}ReliefFeature" % ns_dem)
            lod = etree.SubElement(reliefFeature, "{%s}lod" % ns_dem)
            lod.text = "1"
            reliefComponent=etree.SubElement(reliefFeature, "{%s}reliefComponent" % ns_dem)
            TINRelief = etree.SubElement(reliefComponent, "{%s}TINRelief" % ns_dem)
            name = etree.SubElement(TINRelief, "{%s}name" % ns_gml)
            if ls.find('{%s}name' %ns_gml32) is not None: 
                name.text=ls.find('{%s}name' %ns_gml32).text
            else:
                name.text = "Land Infra Dataset"
            lod = etree.SubElement(TINRelief, "{%s}lod" % ns_dem)
            lod.text = "1"
            if ls.get('{%s}id' %ns_gml32) is not None:  
                lsid = ls.get('{%s}id' %ns_gml32)
            else:
                lsid = "GML_"+str(uuid.uuid4())
                
            TINRelief.attrib['{%s}id' % ns_gml]=lsid
#            desc = etree.SubElement(TINRelief, "{%s}description" % ns_gml)                 
#            if ls.find('{%s}description' %ns_gml32) is not None: 
#                desc.text = ls.find('{%s}description' %ns_gml32).text
#            else:
#                desc.text = "Land Infra Dataset of LandSurface (Terrain)"

            tin = etree.SubElement(TINRelief, "{%s}tin" % ns_dem)
            triangulatedSurface = etree.SubElement(tin, "{%s}TriangulatedSurface" % ns_gml)
            if ls.find('.//{%s}TIN' %ns_tin) is not None: 
                lstin = ls.find('.//{%s}TIN' %ns_tin)
                if lstin.get('{%s}id' %ns_gml32):
                    triangulatedSurface.attrib['{%s}id' % ns_gml] = lstin.get('{%s}id' %ns_gml32)
            
            trianglePatches = etree.SubElement(triangulatedSurface, "{%s}trianglePatches" % ns_gml)
            if ls.findall('.//{%s}SimpleTrianglePatch' %ns_tin):
                for t in ls.findall('.//{%s}SimpleTrianglePatch' %ns_tin):
                    triangle = etree.SubElement(trianglePatches,"{%s}Triangle" % ns_gml)
                    exterior = etree.SubElement(triangle,"{%s}exterior" % ns_gml)
                    linearRing = etree.SubElement(exterior,"{%s}LinearRing" % ns_gml)
        
                    if t.find('.//{%s}posList' %ns_gml32) is not None:
                        poslist = etree.SubElement(linearRing, "{%s}posList" %ns_gml)
                        posL = t.find('.//{%s}posList' %ns_gml32)
                        coords = posL.text.split()
                        newcoords = coords
                        poslist.text = "" 
                        for i in range(0, len(newcoords)):
                            poslist.text = poslist.text + " " + str(newcoords[i])
                        poslist.text = poslist.text + " " + str(newcoords[0]) + " " + str(newcoords[1])+ " " + str(newcoords[2])
                    elif t.findall('.//{%s}pos' %ns_gml32):
                        pls = t.findall('.//{%s}pos' %ns_gml32)
                        for posL in pls:
                            gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)
                            coords = posL.text.split()
                            gmlpos.text = ""
                            for i in range(0, len(coords)):
                                gmlpos.text = gmlpos.text + " " + (coords[i])
                            gmlpos.text = gmlpos.text + " " + coords[0] + " " + str(coords[1])+ " " + str(coords[2])        
        elif obj.find('{%s}SurfacesLayer' %ns_lilf) is not None:
            featureCountDict["surfacesLayer"] =  featureCountDict["surfacesLayer"] + 1
            
        elif obj.find('{%s}LandElement' %ns_lilf) is not None:
            featureCountDict["landElement"] =  featureCountDict["landElement"] + 1
            
            ls = obj.find('{%s}LandElement' %ns_lilf)
            if ls.find('{%s}elementType' %ns_lilf) is not None:
                etype = ls.find('{%s}elementType' %ns_lilf)
                if etype.get('{%s}title' %ns_xlink2) == "Terrain" or \
                etype.get('{%s}title' %ns_xlink2) == "Relief" or \
                etype.get('{%s}title' %ns_xlink2) == "landForm":
#                    spatialRepresentation = ls.find('{%s}spatialRepresentation' %ns_li)
                    cityObjectMember = etree.SubElement(citymodel, "cityObjectMember")
                    reliefFeature = etree.SubElement(cityObjectMember, "{%s}ReliefFeature" % ns_dem)
                    lod = etree.SubElement(reliefFeature, "{%s}lod" % ns_dem)
                    lod.text = "1"
                    reliefComponent=etree.SubElement(reliefFeature, "{%s}reliefComponent" % ns_dem)
                    TINRelief = etree.SubElement(reliefComponent, "{%s}TINRelief" % ns_dem)
                    lod = etree.SubElement(TINRelief, "{%s}lod" % ns_dem)
                    lod.text = "1"
                    
                    if ls.get('{%s}id' %ns_gml32) is not None:  
                        lsid = ls.get('{%s}id' %ns_gml32)
                    else:
                        lsid = "GML_"+str(uuid.uuid4())
                
                    TINRelief.attrib['{%s}id' % ns_gml]=lsid
                    name = etree.SubElement(TINRelief, "{%s}name" % ns_gml)
                    desc = etree.SubElement(TINRelief, "{%s}description" % ns_gml) 
            
                    if ls.find('{%s}name' %ns_gml32) is not None: 
                        name.text=ls.find('{%s}name' %ns_gml32).text
                    else:
                        name.text = "Land Infra Dataset"
    
                    if ls.find('{%s}description' %ns_gml32) is not None: 
                        desc.text = ls.find('{%s}description' %ns_gml32).text
                    else:
                        desc.text = "Land Infra Dataset of LandSurface (Terrain)"
 
                    tin = etree.SubElement(TINRelief, "{%s}tin" % ns_dem)
                    triangulatedSurface = etree.SubElement(tin, "{%s}TriangulatedSurface" % ns_gml)
                    if ls.find('.//{%s}TIN' %ns_tin) is not None: 
                        lstin = ls.find('.//{%s}TIN' %ns_tin)
                        if lstin.get('{%s}id' %ns_gml32):
                            triangulatedSurface.attrib['{%s}id' % ns_gml] = lstin.get('{%s}id' %ns_gml32)
            
                    trianglePatches = etree.SubElement(triangulatedSurface, "{%s}trianglePatches" % ns_gml)
                    if ls.findall('.//{%s}SimpleTrianglePatch' %ns_tin):
                        for t in ls.findall('.//{%s}SimpleTrianglePatch' %ns_tin):
                            triangle = etree.SubElement(trianglePatches,"{%s}Triangle" % ns_gml)
                            exterior = etree.SubElement(triangle,"{%s}exterior" % ns_gml)
                            linearRing = etree.SubElement(exterior,"{%s}LinearRing" % ns_gml)
        
                            if t.find('.//{%s}posList' %ns_gml32) is not None:
                                poslist = etree.SubElement(linearRing, "{%s}posList" %ns_gml)
                                posL = t.find('.//{%s}posList' %ns_gml32)
                                coords = posL.text.split()
                                newcoords = coords
                                poslist.text = "" 
                                for i in range(0, len(newcoords)):
                                    poslist.text = poslist.text + " " + str(newcoords[i])
                                poslist.text = poslist.text + " " + str(newcoords[0])
                            elif t.findall('.//{%s}pos' %ns_gml32):
                                pls = t.findall('.//{%s}pos' %ns_gml32)
                                for posL in pls:
                                    gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)
                                    coords = posL.text.split()
                                    gmlpos.text = ""
                                    for i in range(0, len(coords)):
                                        gmlpos.text = gmlpos.text + " " + (coords[i])
                                    gmlpos.text = gmlpos.text + " " + coords[0]
                  
    for fid,val in d.items():
        cityObjectMember = etree.SubElement(citymodel, "cityObjectMember")
        bldg2 = etree.SubElement(cityObjectMember, "{%s}Building" % ns_bldg)
        
        for v in val:
           if root.find('.//lif:Building[@gml:id="{value}"]'.format(value=v),root.nsmap) is not None:
               fbldg = root.find('.//lif:Building[@gml:id="{value}"]'.format(value=v),root.nsmap)
               if fbldg.find('{%s}type' %(ns_lif)) is not None:
                   btype = fbldg.find('{%s}type' %(ns_lif))
                   
                   if btype.get('{%s}title' %ns_xlink2) == "Building":
                       bldg2.attrib['{%s}id' % ns_gml]= v
                       bldg2name = etree.SubElement(bldg2, "{%s}name" % ns_gml)
                       if fbldg.find('{%s}name' %(ns_gml32)) is not None:
                           bldg2name.text = fbldg.find('{%s}name' %(ns_gml32)).text
                       else:
                           bldg2name.text = "InfraGML FacilityPart Building"
                       bsolid = etree.SubElement(bldg2, "{%s}lod1Solid" % ns_bldg)
                       gmlsolid = etree.SubElement(bsolid, "{%s}Solid" % ns_gml)
                       bexterior = etree.SubElement(gmlsolid,"{%s}exterior" % ns_gml)
                       bcs = etree.SubElement(bexterior,"{%s}CompositeSurface" % ns_gml)
                       for sm in fbldg.findall('.//{%s}surfaceMember' %ns_gml32):
                           surfaceMember = etree.SubElement(bcs,"{%s}surfaceMember" % ns_gml)
                           polygon = etree.SubElement(surfaceMember,"{%s}Polygon" % ns_gml)
                           exterior = etree.SubElement(polygon,"{%s}exterior" % ns_gml)
                           linearRing = etree.SubElement(exterior,"{%s}LinearRing" % ns_gml)
                           if sm.find('.//{%s}posList' %ns_gml32) is not None:
                               poslist = etree.SubElement(linearRing, "{%s}posList" %ns_gml)
                               posL = sm.find('.//{%s}posList' %ns_gml32)
                               coords = posL.text.split()
                               newcoords = coords
                               poslist.text = "" 
                               for i in range(0, len(newcoords)):
                                   poslist.text = poslist.text + " " + str(newcoords[i])
                               poslist.text = poslist.text + " " + str(newcoords[0]) + " " + str(newcoords[1])+ " " + str(newcoords[2])
                           elif sm.findall('.//{%s}pos' %ns_gml32):
                               pls = sm.findall('.//{%s}pos' %ns_gml32)
                               coorlist = []
                               for posL in pls:
                                   gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)
                                   coords = posL.text.split()
                                   coorlist.append(coords)
                                   gmlpos.text = ""
                                   for i in range(0, len(coords)):
                                       gmlpos.text = gmlpos.text + " " + (coords[i])
                               gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)       
                               gmlpos.text =  " " + str(coorlist[0][0])+" " + str(coorlist[0][1])+" " + str(coorlist[0][2])
                   elif btype.get('{%s}title' %ns_xlink2) == "BuildingPart":  

                       if fid.startswith("Facility_"):
                           bldg2.attrib['{%s}id' % ns_gml]= fid[9:]
                       else:
                           bldg2.attrib['{%s}id' % ns_gml]= fid
                       consistsOfbp = etree.SubElement(bldg2, "{%s}consistsOfBuildingPart" % ns_bldg)
                       bp = etree.SubElement(consistsOfbp, "{%s}BuildingPart" % ns_bldg)
                       bpname = etree.SubElement(bp, "{%s}name" % ns_gml)
                       bp.attrib['{%s}id' % ns_gml]= v
                       if fbldg.find('{%s}name' %(ns_gml32)) is not None:
                           bpname.text = fbldg.find('{%s}name' %(ns_gml32)).text
                       else:
                           bpname.text = "InfraGML FacilityPart Building"
                       bsolid = etree.SubElement(bp, "{%s}lod1Solid" % ns_bldg)
                       gmlsolid = etree.SubElement(bsolid, "{%s}Solid" % ns_gml)
                       bexterior = etree.SubElement(gmlsolid,"{%s}exterior" % ns_gml)
                       bcs = etree.SubElement(bexterior,"{%s}CompositeSurface" % ns_gml)
                       for sm in fbldg.findall('.//{%s}surfaceMember' %ns_gml32):
                           surfaceMember = etree.SubElement(bcs,"{%s}surfaceMember" % ns_gml)
                           polygon = etree.SubElement(surfaceMember,"{%s}Polygon" % ns_gml)
                           exterior = etree.SubElement(polygon,"{%s}exterior" % ns_gml)
                           linearRing = etree.SubElement(exterior,"{%s}LinearRing" % ns_gml)
                           if sm.find('.//{%s}posList' %ns_gml32) is not None:
                               poslist = etree.SubElement(linearRing, "{%s}posList" %ns_gml)
                               posL = sm.find('.//{%s}posList' %ns_gml32)
                               coords = posL.text.split()
                               newcoords = coords 
                               poslist.text = "" 
                               for i in range(0, len(newcoords)):
                                   poslist.text = poslist.text + " " + str(newcoords[i])
                               poslist.text = poslist.text + " " + str(newcoords[0]) + " " + str(newcoords[1])+ " " + str(newcoords[2])
                           elif sm.findall('.//{%s}pos' %ns_gml32):
                               pls = sm.findall('.//{%s}pos' %ns_gml32)
                               coorlist = []
                               for posL in pls:
                                   gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)
                                   coords = posL.text.split()
                                   coorlist.append(coords)
                                   gmlpos.text = ""
                                   for i in range(0, len(coords)):
                                       gmlpos.text = gmlpos.text + " " + (coords[i])
                               gmlpos = etree.SubElement(linearRing, "{%s}pos" %ns_gml)       
                               gmlpos.text =  " " + str(coorlist[0][0])+" " + str(coorlist[0][1])+" " + str(coorlist[0][2])

        
    print ("# of Facility(s): ", featureCountDict["facility"])
    print ("# of LandSurface(s): ", featureCountDict["landSurface"])
    print ("# of LandElement(s): ", featureCountDict["landElement"])
    print ("# of SurfacesLayer(s): ", featureCountDict["surfacesLayer"])

    
    citygml = etree.tostring(citymodel, pretty_print=True,xml_declaration=True, encoding='UTF-8')
#    print ("\n#-------------CityGML output-------------------#\n")
    wf=open(outputfile,'wb')
#    wf.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    wf.write(citygml)
    wf.close()
    print ("\n******* Conversion completed!! *******")
    print ("Output written to:", outputfile)

#-------------start of program-------------------#

print ("\n****** InfraGML2CityGML Converter *******\n")  
argparser = argparse.ArgumentParser(description='******* InfraGML2CityGML Converter *******')
argparser.add_argument('-i', '--inputFilename', help='InfraGML dataset filename', required=False)
argparser.add_argument('-o', '--outputFilename', help='CityGML dataset filename', required=False)
args = vars(argparser.parse_args())

inputFileName = args['inputFilename']
if inputFileName:
    inputFile = str(inputFileName)
    print ("InfraGML input file: ", inputFile)
else:
    print ("Error: Enter the InfraGML dataset!! ")
    sys.exit()

outputFileName = args['outputFilename']
if outputFileName:
    outputFile = str(outputFileName)
    print ("CityGML output file: ", outputFile)
else:
    print ("Error: Enter the CityGML filename!! ")
    sys.exit()
    
start = time.time()
infragml2citygml(inputFile,outputFile)
end = time.time()
print ("\n Time taken for CityGML generation: ",end - start, " sec")