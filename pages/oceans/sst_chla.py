import geemap.foliumap as geemap
import ee
import eemont
import streamlit.components.v1 as components
import datetime
import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

import geemap
from config import EE_PROJECT
geemap.ee_initialize(project=EE_PROJECT)  # wraps ee.Authenticate + ee.Initialize

from st_pages import add_indentation
add_indentation()

if 'well_done' not in st.session_state:
    st.session_state.well_done = False
    
st.title("Sea Surface Temperature")

norwegian_med_samerica_df = pd.read_csv('pages/oceans/norwegian_med_samerica_df.csv', index_col=False)

st.write('''The ocean is the biggest habitat on the planet; nearly three quarters of the Earth’s surface is covered by the oceans. Half of all the oxygen we breathe comes from the oceans, with plankton absorbing carbon dioxide and releasing oxygen into the atmosphere by photosynthesis. 

98% of the heat from the sun's rays is absorbed by the oceans. This heat is then moved around the earth via currents, transporting the warm water from the equator around the earth to the poles. This is part of the global thermohaline circulating current, transporting heat from the equator (affecting the Gulf stream and giving us in the UK warm summers!) and cool nutrient-rich water from the poles, which the ocean ecosystems need to survive. Nearly 3 billion humans eat protein from the oceans! 

Even though the oceans are so vast they are a complex ecosystem and with the warming global temperatures due to climate change it is important for us to monitor them. Rising sea temperatures can cause marine heatwaves, leading to toxic algal blooms, coral reef bleaching, and acidification (what we call ocean dead zones). 
''')

st.info("""You are looking at sea surface temperatures and the amount of Chlorophyll-a present in the oceans.
          
       • What is the max sea surface temperature in June 2000 for each of our datasets? 
    • What is the max temperature in June 2010?  
    • What is the difference between the summer and winter temperature in the Arctic ocean, the Mediterranean, and the Congo? 
    • Can you see any trends over the 20 yr timeline? 
""")
          
cola, colb = st.columns([0.25,1])

with cola:
    #radio_choice = st.radio(
    #    "View",
    #    ('Sea Surface Temperature', 'Chlorophyll-a concentration'),
    #)

    start_date=datetime.datetime(2002, 7, 4)
    end_date=datetime.datetime(2021, 5, 28)

    ## Range selector
    format = 'MMM YYYY'  # format output

    slider = st.slider('Select date', min_value=start_date, max_value=end_date, format=format)

    min_val, max_val = st.select_slider(
        'Select a temperature range to display',
        options=range(-20,51,1),
        value=(-5, 40))
    st.write('You selected sea surface temperatures between', str(min_val), 'and', str(max_val), '°C on', slider.strftime("%B %Y."))
    #date = st.date_input('Select date', min_value=start_date, max_value=end_date, value=start_date)
    #color1 = st.color_picker('Min colour', value='#0000ff'
    #color2 = st.color_picker('Max colour', value='#ff0000')
    chla_check_cont = st.container()

with colb:
    m = geemap.Map(locate_control=True, zoom=1, basemap=geemap.basemaps.get("Esri.WorldStreetMap"))
    #m.add_basemap("HYBRID")

    #NOAA/CDR/SST_WHOI/V2
    dataset = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI') \
                .filterDate(slider.strftime('%Y-%m-%d'), (slider+datetime.timedelta(days=31)).strftime('%Y-%m-%d'))
    sst = dataset.select(['sst']).median()
    chla = dataset.select(['chlor_a']).median()
    #st.write(sst.getInfo())
    palette = ['#0000ff', '#00ffff', '#ffff00', '#ff0000']
    remoteSensingReflectanceVis = {'min': min_val, 'max': max_val, 'palette': palette}

    m.addLayer(
        sst, remoteSensingReflectanceVis,
        'Sea Surface Temperature')

    with st.spinner('Loading...'):
        #africa_region = ee.Geometry.Point(df_africa[['Longitude','Latitude']].iloc[0].values.tolist())
        med_region = ee.Geometry.Point(lon=5.0625,lat=39.0625)
        norwegian_region = ee.Geometry.Point(lat=65.01999, lon=-9.980000)
        samerica_region = ee.Geometry.Point(lat=-13.553, lon=-32.59)

        #africa_region = africa_region.buffer(100000).bounds()
        norwegian_region = norwegian_region.buffer(100000).bounds()
        med_region = med_region.buffer(100000).bounds()
        samerica_region = samerica_region.buffer(100000).bounds()

        # atlantic_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = atlantic_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # indian_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = indian_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # pacific_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = pacific_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )
        # arctic_ts = ee.ImageCollection('NASA/OCEANDATA/MODIS-Aqua/L3SMI').filterDate(datetime.datetime(2020,1,1), datetime.datetime(2022,1,25))\
        #     .getTimeSeriesByRegion(
        #     geometry = arctic_region,
        #     bands = ['sst'],
        #     reducer = [ee.Reducer.median(), ee.Reducer.stdDev()],
        #     scale=100
        # )

        # atlantic_df = geemap.ee_to_pandas(atlantic_ts)
        # indian_df = geemap.ee_to_pandas(indian_ts)
        # pacific_df = geemap.ee_to_pandas(pacific_ts)
        # arctic_df = geemap.ee_to_pandas(arctic_ts)

        # atlantic_df['Atlantic'] = atlantic_df['sst']
        # atlantic_df = atlantic_df.loc[atlantic_df['reducer'] == 'median']
        # atlantic_df = atlantic_df.drop(columns=['sst', 'reducer'])
        # indian_df['Indian'] = indian_df['sst']
        # indian_df = indian_df.loc[indian_df['reducer'] == 'median']
        # indian_df = indian_df.drop(columns=['sst', 'reducer'])
        # pacific_df['Pacific'] = pacific_df['sst']
        # pacific_df = pacific_df.loc[pacific_df['reducer'] == 'median']
        # pacific_df = pacific_df.drop(columns=['sst', 'reducer'])
        # arctic_df['Arctic'] = arctic_df['sst']
        # arctic_df = arctic_df.loc[arctic_df['reducer'] == 'median']
        # arctic_df = arctic_df.drop(columns=['sst', 'reducer'])
        # df = pd.merge(atlantic_df, indian_df, on='date')
        # df = pd.merge(df, pacific_df, on='date')
        # df = pd.merge(df, arctic_df, on='date')

    #labels = [str(min_val), f"{min_val + 0.25*(max_val-min_val):.2f}", f"{(min_val + 0.75*(max_val-min_val)):.2f}", str(max_val)]
    #color can be defined using either hex code or RGB (0-255, 0-255, 0-255)
    # colors = [(255, 0, 0), (127, 255, 0), (127, 18, 25), (36, 70, 180), (96, 68, 123)]
    #m.add_colorbar(colors=palette, vmin=min_val, vmax=max_val, caption='Sea Surface Temperature (°C)')

    #if chla_check_cont.checkbox(label='View Chlorophyll-a concentration'):
    m.addLayer(
            chla, {'min': 0, 'max': 1, 'palette': ['F2F2F2','00A600'],},
            'Chlorophyll-a', True)
    #m.add_colorbar(colors=['F2F2F2','00A600'], vmin=0, vmax=1, caption='Chlorophyll-a concentration (milligrammes per cubic metre)')
    #m.add_legend(title='Legend', labels=labels, colors=colors)
    
    left_layer = geemap.ee_tile_layer(sst, remoteSensingReflectanceVis, name='Sea Surface Temperature')
    right_layer = geemap.ee_tile_layer(chla, {'min': 0, 'max': 1, 'palette': ['F2F2F2','00A600'],}, name='Chlorophyll-a')
    m.split_map(left_layer, right_layer)

    #m.addLayer(africa_region,{},'North Atlantic')
    m.addLayer(norwegian_region,{'color':'blue'},'Norwegian Sea')
    m.addLayer(med_region,{'color':'orange'},'Mediterranean Sea')
    m.addLayer(samerica_region,{'color':'green'},'South Atlantic Ocean')

    m.addLayerControl()

    m.to_streamlit(height=700)


