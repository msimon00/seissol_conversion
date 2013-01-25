contains two functions

match_station_to_outputfile(stations, output_directory) and convert_seismograms(station={}, starttime=UTCDateTime(), output_file='')


the main problem is, that seissol keeps no record about what "station" each pick point refers to. The only way to keep track of that (for now) is to "remember" the order the pick points were generated in the input file or check against the X,Y,Z coordinates converted back to lat/lon.


