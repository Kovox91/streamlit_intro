from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import pickle
import os

#create a regressor tree model class that can be used to predict life expectancy based on GDP per capita, population, and other features.
class create_model:
    def __init__(self, data=None):
        self.data = data
        self.model = None
        self.feature_names = ['GDP per capita', 'Population', 'headcount_ratio_upper_mid_income_povline']

    def train_model(self):
        if self.data is None:
            raise Exception("No data provided for training.")
            
        # Prepare the data
        X = self.data[self.feature_names]
        y = self.data['Life Expectancy (IHME)']
        
        self.model = DecisionTreeRegressor(random_state=42)
        
        # Fit the model
        self.model.fit(X, y)
        return self.model

    def predict(self, gdp_per_capita, population, poverty_rate):
        if self.model is None:
            raise Exception("Model has not been trained yet.")
        
        # Create a DataFrame with the same feature names used in training
        X_pred = pd.DataFrame([[gdp_per_capita, population, poverty_rate]], 
                            columns=self.feature_names)
        
        # Make a prediction
        return self.model.predict(X_pred)[0]
    
    def save_model(self, filepath='model.pkl'):
        if self.model is None:
            raise Exception("No trained model to save.")
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    @classmethod
    def load_model(cls, filepath='model.pkl'):
        if not os.path.exists(filepath):
            raise Exception(f"Model file not found at {filepath}")
        instance = cls()
        with open(filepath, 'rb') as f:
            instance.model = pickle.load(f)
        return instance

if __name__ == "__main__":
    # Load the data
    data_url = "https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv"
    data = pd.read_csv(data_url)
    
    # Create and train the model
    model = create_model(data)
    model.train_model()
    
    # Save the trained model
    model.save_model()
    print("Model trained and saved successfully!")