from celery import shared_task
import logging
from django.utils import timezone
from datetime import datetime
import pytz
from django.shortcuts import get_object_or_404

from .models import AWSStation, StationData, TrainStation
from .utils.aws import fetch_aws_data
from .utils.daily_prediction import predict_day1, predict_day2, predict_day3
from .utils.gfs import download_gfs_data


logger = logging.getLogger(__name__)

@shared_task
def scheduled_15_min():
    fetch_and_store_data()
    update_trainstations()
    logger.info("-----------------------15 Min Task Done")
    

@shared_task
def scheduled_daily():
    download_gfs_data()
    predict_day1()
    predict_day2()
    predict_day3()
    logger.info("++++++++++++++++++++++++Daily Prediction Done")
#---------------------------------------------------------------------------------------------------------------------

def fetch_and_store_data():
    stations = AWSStation.objects.all()
    for station in stations:
        data = fetch_aws_data(station.station_id)
        if data:
            save_station_data(station, data)
            
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone)


def save_station_data(station, data):
    rainfall = data.get('rain', 0)
    temperature = data.get('temp_out', 0)
    humidity = data.get('out_humidity', 0)
    wind_speed = data.get('wind_speed', 0)
    
    StationData.objects.create(
        station=station,
        rainfall=rainfall,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        timestamp=timezone.now()
    )

def update_trainstations():
    all_stations = TrainStation.objects.all()
    for station in all_stations:
        station.update()
           
    ist_timezone = pytz.timezone('Asia/Kolkata')
    current_time_ist = datetime.now(ist_timezone)
