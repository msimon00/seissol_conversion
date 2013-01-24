import numpy as np
import os
from obspy.core import UTCDateTime, Trace, Stream




def match_station_to_outputfile(stations, output_directory):
    st=Stream()
    already_used_stations=set()
    matches=[]
    for i, station in enumerate(stations):
        if station['id'] not in already_used_stations:
            i=i+1 
            pickpoint=os.path.join(output_directory,'*-pickpoint-%s-*.dat' % str(i).zfill(5))
            filename=glob(pickpoint)
            try:
                f=open(filename[0])
                f.close()
                matches.append(station, filename[0])
            except:
                print 'cant find ', pickpoint
                sys.exit()
    return matches

def convert_seismograms(station={}, starttime=UTCDateTime(), output_file=''):
    st=Stream()
    try:
        f=open(output_file)
    except:
        print 'cant find ', output_file
        sys.exit()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    data=np.fromfile(file=f, count=-1, sep=" ")
    npts=int(len(data)/4)
    data=np.reshape(data, (npts, 4))
    timestep=data.transpose()[0][1]-data.transpose()[0][0]
    data=data.transpose()[1:]
    data=data.transpose()
    lat= station['latitude']/180*np.pi
    lon= station['longitude']/180*np.pi
    def rot_XYZ_to_ENZ(x,y,z):
        E= - np.cos(lat)*np.cos(lon)*x - np.cos(lat)*np.sin(lon)*y + np.sin(lat)*z
        N= - np.sin(lon)*x + np.cos(lon)*y
        Z=   np.sin(lat)*np.cos(lon)*x + np.sin(lat)*np.sin(lon)*y + np.cos(lat)*z
        return E,N,Z
    data[0],data[1],data[2]=rot_XYZ_to_ENZ(data[0],data[1],data[2])
    data=data.transpose()
    for j, channel in enumerate(['BHE','BHN','BHZ']):
        stats = {'network': station['network'], 'station': station['code'], \
        'location': station['location'],'latitude': station['latitude'], 'longitude':station['longitude'], 'channel':channel,\
        'npts' : len(data[j]), 'sampling_rate': 1/timestep,'mseed':{'dataquality':'D'},\
        'starttime' : starttime,'endtime':starttime+timestep*npts}
        outputdata=np.require(data[j],requirements=['C_CONTIGUOUS'])
        tr=Trace(data=outputdata, header=stats)
        st+=Stream(tr)
    return st



#test:

stations=["tests_data/dataless.seed.BW_FURT", "tests_data/dataless.seed.BW_RJOB"]
output_directory='seissol_out'

match=match_station_to_outputfile(stations, output_directory')

#warning, elements of 'stations' do not yes meet requirements for conversion?

#requirements of station:
station={}
station['network']='EXAM'
station['code']='PLE'
station['location']=''
station['latitude']=90.0
station['longitude']=90.0
starttime=UTCDateTime(2000,1,1)
st=convert_seismograms(station, starttime, 'test_data/out-pickpoint-00001-00015.dat')
