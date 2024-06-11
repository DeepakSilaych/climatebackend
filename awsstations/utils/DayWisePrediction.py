
import pygrib
import pandas as pd
from datetime import timedelta
import os
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator 
import pickle
import matplotlib.dates as mdates
from tensorflow.keras.models import Sequential, load_model
import copy

from awsstations.models import AWSStation, DaywisePrediction
from django.conf import settings

def dailyprediction():

    forecast_hr = np.arange(15,163,3)
    latbounds = [ 18.5 - 0.25 , 19.5 ]
    lonbounds = [ 72.5 , 73.5 + 0.25 ]
    time_from_ref = np.arange(15,163,3)
    columns_prec = []

    for i in ['Prec']:
        for time_steps in forecast_hr:
            for j in np.arange(19.5,18.25,-0.25):
                for k in np.arange(72.5,73.75,0.25):
                    columns_prec.append(f'{i}_{j}_{k}_{time_steps:03d}')


    x = dt.datetime.now().replace(second=0, microsecond=0)


    day= x.day
    month = x.month
    year = x.year


    start_day = f'{year}-{month}-{day}'
    end_day = pd.to_datetime(start_day) + timedelta(hours=24)


    data_prec = pd.DataFrame(index =[pd.to_datetime(start_day) + timedelta(hours=6)], columns = columns_prec)


    root_directory = os.path.join(settings.BASE_DIR, 'files', f"{day:02d}-{month:02d}-{year}")


    counter =0
    for time_step in data_prec.index:
        
        year = time_step.year
        month = time_step.month
        day = time_step.day

        ref_time = time_step.hour
        
        date_temp = pd.date_range(start = time_step + timedelta(hours = 15), end = time_step + timedelta(hours = 162) , freq = '3H')
        col_temp = np.arange(0,25)
        
        data_temp = pd.DataFrame(index  = date_temp, columns=col_temp)
        
        for time_lag in time_from_ref:
            
            filename =f'gfs.t{ref_time:02d}z.pgrb2.0p25.f{time_lag:03d}'
            #directory = find_key(directory_names, filename)
            
            
            
            grib = f'{root_directory}/{filename}'
            grbs = pygrib.open(grib)
            variable_name_to_select = 'Precipitation rate'  # Replace with the variable name you want

            # Loop through the GRIB messages (variables) in the file
            for grb in grbs.select(name=variable_name_to_select):
                # Access the data and metadata of the selected variable
                data = grb.values  # Data values
                latitudes, longitudes = grb.latlons()  # Latitudes and longitudes
                parameter_name = grb.name  # Parameter name (e.g., 'Temperature', 'Wind speed', etc.)
                level_type = grb.typeOfLevel  # Level type (e.g., 'surface', 'isobaricInhPa', etc.)
                level_value = grb.level  # Level value (e.g., 850, 1000, etc.)
                valid_time = grb.validDate  # Valid time of the data


            # latitude lower and upper index
            latli = 2
            latui = 7 

            # longitude lower and upper index
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
                
                    
        data_prec.loc[time_step][0:1250] = np.ravel(data_temp)
        
        counter += 1
        if (counter)%500 == 0:
            print(f'Loop {counter} Done!')
            


    data_prec = data_prec.shift(freq=pd.Timedelta(hours=17, minutes=30))
    data_prec.head()


    data_prec.columns = map(str, data_prec.columns)

    # Specify the common prefix for the columns you want to select
    common_prefix = 'Prec_19.25_72.5','Prec_19.25_72.75','Prec_19.25_73.0','Prec_19.25_73.25','Prec_19.0_72.5','Prec_19.0_72.75','Prec_19.0_73.0','Prec_19.0_73.25','Prec_18.75_72.5','Prec_18.75_72.75','Prec_18.75_73.0','Prec_18.75_73.25','Prec_18.5_72.5','Prec_18.5_72.75','Prec_18.5_73.0','Prec_18.5_73.25'
    selected_columns = [col for col in data_prec.columns if col.startswith(common_prefix) and '015' <= col[-3:] <= '156']

    # Use the selected column names to index the DataFrame
    data_prec = data_prec[selected_columns]

    # Display the selected data
    data_prec


    data_prec_1=data_prec.iloc[:,:128]
    data_prec_2=data_prec.iloc[:, 128:256]
    data_prec_3=data_prec.iloc[:, 256:384]


    n_features = 16
    n_steps = 8
    n_samples_test = data_prec_1.shape[0]
    X_test_prec_cnn_lstm = np.full((n_samples_test,8,4,4),np.nan)


    for i in range(data_prec_1.shape[0]):
        temp_array = np.full((8,4,4),np.nan)
        counter = 0
        
        for j in np.arange(15,37,3):
            
            selected_cols = data_prec_1.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4,-1)
            counter +=1
            
        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)


    X_test_prec_cnn_lstm_daily_1 = np.full((n_samples_test,1,4,4),np.nan)
    for i in range(X_test_prec_cnn_lstm_daily_1.shape[0]):
        X_test_prec_cnn_lstm_daily_1[i,0,:,:] = np.sum(X_test_prec_cnn_lstm[i,0:8,:,:], axis = 0)
    X_test_prec_cnn_lstm_reshaped_1 = np.expand_dims(X_test_prec_cnn_lstm_daily_1, axis=1)
    X_test_prec_cnn_lstm_reshaped_1 = np.moveaxis(X_test_prec_cnn_lstm_reshaped_1, 1, -1)



    n_features = 16
    n_steps = 8
    n_samples_test = data_prec_2.shape[0]
    X_test_prec_cnn_lstm = np.full((n_samples_test,8,4,4),np.nan)

    for i in range(data_prec_2.shape[0]):
        temp_array = np.full((8,4,4),np.nan)
        counter = 0
        
        for j in np.arange(39,61,3):
            
            selected_cols = data_prec_2.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4,-1)
            counter +=1
            
        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)


    X_test_prec_cnn_lstm_daily_2 = np.full((n_samples_test,1,4,4),np.nan)
    for i in range(X_test_prec_cnn_lstm_daily_2.shape[0]):
        X_test_prec_cnn_lstm_daily_2[i,0,:,:] = np.sum(X_test_prec_cnn_lstm[i,0:8,:,:], axis = 0)
    X_test_prec_cnn_lstm_reshaped_2 = np.expand_dims(X_test_prec_cnn_lstm_daily_2, axis=1)
    X_test_prec_cnn_lstm_reshaped_2 = np.moveaxis(X_test_prec_cnn_lstm_reshaped_2, 1, -1)



    n_features = 16
    n_steps = 8
    n_samples_test = data_prec_3.shape[0]
    X_test_prec_cnn_lstm = np.full((n_samples_test,8,4,4),np.nan)


    for i in range(data_prec_3.shape[0]):
        temp_array = np.full((8,4,4),np.nan)
        counter = 0
        
        for j in np.arange(63,85,3):
            
            selected_cols = data_prec_3.filter(regex=f'_{j:03d}$')
            temp_array[counter] = selected_cols.iloc[i].values.reshape(4,-1)
            counter +=1
            
        X_test_prec_cnn_lstm[i] = copy.deepcopy(temp_array)


    X_test_prec_cnn_lstm_daily_3 = np.full((n_samples_test,1,4,4),np.nan)
    for i in range(X_test_prec_cnn_lstm_daily_3.shape[0]):
        X_test_prec_cnn_lstm_daily_3[i,0,:,:] = np.sum(X_test_prec_cnn_lstm[i,0:8,:,:], axis = 0)
    X_test_prec_cnn_lstm_reshaped_3 = np.expand_dims(X_test_prec_cnn_lstm_daily_3, axis=1)
    X_test_prec_cnn_lstm_reshaped_3 = np.moveaxis(X_test_prec_cnn_lstm_reshaped_3, 1, -1)


    stations_ok_merged = sorted(['Andheri','B ward', 'Bandra','C ward', 'Chembur', 'D Ward',
                'Dindoshi','F North', 'F South', 'G South','Gowanpada', 'H West ward', 'K East ward',
                'Kurla', 'L ward', 'M West ward','Malvani','MCGM 1','Mulund','N ward',
                'Nariman Fire','S ward','SWD Workshop dadar','Vikhroli','vileparle W', 'Byculla', 'Chincholi', 
                        'Colaba', 'K West ward','Kandivali', 'Marol','Memonwada','Rawali camp','Thakare natya','Worli','Dahisar'])

    lat_lon = []

    for i in np.arange(18.5,19.5+0.25,0.25):
        for j in np.arange(72.5, 73+0.25,0.25):

            lat_lon.append([i,j])

    lat_lon = np.array(lat_lon)
    lat_lon=lat_lon.astype(float)
    def find_closest_pair(lat_lon_array, target_lat, target_lon):
        # Calculate differences in latitude and longitude
        delta_lat = lat_lon_array[:, 0] - target_lat
        delta_lon = lat_lon_array[:, 1] - target_lon

        # Calculate Euclidean distances
        distances = np.sqrt(delta_lat**2 + delta_lon**2)

        # Find the index of the pair with the minimum distance
        closest_index = np.argmin(distances)

        # Return the closest pair of latitude and longitude
        return lat_lon_array[closest_index]


    predicted_values_dict_1d = {}
    predicted_values_dict_GFS_1d = {}
    predicted_values_dict_CNN_1d = {}
    predicted_values_dict_TL_1d = {}
    predicted_values_dict_2d = {}
    predicted_values_dict_GFS_2d = {}
    predicted_values_dict_GFS3_2d = {}
    predicted_values_dict_CNN_2d = {}
    predicted_values_dict_TL_2d = {}
    predicted_values_dict_3d = {}
    predicted_values_dict_GFS_3d = {}
    predicted_values_dict_CNN_3d = {}
    predicted_values_dict_TL_3d = {}

    with open(os.path.join(settings.BASE_DIR, 'files', 'daily_threshold.pkl'), 'rb') as f:
        thresholds_dict = pickle.load(f)

        
    for station in AWSStation.objects.all():
        model_path = os.path.join(settings.BASE_DIR, 'files', 'Lead Day 1', station.name+'_1', 'CNN.h5')
        model1_path = os.path.join(settings.BASE_DIR, 'files', 'Lead Day 1', station.name+'_1', 'tl.h5')
        
        model = load_model(model_path)
        model1 = load_model(model1_path)

        # Make predictions using the loaded model
        predictions = model.predict(X_test_prec_cnn_lstm_reshaped_1)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped_1)
        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station.name] = pd.DataFrame()
        
        station_lat = station.latitudes
        station_lon = station.longitude

        closest_lat_lon = find_closest_pair(lat_lon, station_lat, station_lon)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        data_GFS_prec_stationwise_testing_daily = {}
        
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3'])
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        
        y_pred_gfs = np.array(data_GFS_prec_stationwise_testing_daily[f'{station.name}']).astype(float)
        

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
        
        # Retrieve the threshold values for the current station and variable
        station_thresholds = thresholds_dict[station.name]
        
        # Apply the thresholds for each column
        threshold = station_thresholds['GFS']
        # Calculate the final values based on thresholds
        Df['Final'] = Df.apply(
            lambda x: x['TL'] if (x['GFS'] > threshold) or (x['GFS2'] > threshold) or (x['GFS3'] > threshold) else x['CNN'],
            axis=1)
        
        
        predicted_values_dict_1d[station.name] = Df['Final']
        predicted_values_dict_GFS_1d[station.name] = Df['GFS3']
        predicted_values_dict_CNN_1d[station.name] = Df['CNN']
        predicted_values_dict_TL_1d[station.name] = Df['TL']
        

        model_path = os.path.join(settings.BASE_DIR, 'files', '2DayLead', station.name, 'CNN2122old.h5')
        model1_path = os.path.join(settings.BASE_DIR, 'files', '2DayLead', station.name, 'tl.h5')
        
        model = load_model(model_path)
        model1 = load_model(model1_path)

        # Make predictions using the loaded model
        predictions = model.predict(X_test_prec_cnn_lstm_reshaped_2)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped_2)
        
        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station.name] = pd.DataFrame()
        

        closest_lat_lon = find_closest_pair(lat_lon, station_lat, station_lon)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        data_GFS_prec_stationwise_testing_daily = {}
        
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3','4','5','6'])
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,3] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,24:32].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,4] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,32:40].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,5] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,40:48].sum(axis = 1)

        y_pred_gfs = np.array(data_GFS_prec_stationwise_testing_daily[f'{station.name}']).astype(float)

        predictions_GFS = y_pred_gfs[:,1]

        GFS = y_pred_gfs[:, 0]
        GFS2 = y_pred_gfs[:, 1]
        GFS3 = y_pred_gfs[:, 2]
        GFS4 = y_pred_gfs[:, 3]
        CNN = predictions
        TL = predictions1
        Df = pd.DataFrame(columns=['GFS', 'GFS2', 'GFS3','GFS4', 'TL', 'CNN', 'Obs'])
        Df['GFS'] = GFS
        Df['GFS2'] = GFS2
        Df['GFS3'] = GFS3
        Df['GFS4'] = GFS4
        Df['CNN'] = CNN
        Df['TL'] = TL

        # Retrieve the threshold values for the current station and variable
        station_thresholds = thresholds_dict[station.name]
        
        # Apply the thresholds for each column
        threshold2 = station_thresholds['GFS2']

        # Calculate the final values based on thresholds
        Df['Final'] = Df.apply(
            lambda x: x['TL'] if (x['GFS2'] > threshold2) or (x['GFS3'] > threshold2) else x['CNN'],
            axis=1)

        predicted_values_dict_2d[station.name] = Df['Final']
        predicted_values_dict_GFS_2d[station.name] = Df['GFS2']
        predicted_values_dict_CNN_2d[station.name] = Df['CNN']
        predicted_values_dict_TL_2d[station.name] = Df['TL']
        predicted_values_dict_GFS3_2d[station.name] = Df['GFS3']
        

        model_path = os.path.join(settings.BASE_DIR, 'files', '3DayLead', station.name, 'CNN2122old.h5')
        model1_path = os.path.join(settings.BASE_DIR, 'files', '3DayLead', station.name, 'tl.h5')
        
        model = load_model(model_path)
        model1 = load_model(model1_path)
        # Make predictions using the loaded model

        predictions = model.predict(X_test_prec_cnn_lstm_reshaped_3)
        predictions1 = model1.predict(X_test_prec_cnn_lstm_reshaped_3)
        
        
        data_GFS_prec_stationwise_testing = {}
        data_GFS_prec_stationwise = {}

        data_GFS_prec_stationwise[station.name] = pd.DataFrame()
        
        closest_lat_lon = find_closest_pair(lat_lon, station_lat, station_lon)
        closest_lat = str(closest_lat_lon[0])
        closest_lon = str(closest_lat_lon[1])

        selected_cols_testing = data_prec.filter(regex=f'{closest_lat}_{closest_lon}')
        
        data_GFS_prec_stationwise_testing[station.name] = copy.deepcopy(selected_cols_testing)
        
        data_GFS_prec_stationwise_daily = {}
        data_GFS_prec_stationwise_testing_daily = {}
        
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'] = pd.DataFrame(index=data_GFS_prec_stationwise_testing[f'{station.name}'].index,columns=['1','2','3','4','5','6'])
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,0] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,0:8].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,1] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,8:16].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,2] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,16:24].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,3] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,24:32].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,4] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,32:40].sum(axis = 1)
        data_GFS_prec_stationwise_testing_daily[f'{station.name}'].iloc[:,5] = data_GFS_prec_stationwise_testing[f'{station.name}'].iloc[:,40:48].sum(axis = 1)

        y_pred_gfs = np.array(data_GFS_prec_stationwise_testing_daily[f'{station.name}']).astype(float)

        predictions_GFS = y_pred_gfs[:,2]

        GFS = y_pred_gfs[:,0]
        GFS2 = y_pred_gfs[:,1]
        GFS3 = y_pred_gfs[:,2]
        GFS4 = y_pred_gfs[:,3]
        GFS5 = y_pred_gfs[:,4]
        GFS6 = y_pred_gfs[:,5]
        CNN = predictions
        TL = predictions1
        Df = pd.DataFrame(columns = ['GFS','GFS2','GFS3','GFS4','GFS5','GFS6','TL','CNN'])
        Df['GFS'] = GFS
        Df['GFS2'] = GFS2
        Df['GFS3'] = GFS3
        Df['GFS4'] = GFS4
        Df['GFS5'] = GFS5
        Df['GFS6'] = GFS6
        Df['CNN'] = CNN
        Df['TL'] = TL

        station_thresholds = thresholds_dict[station.name]

        threshold = station_thresholds['GFS3']
        
        # Calculate the final values based on thresholds
        Df['Final'] = Df.apply(lambda x: x['TL'] if (x['GFS3'] > threshold) or (x['GFS4'] > threshold) or (x['GFS5'] > threshold) else x['CNN'], axis = 1)
        
        Df['Final'] = np.nan_to_num(Df['Final'])
        predicted_values_dict_3d[station.name] = Df['Final']
        predicted_values_dict_GFS_3d[station.name] = Df['GFS3']
        predicted_values_dict_CNN_3d[station.name] = Df['CNN']
        predicted_values_dict_TL_3d[station.name] = Df['TL']

        print("station:", station)
        print("predicted_values_dict_1d:", predicted_values_dict_1d)
        print("predicted_values_dict_2d:", predicted_values_dict_2d)
        print("predicted_values_dict_3d:", predicted_values_dict_3d)



