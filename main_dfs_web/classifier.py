from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd

#Load the data:
training_df = pd.read_pickle('/root/ADA2023/ada-2023-project-adacadabra2023/ada-2023-project-adacadabra2023/main_dfs_web/training_df.pkl') 

# Features (X)
features = training_df[['Season','1st_Style', '2nd_Style', '3rd_Style']]
features_encoded = pd.get_dummies(features, columns=['Season', '1st_Style', '2nd_Style', '3rd_Style'])


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


