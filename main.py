import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
print("https://telepot.readthedocs.io/en/latest/")
import json
print("https://docs.python.org/3/library/json.html")
from time import sleep
from dotenv import load_dotenv
import os
import telepot
from telepot.loop import MessageLoop
import html
load_dotenv('.env')

############
#Costanti
PATH = ".\chromedriver.exe"
API_KEY = os.getenv('API_KEY')
ADMIN_KEY = os.getenv('ADMIN_KEY')
INTERVALLO_CONTROLLO = 60 #Valore in secondi
############

############
#Variabili
ultimaCircolareVista = 0 #Ulima circolare inviata
ultimaCircolare = 0
id = set() #set degli id salvatti
adminId = set() #id degli admin
adminCommands = {}
rispostepronte = {}
run = True
listaCircolari = []
ultimaCircolareSalvata = 0
############

def getUltimaCircolare():
    #https://www.iiscastelli.edu.it/Documents/circolari/CIRC%20107%202EM%20-%20CONVOCAZIONE%20CONSIGLIO%20DI%20CLASSE%20STRAORDINARIO.pdf
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.iiscastelli.edu.it/pager.aspx?page=circolari")
    assert "Circolari" in driver.title
    link = driver.find_element_by_partial_link_text('CIRC ').get_property('href')
    driver.close()
    nome = link[51:-4]
    return {"number":int(link[58:61]), "link": link,"nome":nome.replace("%20"," ")[9:]}



def getCircolareWeb(n):
    n = int(n)
    if n <= int(ultimaCircolare["number"]) and n > 0:
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.iiscastelli.edu.it/pager.aspx?page=circolari")
        assert "Circolari" in driver.title
        parolaRicerca = 'CIRC '
        if n < 10:
            parolaRicerca += "00"
        else:
            if n <100:
                parolaRicerca += "0"

        parolaRicerca += str(n)
        link = driver.find_element_by_partial_link_text(parolaRicerca).get_property('href')
        driver.close()
        nome = link[51:-4]
        return {"number": int(link[58:61]), "link": link, "nome": nome.replace("%20", " ")[9:]}
    else:
        return {"number": -1, "link": -1, "nome": ""}


def stampaCircolare(circ):
    risultato = f"CIRCOLARE N° {circ['number']} \n"
    risultato+= f"{circ['nome']}\n\nPremi il link per aprirla\n{circ['link']}"
    return risultato


def updateData():
    with open("data.json") as t:
        data = json.loads(t.read())
    t.close()
    return data


def updateJson(data):
    with open("data.json","w") as t:
        t.write(json.dumps(data))
    t.close()


def updateVariables():
    global ultimaCircolareVista
    global rispostepronte
    global adminId
    global adminCommands
    global listaCircolari
    global ultimaCircolareSalvata
    data = updateData()
    for i in data["id"]:
        id.add(i)
    ultimaCircolareVista = data["ultimaCircolareVista"]
    rispostepronte = data["rispostepronte"]
    for i in data["adminId"]:
        adminId.add(i)
    listaCircolari = data["circ"]
    adminCommands = data["admincommands"]
    ultimaCircolareSalvata = data["ultimaCircolareSalvata"]



def createData():
    global listaCircolari
    data = {
            "ultimaCircolareVista" : ultimaCircolareVista,
            "ultimaCircolareSalvata" : ultimaCircolareSalvata,
            "rispostepronte" : rispostepronte,
            "admincommands" :adminCommands,
            "adminId": list(adminId),
            "id": list(id),
            "circ": listaCircolari
            }
    return data



############
#Inizializzazione
updateVariables()
ultimaCircolare = getUltimaCircolare()

def aggiornaListaCircolari():
    global listaCircolari
    global ultimaCircolareSalvata
    for i in range(ultimaCircolareSalvata + 1, ultimaCircolare["number"] + 1):
        ultimaCircolareSalvata += 1
        listaCircolari.append(getCircolareWeb(i))
    updateJson(createData())

aggiornaListaCircolari()
###############

bot = telepot.Bot(API_KEY)
print(f"BOT: {bot.getMe()['first_name']} is running.")


