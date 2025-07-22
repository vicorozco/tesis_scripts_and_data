import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt

df = pd.read_csv("sitios_con_metadata.csv")  # Se cargan los datos procesados de todos los sitios web

df['label'] = df['label'].map({'falso': 0, 'verdadero': 1}) # pasar etiquetas a números (falso = 0, verdadero = 1)

X = df.drop(columns=['label'])
X = X.select_dtypes(include=[np.number])  # Solo columnas numéricas por el tipo de random forest utilizado
y = df['label']

accuracies = []
for i in range(20):
    # Separar en entrenamiento (80%) y prueba (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=i
    )

  #configuracion para evitar el sobreajuste del experimento
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=5,
        max_features='sqrt',
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob >= 0.5).astype(int)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    # metricas
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"\n🔁 Iteración {i+1}")    
    print(f"MSE: {mse:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE: {mae:.4f}")
    print(f"R²: {r2:.4f}")


    accuracies.append(acc)

print("\n🔚 Resultados Finales:")
print(f"✅ Accuracy promedio: {np.mean(accuracies):.4f}")
print(f"📈 Desviación estándar: {np.std(accuracies):.4f}")

