import os
import sys
import argparse
import pandas as pd
import pickle as pkl

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

sys.path.append('.')
from src.data.Data import load_data


def create_train_df(df_users, df_ratings):
    # Expertise
    df_users['expertise'] = (df_users['total_nbr_ratings'] >= 3352).astype(int)

    equivalent_expertise = dict(zip(df_users['user_id'], df_users['expertise']))
    df_ratings['expertise']=df_ratings['user_id'].map(equivalent_expertise)
    
    weighted_scores = df_ratings.groupby(['country_brewery', 'Trimester', 'macro_style'], as_index=False).apply(weighted_average)
    weighted_scores = weighted_scores.sort_values(by=['country_brewery', 'Trimester', 'final_score'],  ascending=[True, True, False])
    desired_order = ['country_brewery', 'Trimester', 'macro_style', 'final_score']
    weighted_scores = weighted_scores[desired_order]
    
    top_3_beerstyles = weighted_scores.groupby(['country_brewery', 'Trimester']).head(3)
    styles_combined = top_3_beerstyles.groupby(['country_brewery', 'Trimester'], as_index= False).agg(lambda x: x.tolist())

    styles_combined[['1st_Style', '2nd_Style', '3rd_Style']] = pd.DataFrame(styles_combined['macro_style'].tolist(), index=styles_combined.index)
    styles_combined[['1st_Score', '2nd_Score', '3rd_Score']] = pd.DataFrame(styles_combined['final_score'].tolist(), index=styles_combined.index)
    styles_combined = styles_combined.drop(['macro_style', 'final_score'], axis=1)
    
    ## SANDRA'S
    #top_4_beerstyles = df.groupby(['country_brewery', 'Trimester'])['style'].value_counts().groupby(['country_brewery', 'Trimester']).head(3).reset_index(name='ratings')

    #styles_combined = top_4_beerstyles.groupby(['country_brewery', 'Trimester'], as_index= False).agg(lambda x: x.tolist())
    #styles_combined[['1st_Style', '2nd_Style', '3rd_Style']] = pd.DataFrame(styles_combined['style'].tolist(), index=styles_combined.index)
    #styles_combined[['1st_Rating', '2nd_Rating', '3rd_Rating']] = pd.DataFrame(styles_combined['ratings'].tolist(), index=styles_combined.index)
    #styles_combined = styles_combined.drop(['style', 'ratings'], axis=1)
    return styles_combined

def weighted_average(group):    
    # Define weights based on 'expertise'
    weights = {1: 1.5, 0: 1}

    # Calculate the weighted average
    weighted_avg = (group['detrend'] * group['expertise'].map(weights)).sum() / group['expertise'].map(weights).sum()

    return pd.Series({'macro_style': group['macro_style'].iloc[0], 'country_brewery': group['country_brewery'].iloc[0], 'final_score': weighted_avg})

def train_single_tree(season_df):
    # Features (X)
    print(season_df.head())
    features = season_df[['1st_Style', '2nd_Style', '3rd_Style']]
    #features_encoded = pd.get_dummies(features, columns=[ '1st_Style', '2nd_Style', '3rd_Style'])


    # Target variable (y)
    target = season_df['country_brewery']  # You can choose any of the style columns as the target variable


    # Define the columns and transformers for encoding
    categorical_features = ['1st_Style', '2nd_Style', '3rd_Style']

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
    return dtc_model


def train_classifiers(train_df, models_path):
    for t in train_df.Trimester.unique():
        print('Training for trimester', t)
        season_df = train_df[train_df.Trimester==t]
        tree = train_single_tree(season_df)
        model_path = os.path.join(models_path, f'tree_{t}.pkl')
        with open(model_path, 'wb') as f:
            pkl.dump(tree, f)

def main(args):
    if args.create_df:
        print('Generating train dataset...')
        main_df_ratings = load_data(args.dpath)
        main_df_users = load_data(args.dpath)
        training_df = create_train_df(main_df_users, main_df_ratings)
        with open(args.tpath, 'wb') as f:
            pkl.dump(training_df, f)
        print('Dataframe saved to', args.tpath)
    else:
        training_df = load_data(args.tpath)
        print('Dataframe loaded from', args.tpath)
    print('Training data shape: ', training_df.shape)
    
    if args.no_train:
        print('No training done, remove the flag --no-train to train the tree')
    else:
        print('Training model...')
        train_classifiers(training_df, args.mpath)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dpath', type=str, default='Data/Unified_ratings.pkl', help='Path to original data, used if --create-df specified')
    parser.add_argument('-u', '--users', type=str, default='Data/Users.pkl',help='Path to users dataframe')
    parser.add_argument('-t', '--tpath', type=str, default='Data/web/Train.pkl', help='Path to train data (to save/load)')
    parser.add_argument('-m', '--mpath', type=str, default='web_everything/trees', help='Path to model (save/load)')
    parser.add_argument('--create-df', action='store_true')
    parser.add_argument('--no-train', action='store_true')
    args = parser.parse_args()
    main(args)



