import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from scipy.sparse import hstack, csr_matrix
from imblearn.over_sampling import SMOTE

# Asumiendo que tienes el dataframe 'df' con todas las features ya preparadas

# Codificar etiquetas
le = LabelEncoder()
y = le.fit_transform(df["label"])

# Vectorizar texto
vectorizer = TfidfVectorizer(max_features=1000)
texto_completo = df["Título"] + " " + df["Descripción"]
X_text = vectorizer.fit_transform(texto_completo)

# Variables numéricas
features_num = [
    "Cantidad de imágenes",
    "Enlaces internos",
    "Enlaces externos",
    "longitud_titulo",
    "palabras_titulo",
    "longitud_desc",
    "palabras_desc",
    "prop_enlaces_int_ext",
    "total_enlaces"
]
X_num = df[features_num].fillna(0)
X_num_sparse = csr_matrix(X_num.values)

# Combinar features
X = hstack([X_text, X_num_sparse])

# Dividir antes de aplicar SMOTE para evitar fuga de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Aplicar SMOTE SOLO en datos de entrenamiento (X_train es sparse, se convierte a denso)
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train.todense(), y_train)

# Entrenar Random Forest
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train_res, y_train_res)

# Evaluar
y_pred = clf.predict(X_test.todense())
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=le.classes_))

