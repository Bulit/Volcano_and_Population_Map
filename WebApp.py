from turtle import color, fillcolor
from unicodedata import name
import folium
import pandas

#Read CSV volcano file
data = pandas.read_csv('volcano.csv')
#Get Latitude,Longitude, volcano name and elevation from dataFrame and save it to variable
lat = list(data['Latitude'])
lon = list(data['Longitude'])
volc_name = list(data['Volcano Name'])
elev = list(data['Elevation'])
#Define function to set markers color depending on volcano elevation lvl
def color_elev(elevation):
    if elevation <= 1000:
        return 'green'
    elif elevation >1001 and elevation <=3000:
        return 'blue'
    elif elevation >3001 and elevation <=5000:
        return 'orange'
    else:
        return 'red'
    
#Create map object with starting location, zoom and map type Stemen Terrain
map = folium.Map(location=[50.05, 21.25], zoom_start=9, tiles='Stamen Terrain')

fgv = folium.FeatureGroup('Volcanos')
#Using zip function to iterate through two or more lists
for lt, ln, v_nm, elv in zip(lat, lon, volc_name, elev):
    #Add marker to every postion in lists on map   /// Use for folium.Marker - icon=folium.Icon(color=color_elev(elv))
    #instead of fillcolor=color_elev(elv), color='grey', fill = True, fill_opacity=0.7
    fgv.add_child(folium.CircleMarker(location = [lt, ln], radius= 6, popup=v_nm + '\nElevation:' + str(elv) + 'm',
    color=color_elev(elv), fill = True, fill_opacity=0.4))

fgp = folium.FeatureGroup('Population')
#Loading population GEODATA from world.json
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
#Set colors of filling for country depending of their populations
#green if below 10mil, orange for between 10mil and 20mil and red for above 20mil
style_function=(lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'})))


map.add_child(fgv)
map.add_child(fgp)

#Adding layer control as a child
map.add_child(folium.LayerControl())

#Save map to file.html
map.save('map1.html')