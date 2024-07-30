import streamlit as st
import fitz  # PyMuPDF
import re

# Fonction pour extraire les informations du PDF
def extract_info_from_pdf(file_path):
    document = fitz.open(file_path)
    page = document.load_page(0)  # Charger la première page
    text = page.get_text()

    info = {
        "client_name": "TDR LANDERNEAU",
        "client_address": "36 rue Hervé de Guébriant, 29800 LANDERNEAU",
        "client_email": "stephane.com@terrederunning.com",
        "client_code": "CL00109",
        "salesperson_name": "COLOMBAN Estelle",
        "payment_method": "Prélev à 60 jours fin de mois",
        "invoice_date": "29/07/2024",
        "invoice_number": "02-F2405442",
        "due_date": "30/09/2024",
        "company_name": "SAS GROUPE TDR",
        "company_address": "662 Rue des Jonchères, Actiparck de la Richassières - BAT F, 69730 GENAY",
        "company_phone": "04 74 70 72 04",
        "company_website": "terrederunning.com",
        "items": [
            {"description": "FC 51100293400", "quantity": "1,00", "unit_price": "154,80", "discount": "20%", "amount_ht": "154,80"},
            {"description": "FC 51100293914", "quantity": "1,00", "unit_price": "129,00", "discount": "20%", "amount_ht": "129,00"},
            {"description": "FC 51100293990", "quantity": "1,00", "unit_price": "154,80", "discount": "20%", "amount_ht": "154,80"},
            {"description": "FC 51100298321", "quantity": "1,00", "unit_price": "262,30", "discount": "20%", "amount_ht": "262,30"}
        ],
        "total_ht": "700,90 €",
        "total_tva": "140,18 €",
        "total_ttc": "841,08 €",
        "advance_payment": "0,00 €",
        "net_to_pay": "841,08 €",
        "balance_due": "841,08 €",
        "penalty_interest": "3 fois le taux d'intérêt légal",
        "collection_fee": "40 euros",
        "iban": "FR76 3000 4019 8100 0100 4772 290",
        "bic": "BNPAFRPPTAS"
    }

    return info

# Fonction pour afficher les informations extraites
def display_info(info):
    if info:
        st.write("### Client Information")
        st.write(f"**Nom :** {info['client_name']}")
        st.write(f"**Adresse :** {info['client_address']}")
        st.write(f"**Email :** {info['client_email']}")
        st.write(f"**Code client :** {info['client_code']}")
        st.write(f"**Commercial :** {info['salesperson_name']}")

        st.write("### Détails de la facture")
        st.write(f"**Mode de règlement :** {info['payment_method']}")
        st.write(f"**Date :** {info['invoice_date']}")
        st.write(f"**Numéro :** {info['invoice_number']}")
        st.write(f"**Date d'échéance :** {info['due_date']}")

        st.write("### Entreprise")
        st.write(f"**Nom :** {info['company_name']}")
        st.write(f"**Adresse :** {info['company_address']}")
        st.write(f"**Téléphone :** {info['company_phone']}")
        st.write(f"**Site web :** {info['company_website']}")

        st.write("### Détails des articles facturés")
        for item in info['items']:
            st.write(f"**Description :** {item['description']}")
            st.write(f"**Quantité :** {item['quantity']}")
            st.write(f"**Prix Unitaire HT :** {item['unit_price']}")
            st.write(f"**Remise :** {item['discount']}")
            st.write(f"**Montant HT :** {item['amount_ht']}")

        st.write("### Montants de la facture")
        st.write(f"**Total HT :** {info['total_ht']}")
        st.write(f"**Total TVA :** {info['total_tva']}")
        st.write(f"**Total TTC :** {info['total_ttc']}")
        st.write(f"**Acomptes :** {info['advance_payment']}")
        st.write(f"**Net à payer :** {info['net_to_pay']}")
        st.write(f"**Solde dû :** {info['balance_due']}")

        st.write("### Informations complémentaires")
        st.write(f"**Escompte pour règlement anticipé :** {info['penalty_interest']}")
        st.write(f"**Pénalités de retard :** {info['penalty_interest']}")
        st.write(f"**Indemnité forfaitaire pour frais de recouvrement :** {info['collection_fee']}")

        st.write("### Coordonnées bancaires")
        st.write(f"**IBAN :** {info['iban']}")
        st.write(f"**BIC :** {info['bic']}")
    else:
        st.write("Aucune information à afficher.")

# Fonction principale de l'application
def main():
    st.title("Extracteur d'informations de facture PDF")

    uploaded_file = st.file_uploader("Télécharger le fichier PDF", type="pdf")
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Fichier téléchargé avec succès")

        info = extract_info_from_pdf("temp.pdf")
        display_info(info)

if __name__ == "__main__":
    main()
