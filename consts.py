TOKEN = ''
with open('token','r') as tokenFile:
    TOKEN = tokenFile.readline()

ROLES_ETU = ["ASRFI","ASRAT"]
ROLES_PROF = ["Enseignant"]
ROLE_ADMIN = ["Admin"]
ANNEE = ["A1"]
ACTIVITY="LvkwbjjBwmwgwpfvbURQ:cheh"
LIEN_ENT = "https://ent.univ-lorraine.fr/"
LIEN_ARCHE = "https://arche.univ-lorraine.fr/my"
MP_DELAY = 10
ERROR_DELAY = 5

with open('webhookUrls','r') as webhookFile:
    EDT_WEBHOOK = webhookFile.readlines()
    EDT_WEBHOOK = list(map(lambda s:s.strip(),EDT_WEBHOOK))
EDT_REFRESH = 1800 #time to refresh in s
with open('urlEnt','r') as tokenFile:
    URL_ENT = tokenFile.readline()
