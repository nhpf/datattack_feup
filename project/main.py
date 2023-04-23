import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from preprocess_data import clean_data, parse_categories

# Read the database .CSV
occurrences = pd.read_csv(
    "../Data/anpc-2016.csv", sep=",", on_bad_lines="skip", low_memory=False
)

# Get relevant and error-free data
occurrences = parse_categories(clean_data(occurrences))

occurrences["day_idx"] = occurrences["DataOcorrencia"] - min(
    occurrences["DataOcorrencia"]
)
occurrences["day_idx"] = occurrences["day_idx"].apply(
    lambda occ: occ.total_seconds() / 3600
)

# encode the categorical variables
le_state = LabelEncoder()
region = "Distrito"
occurrences[region] = le_state.fit_transform(occurrences[region])
enc = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded_data = enc.fit_transform(occurrences[[region]])

# combine the encoded variables with the numerical variables
X = pd.concat(
    [pd.DataFrame(encoded_data).reset_index(inplace=True), occurrences["day_idx"]],
    axis=1,
)
print(X)
y = occurrences["category2"]

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=12
)

# train a random forest classifier
clf = RandomForestClassifier(n_estimators=1000, random_state=12)
clf.fit(X_train, y_train)

# make predictions on the test set
y_pred = clf.predict(X_test)

# calculate the accuracy score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy score: {accuracy:.2f}")
