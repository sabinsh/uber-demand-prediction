import pandas as pd
import joblib
from pathlib import Path
import logging
from sklearn import set_config
from sklearn.metrics import mean_absolute_percentage_error


set_config(transform_output="pandas")

# create a logger
logger = logging.getLogger("evaluate_model")
logger.setLevel(logging.INFO)

# attach a console handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# make a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

def load_model(model_path):
    model = joblib.load(model_path)
    return model


if __name__ == "__main__":
    # current path
    current_path = Path(__file__)
    # set the root path
    root_path = current_path.parent.parent.parent
    # data_path
    data_path = root_path / "data/processed/test.csv"
    
    # read the data
    df = pd.read_csv(data_path, parse_dates=["tpep_pickup_datetime"])
    logger.info("Data read successfully")
    
    # set the datetime column as index
    df.set_index("tpep_pickup_datetime", inplace=True)
    
    # make X_test and y_test
    X_test = df.drop(columns=["total_pickups"])
    y_test = df["total_pickups"]
    
    # load the encoder
    encoder_path = root_path / "models/encoder.joblib"
    encoder = joblib.load(encoder_path)
    logger.info("Encoder loaded successfully")
    
    # transform the test data
    X_test_encoded = encoder.transform(X_test)
    logger.info("Data transformed successfully")
    
    # load the model
    model_path = root_path / "models/model.joblib"
    model = load_model(model_path)
    logger.info("Model loaded successfully")
    
    # make predictions
    y_pred = model.predict(X_test_encoded)
    
    # calculate the loss
    loss = mean_absolute_percentage_error(y_test, y_pred)
    logger.info(f"Loss: {loss}")
    