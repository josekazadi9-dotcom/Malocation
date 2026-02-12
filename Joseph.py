# APPLICATION : Malocation (Version Streamlit)

import streamlit as st
import json

FICHIER = "demandeurs.json"

PRIX_MAISONS = {
    "Chambre": 100,
    "Flat": 200,
    "Appartement": 350
}

# Charger les données depuis le fichier JSON
def charger_donnees():
    try:
        with open(FICHIER, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

# Sauvegarder les données dans le fichier JSON
def sauvegarder_donnees(donnees):
    with open(FICHIER, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

# Filtrer les catégories selon salaire et état civil
def filtrer_categories(salaire, etat_civil):
    categories = []
    if salaire > 400:
        categories.append("Flat")
    if salaire > 500:
        categories.append("Appartement")
    if etat_civil != "marié":
        categories.append("Chambre")
    return categories

# Ajouter un demandeur via Streamlit
def ajouter_demandeur(donnees):
    st.subheader("Nouvelle Demande")
    
    with st.form("form_demandeur"):
        nom = st.text_input("Nom")
        postnom = st.text_input("Postnom")
        prenom = st.text_input("Prénom")
        age = st.text_input("Âge")
        etat_civil = st.selectbox("État civil", ["célibataire", "marié"])
        profession = st.text_input("Profession")
        salaire = st.number_input("Salaire de base ($)", min_value=0.0)
        telephone = st.text_input("Téléphone")
        email = st.text_input("Email")
        
        submitted = st.form_submit_button("Ajouter demandeur")
        
        if submitted:
            categories_disponibles = filtrer_categories(salaire, etat_civil)
            
            if not categories_disponibles:
                st.warning("Aucun logement disponible selon vos critères.")
                categorie = "Aucune"
                prix = 0
                final_message = "Nous vous donnerons certaines orientations selon vos moyens."
            else:
                categorie = st.selectbox("Choisissez une catégorie", categories_disponibles)
                prix = PRIX_MAISONS.get(categorie, 0)
                final_message = "Si vous remplissez les conditions, nous vous contacterons pour un rendez-vous."
            
            demandeur = {
                "Nom": nom,
                "Postnom": postnom,
                "Prénom": prenom,
                "Âge": age,
                "Etat_civil": etat_civil,
                "Profession": profession,
                "Salaire": salaire,
                "Categorie": categorie,
                "Prix_loyer": prix,
                "Telephone": telephone,
                "Email": email,
                "Message": final_message
            }
            
            donnees.append(demandeur)
            sauvegarder_donnees(donnees)
            
            st.success("Demandeur enregistré avec succès !")
            st.info(final_message)

# Afficher tous les demandeurs
def afficher_demandeurs(donnees):
    if not donnees:
        st.warning("Aucun demandeur enregistré.")
        return

    st.subheader("Liste des Demandeurs")
    
    trier = st.radio("Trier les demandeurs", ["Aucun", "Par catégorie", "Par salaire"])
    
    if trier == "Par catégorie":
        donnees_sorted = sorted(donnees, key=lambda x: x['Categorie'])
    elif trier == "Par salaire":
        donnees_sorted = sorted(donnees, key=lambda x: x['Salaire'], reverse=True)
    else:
        donnees_sorted = donnees
    
    for i, d in enumerate(donnees_sorted, 1):
        st.markdown(f"### Demandeur {i}")
        st.write(f"**Nom complet:** {d['Nom']} {d['Postnom']} {d['Prénom']}")
        st.write(f"**Âge:** {d['Âge']}")
        st.write(f"**État civil:** {d['Etat_civil']}")
        st.write(f"**Profession:** {d['Profession']}")
        st.write(f"**Salaire:** {d['Salaire']}$")
        st.write(f"**Catégorie:** {d['Categorie']}")
        st.write(f"**Loyer:** {d['Prix_loyer']}$")
        st.write(f"**Téléphone:** {d['Telephone']}")
        st.write(f"**Email:** {d['Email']}")
        st.write(f"**Message:** {d['Message']}")
        st.markdown("---")

# Menu principal Streamlit
def main():
    st.title("Malocation - Gestion des demandes de logement")
    
    donnees = charger_donnees()
    
    menu = st.sidebar.selectbox("Menu", ["Ajouter un demandeur", "Afficher les demandeurs"])
    
    if menu == "Ajouter un demandeur":
        ajouter_demandeur(donnees)
    elif menu == "Afficher les demandeurs":
        afficher_demandeurs(donnees)

if __name__ == "__main__":
    main()