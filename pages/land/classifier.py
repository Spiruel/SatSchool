import geemap.foliumap as geemap
import ee
import eemont
import streamlit.components.v1 as components
import datetime
import pandas as pd
import streamlit as st
import requests

from st_pages import add_indentation
add_indentation()

from streamlit_lottie import st_lottie_spinner

@st.cache_data()
def load_lottieurl(url: str):
  import requests
  r = requests.get(url)
  if r.status_code != 200:
      return None
  return r.json()

lottie_url_download = "https://assets8.lottiefiles.com/packages/lf20_nay3rc6w.json"
lottie_download = load_lottieurl(lottie_url_download)

gaul = ee.FeatureCollection("FAO/GAUL/2015/level2")
jamari = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Jamari'))
cujubim = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Cujubim'))
candeias_do_jamari = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Candeias Do Jamari'))
alto_paraiso = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Alto Paraiso'))
rio_crespo = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Rio Crespo'))
ariquemes = gaul.filter(ee.Filter.eq("ADM2_NAME", 'Ariquemes'))
merged_area = jamari.merge(cujubim).merge(candeias_do_jamari).merge(alto_paraiso).merge(rio_crespo).merge(ariquemes)
#merged_area = merged_area.map(lambda x: x.buffer(10000))]
merged_area = ee.Geometry.Polygon(\
        [[[-63.63427791340328, -8.677221255746861],\
          [-63.63427791340328, -9.913191896377663],\
          [-62.28295955402828, -9.913191896377663],\
          [-62.28295955402828, -8.677221255746861]]], None, False)    

a,b,c = st.columns([2,1,1]) 
a.write('''In the time it takes to say 'deforestation', another chunk of forest the size of a football pitch is destroyed.

That’s every two seconds, every single day.

Deforestation is the second largest leading cause of global warming. The rainforest also hosts the most biodiversity on the planet and provides food, livelihoods, and environmental protection from flooding and storms. As well as being the home for many indigenous peoples, who are under threat.

More than half the world's land-based plants and animals, and three-quarters of all birds, live in and around forests.
 
Forests have a big influence on rainfall patterns, water and soil quality and flood prevention too. Millions of people rely directly on forests as their home or for making a living. But the risks from deforestation go even wider. Trees absorb and store carbon dioxide. If forests are cleared, or even disturbed, they release carbon dioxide and other greenhouse gases.  
''')

st.info("""You are mapping deforestation in Brazil in 2018.
          
          1. Run the classifier to make a rough map of deforestation. Look at the map. Where does the classification work? Where does it not?
    2. Now, using the 'Draw a marker tool', add markers to the map.
    3. Click on the placed markers to find the longitude and latitude for different points of forest and not-forest. 
    4. Add one point of each using the input on the left hand side, and then rerun the classifier. How does the classification change?  
    5. How do you make the most accurate deforestation classification using as few points as possible?""")

b.image("https://eoimages.gsfc.nasa.gov/images/imagerecords/145000/145888/br163defores_tmo_amo_2019.gif", width=300)
c.image("https://eoimages.gsfc.nasa.gov/images/imagerecords/145000/145888/deforestationtimeseriesani_2013_2018.gif", width=300)

cola, colb = st.columns((0.5, 1))
with cola:
  st.write('')
  with st.form("Add training points"):
    lon = st.text_input("Longitude")
    lat = st.text_input("Latitude")
    label_class = st.radio("What is your label?", ['forest', 'not forest'])
    submitted = st.form_submit_button(label="Add point", help=None, on_click=None, args=None, kwargs=None) 

    if submitted:
      if lon.replace('.','',1).replace('-','',1).isdigit():
        lon = float(lon)
        if lat.replace('.','',1).replace('-','',1).isdigit():
          lat = float(lat)

          if lon > -180 and lon < 180 and lat > -90 and lat < 90:
            st.info(f"added lon: {lon:.2f}, lat: {lat:.2f}, class: {label_class}")

            if 'points' not in st.session_state:
              st.session_state.points = []
            st.session_state.points.append({'lon': lon, 'lat': lat, 'class': label_class})

          else:
            st.error("Invalid coordinates")
        else:
          st.error('Invalid latitude given.')
      else:
        st.error('Invalid longitude given.')

  reset_points = st.button('Reset points')
  df_cont = st.container()

  protected_area_check = st.checkbox('Show protected areas on the map')
  measurement_reg_check = st.checkbox('Show region we are measuring deforestation in on the map')

  if reset_points:
    st.session_state.points = []
  classifier_button = st.button('🪄 Run classifier! 🪄')

