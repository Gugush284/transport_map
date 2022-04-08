import folium

map = folium.Map(location=[55.752004, 37.617734],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 10)

a = [55.752004, 55.852004]
b = [37.617734, 37.617734]
points = []


for i in range(2):
    folium.Marker(location=[a[i], b[i]], popup = "Point", icon=folium.Icon(color = 'red')).add_to(map)
    points.append([a[i], b[i]])
folium.PolyLine(points, color="red").add_to(map)

map.save("map1.html")