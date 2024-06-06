
import requests
import shutil
import datetime as dt
from datetime import datetime, timedelta
import time
import os 
from django.conf import settings


def download_gfs_data():
    x = dt.datetime.now().replace(second=0, microsecond=0)
    hour=6
    day = x.day
    month = x.month
    year = x.year
    pdate = datetime(year, month, day, 11, 00, 00).strftime("%Y%m%d")
    direc = os.path.join(settings.BASE_DIR,'files', datetime.now().strftime("%d-%m-%Y"))
    
    direc_prev = os.path.join(settings.BASE_DIR,'files', (datetime.now() - timedelta(days=1)).strftime("%d-%m-%Y"))
    
    #delete old files with yesterday date
    os.system("rm -rf "+direc_prev)
    
    # create new mkdir
    os.mkdir(direc)
    os.chdir(direc)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f003&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f003", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f006&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f006", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f009&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f009", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
            
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f012&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f012", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f015&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f015", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f018&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f018", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f021&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f021", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f024&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f024", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f027&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f027", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
            
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f030&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f030", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f033&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f033", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f036&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f036", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f039&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f039", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f042&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f042", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f045&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f045", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
            
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f048&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f048", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f051&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f051", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f054&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f054", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f057&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f057", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f060&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f060", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f063&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f063", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f066&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f066", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f069&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f069", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f072", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f075", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f078", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f081", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f084", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f087", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f090", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f093", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f096", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f099", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f102", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f105", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f108", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f111", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f114", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f117", 'wb') as f:
        shutil.copyfileobj(r.raw, f)


    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f120", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f123", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f126", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f129", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f132", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f135", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f138", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f141", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f144", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f147", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f150", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f153", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f156", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f159", 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    url="https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl?dir=%2Fgfs."+pdate+"%2F"+str(hour).zfill(2)+"%2Fatmos&file=gfs.t"+str(hour).zfill(2)+"z.pgrb2.0p25.f072&var_PRATE=on&var_UGRD=on&var_VGRD=on&lev_10_m_above_ground=on&lev_surface=on&subregion=&toplat=20&leftlon=72&rightlon=74&bottomlat=18"  
    r = requests.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    with open(f"gfs.t0{hour}z.pgrb2.0p25.f162", 'wb') as f:
        shutil.copyfileobj(r.raw, f)

    os.chdir('../')

