import os
import requests
import pygrib
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import copy
from tensorflow.keras.models import Sequential, load_model
from django.conf import settings
from awsstations.models import AWSStation, DaywisePrediction
import copy
import shutil

stations = AWSStation.objects.all()
         
def predict_day1():
    forecast_hr = np.arange(15,85,3)
    latbounds = [ 18.5 - 0.25 , 19.5 ]
    lonbounds = [ 72.5 , 73.5 + 0.25 ]

    time_from_ref = np.arange(15,85,3)
    columns_prec = []

    for i in ['Prec']:
        for time_steps in forecast_hr:
            for j in np.arange(19.5,18.25,-0.25):
                for k in np.arange(72.5,73.75,0.25):
                    columns_prec.append(f'{i}_{j}_{k}_{time_steps:03d}')


    x = datetime.now().replace(second=0, microsecond=0)
    pd.to_datetime(x)
    day=x.day
    month = x.month
    year = x.year


    start_day = f'{year}-{month}-{day}'
    end_day = pd.to_datetime(start_day) + timedelta(hours=24)
    data_prec = pd.DataFrame(index =[pd.to_datetime(start_day) + timedelta(hours=6)], columns = columns_prec)
    root_directory = os.path.join(settings.BASE_DIR,"files", f"{day:02d}-{month:02d}-{year}")


    for time_step in data_prec.index:
        
        year = time_step.year
        month = time_step.month
        day = time_step.day

        ref_time = time_step.hour
        
        date_temp = pd.date_range(start = time_step + timedelta(hours = 15), end = time_step + timedelta(hours = 84) , freq = '3H')
        col_temp = np.arange(0,25)
        
        data_temp = pd.DataFrame(index  = date_temp, columns=col_temp)
        
        for time_lag in time_from_ref:
            
            filename =f'gfs.t{ref_time:02d}z.pgrb2.0p25.f{time_lag:03d}'
            
            grib = f'{root_directory}/{filename}'
            grbs = pygrib.open(grib)
            variable_name_to_select = 'Precipitation rate' 
            
            for grb in grbs.select(name=variable_name_to_select):
                data = grb.values
                latitudes, longitudes = grb.latlons()  
                parameter_name = grb.name  
                level_type = grb.typeOfLevel 
                level_value = grb.level  
                valid_time = grb.validDate 
                
            latli = 2
            latui = 7 
            lonli = 2
            lonui = 7
            
            time = pd.to_datetime(f'{year}-{month}-{day}') + timedelta(hours = int(int(ref_time) + int(time_lag)))
            data = data[latli:latui,lonli:lonui][::-1]
            time_prev = time - timedelta(hours = 3)

            if ((int(time_lag)%6) == 0):
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] =  (np.ravel(data)*21600) - np.ravel(data_temp.loc[time_prev][0:25])

            elif ((int(time_lag)%6) != 0) & ((int(time_lag)%3) == 0):
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] =  (np.ravel(data)*10800)
            else:
                print(filename)
                
        data_prec.loc[time_step][0:600] = np.ravel(data_temp)
        

    data_prec = data_prec.shift(freq=pd.Timedelta(hours=17, minutes=30))
    data_prec.head()
    data_prec.columns = map(str, data_prec.columns)

    common_prefix = 'Prec_19.25_72.5','Prec_19.25_72.75','Prec_19.25_73.0','Prec_19.25_73.25','Prec_19.0_72.5','Prec_19.0_72.75','Prec_19.0_73.0','Prec_19.0_73.25','Prec_18.75_72.5','Prec_18.75_72.75','Prec_18.75_73.0','Prec_18.75_73.25','Prec_18.5_72.5','Prec_18.5_72.75','Prec_18.5_73.0','Prec_18.5_73.25'
    selected_columns = [col for col in data_prec.columns if col.startswith(common_prefix) and '015' <= col[-3:] <= '084']
    data_prec = data_prec[selected_columns]

    data_prec=data_prec.iloc[:,:128]
    n_samples_test = data_prec.shape[0]
    X_test_prec_cnn_lstm = np.full((n_samples_test,8,4,4),np.nan)

    for i in range(data_prec.shape[0]):
        temp_array = np.full((8,4,4),np.nan)
        counter = 0
        for j in np.arange(15,37,3):
            selected_cols = data_prec.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4,-1)
            counter +=1
        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)
    X_test_prec_cnn_lstm_daily = np.full((n_samples_test,1,4,4),np.nan)

    for i in range(X_test_prec_cnn_lstm_daily.shape[0]):
        X_test_prec_cnn_lstm_daily[i,0,:,:] = np.sum(X_test_prec_cnn_lstm[i,0:8,:,:], axis = 0)
        
    X_test_prec_cnn_lstm_reshaped = np.expand_dims(X_test_prec_cnn_lstm_daily, axis=1)
    X_test_prec_cnn_lstm_reshaped = np.moveaxis(X_test_prec_cnn_lstm_reshaped, 1, -1)

    lat_lon = []

    for i in np.arange(18.5,19.5+0.25,0.25):
        for j in np.arange(72.5, 73+0.25,0.25):

            lat_lon.append([i,j])

    lat_lon = np.array(lat_lon)
    lat_lon=lat_lon.astype(float)
    
    def find_closest_pair(lat_lon_array, target_lat, target_lon):
        delta_lat = lat_lon_array[:, 0] - target_lat
        delta_lon = lat_lon_array[:, 1] - target_lon
        
        distances = np.sqrt(delta_lat**2 + delta_lon**2)
        closest_index = np.argmin(distances)
        return lat_lon_array[closest_index]

    dict_stations = {}
    for station in stations:
        model1_path = os.path.join(settings.BASE_DIR, f'files/Lead Day 1/{station.name}_1/tl.h5')
        model_path = os.path.join(settings.BASE_DIR, f'files/Lead Day 1/{station.name}_1/CNN.h5')
        
        model = load_model(model_path)
        model1 = load_model(model1_path)
        
        predictions = model.predict(X_test_prec_cnn_lstm_reshaped)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped)
        
        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station.name] = pd.DataFrame()

        closest_lat_lon = find_closest_pair(lat_lon, station.latitude, station.longitude)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        
        data_GFS_prec_stationwise_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3'])
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        
        y_pred_gfs = np.array(data_GFS_prec_stationwise_daily[f'{station.name}']).astype(float)

        predictions_GFS = y_pred_gfs[:, 0]

        GFS = y_pred_gfs[:, 0]
        GFS2 = y_pred_gfs[:, 1]
        GFS3 = y_pred_gfs[:, 2]
        CNN = predictions
        TL = predictions1
        Df = pd.DataFrame(columns=['GFS', 'GFS2', 'GFS3', 'TL', 'CNN'])
        Df['GFS'] = GFS
        Df['GFS2'] = GFS2
        Df['GFS3'] = GFS3
        Df['CNN'] = CNN
        Df['TL'] = TL
        threshold = np.percentile(Df['GFS'], 90)
        Df['Final'] = Df.apply(
            lambda x: x['TL'] if (x['GFS'] > threshold) or (x['GFS2'] > threshold) or (x['GFS3'] > threshold) else x['CNN'],
            axis=1)
        predicted_values = Df['Final']
        predicted_values = predicted_values.tolist()
        print('-----------------------------------------------------------------------------------------------------------')
        DaywisePrediction.objects.create(station=station, day1_rainfall=float(predicted_values[0]), timestamp=datetime.now())

