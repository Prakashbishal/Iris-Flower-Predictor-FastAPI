import pandas as pd
from sklearn. datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

iris=load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['flower_name'] = df['target'].apply(lambda i: iris.target_names[i])
df.head()
print(df.describe)
print(df['flower_name'].value_counts())
# Features (inputs)

X = df[iris.feature_names]

# Labels (outputs)
y = df['target']


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=200))
])
pipe.fit(X_train, y_train)

# Save the pipeline (not just model)
import pickle, os
save_dir = r"D:\FastAPI"
file_path = os.path.join(save_dir, "saved_model_iris.pkl")

with open(file_path, "wb") as f:
    pickle.dump(pipe, f)

print("Saved:", file_path)
