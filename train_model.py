import pandas as pd
from challenge.model import DelayModel
from joblib import dump

def main():
    model = DelayModel()
    data = pd.read_csv('C:\Personales\Programas_Python\challenge_MLE\data\data.csv')

    airlines = data['OPERA'].unique().tolist()   
    types = data['TIPOVUELO'].unique().tolist()  
    months = data['MES'].unique().tolist()  

    features, target = model.preprocess(data, target_column="delay")
    model.fit(features, target)

    dump({
        'model': model._model,  
        'preprocessor': model.preprocess,
        'airlines': airlines,    
        'types': types,         
        'months': months       
    }, "challenge/trained_model_with_metadata.joblib")

    print("Model successfully trained and saved in 'challenge/trained_model_with_metadata.joblib'.")

if __name__ == "__main__":
    main()