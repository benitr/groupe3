#!/usr/bin/python
# -*-coding:Utf-8 -*

#########################
#	Script python	#
#	BENIT Romain	#
#	Version 1.1	#
#########################

# Import des modules
import csv, sys

# Initialisation des variables
dico_dns_ns = {}

# Initialisation des fonctions
def dictionnaire(dico, colonne):
    if dico.has_key(colonne):
        dico[colonne] = int(dico.get(colonne))+1
    else :
        dico[colonne] = 1
    return dico

# Debut du script
 
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

print dictionnaire(dico_dns_ns, dns_ns)
