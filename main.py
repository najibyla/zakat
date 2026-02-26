import yfinance as yf
from datetime import datetime
import os
import contextlib

def obtenir_prix_or_gramme(devise="MAD"):
    """
    Récupère le prix actuel d'un gramme d'or dans la devise spécifiée via Yahoo Finance.
    Masque les erreurs internes de l'API pour garder un affichage propre.
    """
    print(f"🌍 Connexion au marché pour récupérer le cours de l'or en {devise.upper()}...")
    
    try:
        # On crée un "trou noir" pour masquer les erreurs rouges et moches de yfinance
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                or_ticker = yf.Ticker("GC=F")
                prix_once_usd = or_ticker.history(period="1d")['Close'].iloc[-1]
                prix_gramme_usd = prix_once_usd / 31.1034768
                
                if devise.upper() != "USD":
                    taux_ticker = yf.Ticker(f"USD{devise.upper()}=X")
                    taux_change = taux_ticker.history(period="1d")['Close'].iloc[-1]
                else:
                    taux_change = 1
                    
        # On calcule le prix final en dehors du bloc silencieux pour pouvoir l'afficher
        prix_final = prix_gramme_usd * taux_change
        print(f"✔️ Prix actuel de l'or : {prix_final:.2f} {devise.upper()} / gramme.")
        return prix_final
        
    except Exception:
        # Notre message propre s'affiche au lieu du pavé d'erreur de Yahoo
        print(f"❌ Impossible de récupérer le cours pour la devise '{devise.upper()}'.")
        
        while True:
            try:
                prix_manuel = float(input(f"-> Veuillez entrer manuellement le prix d'un gramme d'or en {devise.upper()} : "))
                if prix_manuel > 0:
                    return prix_manuel
                print("⚠️ Erreur : Le prix doit être supérieur à zéro.")
            except ValueError:
                print("⚠️ Erreur : Veuillez entrer un montant numérique valide (utilisez un point pour les décimales).")