with colb:
  Map = geemap.Map(zoom=1, basemap=geemap.basemaps.get("Esri.WorldStreetMap"))

  # Define a region of interest as a point.  Change the coordinates
  # to get a classification of any place where there is imagery.
  roi = ee.Geometry.Point(-122.3942, 37.7295)

  l8 = ee.ImageCollection('LANDSAT/LC08/C02/T1')
  image = ee.Algorithms.Landsat.simpleComposite(**{
    'collection': l8.filterDate('2018-01-01', '2018-12-31'),
    'asFloat': True,
  })#.clip(merged_area)

  bands = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B10', 'B11']

  forest_coords = [(-63.0187, -9.3958), (-62.7688, -9.1735)]
  notforest_coords = [(-62.7921, -9.4486), (-62.6788, -9.044)]

  if 'points' in st.session_state:
    for c in st.session_state.points[:15]:
      if c['class'] == 'forest':
        forest_coords.append((c['lon'], c['lat']))
      else:
        notforest_coords.append((c['lon'], c['lat']))

  # Make a FeatureCollection from the hand-made geometries
  notforest_points_lst = []
  for c in notforest_coords:
    notforest_points_lst.append(ee.Geometry.Point(c))
  notforest_points = ee.FeatureCollection(notforest_points_lst)

  forest_points_lst = []
  for c in forest_coords:
    forest_points_lst.append(ee.Geometry.Point(c))
    forest_points = ee.FeatureCollection(forest_points_lst)
  
  # all_points = ee.FeatureCollection([
  #     ee.Feature(notforest_points_lst[0], {'class': 0}),
  #     ee.Feature(notforest_points_lst[1], {'class': 0}),
  #     ee.Feature(forest_points_lst[0], {'class': 1}),
  #     ee.Feature(forest_points_lst[1], {'class': 1}),
  # ])

  all_points_df = []
  for c in notforest_coords:
    all_points_df.append({'lon': c[0], 'lat': c[1], 'class': 'not forest'})
  for c in forest_coords:
    all_points_df.append({'lon': c[0], 'lat': c[1], 'class': 'forest'})
  # if 'points' in st.session_state:
  #   all_points_df += st.session_state.points

  all_points = []
  for row in all_points_df:
    point = ee.Geometry.Point((row['lon'], row['lat']))
    all_points.append( ee.Feature(point, {'class': 0 if row['class'] == 'not forest' else 1}) )
  all_points = ee.FeatureCollection(all_points)

  df = pd.DataFrame(all_points_df)
  if len(df) > 15:
    df_cont.error('Too many points! Reset points to add new points.')

  df[['lon','lat']] = df[['lon','lat']].round(2)
  with df_cont:
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df)

  # Display the classification result and the input image.
  # Map.setCenter(-62.836, -9.2399, 9)
  Map.centerObject(merged_area,8)
  Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'max': 0.5, 'gamma': 2}, 'Cloudless Landsat-8 imagery 2018')

  Map.addLayer(forest_points, {'color':'#90EE90'}, 'training forest points')
  Map.addLayer(notforest_points, {'color':'red'}, 'training not-forest points')

  if protected_area_check:
    dataset = ee.FeatureCollection('WCMC/WDPA/current/polygons')
    Map.addLayer(dataset, {'color': 'green'}, 'WDPA Protected Areas', True, 0.85)

  styleParams = {
     'fillColor': 'b5ffb4',
     'color': '00909F',
     'width': 1.0
   }
  if measurement_reg_check:
    Map.addLayer(merged_area, {'opacity': 0.5}, 'measurement region')

  if classifier_button:
    #with st.spinner('Doing some classification magic...'):
    with st_lottie_spinner(lottie_download, key="classification magic", width=200):
      # Get the values for all pixels in each polygon in the training.

      training = image.sampleRegions(**{
        # Get the sample from the polygons FeatureCollection.
        'collection': all_points,
        # Keep this list of properties from the polygons.
        'properties': ['class'],
        # Set the scale to get Landsat pixels in the polygons.
        'scale': 30
      })

      # Create an SVM classifier with custom parameters.
      classifier = ee.Classifier.libsvm(**{
        'kernelType': 'RBF',
        'gamma': 0.5,
        'cost': 10
      })

      # Train the classifier.
      trained = classifier.train(training, 'class', bands)

      # Classify the image.
      classified = image.classify(trained)

      areaImage = classified.multiply(ee.Image.pixelArea());
      # Calculate the area of loss pixels in the merged area.
      stats = areaImage.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': merged_area,
        'scale': 100,
        'maxPixels': 1e9
      })

      
      Map.addLayer(classified,
                  {'min': 0, 'max': 1, 'palette': ['red', 'green']},
                  'deforestation')

  Map.addLayerControl()
  Map.to_streamlit()

