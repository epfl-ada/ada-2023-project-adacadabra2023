import pandas as pd


def run_query(model, beer1, beer2, beer3):
    # Create df for inference
    features = pd.DataFrame([[beer1, beer2, beer3]], columns=['1st_Style', '2nd_Style', '3rd_Style'])
    y_pred = model.predict(features)
    return y_pred