def calculer_zakat():
    print("=== CALCULATEUR UNIVERSEL DE ZAKAT ===")
    
    # --- BOUCLE POUR LA DEVISE (Force 3 lettres) ---
    while True:
        devise = input("Entrez votre devise en 3 lettres (ex: MAD, EUR, USD, CAD) : ").strip().upper()
        if len(devise) == 3 and devise.isalpha():
            break
        print("⚠️ Erreur : La devise doit obligatoirement comporter 3 lettres (ex: MAD).")
    
    prix_or_gramme = obtenir_prix_or_gramme(devise)
    nissab_or_grammes = 85
    nissab_monnaie = nissab_or_grammes * prix_or_gramme

    print("\n" + "="*70)
    print(f"💡 INFORMATION NISSAB DU JOUR :")
    print(f"Le seuil de la Zakat (85g d'or) est aujourd'hui fixé à : {nissab_monnaie:.2f} {devise}")
    print(f"📌 Rappel (Fiqh) : Le calcul doit toujours se baser sur le cours")
    print(f"de l'or le jour où la Zakat est due (Hawl), et non le jour d'acquisition.")
    print("="*70 + "\n")

    print("Natures de biens disponibles :")
    print("1. monnaie (Argent liquide, épargne, or)")
    print("2. commerce (Marchandises destinées à la vente)")
    print("3. agriculture (Récoltes et fruits)")
    print("4. tresor (Trésors ou minerais découverts)")
    
    correspondances = {
        '1': 'monnaie', 'monnaie': 'monnaie',
        '2': 'commerce', 'commerce': 'commerce',
        '3': 'agriculture', 'agriculture': 'agriculture',
        '4': 'tresor', 'tresor': 'tresor'
    }
    
    while True:
        choix_nature = input("\nEntrez la nature du bien (1/2/3/4 ou le nom) : ").strip().lower()
        if choix_nature in correspondances:
            nature = correspondances[choix_nature]
            break
        print("⚠️ Erreur : La nature du bien saisie n'est pas reconnue. Veuillez réessayer.")
    
    print("\n💰 QUEL MONTANT DÉCLARER ?")
    print("Rappel (Fiqh) : Vous devez déclarer le montant TOTAL que vous possédez AUJOURD'HUI")
    print("(le jour de l'échéance de votre Hawl), et non le montant du premier jour.")
    
    while True:
        try:
            montant = float(input(f"-> Entrez votre montant actuel (en {devise}) : "))
            if montant >= 0:
                break
            print("⚠️ Erreur : Le montant ne peut pas être négatif.")
        except ValueError:
            print("⚠️ Erreur : Veuillez entrer un chiffre valide (ex: 130000 ou 130000.50).")

    # --- LOGIQUE DE CALCUL ---
    if nature in ['monnaie', 'commerce']:
        if montant >= nissab_monnaie:
            while True:
                date_saisie = input("\nÀ quelle date avez-vous atteint le Nissab pour la première fois ? (format JJ/MM/AAAA) : ").strip()
                try:
                    date_nissab = datetime.strptime(date_saisie, "%d/%m/%Y")
                    break
                except ValueError:
                    print("⚠️ Erreur : Le format de la date est incorrect. Veuillez utiliser EXACTEMENT le format JJ/MM/AAAA (ex: 03/03/2025).")
            
            date_actuelle = datetime.now()
            jours_ecoules = (date_actuelle - date_nissab).days
            
            if jours_ecoules >= 354:
                taux = 2.5
                temps = f"{jours_ecoules} jours (soit plus d'une année lunaire)"
                montant_zakat = montant * (taux / 100)
                eq_or = montant_zakat / prix_or_gramme
                
                return (f"\n✅ RÉSULTAT :\nLa zakat de ({nature}) est de {taux}% du montant que tu possèdes "
                        f"après avoir passé {temps} et s'élève à {montant_zakat:.2f} {devise} "
                        f"correspondant à {eq_or:.2f} grammes d'or.")
            else:
                jours_restants = 354 - jours_ecoules
                return (f"\n⏳ RÉSULTAT :\nLa Zakat n'est pas encore due. Vous avez atteint le Nissab il y a {jours_ecoules} jours.\n"
                        f"Il vous reste environ {jours_restants} jours pour compléter une année lunaire (Hawl).")
                
        else:
            return (f"\n❌ RÉSULTAT :\nLa Zakat n'est pas due. Votre montant ({montant:.2f} {devise}) n'atteint pas le Nissab actuel "
                    f"qui est de {nissab_monnaie:.2f} {devise} (85 grammes d'or).")

    elif nature == 'agriculture':
        print("\nType d'irrigation :")
        print("a. Naturelle (pluie, fleuve...) -> 10%")
        print("b. Artificielle (système payant, effort...) -> 5%")
        
        while True:
            irrigation = input("Choisissez l'irrigation (a/b) : ").strip().lower()
            if irrigation in ['a', 'b']:
                break
            print("⚠️ Erreur : Choix invalide. Veuillez entrer 'a' ou 'b'.")
        
        taux = 10 if irrigation == 'a' else 5
        temps = "le jour de la moisson"
        montant_zakat = montant * (taux / 100)
        eq_or = montant_zakat / prix_or_gramme
        
        return (f"\n✅ RÉSULTAT :\nLa zakat de ({nature}) est de {taux}% de la valeur de la récolte "
                f"due après avoir passé {temps} et s'élève à {montant_zakat:.2f} {devise} "
                f"correspondant à {eq_or:.2f} grammes d'or.")

    elif nature == 'tresor':
        taux = 20
        temps = "le moment de sa découverte"
        montant_zakat = montant * (taux / 100)
        eq_or = montant_zakat / prix_or_gramme
        
        return (f"\n✅ RÉSULTAT :\nLa zakat de ({nature}) est de {taux}% du montant "
                f"due après avoir passé {temps} et s'élève à {montant_zakat:.2f} {devise} "
                f"correspondant à {eq_or:.2f} grammes d'or.")

if __name__ == "__main__":
    print(calculer_zakat())
    print("\n" + "-"*50 + "\n")