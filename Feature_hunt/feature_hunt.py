import requests
import re

class Atg:
    """
        Stores information about a single Atg gene/protein

        Atributes:
            name (str): gene/protein name
            accs (list): All corresponding Uniprot accession identifiers
            features (set): All unique features identified on Uniprot for the given protein
    """

    def __init__(self, name_):
        self.name = name_
        self.accs = self.get_accs(self.name)
        self.features = self.get_features()

    def __str__(self):
        string_ = (
                    "\nname: " + self.name + 
                    "\naccessions: " + str(self.accs) +
                    "\nfeatures: " + str(self.features)
                 )
        return string_

    def get_accs(self, gene_name):
        """
            Perform Uniprot search for given gene name in budding yeast and store accession numbers of hits.
        """

        url = "http://www.uniprot.org/uniprot/"
        payload =   {
                        "format": "list",
                        "query": ("organism:Saccharomyces cerevisiae AND gene:" + gene_name)
                    }   

        r = requests.get(url, params=payload)
        hit_num = int(r.headers["X-Total-Results"])

        # Return empty list if no hits found
        if hit_num == 0:
            return []

        return r.text.strip().split()

    def get_features(self):
        """
            Get all unique features annotated on Uniprot for the identified accession numbers
        """

        # Do i need the last stuff? FLAG
        url = "https://www.ebi.ac.uk/proteins/api/features"

        # Consider starting with list and compressing into set at the end for efficiency
        fets = set()

        for acc in self.accs:
            payload = {"accession": acc, "format": "txt"}
            r = requests.get(url, params=payload)
            cont = str(r.content.strip())

            # Extract features from content returned from request
            for fet in re.finditer(("\"type\":\"(\w+)\""), cont):
                fets.add(fet.group(1))

        # Return empty set if no features found
        if len(fets) == 0:
            return set()

        return fets

def main():
    atgs = []

    # Perform search for all autophagy-related (ATG) proteins
    for i in range(1, 50):
        gene_name = "atg" + str(i)
        atgs.append(Atg(gene_name))
        print(atgs[-1])
    
main()