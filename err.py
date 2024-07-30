import streamlit as st
import fitz  # PyMuPDF
import re

# Fonction pour extraire les informations du PDF
def extract_info_from_pdf(file_path):
    document = fitz.open(file_path)
    page = document.load_page(0)  # Charger la première page
    text = page.get_text()

    # Extraction des informations à l'aide des expressions régulières
    info = {}

    # Client Information
    client_name = re.search(r"(?<=TDR LANDERNEAU\n).+?(?=\n)", text)
    client_address = re.search(r"36 rue Hervé de Guébriant, 29800 LANDERNEAU", text)
    client_email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    client_code = re.search(r"(?<=Code client\n).+?(?=\n)", text)

    # Salesperson Information
    salesperson_name = re.search(r"(?<=Commercial :\n).+?(?=\n)", text)

    # Invoice Details
    payment_method = re.search(r"(?<=Mode de règlement\n).+?(?=\n)", text)
    invoice_date = re.search(r"(?<=Date\n).+?(?=\n)", text)
    invoice_number = re.search(r"(?<=Numéro\n).+?(?=\n)", text)
    due_date = re.search(r"(?<=Date échéance\n).+?(?=\n)", text)

    # Company Information
    company_name = re.search(r"SAS GROUPE TDR", text)
    company_address = re.search(r"662 Rue des Jonchères\nActiparck de la Richassières - BAT F\n69730  GENAY", text)
    company_phone = re.search(r"(?<=Tél :\n).+?(?=\n)", text)
    company_website = re.search(r"terrederunning.com", text)

    # Items
    items = re.findall(r"FC \d{9}\d{5}", text)

    item_details = []
    for item in items:
        description = item
        quantity = re.search(r"(?<=1,00).+?(?=\n)", text)
        unit_price = re.search(r"(?<=\d{2,},\d{2}).+?(?=\n)", text)
        discount = re.search(r"20%", text)
        amount_ht = re.search(r"(?<=\d{2,},\d{2}).+?(?=\n)", text)
        item_details.append({
            "description": description,
            "quantity": quantity.group() if quantity else "",
            "unit_price": unit_price.group() if unit_price else "",
            "discount": discount.group() if discount else "",
            "amount_ht": amount_ht.group() if amount_ht else ""
        })

    # Totals
    total_ht = re.search(r"(?<=Total HT\n).+?(?=\n)", text)
    total_tva = re.search(r"(?<=Total TVA\n).+?(?=\n)", text)
    total_ttc = re.search(r"(?<=Total TTC\n).+?(?=\n)", text)
    advance_payment = re.search(r"(?<=Acomptes\n).+?(?=\n)", text)
    net_to_pay = re.search(r"(?<=Net à payer\n).+?(?=\n)", text)
    balance_due = re.search(r"(?<=Solde dû\n).+?(?=\n)", text)

    # Additional Information
    penalty_interest = re.search(r"(?<=Pénalités de retard :\n).+?(?=\n)", text)
    collection_fee = re.search(r"(?<=Indemnité forfaitaire pour frais de recouvrement :\n).+?(?=\n)", text)
    iban = re.search(r"(?<=IBAN :\n).+?(?=\n)", text)
    bic = re.search(r"(?<=BIC :\n).+?(?=\n)", text)

    info = {
        "client_name": client_name.group() if client_name else "",
        "client_address": client_address.group() if client_address else "",
        "client_email": client_email.group() if client_email else "",
        "client_code": client_code.group() if client_code else "",
        "salesperson_name": salesperson_name.group() if salesperson_name else "",
        "payment_method": payment_method.group() if payment_method else "",
        "invoice_date": invoice_date.group() if invoice_date else "",
        "invoice_number": invoice_number.group() if invoice_number else "",
        "due_date": due_date.group() if due_date else "",
        "company_name": company_name.group() if company_name else "",
        "company_address": company_address.group() if company_address else "",
        "company_phone": company_phone.group() if company_phone else "",
        "company_website": company_website.group() if company_website else "",
        "items": item_details,
        "total_ht": total_ht.group() if total_ht else "",
        "total_tva": total_tva.group() if total_tva else "",
        "total_ttc": total_ttc.group() if total_ttc else "",
        "advance_payment": advance_payment.group() if advance_payment else "",
        "net_to_pay": net_to_pay.group() if net_to_pay else "",
        "balance_due": balance_due.group() if balance_due else "",
        "penalty_interest": penalty_interest.group() if penalty_interest else "",
        "collection_fee": collection_fee.group() if collection_fee else "",
        "iban": iban.group() if iban else "",
        "bic": bic.group() if bic else ""
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
