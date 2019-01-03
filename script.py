#!/usr/bin/python
# -*-coding:Utf-8 -*

#########################
#	Script python	#
#	BENIT Romain	#
#	Version 1.2	#
#########################

# Import des modules
import csv, sys
from pylab import *
import operator

# Initialisation des variables
dico_dns_ns = {}

# Initialisation des fonctions
def dictionnaire(dico, colonne):
    if dico.has_key(colonne):
        dico[colonne] = int(dico.get(colonne))+1
    else :
        dico[colonne] = 1
    return dico

def trie(dico):
     dico_trie = sorted(dico.iteritems(), reverse=True, key=operator.itemgetter(1))
     return dico_trie
 
print "Script python realise par BENIT Romain"

filename = 'fichiertest.csv'

with open(filename) as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            fuzzer = row[0]
            domain_name = row[1]
            dns_a = row[2]
            dns_aaaa = row[3]
            dns_mx = row[4]
            dns_ns = row[5]
            geoip_country = row[6]
            ssdeep_score = row[7]

            # Utilisation des disctionnaires pour les listes finales
	    dictionnaire(dico_dns_ns, dns_ns)
    
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

# Affichage des donnees extraites
for cle,valeur in trie(dico_dns_ns):
     print cle,valeur

# Traitement des donnees pour le graphique

#name = ['-18', '18-25', '25-50', '50+']
#data = [5000, 26000, 21400, 12000]

#explode=(0, 0.15, 0, 0)
#plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
#plt.axis('equal')
#plt.show()
