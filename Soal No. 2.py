# Import library
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Dataset
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak'],
    'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No']
}

df = pd.DataFrame(data)

# Encoding
le = LabelEncoder()

for column in df.columns:
    df[column] = le.fit_transform(df[column])

# Split fitur & target
X = df.drop('Play', axis=1)
y = df['Play']

# Model Decision Tree
model = DecisionTreeClassifier(criterion='entropy')
model.fit(X, y)

# Visualisasi tree
plt.figure(figsize=(13,6))
plot_tree(model, feature_names=X.columns, class_names=['No', 'Yes'], filled=True)
plt.show()

# Prediksi data baru
# Outlook = Sunny, Temperature = Cool, Humidity = High, Wind = Strong

# Encode manual sesuai label
# Kita harus mapping ulang:
# Outlook: Overcast=0, Rain=1, Sunny=2
# Temperature: Cool=0, Hot=1, Mild=2
# Humidity: High=0, Normal=1
# Wind: Strong=0, Weak=1

new_data = [[2, 0, 0, 0]]

prediction = model.predict(new_data)

print("Prediksi:", "Yes" if prediction[0] == 1 else "No")