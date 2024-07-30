import streamlit as st
import fitz  # PyMuPDF
import re

# Fonction pour extraire les informations du PDF
def extract_info_from_pdf(file_path):
    document = fitz.open(file_path)
    page = document.load_page(0)  # Charger la première page
    text = page.get_text()

    # Fonction pour extraire un texte basé sur un motif
    def extract_value(pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else "Non trouvé"

    # Extraction des informations
    info = {
        "client_name": extract_value(r"(?<=Nom :\s)(.*?)(?=\n)", text),
        "client_address": extract_value(r"(?<=Adresse :\s)(.*?)(?=\n)", text),
        "client_email": extract_value(r"(?<=Email :\s)(.*?)(?=\n)", text),
        "client_code": extract_value(r"(?<=Code client :\s)(.*?)(?=\n)", text),
        "salesperson_name": extract_value(r"(?<=Commercial :\s)(.*?)(?=\n)", text),
        "payment_method": extract_value(r"(?<=Mode de règlement :\s)(.*?)(?=\n)", text),
        "invoice_date": extract_value(r"(?<=Date :\s)(.*?)(?=\n)", text),
        "invoice_number": extract_value(r"(?<=Numéro :\s)(.*?)(?=\n)", text),
        "due_date": extract_value(r"(?<=Date d'échéance :\s)(.*?)(?=\n)", text),
        "company_name": extract_value(r"(?<=Nom :\s)(.*?)(?=\n)", text),
        "company_address": extract_value(r"(?<=Adresse :\s)(.*?)(?=\n)", text),
        "company_phone": extract_value(r"(?<=Téléphone :\s)(.*?)(?=\n)", text),
        "company_website": extract_value(r"(?<=Site web :\s)(.*?)(?=\n)", text),
        "items": extract_value(r"(?<=Détails des articles facturés)(.*?)(?=\n\n)", text),
        "total_ht": extract_value(r"(?<=Total HT :\s)(.*?)(?=\n)", text),
        "total_tva": extract_value(r"(?<=Total TVA :\s)(.*?)(?=\n)", text),
        "total_ttc": extract_value(r"(?<=Total TTC :\s)(.*?)(?=\n)", text),
        "advance_payment": extract_value(r"(?<=Acomptes :\s)(.*?)(?=\n)", text),
        "net_to_pay": extract_value(r"(?<=Net à payer :\s)(.*?)(?=\n)", text),
        "balance_due": extract_value(r"(?<=Solde dû :\s)(.*?)(?=\n)", text),
        "penalty_interest": extract_value(r"(?<=Escompte pour règlement anticipé :\s)(.*?)(?=\n)", text),
        "collection_fee": extract_value(r"(?<=Indemnité forfaitaire pour frais de recouvrement :\s)(.*?)(?=\n)", text),
        "iban": extract_value(r"(?<=IBAN :\s)(.*?)(?=\n)", text),
        "bic": extract_value(r"(?<=BIC :\s)(.*?)(?=\n)", text),
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
        st.write(info['items'])

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
