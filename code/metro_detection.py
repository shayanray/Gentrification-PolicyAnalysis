import requests
import fiona
import geopandas as gp
from shapely import speedups
from shapely.geometry import LineString, MultiLineString
import numpy as np
import pandas as pd
speedups.disable()
gp.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
gp.io.file.fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'


Amtrak_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Metro\Amtrak_Stations.kml"
orange_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Metro\Metro_Orange_Line_2019.shp"
metroSta_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Metro\Metro_Stations.kml"
metrolinkSta_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Metro\Metrolink_Stations.kml"
la_metroSta_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Metro\LA_Metro\Lines.shp"
median_income_pth = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Data\Income_2016\Median_Household_Income__2016_.shp"


df_amtrak = gp.read_file(Amtrak_path, driver='LIBKML')
df_orange = gp.read_file(orange_path)
df_metroSta = gp.read_file(metroSta_path, driver='LIBKML')
df_metrolinkSta = gp.read_file(metrolinkSta_path, driver='LIBKML')
df_la = gp.read_file(la_metroSta_path)

df_income = gp.read_file(median_income_pth)[["GEOID10","geometry"]]


df_points = gp.GeoDataFrame(pd.concat([df_amtrak, df_metroSta, df_metrolinkSta],ignore_index=True))
df_lines = gp.GeoDataFrame(pd.concat([df_orange, df_la],ignore_index=True))

bad_geoids_points = df_income.geometry.apply(lambda x: df_points.geometry.within(x).any())
bad_geoids_lines = df_income.geometry.apply(lambda x: df_lines.geometry.intersects(x).any())

bad_geoids = bad_geoids_points | bad_geoids_lines

good_geoids = ~bad_geoids

mask = df_income[good_geoids]["GEOID10"].values

data_path = r"C:\Users\Óscar García\Documents\MIT Policy Challenge 2020\Script\Gentrification_merge\Median_Income_Gentrification.csv"

df_data=pd.read_csv(data_path)
df_depurated = df_data[df_data['GEOID10'].isin(mask)]

#interesting_columns=[""]
#df_depurated=df_depurated[interesting_columns]

df_depurated.to_csv("depurated_dataset.csv")