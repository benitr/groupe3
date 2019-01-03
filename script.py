#!/usr/bin/python
# -*-coding:Utf-8 -*

#########################
#	Script python	#
#	BENIT Romain	#
#	Version 1	#
#########################

# Import des modules
import csv, sys

# Initialisation des variables
dns_a_origin = "toto"
dns_ns_origin = "toto"
cpt_dns_a = 0
cpt_dns_ns = 0
dico = {}

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

            if fuzzer == "Original*":
                dns_a_origin = dns_a
                dns_ns_origin = dns_ns
            
            cpt_dns_a = cpt_dns_a + dns_a.count(dns_a_origin)
            cpt_dns_ns = cpt_dns_ns + dns_ns.count(dns_ns_origin)

	    dico[dns_ns] = cpt_dns_ns
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

print "Il y a ",cpt_dns_a," fois l'entre ",dns_a_origin," dans le fichier"
print "Il y a ",cpt_dns_ns," fois l'entre ",dns_ns_origin," dans le fichier"

print dico
