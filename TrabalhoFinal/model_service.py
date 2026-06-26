import logging
import warnings

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, r2_score, mean_squared_error, roc_auc_score
)

try:
    from imblearn.over_sampling import SMOTE
    _tem_smote = True
except ImportError:
    _tem_smote = False
    from sklearn.utils import resample

warnings.filterwarnings("ignore", category=UserWarning)
logger = logging.getLogger(__name__)


def _features_para_classificacao(df):
    cols = ["idade_anos", "febre", "mialgia", "cefaleia", "exantema",
            "vomito", "nausea", "dor_costas", "dor_retro", "artralgia",
            "artrite", "conjuntvit", "petequia_n", "leucopenia", "laco",
            "diabetes", "hipertensa", "hematolog", "hepatopat", "renal"]
    cols = [c for c in cols if c in df.columns]
    X = df[cols].copy()
    for c in X.columns:
        X[c] = pd.to_numeric(X[c], errors="coerce").fillna(0)
    return X


def _selecionar_target(df, nome_desejado="obito", fallback="hospitaliz_bin"):
    alvo = None
    nome_final = nome_desejado
    for candidate in [nome_desejado, fallback]:
        if candidate in df.columns:
            s = df[candidate]
            vc = s.value_counts()
            if s.nunique() >= 2 and vc.min() >= 2:
                alvo = s
                nome_final = candidate
                break
    if alvo is None:
        for candidate in [nome_desejado, fallback]:
            if candidate in df.columns:
                s = df[candidate]
                if s.nunique() < 2:
                    logger.warning("Target '%s' possui apenas uma classe (%d).", candidate, s.nunique())
                else:
                    logger.warning("Target '%s' tem classe minoritaria com apenas %d amostra(s).", candidate, s.value_counts().min())
    return alvo, nome_final


