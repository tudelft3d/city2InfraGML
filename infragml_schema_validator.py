#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu October 04 11:27:23 2018

@author: kavisha
"""

#InfraGML schema validator

from lxml import etree
import argparse


#-------------start of program-------------------#

print ("\n****** Validator for InfraGML Datasets *******\n")  
argparser = argparse.ArgumentParser(description='******* Validator for InfraGML Datasets *******')
argparser.add_argument('-i', '--filename', help='InfraGML dataset filename', required=False)
args = vars(argparser.parse_args())

inputFileName = args['filename']
if inputFileName:
    inputFile = str(inputFileName)
    print ("InfraGML input file: ", inputFile)
else:
    print ("Error: Enter the InfraGML test dataset!! ")


adeSchema = "schema/infragml-1_0_0/infra.xsd"
print ("InfraGML schema: ", adeSchema)


parser = etree.XMLParser(ns_clean=True)
xml = etree.parse(inputFile)
xsd = etree.parse(adeSchema)
xmlschema = etree.XMLSchema(xsd)
valid = xml.xmlschema(xsd)
if valid == True:
    print ("Dataset is Valid!")
else:
    try:
        xmlschema.assert_(xml)
    except etree.XMLSyntaxError as e:
        print ("PARSING ERROR", e)
    
    except AssertionError as e:
        print ("INVALID DOCUMENT", e)