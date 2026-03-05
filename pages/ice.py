from pdb import line_prefix

import streamlit as st
import geemap.foliumap as geemap
#from streamlit_metrics import metric, metric_row
from streamlit_ace import st_ace
import pandas as pd
import ee
import extra_streamlit_components as stx
import re

from st_pages import add_indentation
add_indentation()

instructions = {'1': ['''Firstly, you should define the two radar images you want to use, for different dates.

    Defined below are the radar images that you will be using. They are from the Sentinel-1 satellite and can see through clouds.

        s1_2016 = ee.Image('COPERNICUS/S1_GRD/S1A_EW_GRDM_1SSH_20160602T051612_20160602T051716_011527_011973_749B').select('HH')
       s1_2022 = ee.Image('COPERNICUS/S1_GRD/S1B_IW_GRDH_1SSH_20210321T095950_20210321T100015_026111_031D9E_1D62').select('HH')

''', '''You can now add the two images to the map. 

    You can change the minimum and maximum values of the images. For now, set a minimum of -25 and maximum of 0.

        Map.addLayer(s1_2016, {'min':PUTMINVALUEHERE, 'max':PUTMAXVALUEHERE}, '2016')
       Map.addLayer(s1_2022, {'min':PUTMINVALUEHERE, 'max':PUTMAXVALUEHERE}, '2022')
''', '''To subtract a layer named b from a layer named b, you write,
            
            a.subtract(b)
        
    Define a variable called 'difference' that is the 2016 radar image subtracted from the 2022 radar image.''',
'''Finally, you can now add the difference image to the map! 

    Set a sensible min and max range. You can also define a colourmap to see the difference clearly.

    Add the difference layer to the map, and then set the centre of the map to the location of the difference image,

        Map.addLayer(LAYERVARIABLENAME, {'min':MINVALUEHERE, 'max':MAXVALUEHERE, 'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}, 'diff')
       Map.setCenter(-14.1394, -5.9002)''',
       '''Great! Check your code with the solution given below. 
       
    Now you can also see the difference in the radar images.
       
    Look at where the image is centred over the glacier. Using the map polyline tool,
        measure the distance that the glacier has moved between the two radar images. 
        
    Enter your measurement in the box below.'''
        ],
        '2':['''We first need to load a dataset looking at the bedrock.

            bedrock = ee.Image('NOAA/NGDC/ETOPO1').select('bedrock')
    Show the bedrock layer on the map.

    (The minimum and maximum bedrock elevations are -10898 and 8271, respectively).
''','''You can also look at some natural imagery over Antartica - captured by the Landsat satellites.

    To do this, you should also select the B3, B2, and B1 bands that you want to use as red, green, and blue in the image. 
    Feel free to play around with B4 (the near-infrared band) as well!

        lima_mosaic = ee.Image('USGS/LIMA/MOSAIC')
       antarctica = lima_mosaic.select(['B3', 'B2', 'B1'])
    
    Now you can add this layer to the map with some sensible min and max values.''',
    '''Now you should define a variable for the Cryosat digital elevation model (DEM) ('CPOM/CryoSat2/ANTARCTICA_DEM'). Select the 'elevation' band from the image and add it to the map with the following visualisation,

        visualisation = {
        'min': 0.0,
        'max': 10000.0,
        'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']
        }
       Map.addLayer(LAYERVARIABLENAME, visualisation, 'Cryosat')
    ''',
    '''You now have the bedrock, Cryosat, and Landsat layers on the map. 
    
    You can now add a layer to the map that shows the difference between the Cryosat and Landsat layers.
    
    Subtract the bedrock from the Cryosat DEM and add the difference to the map using the following visualisation,
    
            {'min': -4000,'max': 4000,'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}''',
            '''Great! Now, check your code with the solution given below.
            
    What does this layer look like? 
            
    Compare it to the Landsat imagery and look at the differences
            between East and West Antarctica. 
            
    What does this suggest about melting ice in Antarctica?''',],
        '3':['testa','testb','testc']}

if 'instruction_idx' not in st.session_state.keys():
    st.session_state['instruction_idx'] = 0
if "old_chosen_id" not in st.session_state.keys():
    st.session_state["old_chosen_id"] = '1'

def instruction_step(step):
    st.session_state['instruction_idx'] += step

CODE_DICT = {'2': '''###############
bedrock = ee.Image('NOAA/NGDC/ETOPO1').select('bedrock')
Map.addLayer(bedrock, {'min':-10898, 'max':1000}, 'bedrock')

###############
lima_mosaic = ee.Image('USGS/LIMA/MOSAIC')
antarctica = lima_mosaic.select(['B3', 'B2', 'B1'])
antarcticaVis = {
'min': 0.0,
'max': 10000.0,
}
Map.addLayer(lima_mosaic, antarcticaVis, 'Antartica Imagery (RGB)')

###############
cryosat_dem = ee.Image('CPOM/CryoSat2/ANTARCTICA_DEM').select('elevation')

visualisation = {
'min': 0.0,
'max': 10000.0,
'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']
}

Map.addLayer(cryosat_dem, visualisation, 'Cryosat DEM')

############### PUT SOMETHING BELOW HERE TO SHOW THE SUBTRACTED IMAGE
subtracted = cryosat_dem.subtract(bedrock)
Map.addLayer(subtracted, {'min': -4000,'max': 4000,'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}, 'ice-bedrock difference')

Map.setCenter(0, 0, 4)''',
'1':'''#These are the radar images that you will be using. 
#They are from the Sentinel-1 satellite and can see through clouds.
s1_2016 = ee.Image('COPERNICUS/S1_GRD/S1A_EW_GRDM_1SSH_20160602T051612_20160602T051716_011527_011973_749B').select('HH')
s1_2022 = ee.Image('COPERNICUS/S1_GRD/S1B_IW_GRDH_1SSH_20210321T095950_20210321T100015_026111_031D9E_1D62').select('HH')

#You can add the images to the map like this:
#Make sure you set a minimum and maximum value for the image.
Map.addLayer(s1_2016, {'min':-25, 'max':0}, '2016')
Map.addLayer(s1_2022, {'min':-25, 'max':0}, '2022')

#You can subtract the images like this:
difference = s1_2022.subtract(s1_2016)

#You can add the difference to the map like this:
Map.addLayer(difference, {'min':-5, 'max':5, 'palette': ['001fff', '00ffff', 'fbff00', 'ff0000']}, 'diff')

Map.setCenter(-14.1394, -5.9002)
''',
'3':'''print('something goes here')
###############
bedrock = ee.Image('NOAA/NGDC/ETOPO1').select('bedrock')
Map.addLayer(bedrock, {'min':-10898, 'max':1000}, 'bedrock')'''}


