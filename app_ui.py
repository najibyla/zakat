import streamlit as st
import yfinance as yf
from datetime import datetime, date

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Calculateur Zakat", page_icon="🌙", layout="centered")

# --- FONCTION DE RÉCUPÉRATION (Avec système de Cache) ---
# Le "@st.cache_data" évite de recharger le cours de l'or à chaque clic !
@st.cache_data(ttl=3600) 
def obtenir_prix_or_gramme(devise):
    or_ticker = yf.Ticker("GC=F")
    prix_once_usd = or_ticker.history(period="1d")['Close'].iloc[-1]
    prix_gramme_usd = prix_once_usd / 31.1034768
    
    if devise == "USD":
        return prix_gramme_usd
        
    taux_ticker = yf.Ticker(f"USD{devise}=X")
    taux_change = taux_ticker.history(period="1d")['Close'].iloc[-1]
    return prix_gramme_usd * taux_change

# --- EN-TÊTE DE L'INTERFACE ---
st.title("🌙 Calculateur Universel de Zakat")
st.markdown("Calculez votre aumône purificatrice facilement, selon le cours de l'or en temps réel et les règles du Fiqh.")
st.divider()

# --- COLONNES POUR DEVISE ET NISSAB ---
col1, col2 = st.columns([1, 2])

with col1:
    devise = st.selectbox("Choisissez votre devise", ["MAD", "EUR", "USD", "CAD", "DZD", "TND"], index=0)

with col2:
    try:
        prix_or_gramme = obtenir_prix_or_gramme(devise)
        nissab_monnaie = 85 * prix_or_gramme
        st.info(f"💡 **NISSAB DU JOUR**\n\nLe seuil (85g d'or) est fixé à : **{nissab_monnaie:,.2f} {devise}**")
    except Exception:
        st.error("❌ Impossible de récupérer le cours de l'or. Mode manuel activé.")
        prix_or_gramme = st.number_input("Prix d'un gramme d'or", min_value=1.0, value=1500.0)
        nissab_monnaie = 85 * prix_or_gramme

st.divider()

# --- FORMULAIRE INTERACTIF ---
st.subheader("📝 Vos informations")

nature = st.selectbox(
    "Nature du bien à déclarer :", 
    ["Monnaie (Argent liquide, épargne, or...)", "Commerce (Marchandises)", "Agriculture (Récoltes)", "Trésor (Rikaz)"]
)

montant = st.number_input(f"Montant total possédé aujourd'hui (en {devise}) :", min_value=0.0, step=1000.0, format="%f")

# Affichage dynamique des champs selon la nature
date_nissab = None
irrigation = None

if "Monnaie" in nature or "Commerce" in nature:
    if montant >= nissab_monnaie:
        date_nissab = st.date_input("📅 À quelle date avez-vous atteint le Nissab pour la première fois ?", max_value=date.today())
        st.caption("Rappel : Le Hawl (année lunaire) dure environ 354 jours.")
    elif montant > 0:
        st.warning(f"Le montant saisi n'atteint pas le Nissab actuel de {nissab_monnaie:,.2f} {devise}.")

elif "Agriculture" in nature:
    irrigation = st.radio("💧 Type d'irrigation :", ["Naturelle (pluie, fleuves...) -> 10%", "Artificielle (système payant...) -> 5%"])

# --- BOUTON DE CALCUL ---
st.divider()
if st.button("🚀 Calculer ma Zakat", type="primary"):
    
    if "Monnaie" in nature or "Commerce" in nature:
        if montant < nissab_monnaie:
            st.error(f"❌ **Zakat non due.** Votre montant n'atteint pas le seuil des 85g d'or.")
        else:
            jours_ecoules = (date.today() - date_nissab).days
            if jours_ecoules >= 354:
                montant_zakat = montant * 0.025
                eq_or = montant_zakat / prix_or_gramme
                st.success(f"✅ **RÉSULTAT**\n\nLa Zakat est due. Vous devez verser **2.5%** de votre montant actuel.\n\n"
                           f"Montant à payer : **{montant_zakat:,.2f} {devise}** (soit l'équivalent de {eq_or:.2f}g d'or).")
                st.balloons() # Petite animation sympa !
            else:
                jours_restants = 354 - jours_ecoules
                st.warning(f"⏳ **Zakat non due pour le moment.**\n\nVous avez atteint le Nissab il y a {jours_ecoules} jours. "
                           f"Il reste environ **{jours_restants} jours** avant l'échéance de votre Hawl.")
                
    elif "Agriculture" in nature:
        taux = 0.10 if "Naturelle" in irrigation else 0.05
        montant_zakat = montant * taux
        eq_or = montant_zakat / prix_or_gramme
        st.success(f"✅ **RÉSULTAT**\n\nLa Zakat est due le jour de la moisson (taux de {taux*100}%).\n\n"
                   f"Montant à verser : **{montant_zakat:,.2f} {devise}** (soit {eq_or:.2f}g d'or).")
                   
    elif "Trésor" in nature:
        montant_zakat = montant * 0.20
        eq_or = montant_zakat / prix_or_gramme
        st.success(f"✅ **RÉSULTAT**\n\nLa Zakat est due immédiatement au moment de la découverte (taux de 20%).\n\n"
                   f"Montant à verser : **{montant_zakat:,.2f} {devise}** (soit {eq_or:.2f}g d'or).")