#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu October 04 11:27:23 2018

@author: kavisha
"""

#CityGML2InfraGML converter
#buildings + terrain

from lxml import etree
import time
import argparse
import sys
import uuid

def citygml2infragml(inputfile,outputfile):
    tree = etree.parse(inputfile)
    root = tree.getroot()
    for key in root.nsmap.keys():
        if root.nsmap[key].find('http://www.opengis.net/citygml') != -1:
            if (root.nsmap[key][-3:] == '1.0'):
                citygmlversion = '1.0'
                break
            if (root.nsmap[key][-3:] == '2.0'):
                citygmlversion = '2.0'
                break 
    if citygmlversion == "1.0":
        print ("CityGML v1.0 detected. However, preferred version is 2.0!!")
        ns="http://www.opengis.net/citygml/1.0"
        ns_gml  = "http://www.opengis.net/gml"
        ns_xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
        ns_xsi="http://www.w3.org/2001/XMLSchema-instance"
        ns_xlink="http://www.w3.org/1999/xlink"
        ns_dem="http://www.opengis.net/citygml/relief/1.0"
        ns_bldg="http://www.opengis.net/citygml/building/1.0"
        
        nsmap = {None : ns,
        'gml' : ns_gml,
        'xAL':ns_xAL,
        'xsi':ns_xsi,
        'xlink':ns_xlink ,
        'dem':ns_dem,
        'bldg':ns_bldg       
        }

    elif citygmlversion == "2.0":
        print ("Version: CityGML v2.0")
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

    LandInfraDataset = etree.Element("LandInfraDataset", nsmap=nsmap2)
    LandInfraDataset.attrib['{%s}schemaLocation' %ns_xsi2] = "http://www.opengis.net/infragml/landfeature/1.0 \
    http://schemas.opengis.net/infragml/part1/1.0/land-feature.xsd \
    http://www.opengis.net/infragml/core/1.0 http://schemas.opengis.net/infragml/part0/1.0/core.xsd \
    http://www.opengis.net/infragml/facility/1.0 http://schemas.opengis.net/infragml/part2/1.0/facility.xsd"
    if root.get("{%s}id" % ns_gml) is not None:
        ldid = str(root.get("{%s}id" % ns_gml))
    else:
        ldid = "GML_"+str(uuid.uuid4())
    LandInfraDataset.attrib['{%s}id' % ns_gml32] = ldid
    
    datasetID = etree.SubElement(LandInfraDataset, "{%s}datasetID" % nsinfra)
    ID = etree.SubElement(datasetID, "{%s}ID" % nsinfra)
    identifier = etree.SubElement(ID, "{%s}identifier" % nsinfra)
    identifier.text = ldid
    scope = etree.SubElement(ID, "{%s}scope" % nsinfra)
    scope.text = "OGC LandInfraSWG"
    name = etree.SubElement(LandInfraDataset, "{%s}name" % nsinfra)
    desc = etree.SubElement(LandInfraDataset, "{%s}description" % nsinfra)
    
    if root.find('{%s}name' %ns_gml) is not None: 
        name.text=root.find('{%s}name' %ns_gml).text
    else:
        name.text="Land Infra Dataset"
    
    if root.find('{%s}description' %ns_gml) is not None: 
        desc.text=root.find('{%s}description' %ns_gml).text
    else:
        desc.text="Land Infra Dataset of terrain"
    
    dateTime = etree.SubElement(LandInfraDataset, "{%s}dateTime" % nsinfra)
    dateTime.text = time.strftime("%Y-%m-%dT%H:%M:%S")
    datasetVersion = etree.SubElement(LandInfraDataset, "{%s}datasetVersion" % nsinfra)
    datasetVersion.text = "1.0"
    application = etree.SubElement(LandInfraDataset, "{%s}application" % nsinfra)
    application.text = "Generated using CityGML2InfraGML python utility"
    author = etree.SubElement(LandInfraDataset, "{%s}author" % nsinfra)
    author.text = "3D Geoinformation Group, TU Delft, the Netherlands"
    infraVersion = etree.SubElement(LandInfraDataset, "{%s}infraVersion" % nsinfra)
    infraVersion.text = "1.0"
    language = etree.SubElement(LandInfraDataset, "{%s}language" % nsinfra)
    language.text = "English"
    defaultCRS = etree.SubElement(LandInfraDataset, "{%s}defaultCRS" % nsinfra)
    if root.find('.//{%s}Envelope' %ns_gml) is not None:
        bb = root.find('.//{%s}Envelope' %ns_gml)
        defaultCRS.attrib['{%s}href' % ns_xlink2] = bb.get("srsName")
    else:
       defaultCRS.attrib['{%s}href' % ns_xlink2] = "None"
    
    
    featureCountDict = {"buildingCount": 0, "reliefCount": 0, "tinreliefCount":0, "buildingPartCount":0}
    for obj in root.getiterator('{%s}cityObjectMember'% ns):
        if obj.find('{%s}ReliefFeature' %ns_dem) is not None:
            featureCountDict["reliefCount"] = featureCountDict["reliefCount"] + 1
            relief1 = obj.find('{%s}ReliefFeature' %ns_dem)
            for relief in relief1.findall('.//{%s}TINRelief' %ns_dem):
                featureCountDict["tinreliefCount"] = featureCountDict["tinreliefCount"] + 1
                rfeature = etree.SubElement(LandInfraDataset, "{%s}feature" % nsinfra)
                LandSurface = etree.SubElement(rfeature, "{%s}LandSurface" % ns_lilf)
                name = etree.SubElement(LandSurface, "{%s}name" % ns_gml32)
#                desc = etree.SubElement(LandSurface, "{%s}description" % ns_gml32)
                if relief.find('{%s}name' %ns_gml) is not None:
                    name.text=relief.find('{%s}name' %ns_gml).text
                else:
                    name.text="Land Infra LandSurface Dataset"
                
#                if relief.find('{%s}description' %ns_gml) is not None:
#                    desc.text=relief.find('{%s}description' %ns_gml).text
#                else:
#                    desc.text="Land Infra LandSurface Description"
            
                state = etree.SubElement(LandSurface, "{%s}state" % ns_lilf)
                if relief.find('{%s}terminationDate' %ns) is not None:
                    state.text = "dead"
                else:
                    state.text = "existing"
                 
                landSurfaceID = etree.SubElement(LandSurface, "{%s}landSurfaceID" % ns_lilf)
                ID = etree.SubElement(landSurfaceID, "{%s}ID" % ns_lilf)
                identifier = etree.SubElement(ID, "{%s}identifier" % nsinfra)
                if relief.get("{%s}id" % ns_gml) is not None:
                    identifier.text = relief.get("{%s}id" % ns_gml)
                    LandSurface.attrib['{%s}id' % ns_gml32] = relief.get("{%s}id" % ns_gml)
                else:
                    identifier.text = "GML_"+str(uuid.uuid4())
                    LandSurface.attrib['{%s}id' % ns_gml32] = identifier.text
                scope = etree.SubElement(ID, "{%s}scope" % nsinfra)
                scope.text = "OGC LandInfra SWG" 
            
                spatialRepresentation = etree.SubElement(LandSurface, "{%s}spatialRepresentation" % ns_lilf)
                infratin = etree.SubElement(spatialRepresentation, "{%s}TIN" % ns_tin)
                patches = etree.SubElement(infratin, "{%s}patches" %ns_gml32)
                
                if relief.findall('.//{%s}Triangle' %ns_gml):
                    triangles = relief.findall('.//{%s}Triangle' %ns_gml)
                    for t in triangles:
                        SimpleTrianglePatch = etree.SubElement(patches, "{%s}SimpleTrianglePatch" %ns_tin)                                                   
                        if t.find('.//{%s}posList' %ns_gml) is not None:
                            poslist = etree.SubElement(SimpleTrianglePatch, "{%s}posList" %ns_gml32)
                            posL=t.find('.//{%s}posList' %ns_gml)
                            coords=posL.text.split()
                            newcoords=coords[:-3] 
                            poslist.text = "" 
                            for i in range(0, len(newcoords)):
                                poslist.text = poslist.text + " " + str(newcoords[i])
                        elif t.findall('.//{%s}pos' %ns_gml):
                            pls=t.findall('.//{%s}pos' %ns_gml)
                            for posL in pls:
                                gmlpos = etree.SubElement(SimpleTrianglePatch, "{%s}pos" %ns_gml32)
                                gmlpos.text = ""
                                coords = posL.text.split()
                                for i in range(0, len(coords)):
                                    gmlpos.text = gmlpos.text + " " + str(coords[i])

                material = etree.SubElement(LandSurface, "{%s}material" % ns_lilf)
                material.text = "topsoil"
        if obj.find('{%s}Building' %ns_bldg) is not None:
            featureCountDict["buildingCount"] = featureCountDict["buildingCount"] + 1
            bldg1 = obj.find('{%s}Building' %ns_bldg)
            ffeature = etree.SubElement(LandInfraDataset, "{%s}feature" % nsinfra)
            facility = etree.SubElement(ffeature, "{%s}Facility" % ns_lif)
            if bldg1.get("{%s}id" % ns_gml) is not None:
                fdid1 = str(bldg1.get("{%s}id" % ns_gml))
                fdid = "Facility_"+str(bldg1.get("{%s}id" % ns_gml))
            else:
                fdid1 = str(uuid.uuid4())
                fdid = "Facility_"+ fdid1
            facility.attrib['{%s}id' % ns_gml32] = fdid
            fname = etree.SubElement(facility, "{%s}name" % ns_gml32)
            if bldg1.find('{%s}name' %ns_gml) is not None:
                fname.text=bldg1.find('{%s}name' %ns_gml).text
            else:
                fname.text="Land Infra Facility Dataset"  
            
            facilityID = etree.SubElement(facility, "{%s}facilityID" % ns_lif)
            fID = etree.SubElement(facilityID, "{%s}ID" % ns_lif)
            fidentifier = etree.SubElement(fID, "{%s}identifier" % nsinfra)
            fidentifier.text = fdid 
            fscope = etree.SubElement(fID, "{%s}scope" % nsinfra)
            fscope.text = "OGC LandInfra SWG" 
            ftype = etree.SubElement(facility, "{%s}type" % ns_lif)
            ftype.text = "Building" 
            fstatus = etree.SubElement(facility, "{%s}status" % ns_lif)
            if bldg1.find('{%s}terminationDate' %ns) is not None:
                fstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#dead"
                fstatus.attrib['{%s}title' % ns_xlink] = "dead"
            else:
                fstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#existing"
                fstatus.attrib['{%s}title' % ns_xlink] = "existing"
           
            if bldg1.findall('.//{%s}BuildingPart' %ns_bldg):
                for bp in bldg1.findall('.//{%s}BuildingPart' %ns_bldg):
                    featureCountDict["buildingPartCount"] = featureCountDict["buildingPartCount"] + 1
                    
                    if bp.get("{%s}id" % ns_gml) is not None:
                        bpid = str(bp.get("{%s}id" % ns_gml))
                    else:
                        bpid1 = str(uuid.uuid4())
                        bpid = "#GML_" + bpid1
                    
                    fpart = etree.SubElement(facility, "{%s}part" % ns_lif)
                    fpart.attrib['{%s}href' % ns_xlink] = "#"+bpid
                    
                    if bp.find('{%s}lod1Solid' %ns_bldg) or \
                    bp.find('{%s}lod2Solid' %ns_bldg) is not None:
                        bpfeature = etree.SubElement(LandInfraDataset, "{%s}feature" % nsinfra)
                        bp2 = etree.SubElement(bpfeature, "{%s}Building" % ns_lif)
                        bp2.attrib['{%s}id' % ns_gml32] = bpid
                        
                        bpname = etree.SubElement(bp2, "{%s}name" % ns_gml32)
                        if bp.find('{%s}name' %ns_gml) is not None:
                            bpname.text=bp.find('{%s}name' %ns_gml).text
                        else:
                            bpname.text="Land Infra Facility Dataset"  
            
                        bpspatRep1 = etree.SubElement(bp2, "{%s}spatialRepresentation" % ns_li)
                        bpspatRep2 = etree.SubElement(bpspatRep1, "{%s}SpatialRepresentation" % ns_li)
                        bpgeometry =  etree.SubElement(bpspatRep2, "{%s}geometry" % ns_li)
                        
                        if bp.find('.//{%s}Solid' %ns_gml) is not None:
                            bpcitySolid = bp.find('.//{%s}Solid' %ns_gml)
                            bpsolid =  etree.SubElement(bpgeometry, "{%s}Solid" % ns_gml32)
                            bpexterior = etree.SubElement(bpsolid, "{%s}exterior" % ns_gml32)
                            bpshell = etree.SubElement(bpexterior, "{%s}Shell" % ns_gml32)
                            if bpcitySolid.findall(".//{%s}surfaceMember[@{%s}href]" % (ns_gml, ns_xlink)):
                                for sm in bpcitySolid.findall(".//{%s}surfaceMember[@{%s}href]" % (ns_gml, ns_xlink)):
                                    bpsurfaceMember = etree.SubElement(bpshell, "{%s}surfaceMember" %ns_gml32)
                                    polygon = etree.SubElement(bpsurfaceMember, "{%s}Polygon" %ns_gml32)
                                    polyext = etree.SubElement(polygon, "{%s}exterior" %ns_gml32)
                                    polylr = etree.SubElement(polyext, "{%s}LinearRing" %ns_gml32)
                                    if bp.find(".//{%s}Polygon[@{%s}id]" % (ns_gml, ns_gml)) is not None:
                                        bppoly = bp.find(".//{%s}Polygon[@{%s}id]" % (ns_gml, ns_gml))
                                        if bppoly.find('.//{%s}posList' %ns_gml) is not None:
                                            poslist = etree.SubElement(polylr, "{%s}posList" %ns_gml32)
                                            posL = bppoly.find('.//{%s}posList' %ns_gml)
                                            coords = posL.text.split()
                                            newcoords = coords[:-3] 
                                            poslist.text = "" 
                                            for i in range(0, len(newcoords)):
                                                poslist.text = poslist.text + " " + str(newcoords[i])
                                            
                                        elif bppoly.findall('.//{%s}pos' %ns_gml):
                                            pls = bppoly.findall('.//{%s}pos' %ns_gml)
                                            for posL in pls[:-1]:
                                                gmlpos = etree.SubElement(polylr, "{%s}pos" %ns_gml32)
                                                coords = posL.text.split()
                                                gmlpos.text = ""
                                                for i in range(0, len(coords)):
                                                    gmlpos.text = gmlpos.text + " " + (coords[i])    
                                                    
                            else:                     
                                for bpcityPolygon in bpcitySolid.findall('.//{%s}Polygon' %ns_gml):
                                    bpsurfaceMember = etree.SubElement(bpshell, "{%s}surfaceMember" %ns_gml32)
                                    polygon = etree.SubElement(bpsurfaceMember, "{%s}Polygon" %ns_gml32)
                                    polyext = etree.SubElement(polygon, "{%s}exterior" %ns_gml32)
                                    polylr = etree.SubElement(polyext, "{%s}LinearRing" %ns_gml32)
                                    if bpcityPolygon.find('.//{%s}posList' %ns_gml) is not None:
                                        poslist = etree.SubElement(polylr, "{%s}posList" %ns_gml32)
                                        posL = bpcityPolygon.find('.//{%s}posList' %ns_gml)
                                        coords = posL.text.split()
                                        newcoords = coords[:-3] 
                                        poslist.text = "" 
                                        for i in range(0, len(newcoords)):
                                            poslist.text = poslist.text + " " + str(newcoords[i])
                            
                                    elif bpcityPolygon.findall('.//{%s}pos' %ns_gml):
                                        pls = bpcityPolygon.findall('.//{%s}pos' %ns_gml)
                                        for posL in pls[:-1]:
                                            gmlpos = etree.SubElement(polylr, "{%s}pos" %ns_gml32)
                                            coords = posL.text.split()
                                            gmlpos.text = ""
                                            for i in range(0, len(coords)):
                                                gmlpos.text = gmlpos.text + " " + (coords[i])
                                    
                        
                        facilityPartID = etree.SubElement(bp2, "{%s}facilityPartID" % ns_lif)
                        bpID = etree.SubElement(facilityPartID, "{%s}ID" % ns_lif)
                        bpidentifier = etree.SubElement(bpID, "{%s}identifier" % nsinfra)
                        bpidentifier.text = bpid 
                        bpscope = etree.SubElement(bpID, "{%s}scope" % nsinfra)
                        bpscope.text = "OGC LandInfra SWG" 
                        bptype = etree.SubElement(bp2, "{%s}type" % ns_lif)
                        bptype.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/typeCodelist#BuildingPart"
                        bptype.attrib['{%s}title' % ns_xlink] = "BuildingPart"
             
                        bpstatus = etree.SubElement(bp2, "{%s}status" % ns_lif)
                        if bp.find('{%s}terminationDate' %ns) is not None:
                            bpstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#Dead"
                            bpstatus.attrib['{%s}title' % ns_xlink] = "Dead"
                        else:
                            bpstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#Existing"
                            bpstatus.attrib['{%s}title' % ns_xlink] = "Existing"
                            
            else:
                fpart = etree.SubElement(facility, "{%s}part" % ns_lif)
                fpart.attrib['{%s}href' % ns_xlink] = "#"+fdid1
            
            
            if bldg1.find('{%s}lod1Solid' %ns_bldg) or \
            bldg1.find('{%s}lod2Solid' %ns_bldg) is not None:
                bfeature = etree.SubElement(LandInfraDataset, "{%s}feature" % nsinfra)
                bldg2 = etree.SubElement(bfeature, "{%s}Building" % ns_lif)
                if bldg1.get("{%s}id" % ns_gml) is not None:
                    bdid = str(bldg1.get("{%s}id" % ns_gml))
                else:
                    bdid = "GML_"+str(uuid.uuid4())
                bldg2.attrib['{%s}id' % ns_gml32] = bdid
                bname = etree.SubElement(bldg2, "{%s}name" % ns_gml32)
                if bldg1.find('{%s}name' %ns_gml) is not None:
                    bname.text=bldg1.find('{%s}name' %ns_gml).text
                else:
                    bname.text="Land Infra Facility Dataset"  
            
                bspatRep1 = etree.SubElement(bldg2, "{%s}spatialRepresentation" % ns_li)
                bspatRep2 = etree.SubElement(bspatRep1, "{%s}SpatialRepresentation" % ns_li)
                bgeometry =  etree.SubElement(bspatRep2, "{%s}geometry" % ns_li)
                if bldg1.find('.//{%s}Solid' %ns_gml) is not None:
                    citySolid = bldg1.find('.//{%s}Solid' %ns_gml)
                    bsolid =  etree.SubElement(bgeometry, "{%s}Solid" % ns_gml32)
                    exterior = etree.SubElement(bsolid, "{%s}exterior" % ns_gml32)
                    shell = etree.SubElement(exterior, "{%s}Shell" % ns_gml32)
                    
                    if citySolid.findall(".//{%s}surfaceMember[@{%s}href]" % (ns_gml, ns_xlink)):
                        for sm in citySolid.findall(".//{%s}surfaceMember[@{%s}href]" % (ns_gml, ns_xlink)):
                            surfaceMember = etree.SubElement(shell, "{%s}surfaceMember" %ns_gml32)
                            polygon = etree.SubElement(surfaceMember, "{%s}Polygon" %ns_gml32)
                            polyext = etree.SubElement(polygon, "{%s}exterior" %ns_gml32)
                            polylr = etree.SubElement(polyext, "{%s}LinearRing" %ns_gml32)
                            if bldg1.find(".//{%s}Polygon[@{%s}id]" % (ns_gml, ns_gml)) is not None:
                                bbpoly = bldg1.find(".//{%s}Polygon[@{%s}id]" % (ns_gml, ns_gml))
                                if bbpoly.find('.//{%s}posList' %ns_gml) is not None:
                                    poslist = etree.SubElement(polylr, "{%s}posList" %ns_gml32)
                                    posL = bbpoly.find('.//{%s}posList' %ns_gml)
                                    coords = posL.text.split()
                                    newcoords = coords[:-3] 
                                    poslist.text = "" 
                                    for i in range(0, len(newcoords)):
                                        poslist.text = poslist.text + " " + str(newcoords[i])
                            
                                elif bbpoly.findall('.//{%s}pos' %ns_gml):
                                    pls = bbpoly.findall('.//{%s}pos' %ns_gml)
                                    for posL in pls[:-1]:
                                        gmlpos = etree.SubElement(polylr, "{%s}pos" %ns_gml32)
                                        coords = posL.text.split()
                                        gmlpos.text = ""
                                        for i in range(0, len(coords)):
                                            gmlpos.text = gmlpos.text + " " + (coords[i])                            
                    else:                        
                        for cityPolygon in citySolid.findall('.//{%s}Polygon' %ns_gml):
                            surfaceMember = etree.SubElement(shell, "{%s}surfaceMember" %ns_gml32)
                            polygon = etree.SubElement(surfaceMember, "{%s}Polygon" %ns_gml32)
                            polyext = etree.SubElement(polygon, "{%s}exterior" %ns_gml32)
                            polylr = etree.SubElement(polyext, "{%s}LinearRing" %ns_gml32)
                            if cityPolygon.find('.//{%s}posList' %ns_gml) is not None:
                                poslist = etree.SubElement(polylr, "{%s}posList" %ns_gml32)
                                posL = cityPolygon.find('.//{%s}posList' %ns_gml)
                                coords = posL.text.split()
                                newcoords = coords[:-3] 
                                poslist.text = "" 
                                for i in range(0, len(newcoords)):
                                    poslist.text = poslist.text + " " + str(newcoords[i])
                            
                            elif cityPolygon.findall('.//{%s}pos' %ns_gml):
                                pls = cityPolygon.findall('.//{%s}pos' %ns_gml)
                                for posL in pls[:-1]:
                                    gmlpos = etree.SubElement(polylr, "{%s}pos" %ns_gml32)
                                    coords = posL.text.split()
                                    gmlpos.text = ""
                                    for i in range(0, len(coords)):
                                        gmlpos.text = gmlpos.text + " " + (coords[i])
            
                facilityPartID = etree.SubElement(bldg2, "{%s}facilityPartID" % ns_lif)
                bID = etree.SubElement(facilityPartID, "{%s}ID" % ns_lif)
                bidentifier = etree.SubElement(bID, "{%s}identifier" % nsinfra)
                bidentifier.text = bdid 
                bscope = etree.SubElement(bID, "{%s}scope" % nsinfra)
                bscope.text = "OGC LandInfra SWG" 
                btype = etree.SubElement(bldg2, "{%s}type" % ns_lif)
                btype.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/typeCodelist#Building"
                btype.attrib['{%s}title' % ns_xlink] = "Building"
             
                bstatus = etree.SubElement(bldg2, "{%s}status" % ns_lif)
                if bldg1.find('{%s}terminationDate' %ns) is not None:
                    bstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#Dead"
                    bstatus.attrib['{%s}title' % ns_xlink] = "Dead"
                else:
                    bstatus.attrib['{%s}href' % ns_xlink] = "http://www.opengis.net/infragml/facility/1.0/statusCodelist#Existing"
                    bstatus.attrib['{%s}title' % ns_xlink] = "Existing"
            
    print ("\n# of ReliefFeature(s): ", featureCountDict["reliefCount"])
    print ("# of TINRelief(s): ", featureCountDict["tinreliefCount"])
    print ("# of Buildings(s): ", featureCountDict["buildingCount"]) 
    print ("# of BuildingPart(s): ", featureCountDict["buildingPartCount"]) 
           
    infragml = etree.tostring(LandInfraDataset, pretty_print=True,xml_declaration=True, encoding='UTF-8')
#    print ("\n#-------------InfraGML output-------------------#\n")
    wf=open(outputfile,'wb')
#    wf.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>")
    wf.write(infragml)
    wf.close()
    print ("\n******* Conversion completed!! ********")
    print ("Output written to:", outputfile)

#-------------start of program-------------------#

print ("\n****** CityGML2infraGML Converter *******\n")  
argparser = argparse.ArgumentParser(description='******* CityGML2infraGML Converter *******')
argparser.add_argument('-i', '--inputFilename', help='CityGML dataset filename', required=False)
argparser.add_argument('-o', '--outputFilename', help='infraGML dataset filename', required=False)
args = vars(argparser.parse_args())

inputFileName = args['inputFilename']
if inputFileName:
    inputFile = str(inputFileName)
    print ("CityGML input file: ", inputFile)
else:
    print ("Error: Enter the CityGML dataset!! ")
    sys.exit()

outputFileName = args['outputFilename']
if outputFileName:
    outputFile = str(outputFileName)
#    print ("InfraGML output file: ", outputFile)
else:
    print ("Error: Enter the infraGML filename!! ")
    sys.exit()
    
start = time.time()
citygml2infragml(inputFile,outputFile)
end = time.time()
print ("Time taken for InfraGML generation: ",end - start, " sec")