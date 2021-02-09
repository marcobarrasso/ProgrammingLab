
# Creo la classe ExamException che mi servirà per alzare delle eccezioni nel corso del programma.

class ExamException(Exception):
    pass

# Classe per fil csv.

class CSVTimeSeriesFile:

    def __init__(self, nome):

        # Setto il nome del file.

        self.nome = nome

    # Definisco un metodo che si chiama get_data che mi tornerà il contenuto dell variabile time_series ,
    # una lista di liste.

    def get_data(self):

        # Faccio un controllo sul nome del file , se non è una stinga o se è None (niente) alzo un'eccezione.

        if not isinstance(self.nome, str) or self.nome is None:
            raise ExamException("c'è stato un errore nel corso del programma")

        # Provo ad aprire il file , se non ci riesco  alzo un'eccezione.

        try:
            my_file = open(self.nome, 'r')
        except:
            raise ExamException("errore nell'apertura del file")

        # Inizializzo una lista vuota dove andrò a salvare i valori.

        time_series = []

        # Leggo il file linea per linea.

        for line in my_file:

            # Faccio lo split di ogni linea sulla virgola.

            elements = line.split(',')

        # Se non sto processando l'intestazione...

            if elements[0] != 'epoch':

                # Setto time stamp epoch e temperatura.

                epoch = elements[0]
                temp = elements[1]

                # La variabile epoch è ancora una stringa , poichè ho letto da un file di testo ,
                # quindi converto ad intero ed il programma procede senza interruzioni.

                try:
                    epoch = int(float(epoch))
                except:
                    continue

                try:
                    temp = float(temp)
                except:
                    continue

                # Infine aggiungo alla lista questi valori.

                time_series.append([epoch, temp])

        # Controllo che non ci siano timestamp fuori ordine o duplicati ,
        # quindi i timestamp devono essere in ordine crescente , se non è così alzo un'eccezione.

        for i in range(1, len(time_series)):
            if time_series[i][0] <= time_series[i - 1][0]:
                raise ExamException("errore : timestamp fuori ordine o duplicato")

        # Chiudo il file

        my_file.close()

        # Quando ho processato tutte le righe e fatto tutti i controlli necessari ,
        # ritorno time_series (ovvero la mia lista di liste).

        return time_series

# Definisco una funzione daily_stats che prende in input time_series che tramite un return mi ritorna un'altra lista
# di liste dove ogni lista annidata rappresenta la statistica giornaliera di un dato giorno,
# ovvero la tripletta di temperatura minima, massima e media.

def daily_stats(time_series):

    # Inizializzo tre liste vuote.

    # In questa lista andrò a salvare i valori delle temperture a seconda del giorno che sto analizzando.

    giorni = []

    # In questa lista salverò i valori delle temperature giorno per giorno sotto forma di liste ,
    # quindi alla prima linea avrò una lista che contiene tutte le temperature registrate al primo giorno ,
    # alla seconda linea tutte le temperature registrate il secondo giorno , e così via.

    values = []

    # In questa lista salverò i risultati finali , ovvero temperatura minima , massima e media giorno per giorno.

    risultati = []

    # operazione per trovare l'inizio del primo giorno in secondi.

    day_start_epoch = time_series[0][0] - (time_series[0][0] % 86400)

    # Parametro che tiene conto dei giorni.

    j = 1

    for i in range(len(time_series)):

        # Confronto il timestamp i esimo con il valore in secondi dell'inizio del giorno 1 sommato a  86400
        # (lunghezza di un giorno in secondi) , il quale viene moltiplicato per il parametro j.

        if time_series[i][0] < day_start_epoch + (86400 * j):

            # Se la proposizione sopra è verificata significa che stiamo analizzando un timestamp appartenente al
            # al giorno j , quindi prendiamo la rispettiva tempertura e la inseriamo nella lista [giorni].

            giorni.append(time_series[i][1])

            # Se non è verificata la proposizione a riga 122 significa che stiamo analizzando
            # un timestamp che appartiene al giorno successivo.

        else:

            # Salviamo i dati del giorno che stiamo analizzando nella lista append.

            values.append(giorni)

            # La lista diventa vuota perchè ora dovrò analizzare il giorno successivo a j.

            giorni = []

            # La rispettiva temperatura del timestamp analizzato sopra , che appartiene al giorno successivo
            # rispetto a j , viene inserita nella lista giorni.

            giorni.append(time_series[i][1])

            # Incremento j di uno.

            j += 1

            # Analizzo ogni linea di values , che contiene i valori delle temperature registrate giorno dopo giorno ,
            # e costruisco la tripletta temperatura minima , massima e media per ogni giorno.

    for line in values:
        risultati.append([min(line), max(line), sum(line) / len(line)])

    # Ritorno la lista con i risultati finali.

    return risultati


