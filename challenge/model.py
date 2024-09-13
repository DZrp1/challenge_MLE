import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from typing import Tuple, Union, List
from datetime import datetime

class DelayModel:
    def __init__(self):
        self._model = None
        self._x_test = None
        self._y_test = None
    
    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        # Function to calculate the difference in minutes between the departure time and arrival time
        def get_min_diff(row):
            try:
                fecha_o = datetime.strptime(row['Fecha-O'], '%Y-%m-%d %H:%M:%S')
                fecha_i = datetime.strptime(row['Fecha-I'], '%Y-%m-%d %H:%M:%S')
                return ((fecha_o - fecha_i).total_seconds()) / 60
            except Exception:
                return None

        data['min_diff'] = data.apply(get_min_diff, axis=1)

        # Mark delay if the difference exceeds the threshold
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        # Create features using dummies
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)

        # Select the Top 10 features
        top_10_features = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]

        for feature in top_10_features:
            if feature not in features.columns:
                features[feature] = 0

        features = features[top_10_features]

        if target_column:
            target = data[[target_column]]
            return features, target
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        # Split the data into training and test sets and calculate class balance
        x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.33, random_state=42)

        self._x_test = x_test
        self._y_test = y_test.values.ravel()

        n_y0 = len(y_train[y_train.iloc[:, 0] == 0])
        n_y1 = len(y_train[y_train.iloc[:, 0] == 1])
        
        self._model = LogisticRegression(class_weight={1: n_y0/len(y_train), 0: n_y1/len(y_train)})
        self._model.fit(x_train, y_train.values.ravel())

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """
        predictions = self._model.predict(features)
        return predictions.tolist()





