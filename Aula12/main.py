"""
Exercício: kNN aplicado ao dataset de Dengue (SINAN)
Target: classi_fin (classificação final)
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings("ignore")
# ─── 1. CARREGAR O DATASET ────────────────────────────────────────────────────
df = pd.read_csv("dataset.csv", low_memory=False)
print(f"Shape original: {df.shape}")

# ─── 2. DEFINIR O TARGET ──────────────────────────────────────────────────────
TARGET = "classi_fin"

# Remove linhas sem target
df = df.dropna(subset=[TARGET])
df[TARGET] = df[TARGET].astype(int)

# Mapeamento dos códigos do SINAN para classi_fin:
#   5  = Descartado
#   10 = Dengue
#   11 = Dengue com sinais de alarme
#   12 = Dengue grave
#   13 = Chikungunya
label_map = {5: "Descartado", 10: "Dengue", 11: "Dengue c/ alarme", 12: "Dengue grave", 13: "Chikungunya"}
df["classi_label"] = df[TARGET].map(label_map).fillna("Outro")
print("\nDistribuição do target:")
print(df["classi_label"].value_counts())

# ─── 3. SELECIONAR FEATURES ───────────────────────────────────────────────────
# Features clínicas e demográficas relevantes para o modelo
FEATURES_CANDIDATAS = [
    # Demográficas
    "nu_idade_n", "cs_sexo", "cs_gestant", "cs_raca", "cs_escol_n",
    # Sintomas (1=Sim, 2=Não)
    "febre", "mialgia", "cefaleia", "exantema", "vomito", "nausea",
    "dor_costas", "conjuntvit", "artrite", "artralgia", "petequia_n",
    "leucopenia", "laco", "dor_retro",
    # Comorbidades
    "diabetes", "hematolog", "hepatopat", "renal", "hipertensa", "acido_pept",
    # Sinais de alarme
    "alrm_hipot", "alrm_plaq", "alrm_vom", "alrm_sang", "alrm_hemat",
    "alrm_abdom", "alrm_letar", "alrm_hepat", "alrm_liq",
    # Hospitalização
    "hospitaliz",
]

# Mantém apenas as que existem no dataframe
features_presentes = [f for f in FEATURES_CANDIDATAS if f in df.columns]
df_model = df[features_presentes + [TARGET]].copy()

print(f"\nFeatures candidatas : {len(FEATURES_CANDIDATAS)}")
print(f"Features presentes  : {len(features_presentes)}")

# ─── 4. REMOVER COLUNAS COM >50% NULOS ───────────────────────────────────────
limite_nulos = 0.50
nulos_pct = df_model.isnull().mean()
colunas_remover = nulos_pct[nulos_pct > limite_nulos].index.tolist()
if TARGET in colunas_remover:
    colunas_remover.remove(TARGET)

df_model = df_model.drop(columns=colunas_remover)
print(f"\nColunas removidas (>50% nulos): {colunas_remover}")
print(f"Features restantes: {[c for c in df_model.columns if c != TARGET]}")

# ─── 5. TRATAR VALORES AUSENTES RESTANTES ────────────────────────────────────
# Força o mapeamento direto de M/F/I para números, sem depender de checagem de tipo
if "cs_sexo" in df_model.columns:
    df_model["cs_sexo"] = df_model["cs_sexo"].replace({"M": 0, "F": 1, "I": 2})

# Colunas categóricas binárias (1/2): imputa com moda
# Colunas numéricas contínuas: imputa com mediana
for col in df_model.columns:
    if col == TARGET:
        continue
    if df_model[col].isnull().any():
        if df_model[col].nunique() <= 10:
            df_model[col] = df_model[col].fillna(df_model[col].mode()[0])
        else:
            df_model[col] = df_model[col].fillna(df_model[col].median())
            
print(f"\nShape após limpeza: {df_model.shape}")
print(f"Nulos restantes   : {df_model.isnull().sum().sum()}")

# ─── 6. SEPARAR X e y ────────────────────────────────────────────────────────
# BLINDAGEM: Converte todas as features preditoras à força para float. 
# Qualquer string perdida ou espaço em branco do SINAN (" ", "NA") vira NaN e depois é preenchido com 0.
X_df = df_model.drop(columns=[TARGET]).apply(pd.to_numeric, errors='coerce').fillna(0)

X = X_df.values
y = df_model[TARGET].values
feature_names = X_df.columns.tolist()
# ─── 7. DIVIDIR (70% treino / 30% teste) ─────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
print(f"\nTreino: {len(X_train)} | Teste: {len(X_test)}")

# ─── 8. ESCALONAMENTO (StandardScaler) ───────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ─── 9. BUSCA DO MELHOR k COM VALIDAÇÃO CRUZADA ───────────────────────────────
k_values     = range(1, 16, 2)
weight_types = ["uniform", "distance"]

print(f"\n{'k':>4} {'weights':>10} {'CV mean':>10} {'CV std':>8}")
print("-" * 40)

results = []
for weights in weight_types:
    for k in k_values:
        knn = KNeighborsClassifier(n_neighbors=k, weights=weights, n_jobs=-1)
        cv_scores = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring="accuracy")
        results.append({
            "k": k, "weights": weights,
            "cv_mean": cv_scores.mean(),
            "cv_std":  cv_scores.std(),
        })
        print(f"{k:>4} {weights:>10} {cv_scores.mean():>10.4f} {cv_scores.std():>8.4f}")

# ─── 10. MELHOR MODELO ────────────────────────────────────────────────────────
best = max(results, key=lambda r: (r["cv_mean"], -r["cv_std"]))
print(f"\nMelhor configuração : k={best['k']}, weights='{best['weights']}'")
print(f"CV acurácia média   : {best['cv_mean']:.4f} ± {best['cv_std']:.4f}")

knn_best = KNeighborsClassifier(n_neighbors=best["k"], weights=best["weights"], n_jobs=-1)
knn_best.fit(X_train_scaled, y_train)
y_pred = knn_best.predict(X_test_scaled)

test_acc = accuracy_score(y_test, y_pred)
print(f"Acurácia no teste   : {test_acc:.4f}")

# ─── 11. IMPACTO DO ESCALONAMENTO ─────────────────────────────────────────────
knn_raw = KNeighborsClassifier(n_neighbors=best["k"], weights=best["weights"], n_jobs=-1)
knn_raw.fit(X_train, y_train)
raw_acc = accuracy_score(y_test, knn_raw.predict(X_test))
print(f"\nAcurácia SEM escalonamento : {raw_acc:.4f}")
print(f"Acurácia COM escalonamento : {test_acc:.4f}")

# ─── 12. RELATÓRIO FINAL ──────────────────────────────────────────────────────
classes_presentes = sorted(df_model[TARGET].unique().astype(int))
nomes_classes = [label_map.get(c, str(c)) for c in classes_presentes]

print("\n--- Relatório de classificação ---")
print(classification_report(y_test, y_pred, target_names=nomes_classes))

print("--- Matriz de confusão ---")
cm = confusion_matrix(y_test, y_pred)
header = f"{'':>20}" + "".join(f"{n:>20}" for n in nomes_classes)
print(header)
for i, row in enumerate(cm):
    print(f"{nomes_classes[i]:>20}" + "".join(f"{v:>20}" for v in row))