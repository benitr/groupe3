#!/usr/bin/python
# -*-coding:Utf-8 -*

#############################
#		Script python		#
#		BENIT Romain		#
#		Version 1			#
#############################

# Import des modules
import os, sys

# Gestion du nombre d'arguments
domain = sys.argv[1]
if len(sys.argv) < 2 :
    print "Erreur, il n'y a pas le bon nombre d'arguments"
    print "Utilisation : ./godaddy.py 'DOMAIN'"
    exit()

if not os.path.splitext(domain)[1] == ".com":
    print "Erreur, '"+domain+"' n'est pas un nom de domain acceptable"
    exit()

commande = 'curl -s -X GET "https://api.ote-godaddy.com/v1/domains/available?domain='+domain+'&checkType=FAST&forTransfer=false" -H "accept: application/json" -H "Authorization: sso-key 3mM44UZC2ozGTC_VEsj87nyR35LSegMkrVMJe:VEstF2GMNwi84FD7uydj82"'
# commande = 'ls'

p = os.popen(commande)
while 1:
    line = p.readline()
    if not line: break
    # print line
    if 'available":false' in line:
        print "Ce nom de domaine n'est PAS disponible"
    else:
        print "Ce nom de domaine est disponible à l'achat"
