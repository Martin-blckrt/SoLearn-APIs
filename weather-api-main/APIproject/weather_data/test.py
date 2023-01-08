import json
import os
import pandas as pd

if __name__ == '__main__':
    try:
        file = open(os.path.join(os.getcwd(), 'weather_data', 'test.json'))
    except:
        raise
    data_json = json.load(file)
    data_json_reduced = data_json['data']
    data_df = pd.DataFrame(data_json_reduced)
    print(data_df)