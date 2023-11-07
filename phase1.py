import argparse
from datetime import datetime
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
    parser = argparse.ArgumentParser("Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.")

    #ajout d'argument positionnel symbole
    parser.add_argument("symbole",
                        nargs = "+",
                        type = str,
                        help = "Nom d'un symbole boursier"
                        )
    
    #ajout de l'argument -d
    parser.add_argument("-d", "--debut",
                        type = str,
                        dest = "debut",
                        metavar= "DATE",
                        help = "Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
                        )
    
    #ajout de l'argument -f
    parser.add_argument("-f", "--fin",
                        dest = "fin",
                        type = str,
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





#fonction pour transformer la date en instance datetime.date
#(Par exemple: '2003-03-03' doit retourner sous la forme datetime.date(2003, 03, 03))
def date_forme_instance(uneDate):
    uneDate_en_datetime = datetime.strptime(uneDate, '%Y-%m-%d')
    uneDate_en_date = uneDate_en_datetime.date()
    return uneDate_en_date





#retourne en tuple la valeur d'une bourse de compagnie
def produire_historique(nomSymbole, daDebut, daFin, valDé):
    """
    Cherche les données de la bourse en allant dans le serveur de l'école récolter ces données.
    
    returns:
        Une liste de tuple avec les dates et les valeurs
        d'une bourse de compagnie et son historique.

    """

    #lien pour se connecter au serveur de l'école et récupérer les données
    url = f'https://pax.ulaval.ca/action/{nomSymbole}/historique/'
    params = {
    'début': daDebut,
    'fin': daFin,
    }
    reponse = requests.get(url = url, params = params)
    #On traite sesinformations pour pouvoir les manipuler pour la suite
    reponse = json.loads(reponse.text)

    #On se concentre sur le dictionnaire de l'historique de la variable réponse
    historDate = reponse.get("historique")
    listeRep = []
    for i in historDate:
        listeRep.append((i.key(), i[valDé]))
    
    #message à mettre dans le terminal lorsque qu'on enclenche la commande:
    messagePt1 = f'titre={nomSymbole}: valeur={valDé}, début={date_forme_instance(daDebut)}, fin={date_forme_instance(daFin)}


    

if __name__ == "__main__":
    args = analyser_commande()