import geemap.foliumap as geemap
import ee
from config import EE_PROJECT
ee.Initialize(project=EE_PROJECT)

import streamlit as st

from st_pages import add_indentation
add_indentation()

st.markdown(
    ''':balloon:**Welcome to the Night Light Imagery worksheet!:balloon: :full_moon_with_face:**''')
st.markdown('''
       **In this activity, we'll delve into the captivating world of nocturnal landscapes. Using satellite imagery, we'll explore the distribution and intensity of artificial nighttime lights across different regions.**''')
st.markdown('''
      :one:  There are bright spots in the satellite image at night. Can you identify the brightest ones and link them to the largest cities in Europe??''')       
with st.expander("Hint"):
     st.markdown("""Can you spot London? Paris? Madrid? Moscow? You can change the layer by moving to the icon at the top right corner, then untick 'Worldimagery' to get the country and city names appear below the city light imagery. 
        Feel the names are not clear to see? You can go to the left of the imagery and change the values for 'Opacity'.""")
st.markdown('''
    :two: The bright spots appear in several different colors, such as the white colour in London, yellow in Madrid, and red in Moscow. What do these colors suggest? \n
       How many colors can you spot in Shanghai? Can you tell a story about the city's development over the years?''')
with st.expander("Hint1"):
     st.markdown("""The city light satellite imagery is comprised of 3 RGB channels. As shown in the channel panel on the left, each color channel refers to a light imagery of a specific year. from the colour mixture chart, white colour comes from the mixture of blue, green, and red colours. So the white colours in the night light imagery suggests that the city areas exist since 1993. """)
     st.image('./pages/intro/RGB.PNG',width=700) 
with st.expander("Hint2"):
     st.markdown("""For seeing the changes in a specific year, you can use the channel setting as it is or can drag the bars to change the years for the channels (try 1993 for Blue, 1993 for Green and 2013 for Red, the city development between 1993-2013 just appears in Red!""")
st.markdown('''      
    :three: There is an interesting feature in the imagery: the national border between North Korea and South Korea. \n
       Can you describe the pattern of lights (colour, brightness, number ...) in this region? Can you give a suggestion for this difference.''')
with st.expander("Hint"):
     st.markdown('''Economy and population differences?''')
st.markdown('''      
    :four: [Bonus]There are also some other interesting features in the image. For example, the light pattern that resembles 'Christmas tree' in Northern Russia.  \n
       Can you describe the pattern of lights over this region? What do the different colours suggest? What do you think could cause this 'Christmas tree' pattern?''')
with st.expander("Hint"):
     st.markdown('''Economy and population differences?''')

# Create the map with the actual basemap object
Map = geemap.Map(center=(48.37, 7.10), zoom=4, basemap=geemap.basemaps.get("Esri.WorldStreetMap"))
#Map.set_options("HYBRID")

cola, colb = st.columns([0.25,1])
year1 = cola.slider("Channel 1 - Red", 1993, 2013, 2013)
year2 = cola.slider("Channel 2 - Green", 1993, 2013, 2003)
year3 = cola.slider("Channel 3 - Blue", 1993, 2013, 1993)
opac = cola.slider("Opacity", 0., 100., 75.)



lightsr = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').filter(ee.Filter.date(f'{year1}-01-01', f'{year1}-12-31'))\
  .select('stable_lights').mean().rename(f'{year1}');

lightsg = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').filter(ee.Filter.date(f'{year2}-01-01', f'{year2}-12-31'))\
  .select('stable_lights').mean().rename(f'{year2}');

lightsb = ee.ImageCollection('NOAA/DMSP-OLS/NIGHTTIME_LIGHTS').filter(ee.Filter.date(f'{year3}-01-01', f'{year3}-12-31'))\
  .select('stable_lights').mean().rename(f'{year3}');

changeImage = lightsr.addBands(lightsg).addBands(lightsb);

Map.addLayer(changeImage, {'min':0,'max':63, 'opacity':opac/100}, "RGB composite", 1, 1);

with colb:
    Map.to_streamlit(height=700)


# This image uses additive color to compare brightness of stable nighttime lights in 2013, 2003, 1993.  

# - Red channel = 2013  
# - Green channel = 2003  
# - Blue channel = 1993     

# If you are new to reading additive color, the picture below illustrates how colors represent combinations of pixel values.

# ![RGB key](https://github.com/jeffhowarth/eeprimer/raster/readings/rgbLights/images/RGB_alt3.png)  

# ## Heat pattern  

# The picture of Shanghai, China shows a recurring pattern that resembles heat from a fire: white core, yellow periphery, red terminal edge.  

# #![Shanghai, China](https://github.com/jeffhowarth/eeprimer/blob/master/readings/rgbLights/eples/shanghai.png?raw=true)  

# This pattern often shows urban sprawl. Locations with bright stable lights in all three years appear white. Locations that became bright in 2003 and remained bright in 2013 appear yellow. Locations that became bright in 2013 appear red.   

# ## Holiday lights pattern

# In many places, bright dots of many different colors appear near each other and resemble holiday lights. These represent places with bright lights that were stable for a year, but not stable for a decade or more. These often mark places of fossil fuel extraction. Some examples include:  

# #### Noyabrsk, Russia  

# ![Noyabrsk, Russia](https://github.com/jeffhowarth/eeprimer//master/rings/rgbLights/examples/noyabrsk.png?raw=true)  

# #### Yenagoa, Nigeria  

# ![Yenagoa, Nigeria](https://github.com/jeffhowarth/eeprimer/blob/masteeadings/rgghts/examples/yenagoa.png?raw=true)  

# ## Aurora pattern    

# Similar to the holiday lights pattern, some lights were were stable for a year but not for a decade, creating an aurora pattern. In comparison to the holiday light pattern, aurora patterns generally occur on the ocean and appear more diffuse. They are likely caused by shifts in the intensity of fishing activities that employ bright lights (like squid fishing).

# #### Korea Strait

# ![Korea Strait](https://github.com/jeffhowarth/eeprimer/blob/mastreadings/rgbLights/examples/koreaStrait.png?raw=true)  

# ## Red Giants  

# In some places, giant red patches of light appear, marking places that became bright in 2013 that had been dark in 2003 and 1993. These often mark large-scale fossil fuel extraction activities. The picture below shows examples of red giants in North Dakota and Texas.    

# ![Willison, ND](https://github.com/jeffhowarth/eepr/blob/master/readings/rgbLights/examples/williston.png?raw=true)

# ## National boundaries  

# In a number of places, difference in nighttimes lights mark national boundaries. In the example above, South Korea appears as an island because of the darkness of North Korea. Some other interesting examples include:  

# #### Lebanon - Israel

# ![Lebanon-Israel](https://github.com/jeffhowarth/eeprimer/blob/mr/readings/rgbLights/examples/Lebanon-Israel.png?raw=true)  

# #### Pakistan - India  

# ![Pakistan-India](https://github.com/jeffhowarth/eeprimer/blob/master/readingbLights/examples/Pakistan-India.png?raw=true)  
#     """)
