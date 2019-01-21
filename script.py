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
import os

# Initialisation des variables
dico_dns_ns = {}
name_dns_ns = []
data_dns_ns = []

dico_geoip_country = {}
name_geoip_country = []
data_geoip_country = []

i = 0
cpt = 0
avancement =0

output_file = open('output_file.txt','w')

# Liste des nom de domain de parking
# Source : https://www.securitee.org/files/parking-sensors_ndss2015.pdf
# parking_domain = ["sedoparking.com", "internettraffic.com", "cashparking.com", "fabulous.com", "dsredirection.com", "above.com", "parkingcrew.net", "ztomy.com", "fastpark.net", "voodoo.com", "rookdns.com", "bodis.com", "domainapps.com", "trafficz.com", "pql.net", "domaincontrol.com" ]
parking_domain = []
parking_domain_found = []

domain_dispo = []
domain_not_dispo = []

# Initialisation des fonctions
def dictionnaire(dico, colonne):
    if dico.has_key(colonne) :
        dico[colonne] = int(dico.get(colonne))+1
    else :
        dico[colonne] = 1
    return dico

def trie(dico):
     del dico[""]
     dico_trie = sorted(dico.iteritems(), reverse=True, key=operator.itemgetter(1))
     return dico_trie

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

def parking(park_list, dico):
    for parking in park_list:
        for dic in dico:
            if parking in dic:
                parking_domain_found.append(dic)

def godaddy(domain):
    commande = 'curl -s -X GET "https://api.ote-godaddy.com/v1/domains/available?domain='+domain+'&checkType=FAST&forTransfer=false" -H "accept: application/json" -H "Authorization: sso-key 3mM44UZC2ozGTC_VEsj87nyR35LSegMkrVMJe:VEstF2GMNwi84FD7uydj82"'
    p = os.popen(commande)
    line = p.readline()
    if 'available":false' in line:
        domain_not_dispo.append(domain)
    else:
        domain_dispo.append(domain)

print "Script python realise par le groupe 3"
print "BENIT Romain"
print "MALLET Maxime"
print "SAOULI Mohamed"
print "FERAFIAT Lionel"
print "###############"
print ""

# Gestion du nombre d'arguments
if len(sys.argv) < 2 :
    print "Erreur, il n'y a pas le bon nombre d'arguments"
    print "Utilisation : ./script.py 'FICHIER.CSV'"
    exit()

# Gestion des arguments

if "--input" in sys.argv:
    filename = sys.argv[sys.argv.index("--input")+1]

fichier = "ParkingDomains.txt"
if not os.path.isfile(filename):
    print "Erreur,'"+filename+"' n'est pas un fichier"
    exit()

if not os.path.splitext(filename)[1] == ".csv":
    print "Erreur, '"+filename+"' n'est pas un fichier CSV"
    exit()

if not os.path.isfile(fichier):
    print "Erreur, '"+fichier+"' n'est pas un fichier"
    exit()

if not os.path.splitext(fichier)[1] == ".txt":
    print "Erreur, '"+fichier+"' n'est pas un fichier TXT"
    exit()

#if "--godaddy" in sys.argv:
#    print sys.argv.index("--godaddy")+1
#    print "Bravo"

# Lecture du fichier contenant les domain
with open(fichier, "r") as fichier:
    fichier_entier = fichier.read()
    parking_domain = fichier_entier.split("\n")
    parking_domain.remove("")
    fichier.close()
# print parking_domain

# Lecture du fichier CSV
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

            # On enlève la 1ere ligne
			if not fuzzer == "fuzzer":
            	# Utilisation des disctionnaires pour les listes finales
				dictionnaire(dico_dns_ns, dns_ns)
				dictionnaire(dico_geoip_country, geoip_country)

            	# Remplissage des listes pour les domaines disponibles
				if "--godaddy" in sys.argv:
					godaddy(domain_name)

	except csv.Error as e:
		sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

# Affichage des donnees extraites
print ""
print "*** DNS_NS ***"
output_file.write("*** DNS_NS ***\n")
for cle,valeur in trie(dico_dns_ns):
    	if i < 5:
    		name_dns_ns.append(cle)
    		data_dns_ns.append(valeur)
    	elif i >= 5:
    		cpt = int(valeur)+cpt
    	i = i+1
    	print cle,valeur
        output_file.write(cle+":"+str(valeur)+"\n")
if cpt > 0:
    name_dns_ns.append("Autres")
    data_dns_ns.append(cpt)
cpt=0
i=0

print ""
print "*** GEOIP_COUNTRY ***"
output_file.write("\n*** GEOIP_COUNTRY ***\n")
for cle,valeur in trie(dico_geoip_country):
	if i < 5:
		name_geoip_country.append(cle)
		data_geoip_country.append(valeur)
	elif i >= 5:
		cpt = int(valeur)+cpt
	i = i+1
	print cle,valeur
	output_file.write(cle+":"+str(valeur)+"\n")
if cpt > 0:
    name_geoip_country.append("Autres")
    data_geoip_country.append(cpt)

# print dico_dns_ns
# print dico_geoip_country

# Gestion des domains parking
parking(parking_domain,dico_dns_ns)
print ""
print "*** Liste des domaines parking ***"
output_file.write("\n*** Liste des domaines parking ***\n")
for park in parking_domain_found:
    print park
    output_file.write(park+"\n")

# Affichage des domaines
if "--godaddy" in sys.argv:
	print ""
	print "*** Liste des domaines disponibles ***"
	print "Total : "+str(len(domain_dispo))
	output_file.write("\n*** Liste des domaines disponibles ***\n")
	output_file.write("Total : "+str(len(domain_dispo))+"\n")
	for dom_dispo in domain_dispo:
	    print dom_dispo
	    output_file.write(dom_dispo+"\n")

#print domain_dispo
#print len(domain_dispo)

	print ""
	print "*** Liste des domaines NON disponibles ***"
	print "Total : "+str(len(domain_not_dispo))
	output_file.write("\n*** Liste des domaines NON disponibles ***\n")
	output_file.write("Total : "+str(len(domain_not_dispo))+"\n")
	for dom_not_dispo in domain_not_dispo:
	    print dom_not_dispo
	    output_file.write(dom_not_dispo+"\n")


#print domain_not_dispo
#print len(domain_not_dispo)

# Fermeture du fichier TXT
output_file.close()

# Traitement des donnees pour le graphique
pyplot.figure(1)
pyplot.subplot(1, 3, 1)
plt.title("DNS NS")
plt.pie(data_dns_ns, labels=name_dns_ns, autopct=make_autopct(data_dns_ns), startangle=90, shadow=True)
plt.axis('equal')
pyplot.subplot(1, 3, 3)

plt.title("GEOIP COUNTRY")
plt.pie(data_geoip_country, labels=name_geoip_country, autopct=make_autopct(data_dns_ns),startangle=90, shadow=True)
plt.axis('equal')

plt.show()
