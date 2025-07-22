import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("sitios_con_metadata.csv")

# Crear ssl_confiable y eliminar columnas individuales (evitar sesgos)
df["ssl_confiable"] = df["tiene_ssl"] & df["ssl_valido"]
df = df.drop(columns=["tiene_ssl", "ssl_valido"])

features = [
    'ssl_confiable', 'hsts', 'csp', 'x_content_type_options', 'x_frame_options',
    'cookies_seguras', 'url_sospechosa', 'longitud_texto', 'caracteres_extranos',
    'dominio_gobierno_edu', 'num_imagenes', 'tiene_favicon', 'referrer_policy', 'nro_guiones'
]

X = df[features]
y = df["label"]

le = LabelEncoder()
y_encoded = le.fit_transform(y) # Codificar etiquetas

# Definir umbral personalizado
umbral = 0.85

accuracies = []

for i in range(20):
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=i)


    clf = RandomForestClassifier(class_weight='balanced', random_state=i)
    clf.fit(X_train, y_train)
    y_probs = clf.predict_proba(X_test)[:, 1]
    y_pred = (y_probs >= umbral).astype(int)

    # metricas
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    accuracies.append(acc)

    print(f"\n🎯 Corrida {i + 1}")
    print(f"📊 Accuracy: {acc:.4f}")
    print(f"\n📉 Matriz de confusión:\n{cm}")
    print(f"\n📋 Reporte de clasificación:\n{report}")
    

    # Validación cruzada (5 folds)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
    print("\n🔁 Validación cruzada (5-fold):")
    print("Accuracies por fold:", scores)
    print("Promedio:", scores.mean())
    print("Desviación estándar:", scores.std())

#  Importancia de características, como las toma el experimento
importancia = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
print("\n⭐ Importancia de las características:")
print(importancia)

print("\n🔁 Resumen de 20 corridas:")
print("📊 Accuracy promedio:", round(np.mean(accuracies), 4))
print("📉 Desviación estándar:", round(np.std(accuracies), 4))

