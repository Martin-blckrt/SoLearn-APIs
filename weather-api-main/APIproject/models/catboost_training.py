from catboost import CatBoostRegressor
import pandas as pd
import numpy as np
import time
import os

DATA_PATH = os.path.join(os.getcwd(), 'data', 'hourly_weather_delteil.csv')

SAVE_PATH = os.path.join(os.getcwd(), 'saved_models', 'catboost_model.json')

CROSS_VAL = 10

model = CatBoostRegressor(
    loss_function = 'RMSE', 
    logging_level = 'Silent', 
    depth         = 7,
    iterations    = 1000,
    l2_leaf_reg   = 1,
    learning_rate = 0.03,
    thread_count  = 4,
    task_type     = "GPU"
)

def load():
    big_df = pd.read_csv(DATA_PATH, low_memory=False, index_col='datetime', parse_dates=True)
    df = big_df[[
    'Substation',
    't_h',
    'HiSolarRad',
    'SolarRad',
    'SolarEnergy',
    'd_m',
    'OutHum',
    'Bar',
    'DewPt',
    'P_GEN_MAX']]
    for key in df.columns:   
        df[key].replace(to_replace='---', value=np.nan)
    df = df.dropna()
    return df

def train(X_train, y_train):
    print("-------------Model trained-----------")
    tic = time.perf_counter()
    model.fit(X_train, y_train)
    toc = time.perf_counter()
    print(f"Executed in {toc - tic:0.4f} seconds")

def predict(X_test, y_test):
    print("-------------Predictions-------------")
    tic = time.perf_counter()
    cross_predictions = cross_val_predict(model, X_test, y_test, cv=CROSS_VAL)
    toc = time.perf_counter()
    print(f"Executed in {toc - tic:0.4f} seconds")
    print(cross_predictions)

def errors(X_test, y_test, RMSE=True, MSE=True, MAE=True):
    print("----------------Errors---------------")
    if RMSE or MSE:
        tic = time.perf_counter()
        mse_scores = cross_val_score(model, X_test, y_test, scoring='neg_mean_squared_error', cv=CROSS_VAL)
        mse_scores = abs(mse_scores)
        toc = time.perf_counter()
        print(f"Executed in {toc - tic:0.4f} seconds")
        if MSE:
            print('Mean Squared Error: %.5f (%.5f)' % (np.mean(mse_scores), np.std(mse_scores)))
        if RMSE:
            print('Root Mean Squared Error: %.5f (%.5f)' % (np.sqrt(np.mean(mse_scores)), np.std(mse_scores)))
    if MAE:
        tic = time.perf_counter()
        mae_scores = cross_val_score(model, X_test, y_test, scoring='neg_mean_absolute_error', cv=CROSS_VAL)
        mae_scores = abs(mae_scores)
        toc = time.perf_counter()
        print(f"Executed in {toc - tic:0.4f} seconds")
        print('Mean Absolute Error: %.5f (%.5f)' % (np.mean(mae_scores), np.std(mae_scores)))
    if not RMSE and not MSE and not MAE:
        print("No error selected during the call of the function")
    print("-------------------------------------")

def save():
    model.save_model(
            os.path.join(SAVE_PATH),
           format="json",
           export_parameters=None,
           pool=None)

def main():
    df = load()
    
    df_YMCA = df[df['Substation'] == 'YMCA']
    df_YMCA = df_YMCA.drop('Substation', axis=1)
    X_train = df_YMCA.drop(['P_GEN_MAX'], axis=1)
    y_train = df_YMCA['P_GEN_MAX']

    train(X_train, y_train)

    df_MD = df[df['Substation'] == 'Maple Drive East']
    df_MD = df_MD.drop('Substation', axis=1)
    X_test_MD_max = df_MD.drop(['P_GEN_MAX'], axis=1)
    y_test_MD_max = df_MD['P_GEN_MAX']

    predict(X_test_MD_max, y_test_MD_max)
    errors(X_test_MD_max, y_test_MD_max)
    save()

if __name__ == '__main__':
    main()