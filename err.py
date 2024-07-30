import streamlit as st
import fitz  # PyMuPDF

def extract_info_from_pdf(file_path):
    # Open the PDF file
    document = fitz.open(file_path)
    page = document.load_page(0)  # Load the first page
    text = page.get_text()

    # Extracting the information from the text
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
        "account_balance": "",
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
            info["total_ht"] = lines[i + 1].strip()
        elif "Total TVA" in line:
            info["total_tva"] = lines[i + 1].strip()
        elif "Total TTC" in line:
            info["total_ttc"] = lines[i + 1].strip()
        elif "Net à payer" in line:
            info["account_balance"] = lines[i + 1].strip()
        elif "IBAN" in line:
            info["iban"] = lines[i + 1].split(':')[-1].strip()
        elif "BIC" in line:
            info["bic"] = lines[i + 1].split(':')[-1].strip()
        elif "Description" in line:
            j = i + 1
            while j < len(lines) and "Total HT" not in lines[j]:
                parts = lines[j].split()
                if len(parts) > 3:
                    info["items"].append({
                        "description": ' '.join(parts[:-3]),
                        "quantity": parts[-3],
                        "unit_price": parts[-2],
                        "amount_ht": parts[-1]
                    })
                j += 1

    return info

def display_info(info):
    st.write("### Client Information")
    st.write(f"**Name:** {info['client_name']}")
    st.write(f"**Address:** {info['client_address']}")
    st.write(f"**Email:** {info['client_email']}")
    st.write(f"**Client Code:** {info['client_code']}")
    st.write(f"**Salesperson:** {info['salesperson_name']}")
    
    st.write("### Invoice Information")
    st.write(f"**Payment Method:** {info['payment_method']}")
    st.write(f"**Invoice Date:** {info['invoice_date']}")
    st.write(f"**Invoice Number:** {info['invoice_number']}")
    st.write(f"**Due Date:** {info['due_date']}")

    st.write("### Company Information")
    st.write(f"**Name:** {info['company_name']}")
    st.write(f"**Address:** {info['company_address']}")
    st.write(f"**Phone:** {info['company_phone']}")
    st.write(f"**Website:** {info['company_website']}")

    st.write("### Items")
    for item in info['items']:
        st.write(f"**Description:** {item['description']}")
        st.write(f"**Quantity:** {item['quantity']}")
        st.write(f"**Unit Price:** {item['unit_price']}")
        st.write(f"**Amount HT:** {item['amount_ht']}")

    st.write("### Totals")
    st.write(f"**Total HT:** {info['total_ht']}")
    st.write(f"**Total TVA:** {info['total_tva']}")
    st.write(f"**Total TTC:** {info['total_ttc']}")
    st.write(f"**Net to Pay:** {info['account_balance']}")

    st.write("### Bank Details")
    st.write(f"**IBAN:** {info['iban']}")
    st.write(f"**BIC:** {info['bic']}")

def main():
    st.title("PDF Invoice Information Extractor")

    uploaded_file = st.file_uploader("Upload PDF File", type="pdf")
    if uploaded_file is not None:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File uploaded successfully")

        info = extract_info_from_pdf("temp.pdf")
        display_info(info)

if __name__ == "__main__":
    main()
