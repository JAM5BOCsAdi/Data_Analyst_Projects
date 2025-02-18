from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

# 1. Adatok betöltése
iris = load_iris()
X, y = iris.data, iris.target  # X = tulajdonságok, y = címkék (Setosa, Versicolor, Virginica)

# 2. Adatok felosztása tanulási és tesztelési halmazra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Döntési fa modell létrehozása és tanítása
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# 4. Előrejelzés és pontosság mérése
y_pred = clf.predict(X_test)
print(f"Pontosság: {accuracy_score(y_test, y_pred):.2f}")

# 5. Döntési fa vizualizációja
plt.figure(figsize=(12, 8))
plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=True)
plt.show()


# ----------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Adatok generálása
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
y = np.array([2, 4, 6, 8, 10])  # y = 2*x (egyszerű lineáris kapcsolat)

# Modell létrehozása és betanítása
regressor = LinearRegression()
regressor.fit(X, y)

# Előrejelzés
X_pred = np.array([[6]])
y_pred = regressor.predict(X_pred)
print(f"6-ra becsült érték: {y_pred[0]}")

# Vizualizáció
plt.scatter(X, y, color="blue")
plt.plot(X, regressor.predict(X), color="red")
plt.xlabel("X értékek")
plt.ylabel("Y értékek")
plt.title("Lineáris regresszió példa")
plt.show()

# ----------------------------------------------------------------
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

# MNIST adatbázis betöltése
mnist = keras.datasets.mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Adatok normalizálása (0–1 közé)
X_train, X_test = X_train / 255.0, X_test / 255.0

# Neurális hálózat létrehozása
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # 28x28-as képek kiterítése vektorrá
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(10, activation='softmax')  # 10 kimeneti osztály (0-9 számjegyek)
])

# Modell fordítása
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Modell betanítása
model.fit(X_train, y_train, epochs=5)

# Modell kiértékelése
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Teszt pontosság: {test_acc:.2f}")

# Egy számjegy megjelenítése és predikciója
plt.imshow(X_test[0], cmap="gray")
plt.show()

prediction = np.argmax(model.predict(np.array([X_test[0]])))
print(f"Előrejelzett szám: {prediction}")


