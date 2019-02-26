# CityGML2InfraGML
An experimental python utility to convert CityGML datasets to InfraGML and vice versa.

Things to know
---------------

### CityGML

[CityGML](http://www.citygml.org) is an open 3D data modelling standard for the storage and exchange of 3D city models. It models the geometry, semantics, and graphical appearance associated with 3D city models. It is implemented as an application schema of the Geography Markup Language version 3.1.1 (GML3). The data model of CityGML comprises of a core module and several thematic modules such as Building, Relief, Bridge, Transportation, Vegetation, and WaterBody.

### InfraGML

[InfraGML]( https://www.khronos.org/gltf/) is the GML based implementation of the LandInfra conceptual model. LandInfra covers land and civil engineering infrastructure facilities, such as roads, buildings, railways, projects, alignment, survey, land features and land division. InfraGML is published as an 8 part standard and each part has a separate schema (XSD ﬁle): Core, Features, Projects, Alignments, Roads, Railways, Survey and LandDivision.

System requirements
---------------------

Python packages:

+ [lxml](http://lxml.de)
+ [argparse](https://docs.python.org/3/library/argparse.html)
+ [time](https://docs.python.org/3/library/time.html)
+ [uuid](https://docs.python.org/3/library/uuid.html)

### OS and Python version

The software has been developed on MacOS in Python 3.7, and has not been tested with other configurations. Hence, it is possible that some of the functions will not work on Windows.


How to use?
-----------

### CityGML2InfraGML
To convert CityGML data into InfraGML, use the following command:

```
python3 city2infragml.py -i /path/to/CityGMLfile/ -o /path/to/new/InfraGMLfile/
```

### InfraGML2CityGML

To convert InfraGML data into CityGML, use the following command:

```
python3 infra2citygml.py -i /path/to/InfraGMLfile/ -o /path/to/new/CityGMLfile/
```
Note: By default, LOD1 model is generated while converting from InfraGML to CityGML.
At this moment, the converter is not programmed to determine the surface semantics (roofs, walls, ground) & LODs.

Mandatory:

+ CityGML 1.0 or 2.0
+ Only Building (& BuildingPart) and Relief (Terrain) classes
+ Buildings (& BuildingPart) must have `<gml:Solid>` geometry
+ Files must end with `.gml`, `.GML`, `.xml`, or `.XML`
+ Vertices in `<gml:posList>` or `<gml:pos>`
+ Your files must be valid (see the next section)

Optional, but recommended:

+ `<gml:id>` for each `<bldg:Building>` and `<dem:ReliefFeature>`

### CityGML
[Hugo Ledoux](https://3d.bk.tudelft.nl/hledoux/) built [val3dity](http://geovalidation.bk.tudelft.nl/val3dity/), a thorough GML validator which is available for free through a web interface. Use this tool to test your CityGML files.

### InfraGML
To validate your InfraGML files against the schema you can use our [Validator](infragml_schema_validator.py).

```
python3 infragml_schema_validator.py -i /path/to/InfraGMLfile/
```
Note: We introduced an additional wrapper schema [(infra.xsd)](schema/infragml-1_0_0/infra.xsd) to validate different LandInfra features (e.g. terrain, facilties, roads) within a single dataset.

### Coming soon
Support for converting features such as Roads, Railways, Water bodies, vegetation, etc. will be available soon.

Conditions for use
---------------------
This software is free to use. You are kindly asked to acknowledge its use by citing it in a research paper you are writing, reports, and/or other applicable materials.
