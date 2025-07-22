import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("sitios_con_metadata.csv")
print("PEURB")
for col in ['ssl_valido', 'hsts', 'x_content_type_options', 'referrer_policy', 'csp', 'x_frame_options', 'cookies_seguras']:
    print(f"{col}:\n{df[col].value_counts(normalize=True)}\n")

# Crear ssl_confiable y eliminar los campos originales
df["ssl_confiable"] = df["tiene_ssl"] & df["ssl_valido"]
df = df.drop(columns=["tiene_ssl", "ssl_valido"])

features = [ 'ssl_confiable', 'hsts','csp','x_content_type_options', 'x_frame_options','cookies_seguras','url_sospechosa',
    'longitud_texto', 'caracteres_extranos', 'dominio_gobierno_edu',
    'num_imagenes', 'tiene_favicon',
    'referrer_policy',
    'nro_guiones'
]

X = df[features]
y = df['label']




#   80% entrenamiento, 20% prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)

#  Random Forest
clf = RandomForestClassifier(class_weight='balanced', random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

print("📊 Accuracy:", accuracy_score(y_test, y_pred))
print("\n🧮 Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))
print("\n📋 Reporte de clasificación:")
print(classification_report(y_test, y_pred))

# Validación cruzada (5 folds)
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(clf, X, y, cv=cv, scoring='accuracy')
print("\nValidación cruzada (5-fold):")
print("Accuracies por fold:", scores)
print("Promedio:", scores.mean())
print("Desviación estándar:", scores.std())

# Importancia de características
importancia = pd.Series(clf.feature_importances_, index=features).sort_values(ascending=False)
print("\nImportancia de las características:")
print(importancia)





