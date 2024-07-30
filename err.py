import fitz  # PyMuPDF
import pandas as pd
import pytesseract
from pytesseract import Output

# Configure pytesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'path_to_your_tesseract_executable'

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

def extract_tables_from_text(text):
    lines = text.split("\n")
    first_table_data = []
    small_table_data = []
    in_first_table = False
    in_small_table = False

    for line in lines:
        if "Date" in line and "Numéro" in line:
            in_first_table = True
            in_small_table = False
        elif "Solde dû" in line:
            in_first_table = False
            in_small_table = True

        if in_first_table:
            first_table_data.append(line)
        if in_small_table:
            small_table_data.append(line)

    return first_table_data, small_table_data

def parse_first_table(table_data):
    columns = ["Date", "Numéro", "Date d'échéance", "Mode de règlement", "Code client", "N° de TVA intracom"]
    data = []

    for line in table_data:
        if any(col in line for col in columns):
            continue
        if len(line.split()) > 5:
            data.append(line.split())

    df = pd.DataFrame(data, columns=columns)
    return df

def parse_small_table(table_data):
    for line in table_data:
        if "€" in line:
            solde_du = line.split()[-1]
            return solde_du

def main(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    first_table_data, small_table_data = extract_tables_from_text(text)
    first_table_df = parse_first_table(first_table_data)
    solde_du = parse_small_table(small_table_data)

    print("Premier Tableau :")
    print(first_table_df)
    print("\nPetit Tableau :")
    print(f"Solde dû : {solde_du}")

if __name__ == "__main__":
    pdf_path = "path_to_your_pdf_file.pdf"
    main(pdf_path)
