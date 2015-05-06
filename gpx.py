import gpxpy

gpx_file = open("file", 'r')
gpx = gpxpy.parse(gpx_file)

points = []
for point in gpx.tracks[0].segments[0].points:
 points.append((point.latitude,point.longitude,point.elevation,point.time))
