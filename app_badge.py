import streamlit as st
import pandas as pd
#import qrcode
import os
import shutil


# Fichier Excel et dossier QR Code
excel_path = "D:/Badges/badges.xlsx"
qr_dir = "D:/Badges/qrcodes/"
os.makedirs(qr_dir, exist_ok=True)

# Charger les données existantes
def load_data():
    if os.path.exists(excel_path):
        return pd.read_excel(excel_path)
    else:
        return pd.DataFrame(columns=["N° Salarié", "Nom", "Prénom", "Fonction", "Photo", "QRCode"])

# Enregistrer le salarié
def save_employee(data):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(excel_path, index=False)

# Générer le QR Code
def generate_qrcode(numero):
    qr_data = f"https://www.badge.soummam-dz.com/?m={numero}"
    qr_img = qrcode.make(qr_data)
    qr_path = os.path.join(qr_dir, f"{numero}.png")
    qr_img.save(qr_path)
    return qr_path

# Interface Streamlit
st.title("💼 Ajout Salarié - Génération de Badge")

with st.form("ajout_salarie"):
    numero = st.text_input("N° Salarié")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    fonction = st.text_input("Fonction")
    photo_path = st.text_input("Chemin vers la photo", value="D:/Badges/photos/")

    submitted = st.form_submit_button("Ajouter le salarié")

    if submitted:
        if numero and nom and prenom and fonction:
            photo_complete = os.path.join(photo_path, f"{numero}.jpg")
            qr_code_path = generate_qrcode(numero)

            employee_data = {
                "N° Salarié": numero,
                "Nom": nom,
                "Prénom": prenom,
                "Fonction": fonction,
                "Photo": photo_complete,
                "QRCode": qr_code_path
            }

            save_employee(employee_data)
            st.success(f"✅ Salarié {prenom} {nom} ajouté avec succès !")
            st.image(qr_code_path, caption="QR Code généré", width=200)
        else:
            st.error("❌ Merci de remplir tous les champs.")
            st.markdown("---")
st.subheader("🛠 Générer les QR Codes pour tous les salariés existants")

if st.button("🔁 Générer QR Codes"):
    try:
        df = load_data()

        if df.empty:
            st.warning("⚠️ Aucun salarié trouvé dans le fichier Excel.")
        else:
            os.makedirs(qr_dir, exist_ok=True)

            for index, row in df.iterrows():
                numero = str(row["N° Salarié"]).strip()

                if pd.isna(numero) or numero == "":
                    continue

                qr_link = f"https://www.badge.soummam-dz.com/?m={numero}"
                qr_path = os.path.join(qr_dir, f"{numero}.png")

                if not os.path.exists(qr_path):
                    img = qrcode.make(qr_link)
                    img.save(qr_path)

                df.at[index, "QRCode"] = qr_path

            df.to_excel(excel_path, index=False)
            st.success("✅ QR Codes générés et fichier Excel mis à jour avec succès.")
    except Exception as e:
        st.error(f"❌ Erreur : {e}")