if 'well_done' not in st.session_state:
    st.session_state.well_done = False

# st.markdown(
# "<h1 style='text-align: center; color: #565656; background: #99FFFF'> Ice 🧊</h1>",
# unsafe_allow_html=True)

empty = st.empty()

with empty:
    chosen_id = stx.tab_bar(data=[
        stx.TabBarItemData(id=1, title="Code exercise 1", description="Sentinel 1 difference"),
        stx.TabBarItemData(id=2, title="Code exercise 2", description="Ice mass balance"),
    ], default=1, key='orig')
#st.info(f"{chosen_id=}")

if not st.session_state.well_done and chosen_id != '1':
   st.warning("You should complete the first exercise before you try the other ones!")

if chosen_id == '1':
    st.info("In this exercise you are looking at radar images over Antartica. You need to subtract the two images in order to see how much the ice has moved. You can\
    then use the polyline tool on the map to measure the distance and find your answer.")
    if chosen_id != st.session_state["old_chosen_id"]:
    	st.session_state['instruction_idx'] = 0
    	st.session_state["old_chosen_id"] = chosen_id
elif chosen_id == '2':
    st.info("In this exercise you will be using different digital elevation models in order to subtract the ice surface elevation from the underlying bedrock.")
    if chosen_id != st.session_state["old_chosen_id"]:
        st.session_state['instruction_idx'] = 0
        st.session_state["old_chosen_id"] = chosen_id
elif chosen_id == '3':
    st.info("In this exercise you will do something else. Maybe over the Arctic?")
    if chosen_id != st.session_state["old_chosen_id"]:
        st.session_state['instruction_idx'] = 0
        st.session_state["old_chosen_id"] = chosen_id

display, editor = st.columns((1, 1))

INITIAL_CODE = CODE_DICT[str(chosen_id)]


with editor:
    #st.write('### Code editor')
    st.write('')
               
    st.warning(f'''{st.session_state['instruction_idx'] + 1}) {instructions[chosen_id][st.session_state['instruction_idx']]}''')
    
    st.button("◀️ go back", on_click=instruction_step, args=(-1,), disabled=bool(st.session_state['instruction_idx'] == 0))
    st.button("▶️ continue", on_click=instruction_step, args=(1,), disabled=bool(st.session_state['instruction_idx']+1 >= len(instructions[chosen_id])))
    
    st.caption('The code in the box below is run in the browser. You can edit it and see the results on the left.')
    code = st_ace(
            value= '',
            language="python",
            theme="github",
            font_size=18,
            tab_size=4,
            show_gutter=True,
            key=str(chosen_id)
        )
        
    st.write('Hit `CTRL+ENTER` to refresh')
    st.write('*Remember to save your code separately!*')
                  
    with st.expander('Code solution'):
	    st.caption('The code in the box below is given for you. It gives the images that you will be using as code variables.')
	    st.code(CODE_DICT[str(chosen_id)])

with display:
    Map = geemap.Map(draw_export=False, plugin_Draw=True, add_google_map = False, tiles=None)
    Map.addLayer(ee.Image())
    #Map.add_basemap("HYBRID")

    code = code.replace('print(','st.write(')

    executable_code = []
    proj_change = ".changeProj('EPSG:3031', 'EPSG:3857')"
    for line in code.split('\n'):
        if 'Map.addLayer(' in line:
            if proj_change not in line:
                line_suffix = ''.join(line.split('Map.addLayer(')[1:])
                COMMA_MATCHER = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
                args = COMMA_MATCHER.split(line_suffix)
                #st.write(args)
                if args[0][-1] == ')':
                    first_arg = args[0][:-1]
                    args = []
                    args.append(first_arg)
                    args.append(')')

                first_arg = args[0] + proj_change + ','
                new_line = 'Map.addLayer(' + first_arg + ','.join(args[1:])
                #st.write('line', line)
                #st.write(new_line)
                executable_code.append(new_line)
        else:
            executable_code.append(line)
    executable_code = '\n'.join(executable_code)
    #st.code(executable_code)
    try:
        exec(executable_code)
    except Exception as e:
        st.error(f'There was an error in your code!\n{e}')

    Map.to_streamlit(height=600)
    
    if chosen_id == '1':
        corr = 3
        ans = st.text_input('How far (in km) has the ice moved in the radar images from 2016 to 2022?', help='Distance (in km) that the ice has moved from 2016 to 2022', max_chars=4)
        if ans.replace('.','',1).isdigit():
            ans = float(ans)
            if ans < corr+corr*0.1 and ans > corr-corr*0.1:
                st.success('Well done!')
                if st.session_state.well_done is False:
                    st.snow()
                st.session_state.well_done = True
            else:
                st.error('Incorrect. Try again.')
                st.session_state.well_done = False