def run_knn(df):
    logger.info("=" * 50)
    logger.info("KNN - Classificacao (com balanceamento)")

    y, target_name = _selecionar_target(df)
    if y is None:
        logger.warning("Nenhum target viavel. Pulando KNN.")
        return None

    X = _features_para_classificacao(df)
    if X.shape[1] == 0:
        logger.warning("Nenhuma feature disponivel. Pulando KNN.")
        return None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if _tem_smote:
        logger.info("Aplicando SMOTE no treino (k_neighbors=3)...")
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_train, y_train = smote.fit_resample(X_train, y_train)
        logger.info("Treino apos SMOTE: %d amostras", len(y_train))
    else:
        logger.info("SMOTE indisponivel. Fazendo upsample manual...")
        df_train = pd.concat([X_train, y_train], axis=1)
        majoritaria = df_train[df_train[target_name] == 0]
        minoritaria = df_train[df_train[target_name] == 1]
        n_min = len(minoritaria)
        if n_min > 0:
            minoritaria_up = resample(minoritaria, replace=True, n_samples=len(majoritaria), random_state=42)
            df_bal = pd.concat([majoritaria, minoritaria_up])
            X_train = df_bal.drop(columns=[target_name])
            y_train = df_bal[target_name]
            logger.info("Treino apos upsample: %d amostras", len(y_train))
        else:
            logger.warning("Classe minoritaria vazia mesmo apos split.")

    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1_bin = f1_score(y_test, y_pred, zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 0.0

    logger.info("Target: %s", target_name)
    logger.info("Acuracia: %.4f | Precision: %.4f | Recall: %.4f | F1: %.4f", acc, prec, rec, f1_bin)
    logger.info("F1-Macro: %.4f | ROC-AUC: %.4f", f1_macro, auc)
    logger.info("Matriz de Confusao:\n%s", cm)

    return {
        "modelo": "KNN",
        "tipo": "classificacao",
        "target": target_name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1_bin,
        "f1_macro": f1_macro,
        "roc_auc": auc,
        "confusion_matrix": cm,
        "y_test": y_test,
        "y_pred": y_pred,
    }


def run_regressao_simples(df_agg_semana):
    logger.info("=" * 50)
    logger.info("Regressao Linear Simples (casos ~ sem_not)")

    if df_agg_semana is None or "casos" not in df_agg_semana.columns:
        logger.warning("Agregacao semanal nao disponivel. Pulando Reg. Simples.")
        return None

    agg = df_agg_semana.copy()
    logger.info("df_agg_semana.shape: %s", agg.shape)
    logger.info("df_agg_semana.head(3):\n%s", agg.head(3).to_string())
    logger.info("casos - min: %d  max: %d  media: %.1f  std: %.1f",
                 agg["casos"].min(), agg["casos"].max(),
                 agg["casos"].mean(), agg["casos"].std())

    if agg.shape[0] < 5:
        logger.warning("Poucas semanas (%d) para regressao.", agg.shape[0])
        return None

    agg["sem_not_int"] = pd.to_numeric(agg["sem_not"], errors="coerce")
    X = agg[["sem_not_int"]].values
    y = agg["casos"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    logger.info("R²: %.4f | RMSE: %.2f", r2, rmse)

    return {
        "modelo": "Regressao Linear Simples",
        "tipo": "regressao",
        "r2": r2,
        "rmse": rmse,
        "y_test": y_test,
        "y_pred": y_pred,
    }


def run_regressao_multipla_regularizada(df_agg_semana):
    logger.info("=" * 50)
    logger.info("Regressao Regularizada (Ridge + Lasso) com tuning de alpha")

    if df_agg_semana is None or "casos" not in df_agg_semana.columns:
        logger.warning("Agregacao semanal nao disponivel. Pulando Reg. Regularizada.")
        return None

    agg = df_agg_semana.copy()
    logger.info("df_agg_semana.shape: %s", agg.shape)
    logger.info("df_agg_semana.head(3):\n%s", agg.head(3).to_string())

    if agg.shape[0] < 10:
        logger.warning("Poucas linhas (%d) para regressao regularizada.", agg.shape[0])
        return None

    agg["sem_not_int"] = pd.to_numeric(agg["sem_not"], errors="coerce")
    agg["nu_ano"] = pd.to_numeric(agg["nu_ano"], errors="coerce").fillna(0)

    features = ["sem_not_int", "nu_ano"]

    if "sg_uf_not" in agg.columns:
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        agg["uf_encoded"] = le.fit_transform(agg["sg_uf_not"].astype(str))
        features.append("uf_encoded")

    logger.info("Features para regressao regularizada: %s", features)

    X = agg[features].values
    y = agg["casos"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    alphas = np.logspace(-3, 3, 20)
    resultados = []

    for ModelClass, nome in [(Ridge, "Ridge"), (Lasso, "Lasso")]:
        scores = []
        for alpha in alphas:
            model = ModelClass(alpha=alpha, max_iter=10000, random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            scores.append(r2_score(y_test, y_pred))

        best_idx = int(np.argmax(scores))
        best_alpha = float(alphas[best_idx])

        best_model = ModelClass(alpha=best_alpha, max_iter=10000, random_state=42)
        best_model.fit(X_train, y_train)
        y_pred = best_model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        logger.info("%s - Melhor alpha: %.4f | R²: %.4f | RMSE: %.2f",
                     nome, best_alpha, r2, rmse)

        resultados.append({
            "modelo": f"Regressao {nome}",
            "tipo": "regressao",
            "r2": r2,
            "rmse": rmse,
            "y_test": y_test,
            "y_pred": y_pred,
            "alpha_curve": {
                "alphas": alphas.tolist(),
                "scores": scores,
                "best_alpha": best_alpha,
            },
        })

    return resultados


def run_logistica(df):
    logger.info("=" * 50)
    logger.info("Regressao Logistica (class_weight=balanced)")

    y, target_name = _selecionar_target(df)
    if y is None:
        logger.warning("Nenhum target viavel. Pulando Reg. Logistica.")
        return None

    X = _features_para_classificacao(df)
    if X.shape[1] == 0:
        logger.warning("Nenhuma feature disponivel. Pulando Reg. Logistica.")
        return None

    feature_names = X.columns.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if _tem_smote:
        logger.info("Aplicando SMOTE no treino (k_neighbors=3)...")
        smote = SMOTE(random_state=42, k_neighbors=3)
        X_train, y_train = smote.fit_resample(X_train, y_train)
        logger.info("Treino apos SMOTE: %d amostras", len(y_train))

    model = LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1_bin = f1_score(y_test, y_pred, zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob) if len(np.unique(y_test)) > 1 else 0.0

    logger.info("Target: %s", target_name)
    logger.info("Acuracia: %.4f | Precision: %.4f | Recall: %.4f | F1: %.4f", acc, prec, rec, f1_bin)
    logger.info("F1-Macro: %.4f | ROC-AUC: %.4f", f1_macro, auc)
    logger.info("Matriz de Confusao:\n%s", cm)

    return {
        "modelo": "Regressao Logistica",
        "tipo": "classificacao",
        "target": target_name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1_bin,
        "f1_macro": f1_macro,
        "roc_auc": auc,
        "confusion_matrix": cm,
        "y_test": y_test,
        "y_pred": y_pred,
        "y_prob": y_prob,
        "coef": model.coef_[0].tolist(),
        "feature_names": feature_names,
    }


def run_models(df, df_agg_semana=None):
    logger.info("=" * 60)
    logger.info("INICIANDO MODELAGEM")
    logger.info("=" * 60)

    resultados = []

    knn = run_knn(df)
    if knn:
        resultados.append(knn)

    reg_simples = run_regressao_simples(df_agg_semana)
    if reg_simples:
        resultados.append(reg_simples)

    reg_ridge_lasso = run_regressao_multipla_regularizada(df_agg_semana)
    if reg_ridge_lasso:
        resultados.extend(reg_ridge_lasso)

    logistica = run_logistica(df)
    if logistica:
        resultados.append(logistica)

    logger.info("=" * 60)
    logger.info("MODELAGEM FINALIZADA - %d modelos executados.", len(resultados))
    logger.info("=" * 60)

    return resultados
