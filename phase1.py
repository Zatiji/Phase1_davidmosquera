import argparse
from datetime import date
import json


def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """
    parser = argparse.ArgumentParser("Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")

    #ajout d'argument positionnel symbole
    parser.add_argument("symbole",
                        nargs = "+",
                        type = str,
                        help = "Nom d'un symbole boursier"
                        )
    
    #ajout de l'argument -d
    parser.add_argument("-d", "--debut",
                        dest = "debut",
                        metavar= "DATE",
                        help = "Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
                        )
    
    #ajout de l'argument -f
    parser.add_argument("-f", "--fin",
                        dest = "fin",
                        metavar = "DATE",
                        help = "Date recherchée la plus récente (format: AAAA-MM-JJ)"
                        )
    
    #Ajout de l'argument -v
    parser.add_argument("-v", "--valeur",
                        dest = "valeur",
                        choices=["fermeture","ouverture","min","max","volume"],
                        default = "fermeture",
                        help = "La valeur désirée (par défaut: fermeture)"
                       )
    

    return parser.parse_args()

if __name__ == "__main__":
    args = analyser_commande()