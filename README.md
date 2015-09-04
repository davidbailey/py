ad.py:

basemap.py: Uses Basemap and CoreLocation (via PyObjC), and bumpy to generate a map and highlight your location.

finance.py: Financial calculators.

freq.py: Uses pandas and matplotlib to plot a frequency.csv file.

getFlows.py: Uses lxml, pycurl, and pandas to query a Lancope API and download Netflows to a .csv file.

gis.py: Playing around with fiona, shapely, and descartes to draw maps.

gpx.py: Uses gpxpy to convert a gpx file into a list of points.

iphorse.py:

map.py: Uses openstreetmap (overly), shapley, and descartes to draw a map of primary roads in Los Angeles County.

nessus_report.py is a Python script that take a SQLite database containing Nessus vulnerability scan results, processes, them, and generates PDF reports. It is intended for large multi-department organizations that need to quickly sort through large amounts of scan data and create relevent reports for each department.

 1. Run a Nessus scan. Export the results as a .csv file.
 2. Add a department column with each department's name to each scan result file.
 3. Import the .csv files into a SQLite database.
 4. Run nessus_report.py.

risk.py: Playing around with plots.

splunk.py: Uses the Splunk API, geoip, ipwhois, pandas, numpy, and re to look up recent successful logins and track down the client computer.

splunkfile.py: Uses pandas and re to search through a spunk.csv file and find successful logins.

stocks.py: Playing around with lots of modules to look at stock market data, compute regressions, and create simulations.

trafficSim.py: A traffic simulation. Still in development.

transportationBook.py:

modules: A list of modules used in these files.

