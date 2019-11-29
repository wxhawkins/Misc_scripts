import requests
import re
import pandas as pd

# Declare globals
in_file = "./in_files/hhblits_ScAtg23.out"
out_file = "./out_files/out_file.xlsx"
url = "http://www.uniprot.org/uniprot/"

def extract_acc(line):
    """
        Extracts Uniprot accession ID from line containing bulk information on a given protein.

        Args:
            line (str)
    """

    acc = re.search(("tr\|(\w+)\|"), line).group(1)
    return acc

def get_tax(acc):
    """
        Searches Unitprot for given accession ID and returns the taxonomy as a list of
        individual toxonomic levels.

        Args:
            acc (str): Uniprot accession ID
    """

    payload =   {
                    "format": "txt",
                    "query": acc
                }   

    r = requests.get(url, params=payload)

    cont = r.text
    # Extract lines containing taxonomic information
    hits = re.finditer(("OC\s+(.*)"), cont)
    tax = []

    # Clean, split and concatonate taxonomic lines
    for hit in hits:
        str_ = hit.group(1).replace(" ", "").rstrip(";")
        tax += str_.split(";")

    return tax

def get_accs(file_):
    """
        Extracts accession IDs from HHblits raw output file.

        Args:
            file_ (str): path to HHblits raw output file
    """

    with open(file_, "r") as ori_file:
        master_file = ori_file.read()

    # Extract summary lines
    lines = re.finditer(("\d+\s+tr\|.*"), master_file)
    accs = []
    for line in lines:
        accs.append(extract_acc(str(line)))

    return accs

def show_results(results):
    """
        Display results in a clean format.

        Args:
            results (dict)
    """

    for acc, tax in results.items():
        cleaned = ", ".join(tax)[:-1]
        print(acc + ": " + cleaned)

def output_results(results):
    """
        Output results to Excel file

        Args:
            results (dict)
    """

    for acc, tax in results.items():
        # Colapse list into string
        results[acc] = ", ".join(tax)[:-1]
        
    ser = pd.Series(results, name="Taxonomy")
    ser.to_excel(out_file)

def main():
    accs = get_accs(in_file)
    results = {}
    for num, acc in enumerate(accs):
        tax = get_tax(acc)
        results[acc] = get_tax(acc)

        # Impose limit if desired
        if num > 100:
            break

    show_results(results)
    output_results(results)    

main()