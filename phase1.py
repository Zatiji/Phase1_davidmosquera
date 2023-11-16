import argparse
import datetime
import json
import requests


def analyser_commande():
    """
    Générer un interpréteur de commande.

    Returns:
        Un objet Namespace tel que retourné par parser.parse_args().
        Cet objet aura l'attribut «symboles» représentant la liste des
        symboles à traiter, et les attributs «début», «fin» et «valeur»
        associés aux arguments optionnels de la ligne de commande.
    """

    parser = argparse.ArgumentParser(description="Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")

    #ajout d'argument positionnel symbole
    parser.add_argument("symboles",
                        nargs = "+",
                        type = str,
                        help = "Nom d'un symbole boursier"
                        )
    
    #ajout de l'argument -d
    parser.add_argument("-d", "--debut",
                        type = datetime.date.fromisoformat,
                        dest = "debut",
                        metavar= "DATE",
                        help = "Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
                        )
    
    #ajout de l'argument -f
    parser.add_argument("-f", "--fin",
                        dest = "fin",
                        default = datetime.date.today(),
                        type = datetime.date.fromisoformat,
                        metavar = "DATE",
                        help = "Date recherchée la plus récente (format: AAAA-MM-JJ)"
                        )
    
    #Ajout de l'argument -v
    parser.add_argument("-v", "--valeur",
                        dest = "valeur",
                        type = str,
                        choices=["fermeture","ouverture","min","max","volume"],
                        default = "fermeture",
                        help = "La valeur désirée (par défaut: fermeture)"
                       )
    
    return parser.parse_args()

def produire_historique(nomSymbole, daDebut, daFin, valName):
    """
    Cherche les données de la bourse en allant dans le serveur de l'école récolter ces données.
    
    returns:
        Une liste de tuple avec les dates et les valeurs
        d'une bourse de compagnie et son historique.

    """
    #on met en dadébut en défault s'il n'est pas nommé:
    if daDebut == None:
        daDebut = daFin

    #On met une boucle car nomSymbole commence comme une liste de string
    for i in nomSymbole:
        #lien pour se connecter au serveur de l'école et récupérer les données
        url = f'https://pax.ulaval.ca/action/{i}/historique/'
        params = {
        'début': daDebut,
        'fin': daFin,
        }
        reponse = requests.get(url = url, params = params)
        reponse = json.loads(reponse.text)

        #On se concentre sur le dictionnaire de l'historique de la variable réponse
        historDate = reponse.get("historique")

        #On crée la liste de tuple et rajoute les tuples dans la liste
        listeRep = []
        for j in historDate:
            #le dictionnaire affecté au dates (j) ayant les valeurs des éléments.
            dernier_dico = historDate.get(j)

            #On transforme la clé (string) en format datetime.date()
            iso_date = datetime.date.fromisoformat(j)

            #on ajoute le tuple dans la liste.
            listeRep.append((iso_date, dernier_dico.get(valName)))

        #message à mettre dans le terminal lorsque qu'on enclenche la commande:
        print(f"titre={i}: valeur={valName}, début={datetime.date.fromisoformat(daDebut)}, fin={datetime.date.fromisoformat(daFin)}")
        print(listeRep)

#condition de start
if __name__ == "__main__":
    args = analyser_commande()
    produire_historique(args.symboles, args.debut, args.fin, args.valeur)
