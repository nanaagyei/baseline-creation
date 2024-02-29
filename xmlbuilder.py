import xml.etree.ElementTree as ET
from xml.dom import minidom

# create root element
root = ET.Element('OPTIONS')

# create BASELINES element
baselines = ET.SubElement(root, 'BASELINES')


distance = ET.SubElement(baselines, 'DISTANCE')
from_point = ET.SubElement(distance, 'FROM')
from_point.text = 'PLNA'
to_point = ET.SubElement(distance, 'TO')
to_point.text = 'ANAT'

# create CONSTRAINT_WEIGHT element
constraint_weight = ET.SubElement(root, 'CONSTRAINT_WEIGHT')

# ask user to choose between Normal and Loose for constraint_weight
user_input_constraint_weight = input("Enter 'Normal' or 'Loose' for Constraint Weight: ")
if user_input_constraint_weight == 'Normal':
    constraint_weight.text = 'Normal'
elif user_input_constraint_weight == 'Loose':
    constraint_weight.text = 'Loose'


# create ELEVATION_CUTOFF element
elevation_cutoff = ET.SubElement(root, 'ELEVATION_CUTOFF')
elevation_cutoff.text = '15.0'

# create EMAIL_ADDRESS element
email_address = ET.SubElement(root, 'EMAIL_ADDRESS')
email_address.text = 'ohenew@oregonstate.edu'

# create GEOID_MODEL element
geoid_model = ET.SubElement(root, 'GEOID_MODEL')
geoid_model.text = 'LET OPUS CHOOSE'

# create REFERENCE_FRAME element
reference_frame = ET.SubElement(root, 'REFERENCE_FRAME')
reference_frame.text = 'LET OPUS CHOOSE'

# create GNSS element
gnss = ET.SubElement(root, 'GNSS')
gnss.text = 'GPS-Only'

# create TROPO_INTERVAL element
tropo_interval = ET.SubElement(root, 'TROPO_INTERVAL')
tropo_interval.text = '7200'

# create TROPO_MODEL element
tropo_model = ET.SubElement(root, 'TROPO_MODEL')
tropo_model.text = 'Piecewise Linear'

# create CORS element
cors = ET.SubElement(root, 'CORS')

# create HUB elements
hub1 = ET.SubElement(cors, 'HUB')
hub1.text = 'PLNA'
fix1 = ET.SubElement(hub1, 'FIX')
fix1.text = '3-D'

hub2 = ET.SubElement(cors, 'HUB')
hub2.text = 'BURN'
fix2 = ET.SubElement(hub2, 'FIX')
fix2.text = 'NONE'

# create XML tree
tree = ET.ElementTree(root)


# write pretty-printed XML tree to file
xml_str = ET.tostring(root)
dom = minidom.parseString(xml_str)
with open('options.xml', 'w') as f:
    dom.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='utf-8')
    

# print pretty-printed XML tree to console
with open('options.xml', 'r') as f:
    print(f.read())