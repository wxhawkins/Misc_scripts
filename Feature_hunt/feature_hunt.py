import argparse
import re

import requests

# Establish argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gene", action="store", type=str, dest="gene_term", required=True, help="Gene term to search for.")
parser.add_argument("-f", "--feature", action="store", type=str, dest="feature_term", default=None, help="Feature term to search for.")

args = parser.parse_args()


class Protein:
    """
        Stores information about a single gene/protein

        Atributes:
            name (str): gene/protein name
            accs (list): All corresponding Uniprot accession identifiers
            features (set): All unique features identified on Uniprot for the given protein
    """


    def __init__(self, name_):
        self.name = name_
        self.accs = self.get_accs()
        self.features = self.get_features()


    def __str__(self):
        string_ = (
                    "\nName: " + self.name + 
                    "\nAccessions: " + str(self.accs) +
                    "\nFeatures: " + str(self.features)
                 )
        return string_


    def get_accs(self):
        """
            Perform Uniprot search for given gene name in budding yeast and store accession numbers of hits.
        """

        url = "http://www.uniprot.org/uniprot/"
        payload =   {
                        "format": "list",
                        "query": ("organism:Saccharomyces cerevisiae AND gene:" + self.name)
                    }   

        r = requests.get(url, params=payload)
        hit_num = int(r.headers["X-Total-Results"])
        print(r.text)

        # Return empty list if no hits found
        if hit_num == 0:
            return []

        return r.text.strip().split()


    def get_features(self):
        """
            Get all unique features annotated on Uniprot for the identified accession numbers
        """

        url = "https://www.ebi.ac.uk/proteins/api/features"

        # Convert to set to remove redundant entries
        fets = set()

        for acc in self.accs:
            payload = {"accession": acc, "format": "txt"}
            r = requests.get(url, params=payload)
            cont = str(r.content.strip())

            # Extract features from content returned from request
            for fet in re.finditer((r"\"type\":\"(\w+)\""), cont):
                fets.add(fet.group(1))

        # Return empty set if no features found
        if len(fets) == 0:
            return set()

        return fets


def main():
    proteins = []

    # Perform search using provided gene search term
    for i in range(1, 50):
        gene_name = args.gene_term + str(i)
        proteins.append(Protein(gene_name))
        print(proteins[-1])
    
    hit_count = 0
    print("Feature hits".center(100, "-"))
    for atg in proteins:
        if args.feature_term in atg.features:
            cc_chit_countount += 1
            print(atg.name)

    trash = [prot for prot in proteins if len(prot.accs) > 0]
    print("num proteins =", len(trash))
    print("hit count =", hit_count)


if __name__ == "__main__":
    main()