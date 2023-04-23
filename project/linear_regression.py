import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import LinearRegression
from preprocess_data import datetime_to_hours_int
from sklearn.feature_extraction import FeatureHasher
from preprocess_data import clean_data, parse_categories

# Read the database .CSV
occurrences = pd.read_csv(
    "Data/anpc-2016.csv", sep=",", on_bad_lines="skip", low_memory=False
)

# Get relevant and error-free data
occurrences = parse_categories(clean_data(occurrences))


def hashed_reg(occurrences):
    # Encode the categorical variables using feature hashing with HashingVectorizer
    num_districts = occurrences.nunique()["Distrito"]
    hash_size_increase = 2.5  # Increase number of features to avoid hash collision
    district_vectorizer = HashingVectorizer(
        n_features=num_districts, norm=None, alternate_sign=False
    )
    X_cat = district_vectorizer.fit_transform(occurrences["Distrito"])

    num_categories = occurrences.nunique()["category2"]
    hash_size_increase = 2.5  # Increase number of features to avoid hash collision
    category_vectorizer = HashingVectorizer(
        n_features=num_categories, norm=None, alternate_sign=False
    )
    X_cat2 = category_vectorizer.fit_transform(occurrences["category2"])

    # Combine the encoded categorical variables and the numerical variable
    X = pd.concat(
        [
            pd.DataFrame(X_cat.toarray()),
            pd.DataFrame(X_cat2.toarray()),
            pd.DataFrame(
                datetime_to_hours_int(
                    occurrences["DataOcorrencia"] - min(occurrences["DataOcorrencia"])
                )
            ),
        ],
        axis=1,
    )

    # Fit a linear regression model to the data
    model = LinearRegression()
    model.fit(X, occurrences["hh"])

    return model.predict(X)


def hashed_reg_2(occurrences):
    num_districts = occurrences.nunique()["Distrito"]
    hash_size_increase = 2.5  # Increase number of features to avoid hash collision
    h = FeatureHasher(
        n_features=int(hash_size_increase * num_districts), input_type="string"
    )
    return h.transform(list(occurrences["Distrito"]))


hashed_reg(occurrences)
