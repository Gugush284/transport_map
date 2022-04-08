import folium

map = folium.Map(location=[55.752004, 37.617734],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 10)
map.save("map1.html")