df_data = norwegian_med_samerica_df#[::20]#[['Atlantic', 'Indian', 'Pacific', 'Arctic', 'date']]
df_data['date'] = pd.to_datetime(df_data['Time'])
del df_data['Time']


st.info("""Use the slider to add and subtract an offset from the sea surface temperatures in the
different regions. 
          
       • What are the average sea surface temperatures in the different regions (over the last 13 years) to the nearest degree?
""")

a, b = st.columns([0.25,1])
#norwegian_offset = a.slider("Select norwegian offset", -25,25,0)
#med_offset = a.slider("Select Mediterranean offset", -25,25,0)
#med_offset = a.slider("Select Mediterranean offset", -25,25,0)

#df_data['SST_norwegian'] += norwegian_offset
#df_data['SST_med'] += med_offset

df_data_melted = pd.melt(df_data, id_vars=['date'])
df_data_melted = df_data_melted[df_data_melted['date'] >= datetime.datetime(2006,1,1)]

c = alt.Chart(df_data_melted, title='Measurements of sea surface temperatures since 2008').mark_line().encode(
     x='date', y='value',color='variable').interactive()

b.altair_chart(c, use_container_width=True)
#b.write(f"The average value of norwegian sea surface temperatures offset by {norwegian_offset}°C is {df_data['SST_norwegian'].mean():.2f}°C.")
#b.write(f"The average value of Mediterranean sea surface temperatures offset by {med_offset}°C is {df_data['SST_med'].mean():.2f}°C.")

form = a.form("my_form")
norwegian_ans = form.number_input("What is the average Norwegian sea surface temperature?", min_value=-27, max_value=27, value=0, step=1, help='Average sea surface temperature in the norwegian since 2006, in °C')
med_ans = form.number_input("What is the average Mediterranean sea surface temperature?", min_value=-27, max_value=27, value=0, step=1, help='Average sea surface temperature in the Mediterranean since 2008, in °C')
samerica_ans = form.number_input("What is the average sea surface temperature for the South Atlantic Ocean?", min_value=-27, max_value=27, value=0, step=1, help='Average sea surface temperature in the South Atlantic Ocean since 2006, in °C')
submit = form.form_submit_button("Check answers")

norwegian_median = df_data['SST_norwegian'].median()
med_median = df_data['SST_med'].median()
samerica_median = df_data['SST_samerica'].median()

#st.write(norwegian_median, med_median, samerica_median)

tol = 2 #correct answer within +/- tol degrees
if submit:
    if norwegian_ans <= norwegian_median-tol or norwegian_ans <= norwegian_median+tol:
        if med_ans >= med_median-tol and med_ans <= med_median+tol:
            if samerica_ans >= samerica_median-tol and samerica_ans <= samerica_median+tol:
                if st.session_state.well_done is False:
                    st.balloons()
                a.success('Well done!')
                st.session_state.well_done = True
            else:
                a.error('Almost! Double-check your South Atlantic Ocean answer.')
                st.session_state.well_done = False
        else:
            a.error('Incorrect. Double-check your Mediterranean Sea answer and try again.')
            st.session_state.well_done = False
    else:
        a.error('Incorrect. Double-check your Mediterranean Sea answer and try again.')
        st.session_state.well_done = False
