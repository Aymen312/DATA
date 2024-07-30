import streamlit as st
import fitz  # PyMuPDF
import re

# Fonction pour extraire les informations du PDF
def extract_info_from_pdf(file_path):
    document = fitz.open(file_path)
    page = document.load_page(0)  # Charger la première page
    text = page.get_text()

    info = {
        "client_name": "",
        "client_address": "",
        "client_email": "",
        "client_code": "",
        "salesperson_name": "",
        "payment_method": "",
        "invoice_date": "",
        "invoice_number": "",
        "due_date": "",
        "company_name": "",
        "company_address": "",
        "company_phone": "",
        "company_website": "",
        "items": [],
        "total_ht": "",
        "total_tva": "",
        "total_ttc": "",
        "advance_payment": "",
        "account_balance": "",
        "penalty_interest": "",
        "collection_fee": "",
        "iban": "",
        "bic": ""
    }

    lines = text.split('\n')

    for i, line in enumerate(lines):
        if "TDR LANDERNEAU" in line:
            info["client_name"] = "TDR LANDERNEAU"
            info["client_address"] = lines[i + 1].strip()
            info["client_email"] = lines[i + 2].strip()
        elif "Commercial :" in line:
            info["salesperson_name"] = line.split(':')[1].strip()
        elif "Mode de règlement" in line:
            info["payment_method"] = lines[i + 1].strip()
        elif "Code client" in line:
            info["client_code"] = lines[i + 1].strip()
        elif "Date" in line and "29/07/2024" in line:
            info["invoice_date"] = line.split()[-1].strip()
        elif "Numéro" in line and "02-F2405442" in line:
            info["invoice_number"] = line.split()[-1].strip()
        elif "Date échéance" in line:
            info["due_date"] = lines[i + 1].strip()
        elif "SAS GROUPE TDR" in line:
            info["company_name"] = "SAS GROUPE TDR"
            info["company_address"] = "662 Rue des Jonchères, Actiparck de la Richassières - BAT F, 69730 GENAY"
            info["company_phone"] = "04 74 70 72 04"
            info["company_website"] = "terrederunning.com"
        elif "Total HT" in line:
            info["total_ht"] = re.search(r"Total HT\s+(\d+,\d+ €)", text).group(1)
        elif "Total TVA" in line:
            info["total_tva"] = re.search(r"Total TVA \(20%\)\s+(\d+,\d+ €)", text).group(1)
        elif "Total TTC" in line:
            info["total_ttc"] = re.search(r"Total TTC\s+(\d+,\d+ €)", text).group(1)
        elif "Acomptes" in line:
            info["advance_payment"] = re.search(r"Acomptes\s+(\d+,\d+ €)", text).group(1)
        elif "Net à payer" in line:
            info["account_balance"] = re.search(r"Net à payer\s+(\d+,\d+ €)", text).group(1)
        elif "Solde dû" in line:
            info["account_balance"] = re.search(r"Solde dû\s+(\d+,\d+ €)", text).group(1)
        elif "IBAN" in line:
            info["iban"] = re.search(r"IBAN\s+([A-Z0-9]+)", text).group(1)
        elif "BIC" in line:
            info["bic"] = re.search(r"BIC\s+([A-Z0-9]+)", text).group(1)
        elif "Description" in line:
            j = i + 1
            while j < len(lines) and "Total HT" not in lines[j]:
                parts = lines[j].split()
                if len(parts) > 3:
                    info["items"].append({
                        "description": ' '.join(parts[:-4]),
                        "quantity": parts[-4],
                        "unit_price": parts[-3],
                        "discount": parts[-2],
                        "amount_ht": parts[-1]
                    })
                j += 1

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
        st.write(f"**Net à payer :** {info['account_balance']}")
        st.write(f"**Solde dû :** {info['account_balance']}")

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