def predict_day2():
    forecast_hr = np.arange(15, 157, 3)
    latbounds = [18.5 - 0.25, 19.5]
    lonbounds = [72.5, 73.5 + 0.25]
    time_from_ref = np.arange(15, 157, 3)

    columns_prec = []
    for i in ['Prec']:
        for time_steps in forecast_hr:
            for j in np.arange(19.5, 18.25, -0.25):
                for k in np.arange(72.5, 73.75, 0.25):
                    columns_prec.append(f'{i}_{j}_{k}_{time_steps:03d}')

    x = datetime.now().replace(second=0, microsecond=0)
    pd.to_datetime(x)
    day = x.day
    month = x.month
    year = x.year

    start_day = f'{year}-{month}-{day}'
    end_day = pd.to_datetime(start_day) + timedelta(hours=24)
    data_prec = pd.DataFrame(index=[pd.to_datetime(start_day) + timedelta(hours=6)], columns=columns_prec)
    root_directory = os.path.join(settings.BASE_DIR,"files", f"{day:02d}-{month:02d}-{year}")

    for time_step in data_prec.index:
        year = time_step.year
        month = time_step.month
        day = time_step.day
        ref_time = time_step.hour
        
        date_temp = pd.date_range(start=time_step + timedelta(hours=15), end=time_step + timedelta(hours=156), freq='3H')
        col_temp = np.arange(0, 25)
        data_temp = pd.DataFrame(index=date_temp, columns=col_temp)
        
        for time_lag in time_from_ref:
            filename = f'gfs.t{ref_time:02d}z.pgrb2.0p25.f{time_lag:03d}'
            grib = f'{root_directory}/{filename}'
            grbs = pygrib.open(grib)
            variable_name_to_select = 'Precipitation rate'

            for grb in grbs.select(name=variable_name_to_select):
                data = grb.values
                latitudes, longitudes = grb.latlons()
                parameter_name = grb.name
                level_type = grb.typeOfLevel
                level_value = grb.level
                valid_time = grb.validDate

            latli = 2
            latui = 7
            lonli = 2
            lonui = 7

            time = pd.to_datetime(f'{year}-{month}-{day}') + timedelta(hours=int(int(ref_time) + int(time_lag)))
            data = data[latli:latui, lonli:lonui][::-1]
            time_prev = time - timedelta(hours=3)

            if (int(time_lag) % 6) == 0:
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] = (np.ravel(data) * 21600) - np.ravel(data_temp.loc[time_prev][0:25])
            elif (int(time_lag) % 6) != 0 and (int(time_lag) % 3) == 0:
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] = (np.ravel(data) * 10800)
            else:
                print(filename)

        data_prec.loc[time_step][0:1200] = np.ravel(data_temp)
        
    data_prec = data_prec.shift(freq=pd.Timedelta(hours=17, minutes=30))
    data_prec.columns = map(str, data_prec.columns)

    common_prefix = 'Prec_19.25_72.5', 'Prec_19.25_72.75', 'Prec_19.25_73.0', 'Prec_19.25_73.25', 'Prec_19.0_72.5', 'Prec_19.0_72.75', 'Prec_19.0_73.0', 'Prec_19.0_73.25', 'Prec_18.75_72.5', 'Prec_18.75_72.75', 'Prec_18.75_73.0', 'Prec_18.75_73.25', 'Prec_18.5_72.5', 'Prec_18.5_72.75', 'Prec_18.5_73.0', 'Prec_18.5_73.25'
    selected_columns = [col for col in data_prec.columns if col.startswith(common_prefix) and '015' <= col[-3:] <= '156']

    data_prec = data_prec[selected_columns]
    data_prec = data_prec.iloc[:, 128:256]

    n_samples_test = data_prec.shape[0]

    X_test_prec_cnn_lstm = np.full((n_samples_test, 8, 4, 4), np.nan)

    for i in range(data_prec.shape[0]):
        temp_array = np.full((8, 4, 4), np.nan)
        counter = 0
        
        for j in np.arange(39, 61, 3):
            selected_cols = data_prec.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4, -1)
            counter += 1
            
        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)

    X_test_prec_cnn_lstm_daily = np.full((n_samples_test, 1, 4, 4), np.nan)

    for i in range(X_test_prec_cnn_lstm_daily.shape[0]):
        X_test_prec_cnn_lstm_daily[i, 0, :, :] = np.sum(X_test_prec_cnn_lstm[i, 0:8, :, :], axis=0)

    X_test_prec_cnn_lstm_reshaped = np.expand_dims(X_test_prec_cnn_lstm_daily, axis=1)
    X_test_prec_cnn_lstm_reshaped = np.moveaxis(X_test_prec_cnn_lstm_reshaped, 1, -1)

    lat_lon = []
    for i in np.arange(18.5, 19.5 + 0.25, 0.25):
        for j in np.arange(72.5, 73 + 0.25, 0.25):
            lat_lon.append([i, j])
    lat_lon = np.array(lat_lon)
    lat_lon = lat_lon.astype(float)

    def find_closest_pair(lat_lon_array, target_lat, target_lon):
        delta_lat = lat_lon_array[:, 0] - target_lat
        delta_lon = lat_lon_array[:, 1] - target_lon
        distances = np.sqrt(delta_lat**2 + delta_lon**2)
        closest_index = np.argmin(distances)
        return lat_lon_array[closest_index]

    dict = {}

    for station in stations:
        model1_path = os.path.join(settings.BASE_DIR, f'files/2DayLead/{station.name}/tl.h5')
        model_path = os.path.join(settings.BASE_DIR, f'files/2DayLead/{station.name}/CNN2122old.h5')
        
        
        model = load_model(model_path)
        model1 = load_model(model1_path)

        predictions = model.predict(X_test_prec_cnn_lstm_reshaped)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped)

        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station] = pd.DataFrame()
        

        closest_lat_lon = find_closest_pair(lat_lon, station.latitude, station.longitude)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        
        data_GFS_prec_stationwise_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3'])
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        
        y_pred_gfs = np.array(data_GFS_prec_stationwise_daily[f'{station.name}']).astype(float)
        predictions_GFS = y_pred_gfs[:, 0]

        GFS = y_pred_gfs[:, 0]
        GFS2 = y_pred_gfs[:, 1]
        GFS3 = y_pred_gfs[:, 2]
        CNN = predictions
        TL = predictions1
        Df = pd.DataFrame(columns=['GFS', 'GFS2', 'GFS3', 'TL', 'CNN'])
        Df['GFS'] = GFS
        Df['GFS2'] = GFS2
        Df['GFS3'] = GFS3
        Df['CNN'] = CNN
        Df['TL'] = TL

        threshold2 = np.percentile(Df['GFS2'], 90)
        Df['Final'] = Df.apply(
            lambda x: x['TL'] if (x['GFS2'] > threshold2) or (x['GFS3'] > threshold2) else x['CNN'],
            axis=1)

        predicted_values = Df['Final']
        predicted_values = predicted_values.tolist()
        
        today_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')
        today_data.day2_rainfall = float(predicted_values[0])
        today_data.save()
    
