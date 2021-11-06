# Bot di telegram per avvisare della pubblicazione di una nuova circolare

### Premesse
Il token non è pubblicato per questioni di privacy.

### Installazione delle librerie
`pip install telepot`
`pip install selenium
`pip install python-dotenv`

### Modifica lirebrie

Sostituire la funzione `def _extract_message(update):` nel file `loop.py` con 

`def _extract_message(update):
    try:
        key = _find_first_key(update, ['message',
                                       'edited_message',
                                       'channel_post',
                                       'edited_channel_post',
                                       'callback_query',
                                       'inline_query',
                                       'chosen_inline_result',
                                       'shipping_query',
                                       'pre_checkout_query'])
        return key, update[key]
    except:
        key = _find_first_key(update, ['update_id',
                                       'message',
                                       'edited_message',
                                       'channel_post',
                                       'edited_channel_post',
                                       'callback_query',
                                       'inline_query',
                                       'chosen_inline_result',
                                       'shipping_query',
                                       'pre_checkout_query'])
        return key, update[key]
`




### Funzioni

`getUltimaCircolare()` Permette di ottenere un dizionario con l'ultima circolare nel formato
`{"number","link","nome"}`

`getCircolareWeb(n)` Permette di ottenere un dizionario dal numero della circolare nel formato
`{"number","link","nome"}`

`stampaCircolare(circ)` Ritorna una str con la circolare

`updateData()` Ritorna tutto il contenuto del file `data.json`

`updateJson(data)` Scrive nel file `data.json` tutto il contenuto del 
parametro `data`

`updateVariables()` Separa tutto il contenuto di `data.json` in tutte le
liste del programma

`createData()` Ritorna una serie di dati che corrispondono al file `data.json`
ma prendendo i valori dalle variabili del programma

`aggiornaListaCircolari()`Permette di aggiornare l a lista delle circolari salvate


`broadcast(message)` Permette di inviare a tutti un messaggio

`broadcastAdmin(message)` Permette di inviare a tutti gli admin un messaggio

`notify()` Invia a tutti se esce una nuova circolare


`removeId(ID)` Permette di rimuovere un id dalla lista degli id salvati in `data.json`

`saveId(ID)` Permette di salvare un id all'interno del file `data.json`

`removeAdmin(ID)` Permette di rimuovere un id dalla lista degli admin salvati in `data.json`

`saveAdmin(ID)` Permette di salvare un admin all'interno del file `data.json`



## Licenza
BotCircolari by Marco Leporati is licensed under <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