def broadcast (message):
    message = str(message)
    print(f"Broadcasting:\n{message}")
    for i in id:
        try:
            bot.sendMessage(int(i), message)
        except:
            pass

def notify():
    global ultimaCircolareVista
    while ultimaCircolareVista < ultimaCircolare["number"]:
        ultimaCircolareVista += 1
        updateJson(createData())
        broadcast("è uscita una nuova circolare!\n------------------------------------\n"
                  .upper() + stampaCircolare(getCircolareWeb(ultimaCircolareVista))
                   + "\nSe non vuoi più ricevere notifiche digita /annullaiscrizione\n")
        return True
    return False


def removeId(ID):
    global id
    ID = int(ID)
    id.remove(ID)
    updateJson(createData())

def saveId(ID):
    global id
    if not(ID in id):
        id.add(int(ID))
        updateJson(createData())

def removeAdmin(ID):
    ID = int(ID)
    adminId.remove(ID)
    updateJson(createData())

def saveAdmin(ID):
    adminId.add(int(ID))
    updateJson(createData())

# print("INIZIO")
# for i in bot.getUpdates():
#     print(i)
# print("FINE")


def handle(msg):
    #print(msg)

    global run
    testo = msg['text']
    mittente = int(msg['from']['id'])

    print(f"Da: {mittente} Messaggio: {testo}")

    saveId(mittente)
    comando = ""

    #adminAdd
    if len(testo) >= 9:
        if testo[0:9].lower() == "/adminadd":
            comando = "saveadmin"
            if len(testo) > 9:
                if testo[9:] == ADMIN_KEY:
                    saveAdmin(mittente)
                    bot.sendMessage(mittente, "Aggiunto alla lista degli admin!\n")
                else:
                    bot.sendMessage(mittente, "Password errata\n")
            else:
                bot.sendMessage(mittente, "Riscrivi il comando con la sintassi /adminadd[Password]\n")

    #Cerca circolare per numero
    for i in range(1,ultimaCircolare["number"]+1):
        if "/"+str(i) == testo.lower():
            bot.sendMessage(mittente, stampaCircolare(listaCircolari[i-1]))
            comando = "num"
            break

    #Risposte automatiche
    if comando == "":
        for c,r in rispostepronte.items():
            if testo.lower() == c:
                bot.sendMessage(mittente,r)
                comando = c
                break

        # Parte admin
        admin = False
        for i in adminId:
            if i == mittente:
                admin = True
                break

        #Admin broadcast
        if testo[0:15].lower() == "/adminbroadcast":
            if admin:
                if len(testo)>=17:
                    broadcast(msg['text'][16:])
                    bot.sendMessage(mittente,adminCommands["/adminbroadcast [Messaggio]"])
                    comando = "broadcast"
                else:
                    bot.sendMessage(mittente, "Dopo il comando inserisci uno spazio e il tuo messaggio!")
                    comando = "null"
            else:
                bot.sendMessage(mittente, "Non sei un amministratore!\n")
                comando = "NOTADMIN"


        for c, r in adminCommands.items():
            if testo == c:
                if admin:
                    comando = c
                    bot.sendMessage(mittente,r)
                else:
                    bot.sendMessage(mittente, "Non sei un amministratore!\n")
                    comando = "NOTADMIN"
                break

    if comando != "":
        if comando == "/annullaiscrizione":
            removeId(mittente)
        else:
            if comando == "/ultima":
                bot.sendMessage(mittente,"Ecco l'ultima circolare\n------------------------------------\n" + stampaCircolare(ultimaCircolare))
            else:
                if comando == "/adminremove":
                    removeAdmin(mittente)
                else:
                    if comando == "/adminstop":
                        run = False
                    else:
                        if comando == "/adminrun":
                            run = True
    else:
        bot.sendMessage(mittente, 'Comando non supporato!\nDigita /help per la lista dei comandi\n')


MessageLoop(bot, handle).run_as_thread()


while run:
    if notify():
        aggiornaListaCircolari()
    sleep(INTERVALLO_CONTROLLO)
    ultimaCircolare = getUltimaCircolare()