def predict_day3():
    forecast_hr = np.arange(15, 157, 3)
    latbounds = [18.5 - 0.25, 19.5]
    lonbounds = [72.5, 73.5 + 0.25]
    time_from_ref = np.arange(15, 157, 3)

    columns_prec = []
    for i in ['Prec']:
        for time_steps in forecast_hr:
            for j in np.arange(19.5, 18.25, -0.25):
                for k in np.arange(72.5, 73.75, 0.25):
                    columns_prec.append(f'{i}_{j}_{k}_{time_steps:03d}')

    x = datetime.now().replace(second=0, microsecond=0)
    pd.to_datetime(x)
    day = x.day
    month = x.month
    year = x.year

    start_day = f'{year}-{month}-{day}'
    end_day = pd.to_datetime(start_day) + timedelta(hours=24)
    data_prec = pd.DataFrame(index=[pd.to_datetime(start_day) + timedelta(hours=6)], columns=columns_prec)
    root_directory = os.path.join(settings.BASE_DIR,"files", f"{day:02d}-{month:02d}-{year}")

    for time_step in data_prec.index:
        year = time_step.year
        month = time_step.month
        day = time_step.day
        ref_time = time_step.hour

        date_temp = pd.date_range(start=time_step + timedelta(hours=15), end=time_step + timedelta(hours=156), freq='3H')
        col_temp = np.arange(0, 25)

        data_temp = pd.DataFrame(index=date_temp, columns=col_temp)

        for time_lag in time_from_ref:
            filename = f'gfs.t{ref_time:02d}z.pgrb2.0p25.f{time_lag:03d}'
            grib = f'{root_directory}/{filename}'
            grbs = pygrib.open(grib)
            variable_name_to_select = 'Precipitation rate'

            for grb in grbs.select(name=variable_name_to_select):
                data = grb.values
                latitudes, longitudes = grb.latlons()
                parameter_name = grb.name
                level_type = grb.typeOfLevel
                level_value = grb.level
                valid_time = grb.validDate

            latli = 2
            latui = 7
            lonli = 2
            lonui = 7

            time = pd.to_datetime(f'{year}-{month}-{day}') + timedelta(hours=int(ref_time) + int(time_lag))
            data = data[latli:latui, lonli:lonui][::-1]
            time_prev = time - timedelta(hours=3)

            if (int(time_lag) % 6) == 0:
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] = (np.ravel(data) * 21600) - np.ravel(data_temp.loc[time_prev][0:25])
            elif (int(time_lag) % 6) != 0 & (int(time_lag) % 3) == 0:
                if len(np.ravel(data)) == 25:
                    data_temp.loc[time][0:25] = (np.ravel(data) * 10800)
            else:
                print(filename)

        data_prec.loc[time_step][0:1200] = np.ravel(data_temp)

    data_prec = data_prec.shift(freq=pd.Timedelta(hours=17, minutes=30))
    data_prec.head()

    data_prec.columns = map(str, data_prec.columns)
    common_prefix = 'Prec_19.25_72.5','Prec_19.25_72.75','Prec_19.25_73.0','Prec_19.25_73.25','Prec_19.0_72.5','Prec_19.0_72.75','Prec_19.0_73.0','Prec_19.0_73.25','Prec_18.75_72.5','Prec_18.75_72.75','Prec_18.75_73.0','Prec_18.75_73.25','Prec_18.5_72.5','Prec_18.5_72.75','Prec_18.5_73.0','Prec_18.5_73.25'
    selected_columns = [col for col in data_prec.columns if col.startswith(common_prefix) and '015' <= col[-3:] <= '084']

    data_prec = data_prec[selected_columns]
    data_prec = data_prec.iloc[:, 256:384]
    n_samples_test = data_prec.shape[0]

    X_test_prec_cnn_lstm = np.full((n_samples_test, 8, 4, 4), np.nan)
    
    for i in range(data_prec.shape[0]):
        temp_array = np.full((8, 4, 4), np.nan)
        counter = 0

        for j in np.arange(63, 85, 3):
            selected_cols = data_prec.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4, -1)
            counter += 1

        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)

    X_test_prec_cnn_lstm_daily = np.full((n_samples_test, 1, 4, 4), np.nan) 

    for i in range(X_test_prec_cnn_lstm_daily.shape[0]):
        X_test_prec_cnn_lstm_daily[i, 0, :, :] = np.sum(X_test_prec_cnn_lstm[i, 0:8, :, :], axis=0)

    X_test_prec_cnn_lstm_daily.shape

    X_test_prec_cnn_lstm_reshaped = np.expand_dims(X_test_prec_cnn_lstm_daily, axis=1)
    X_test_prec_cnn_lstm_reshaped = np.moveaxis(X_test_prec_cnn_lstm_reshaped, 1, -1)
    X_test_prec_cnn_lstm_reshaped.shape

    lat_lon = []

    for i in np.arange(18.5, 19.5 + 0.25, 0.25):
        for j in np.arange(72.5, 73 + 0.25, 0.25):
            lat_lon.append([i, j])

    lat_lon = np.array(lat_lon)
    lat_lon = lat_lon.astype(float)

    def find_closest_pair(lat_lon_array, target_lat, target_lon):
        delta_lat = lat_lon_array[:, 0] - target_lat
        delta_lon = lat_lon_array[:, 1] - target_lon
        distances = np.sqrt(delta_lat**2 + delta_lon**2)
        closest_index = np.argmin(distances)
        return lat_lon_array[closest_index]

    start_day
    dict = {}

    for station in stations:
        model1_path = os.path.join(settings.BASE_DIR, f'files/3DayLead/{station.name}_1/tl.h5')
        model_path = os.path.join(settings.BASE_DIR, f'files/3DayLead/{station.name}_1/CNN2122old.h5')

        model = load_model(model_path)
        model1 = load_model(model1_path)
        
        predictions = model.predict(X_test_prec_cnn_lstm_reshaped)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped)
        
        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station.name] = pd.DataFrame()

        closest_lat_lon = find_closest_pair(lat_lon, station.latitude, station.longitude)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        
        data_GFS_prec_stationwise_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3'])
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        
        y_pred_gfs = np.array(data_GFS_prec_stationwise_daily[f'{station.name}']).astype(float)

        predictions_GFS = y_pred_gfs[:, 0]

        GFS = y_pred_gfs[:, 0]
        GFS2 = y_pred_gfs[:, 1]
        GFS3 = y_pred_gfs[:, 2]
        CNN = predictions
        TL = predictions1
        Df = pd.DataFrame(columns=['GFS', 'GFS2', 'GFS3', 'TL', 'CNN'])
        Df['GFS'] = GFS
        Df['GFS2'] = GFS2
        Df['GFS3'] = GFS3
        Df['CNN'] = CNN
        Df['TL'] = TL
        threshold = np.percentile(Df['GFS'], 90)
        Df['Final'] = Df.apply(
            lambda x: x['TL'] if (x['GFS'] > threshold) or (x['GFS2'] > threshold) or (x['GFS3'] > threshold) else x['CNN'],
            axis=1)
        predicted_values = Df['Final']
        predicted_values = predicted_values.tolist()
        
        today_data = DaywisePrediction.objects.filter(station=station).latest('timestamp')
        today_data.day3_rainfall = float(predicted_values[0])
        today_data.save()
        