with colb:
  # rel_counts = pd.DataFrame(data=df_data, columns=["atlantic"])
  # st.table(rel_counts.style.format("{:.2f}"))
  labels_ = ['forest', 'not forest']
  import numpy as np
  import altair as alt

  if classifier_button:
    st.write(f"You used {len(df)} points to classify deforestation, with {len(df[df['class'] == 'not forest'])} points\
           being labelled as forest and {len(df[df['class'] == 'forest'])} points being labelled as not forest.\
           Can you see where the classification has done well, and where it hasn't done well? Why do you think this?")
    # Get a confusion matrix representing train accuracy.
    trainAccuracy = trained.confusionMatrix()

    # # Get a confusion matrix representing expected accuracy.
    # testAccuracy = validated.errorMatrix('Land_Cover_Type_1', 'classification')
    # st.write('Validation error matrix: ', testAccuracy.getInfo())
    # st.write('Validation overall accuracy: ', testAccuracy.accuracy().getInfo())

    # with st.expander('test'):
    #   st.write('Resubstitution error matrix: ', trainAccuracy.getInfo())
    train_acc_result = trainAccuracy.accuracy().getInfo()*100
    st.write(f'The overall (training) accuracy is {train_acc_result:.0f}%. This means that the points you used for the\
      classifier are {train_acc_result:.0f}% accurate when compared to the map produced by the classifier.')

    # with st.expander('Read more about your accuracy results:'):
    #   cm = np.array(trainAccuracy.getInfo()) #confusion_matrix(y_true, y_pred)
    #   cm = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])
    #   labels_repeated = []
    #   for _ in range(np.unique(labels_).shape[0]):
    #       labels_repeated.append(np.unique(labels_))
    #   source = pd.DataFrame({'predicted class': np.transpose(np.array(labels_repeated)).ravel(),
    #                       'true class': np.array(labels_repeated).ravel(),
    #                       'fraction': np.round(cm.ravel(), 2)})
    #   #st.dataframe(source)
    #   heat = alt.Chart(source, height=500, width=500, title="confusion matrix").mark_rect(opacity=0.7).encode(
    #       x='predicted class:N',
    #       y='true class:N',
    #       color=alt.Color('fraction:Q', scale=alt.Scale(scheme='blues')),
    #       tooltip="fraction")

    #   st.info('This is a confusion matrix. It shows the number of times a prediction was made for a given class,\
    #           and the number of times the prediction was correct. The diagonal shows the number of times the prediction\
    #             was correct for that class. The off-diagonal shows the number of times the prediction was correct for a\
    #               different class. The higher the number in the diagonal, the better the prediction. The lower the number\
    #                 in the off-diagonal, the better the prediction.')

    #   st.altair_chart(heat)

    st.subheader('According to your deforestation classifier:')
    with st.spinner('Loading...'):
      total_area = 24225
      forest_area = stats.getInfo()['classification']*1e-6
      st.metric(label="Amount of area marked as forested in measurement region", value=f'{forest_area:.0f} square kilometres ({forest_area/total_area*100:.0f}%)')
      st.metric(label="Total area of the measurement region", value=f'{total_area:.0f} square kilometres')
      #stateArea = merged_area.geometry().area()
      #stateAreaSqKm = ee.Number(stateArea).divide(1e6).round()
      #st.write(stateAreaSqKm.getInfo())

  area_ans = st.number_input('How much area in the measured region is not forest? (in sqkm)', step=100, help='Nearest 100 sqkm')
  if area_ans == 8200: #total_area - forest_area
    st.success('You are correct!')
    st.balloons()
