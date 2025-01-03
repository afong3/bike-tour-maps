import pandas as pd
import glob 
import gpxpy
import numpy as np
import srtm
from scipy.interpolate import RegularGridInterpolator

def load_data(min_lon = None, min_lat = None, max_lon = None, max_lat = None): 
    files = glob.glob("./activities_gpx/*.gpx")
    
    in_bounds = []
    for file in files:
        gpx_file = open(file, 'r')
        gpx = gpxpy.parse(gpx_file)

        bounds = gpx.tracks[0].segments[0].get_bounds()
        
        # GPX without bounds should not be included
        if bounds is None:
            continue
        
        q1 = gpx.tracks[0].segments[0].points[int(len(gpx.tracks[0].segments[0].points) / 4)] 
        q2 = gpx.tracks[0].segments[0].points[int(len(gpx.tracks[0].segments[0].points) / 2)] 
        q3 = gpx.tracks[0].segments[0].points[int(len(gpx.tracks[0].segments[0].points) * 3 / 4)]  
        q4 = gpx.tracks[0].segments[0].points[int(len(gpx.tracks[0].segments[0].points) - 1)] 

        test_points = np.array([(q1.longitude, q1.latitude),(q2.longitude, q2.latitude), (q3.longitude, q3.latitude), (q4.longitude, q4.latitude) ])

        filter = np.logical_and(test_points[:, 0] > min_lon, np.logical_and(test_points[:,0] < max_lon, np.logical_and(test_points[:, 1] > min_lat, test_points[:,1] < max_lat)))
        # Filter by bounding box
        if bounds.min_latitude > min_lat and bounds.max_latitude < max_lat and bounds.min_longitude > min_lon and bounds.max_longitude < max_lon:
            in_bounds.append(gpx)
        elif sum(filter) > 0:
            in_bounds.append(gpx)

    return in_bounds 

def gpx_to_array(gpx_list):
    # Need to make separate the activites from each other otherwise the plotting is going to have a straight line jumping around 
    i = 0
    for activity in gpx_list:
        for track in activity.tracks:
            for segment in track.segments:
                for point in segment.points:
                    if i == 0:
                        coords = np.array([point.longitude, point.latitude, point.elevation, i])
                    else:
                        coords = np.vstack([coords, np.array([point.longitude, point.latitude, point.elevation, i])])
        i += 1

    return coords

def latlon_to_xy(coords, min_lon, min_lat, max_lon, max_lat, max_x = 300, max_y = 150):
    coords[:,0] = (coords[:,0] - min_lon) / (max_lon - min_lon) * (max_x - 1) # longitude
    coords[:,1] = (coords[:,1] - min_lat) / (max_lat - min_lat) * (max_y - 1) # latitude

    coords = coords[coords[:, 0] >= 0]
    coords = coords[coords[:, 0] < (max_x - 1)]
    coords = coords[coords[:, 1] >= 0]
    coords = coords[coords[:, 1] < (max_y - 1)]
    return coords 

def floor_y(coords):
    coords = np.hstack([coords, np.floor(coords[:, 1]).reshape([-1, 1])])

    return coords 

def interpolate_elevation(coords, values):
    x = np.arange(0, values.shape[1], 1)
    y = np.arange(0, values.shape[0], 1)
    interp = RegularGridInterpolator((y, x), values)
    elevations = interp(coords[:, (1, 0)])
    coords[:, 2] = elevations

    return coords

def offset_elevations(coords):
    coords = np.hstack([coords, (coords[:, 2] + (-6 * coords[:,4])).reshape([-1,1])])

    return coords

def main():
    gpx_list = load_data(19.649048,42.383214,20.319214,42.787413)
    coords_arr = gpx_to_array(gpx_list)
    coords_arr = latlon_to_xy(coords_arr, 19.649048,42.383214,20.319214,42.787413, max_x = 300, max_y = 150)
    coords_arr = floor_y(coords_arr)
    coords_arr = offset_elevations(coords_arr)
    print(coords_arr)
if __name__ == "__main__":
    main()