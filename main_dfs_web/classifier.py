import argparse
import pandas as pd


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def create_train_df(df):
    top_4_beerstyles = df.groupby(['country_brewery', 'Season'])['style'].value_counts().groupby(['country_brewery', 'Season']).head(3).reset_index(name='ratings')

    styles_combined = top_4_beerstyles.groupby(['country_brewery', 'Season'], as_index= False).agg(lambda x: x.tolist())
    styles_combined[['1st_Style', '2nd_Style', '3rd_Style']] = pd.DataFrame(styles_combined['style'].tolist(), index=styles_combined.index)
    styles_combined[['1st_Rating', '2nd_Rating', '3rd_Rating']] = pd.DataFrame(styles_combined['ratings'].tolist(), index=styles_combined.index)
    styles_combined = styles_combined.drop(['style', 'ratings'], axis=1)
    return df


def train_classifier(training_df, save_path):
    #Load the data:

    # Features (X)
    features = training_df[['Season','1st_Style', '2nd_Style', '3rd_Style']]
    #features_encoded = pd.get_dummies(features, columns=['Season', '1st_Style', '2nd_Style', '3rd_Style'])


    # Target variable (y)
    target = training_df['country_brewery']  # You can choose any of the style columns as the target variable


    # Define the columns and transformers for encoding
    categorical_features = ['Season', '1st_Style', '2nd_Style', '3rd_Style']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ])

    # Create the Decision Tree Classifier
    dtc = DecisionTreeClassifier(random_state=27)


    # Create the pipeline
    dtc_model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', dtc)])


    # Train the model on the training data
    dtc_model.fit(features, target)

    # Make predictions on the test set
    y_pred = dtc_model.predict(features)

    # Evaluate the accuracy
    accuracy = accuracy_score(target, y_pred)
    print(f'Accuracy: {accuracy}')


def main(args):
    if args.create_df:
        training_df = create_train_df()
    else:
        training_df = pd.read_pickle('/root/ADA2023/ada-2023-project-adacadabra2023/ada-2023-project-adacadabra2023/main_dfs_web/training_df.pkl') 
    train_classifier(training_df)
    

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dpath', type=str, default= 'Data')
    parser.add_argument('-m', '--mpath', type=str, default= 'models')
    parser.add_argument('--create-df', action='store_true')
    args = parser.parse_args()
    main(args)



