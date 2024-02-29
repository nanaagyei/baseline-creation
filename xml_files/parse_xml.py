import xml.etree.ElementTree as ET
import xlsxwriter

# Parse the XML file
tree = ET.parse(r'D:\baseline creation\xml_files\p393049a.22o.xml')
root = tree.getroot()

# Create an Excel workbook and worksheet
workbook = xlsxwriter.Workbook('output.xlsx')
worksheet = workbook.add_worksheet()

# Write the header row to the worksheet
header = ['RINEX FILE', 'TIME', 'START', 'START TIME', 'EPHEMERIS', 'STOP', 'STOP TIME', 'OBS USED', 'OBS %', '# FIXED AMB', 'FIXED AMB %', 'ANT NAME', 'X-1', 'X-2', 'X-3', 'X-4', 'Y-1', 'Y-2', 'Y-3', 'Y-4', 'Z-1', 'Z-2', 'Z-3', 'Z-4', 'LAT-1', 'LAT-2', 'LAT-3', 'LAT-4', 'LAT-5', 'LAT-6', 'LAT-7', 'LAT-8', 'E LON-1', 'E LON-2', 'E LON-3', 'E LON-4', 'E LON-5', 'E LON-6', 'E LON-7', 'E LON-8', 'W LON-1', 'W LON-2', 'W LON-3', 'W LON-4', 'W LON-5', 'W LON-6', 'W LON-7', 'W LON-8', 'EL HGT-1', 'EL HGT-2', 'EL HGT-3', 'EL HGT-4', 'ORTHO HGT-1', 'ORTHO HGT-2', 'Easting (X) [meters]-1', 'Easting (X) [meters]-2', 'Northing (Y) [meters]-1', 'Northing (Y) [meters]-2', 'Easting (X) [feet] SPC (3601 OR N)', 'Northing (Y) [feet] SPC (3601 OR N)']
for i, h in enumerate(header):
    worksheet.write(0, i, h)

"""
# Iterate over the data in the XML file and write it to the worksheet
for i, data_sources in enumerate(root.findall('DATA_SOURCES')):
    row = i + 1
    rinex_file = data_sources.find('RINEX_FILE').text
    worksheet.write(row, 0, rinex_file)
    # TODO: Write the other data from the XML file to the worksheet

"""

# Iterate over the data in the XML file and write it to the worksheet
for i, data_sources in enumerate(root.findall('DATA_SOURCES')):

    # Find the ANTENNA element and extract the NAME element's text
    antenna = data_sources.find('ANTENNA')
    ant_name = antenna.find('NAME').text

    # Append the ANT NAME text to the header
    header.append(f'ANT NAME - {ant_name}')

    # Find the COORD_SET element and extract the X, Y, and Z coordinates
    coord_set = data_sources.find('COORD_SET')
    x = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="X"]').text
    y = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="Y"]').text
    z = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="Z"]').text

    # Append the X, Y, and Z coordinates to the header
    header.extend([f'X - {x}', f'Y - {y}', f'Z - {z}'])

    # Find the ELLIP_COORD element and extract the latitude, longitude, and elevation height coordinates
    ellip_coord = coord_set.find('ELLIP_COORD')
    lat = ellip_coord.find('LAT').text
    lon = ellip_coord.find('EAST_LONG').text
    el_hgt = ellip_coord.find('EL_HEIGHT').text

    #Append the extracted coordinates to the row_data list
    header.extend([f'LAT-1 - {lat}' ,f'LON-1 - {lon}' ,f'EL HGT-1 - {el_hgt}'])

    # Find the DATA_QUALITY element and extract the accuracy and RMS elements
    data_quality = root.find('DATA_QUALITY')
    accuracy = data_quality.find('ACCURACY')
    rms = data_quality.find('RMS').text

    # Append the accuracy and RMS elements to the header
    header.extend([f'ACCURACY - {accuracy.get("UNIT")}', f'RMS - {rms}'])

    # Find the POSITION element and extract the REF_FRAME and EPOCH elements
    position = root.find('POSITION')
    ref_frame = position.find('REF_FRAME').text
    epoch = position.find('EPOCH').text

    # Append the REF_FRAME and EPOCH elements to the header
    header.extend([f'REF_FRAME - {ref_frame}', f'EPOCH - {epoch}'])

    # Iterate over the data in the XML file again and write it to the worksheet
for i, data_sources in enumerate(root.findall('DATA_SOURCES')):
    # Initialize a list to hold the row data
    row_data = []
    
    # Find the RINEX_FILE element and extract its text
    rinex_file = data_sources.find('RINEX_FILE').text
    row_data.append(rinex_file)
    
    # Find the OBSERVATION_TIME element and extract the START and END attributes
    observation_time = data_sources.find('OBSERVATION_TIME')
    start = observation_time.get('START')
    end = observation_time.get('END')
    row_data.extend([start, end])
    
    # Find the EPHEMERIS_FILE element and extract its TYPE attribute
    ephemeris_file = data_sources.find('EPHEMERIS_FILE')
    ephemeris_type = ephemeris_file.get('TYPE')
    row_data.append(ephemeris_type)
    
    # Find the DATA_QUALITY element and extract the PERCENT_OBS_USED and PERCENT_AMB_FIXED elements
    data_quality = root.find('DATA_QUALITY')
    percent_obs_used = data_quality.find('PERCENT_OBS_USED').text
    percent_amb_fixed = data_quality.find('PERCENT_AMB_FIXED').text
    row_data.extend([percent_obs_used, percent_amb_fixed])
    
    # Find the COORD_SET element and extract the X, Y, and Z coordinates
    coord_set = data_sources.find('COORD_SET')
    x = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="X"]').text
    y = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="Y"]').text
    z = coord_set.find('RECT_COORD').find('COORDINATE[@AXIS="Z"]').text
    row_data.extend([x, y, z])
    
    # Find the ELLIP_COORD element and extract the latitude, longitude, and elevation height coordinates
    ellip_coord = coord_set.find('ELLIP_COORD')
    lat = ellip_coord.find('LAT').text
    lon = ellip_coord.find('EAST_LONG').text
    el_hgt = ellip_coord.find('EL_HEIGHT').text
    row_data.extend([lat, lon, el_hgt])
    
    # Write the row data to the worksheet
    worksheet.write_row(i+1, 0, row_data)


# Save and close the workbook
workbook.close()
