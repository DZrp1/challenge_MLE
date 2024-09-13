import pandas as pd
import pickle
from model import DelayModel

data = pd.read_csv('../data/data.csv')

# Training and saving the model
model = DelayModel()
features, target = model.preprocess(data, target_column="delay")
model.fit(features, target)

with open('C:\\Personales\\Programas_Python\\challenge_MLE\\challenge\\delay_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Extracting and saving validation lists
airlines = data['OPERA'].unique().tolist()
types = data['TIPOVUELO'].unique().tolist()
months = data['MES'].unique().tolist()

with open('C:\\Personales\\Programas_Python\\challenge_MLE\\challenge\\validation_data.pkl', 'wb') as f:
    pickle.dump({'airlines': airlines, 'types': types, 'months': months}, f)

print("Model and validation lists saved.")
