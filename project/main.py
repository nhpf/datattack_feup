import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colormaps
import matplotlib.patches as mpatches
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import LinearRegression
from preprocess_data import clean_data, parse_categories

# pd.set_option("display.max_rows", None)
# pd.set_option("display.max_columns", None)
# pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)

# Read the database .CSV
occurrences = pd.read_csv(
    "../Data/anpc-2016.csv", sep=",", on_bad_lines="skip", low_memory=False
)

# Get relevant and error-free data
occurrences = parse_categories(clean_data(occurrences))

# print(occurrences['category1'].value_counts())
#
# print(occurrences.head())
# print(occurrences.columns)

# Encode the categorical variables using feature hashing with HashingVectorizer
num_districts = occurrences.nunique()["Distrito"]
hash_size_increase = 2.5  # Increase number of features to avoid hash collision
# print(num_districts)

district_vectorizer = HashingVectorizer(n_features=int(hash_size_increase * num_districts))
X_cat = district_vectorizer.fit_transform(occurrences["Distrito"])

# Combine the encoded categorical variables and the numerical variable
X = pd.DataFrame(X_cat.toarray())
X["category2"] = occurrences["category2"]

# Fit a linear regression model to the data
model = LinearRegression()
# model.fit(X.drop("y", axis=1), X["y"]) # TODO: replace y by man-hour

# Make some predictions using the model
# X_new = pd.DataFrame({"x1": ["A", "C", "B"], "x2": ["X", "Y", "Y"]})
# X_cat_new = district_vectorizer.transform(X_new["x1"] + "_" + X_new["x2"])
# X_new_encoded = pd.DataFrame(X_cat_new.toarray())
# y_pred = model.predict(X_new_encoded)
# print(y_pred)

# Random forest
