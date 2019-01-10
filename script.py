#!/usr/bin/python
# -*-coding:Utf-8 -*

#############################
#		Script python		#
#		BENIT Romain		#
#		Version 1.3			#
#############################

# Import des modules
import csv, sys
from pylab import *
from matplotlib import pyplot
import operator

# Initialisation des variables
dico_dns_ns = {}
name_dns_ns = []
data_dns_ns = []

dico_geoip_country = {}
name_geoip_country = []
data_geoip_country = []

i = 0
cpt = 0

# Initialisation des fonctions
def dictionnaire(dico, colonne):
    if dico.has_key(colonne):
        dico[colonne] = int(dico.get(colonne))+1
    else :
        dico[colonne] = 1
    return dico

def trie(dico):
     del dico[""]
     dico_trie = sorted(dico.iteritems(), reverse=True, key=operator.itemgetter(1))
     return dico_trie

print "Script python realise par BENIT Romain"
# print ""
# print "Entrer vos choix :"
# print "1 : URL du site"
# print "2 : Nom de domaine"
#
# a = raw_input('Entrez une donnée : ')
#
# print a


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
			dictionnaire(dico_geoip_country, geoip_country)

	except csv.Error as e:
		sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

# Affichage des donnees extraites
print ""
print "*** DNS_NS ***"
for cle,valeur in trie(dico_dns_ns):
    	if i < 5:
    		name_dns_ns.append(cle)
    		data_dns_ns.append(valeur)
    	elif i >= 5:
    		cpt = int(valeur)+cpt
    	i = i+1
    	print cle,valeur
name_dns_ns.append("Autres")
data_dns_ns.append(cpt)
cpt=0
i=0

print ""
print "*** GEOIP_COUNTRY ***"

for cle,valeur in trie(dico_geoip_country):
	if i < 5:
		name_geoip_country.append(cle)
		data_geoip_country.append(valeur)
	elif i >= 5:
		cpt = int(valeur)+cpt
	i = i+1
	print cle,valeur
name_geoip_country.append("Autres")
data_geoip_country.append(cpt)

# Traitement des donnees pour le graphique

pyplot.figure(1)
pyplot.subplot(1, 3, 1)
plt.title("DNS NS")
plt.pie(data_dns_ns, labels=name_dns_ns, autopct='%1.1f%%',startangle=90, shadow=True)
plt.axis('equal')
pyplot.subplot(1, 3, 3)
plt.title("GEOIP COUNTRY")
plt.pie(data_geoip_country, labels=name_geoip_country, autopct='%1.1f%%',startangle=90, shadow=True)
plt.axis('equal')

plt.show()
