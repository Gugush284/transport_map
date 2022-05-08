import folium
from folium.plugins import MarkerCluster

map = folium.Map(location=[55.752004, 37.617734],
                min_zoom=8, 
                max_zoom=18, 
              zoom_start = 10)

f = open("E:/databasa.txt", "r", encoding='utf-8')
i = 0
k = 0
name = ""
buf = ""
N = 0
x = 1.1
y = 1.1
points = []
names = []
for line in f:
    N = N + 1
    i = 0
    while(line[i] != '3' or line[i+1] != '7' or line[i+2] != '.'):
        name = name + line[i]
        i = i + 1
    name = name[:len(name)-1]
    k = i
    while(line[k] != ' '):
        buf = buf + line[k]
        k = k + 1
    x = float(buf)
    buf = ""
    k = k + 1
    while(line[k] != ' '):
       buf = buf + line[k]
       k = k + 1
    y = float(buf)
    points.append([y, x])
    names.append(name)
    buf = ""
    name = ""

print(N)
print(names[N-1])
marker_cluster = MarkerCluster().add_to(map)

for i in range(len(names)):
    folium.CircleMarker(location=points[i],radius=9, popup = names[i], fill_color="red", color="gray", fill_opacity = 0.9).add_to(marker_cluster)


map.save("map.html")
