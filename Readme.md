# 🌙 Calculateur Universel de Zakat

Un outil moderne et précis pour calculer la Zakat (aumône légale) en fonction des cours de l'or en temps réel. Ce projet propose une interface web élégante et une logique métier rigoureuse basée sur les principes du Fiqh.

## ✨ Fonctionnalités

- **Cours en temps réel** : Récupération automatique du prix de l'or via l'API Yahoo Finance (`yfinance`).
- **Support Multi-devises** : Calcul automatique du Nissab dans la devise de votre choix (MAD, EUR, USD, etc.).
- **Logique de Date (Hawl)** : Vérification de l'écoulement d'une année lunaire (354 jours) à partir de la date d'acquisition du Nissab.
- **Gestion des erreurs** : Saisie robuste des données avec messages d'erreur clairs.
- **Interface Moderne** : UI intuitive propulsée par Streamlit.

## 🛠️ Installation

Ce projet utilise [uv](https://github.com/astral-sh/uv) pour une gestion extrêmement rapide de l'environnement virtuel et des dépendances.

### 1. Cloner le dépôt
```bash
git clone [https://github.com/najibyla/zakat.git](https://github.com/najibyla/zakat.git)
cd zakat
```
### 2. Créer l'environnement virtuel et installer les dépendances
```Bash
uv venv
source .venv/bin/activate  # Sur Linux/macOS
uv pip install -r requirements.txt
```
#### 🚀 Utilisation
Version Interface Web (Recommandé)
Pour lancer l'application avec une interface graphique dans votre navigateur :

```Bash
uv run streamlit run app_ui.py
```
#### Version Terminal
Pour lancer la version classique en ligne de commande :

```Bash
uv run python main.py
```
### 📖 Rappels Juridiques (Fiqh) intégrés
- Nissab : Fixé à la valeur de 85 grammes d'or pur.
- Hawl : La richesse doit être possédée depuis une année lunaire complète.
- Taux : 2.5% sur les liquidités et le commerce, 5% ou 10% pour l'agriculture, 20% pour les trésors.

### 🧰 Technologies utilisées
- Python 3.13+
- Streamlit (Interface utilisateur)
- yfinance (Données boursières en temps réel)
- uv (Gestionnaire de paquets)

Développé avec soin par najibyla
