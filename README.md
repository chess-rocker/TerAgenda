# TerAgenda

TerAgenda è un'applicazione web pensata per aiutare medici e pazienti a tenere sotto controllo le terapie farmacologiche. L'idea è semplice: il medico prescrive una terapia, l'app genera da sola il calendario delle dosi da assumere, e il paziente ha sempre sott'occhio cosa deve prendere oggi, con la possibilità di segnare ogni dose come presa o saltata.

Nasce per rispondere a un problema molto concreto in ambito sanitario: quante volte capita di dimenticare una compressa, o di non ricordare più se l'abbiamo già presa? TerAgenda vuole essere un piccolo aiuto proprio per questo.

Per testare la app, a seguito il link [Guida Utente](./GUIDA_UTENTE.md): spiega passo passo come avviarla e come usarla, sia dal lato medico che dal lato paziente.

---

## Cosa puoi fare con TerAgenda

- Registrarti e accedere come medico o come paziente
- (Da medico) creare una terapia per un paziente: l'app genera automaticamente tutte le assunzioni previste
- (Da paziente) vedere in una dashboard semplice le dosi da prendere oggi
- Aggiornare lo stato di ogni dose: **Da prendere**, **Presa**, **Saltata**
- Filtrare la dashboard per stato
- (Da medico) firmare digitalmente una terapia, per tenerne traccia in modo verificabile

---

## Com'è fatta l'app

Niente di complicato: un frontend semplice in HTML, CSS e JavaScript che parla con un backend scritto in Python (FastAPI), il quale a sua volta si appoggia a un database SQLite per salvare tutto.

- **Frontend**: pagine HTML con un po' di JavaScript, giusto per gestire login e dashboard
- **Backend**: un'API REST che espone le funzionalità (creare terapie, aggiornare assunzioni, ecc.)
- **Database**: SQLite, leggero e già pronto all'uso senza bisogno di configurazioni

---

## Struttura del progetto

```
TerAgenda/
│
├── app/                 # Backend FastAPI
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── utils/
│   └── main.py
│
├── frontend/            # Interfaccia utente
│   ├── login.html
│   ├── dashboard.html
│   ├── script.js
│   └── style.css
│
├── docs/                # Diagrammi (Casi d'uso, UML, ER)
├── GUIDA_UTENTE.md       # Guida passo-passo all'utilizzo
├── requirements.txt
└── README.md
```

---

## Come avviarla in due minuti

1. Clona il repository:

```bash
git clone https://github.com/chess-rocker/TerAgenda.git
cd TerAgenda
```

2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3. Avvia il backend:

```bash
uvicorn app.main:app --reload
```

4. Ora puoi accedere a:
- API: http://127.0.0.1:8000
- Documentazione interattiva delle API: http://127.0.0.1:8000/docs
- Frontend: apri `frontend/login.html` (meglio se servito da un piccolo server locale, vedi la [Guida Utente](./GUIDA_UTENTE.md) per i dettagli)

---

## Il database

Usiamo SQLite, quindi non serve installare o configurare nulla: il file del database viene creato automaticamente al primo avvio del backend, e non è incluso nel repository (per non portarsi dietro dati di test).

---

## Le API principali

| Metodo | Endpoint                | A cosa serve                              | Serve essere autenticati? |
| ------ | ------------------------ | ----------------------------------------- | ------------------------- |
| POST   | /register                | Creare un nuovo account                   | No                         |
| POST   | /login                   | Accedere e ottenere il token              | No                         |
| GET    | /users/me                | Vedere i propri dati                      | Sì                         |
| POST   | /terapie                 | Creare una terapia (genera le assunzioni) | Sì, solo medico            |
| GET    | /terapie                 | Vedere le terapie (filtro per paziente/medico) | Sì                    |
| GET    | /terapie/{id}            | Dettaglio di una terapia                  | Sì                         |
| PUT    | /terapie/{id}/firma      | Firmare digitalmente una terapia          | Sì, solo il medico che l'ha creata |
| GET    | /assunzioni              | Vedere le assunzioni                      | Sì                         |
| PUT    | /assunzioni/{id}         | Aggiornare lo stato di una dose           | Sì                         |
| POST   | /farmaci                 | Aggiungere un farmaco al catalogo         | Sì, solo medico            |
| PUT    | /farmaci/{id}            | Modificare un farmaco                     | Sì, solo medico            |
| DELETE | /farmaci/{id}            | Eliminare un farmaco                      | Sì, solo medico            |

Per le chiamate che richiedono autenticazione basta aggiungere l'header `Authorization: Bearer <token>`, con il token ottenuto facendo login su `/login`. Trovi esempi pratici, con i payload da copiare, nella [Guida Utente](./GUIDA_UTENTE.md).

---

## Come è stata testata

Il flusso è stato provato end-to-end più volte, verificando in particolare:

- Login e registrazione
- Creazione di una terapia e generazione automatica delle assunzioni
- Aggiornamento dello stato di una dose (presa/saltata)
- Filtri della dashboard
- Che le operazioni riservate al medico siano davvero bloccate per chi non lo è

---

## Documentazione e diagrammi

Nella cartella `docs/` trovi i diagrammi del progetto (Entità-Relazione, classi, casi d'uso). Per il funzionamento pratico dell'app, invece, fai riferimento alla [Guida Utente](./GUIDA_UTENTE.md).

---

## Un po' di sicurezza

Trattandosi di dati sanitari, è necessario non lasciare l'app completamente aperta:

- Il login rilascia un token (JWT) che dura 8 ore, da usare per tutte le operazioni successive
- Le password non vengono mai salvate in chiaro, ma come hash (bcrypt)
- Alcune operazioni delicate (creare terapie, gestire farmaci, firmare una terapia) sono riservate a chi ha il ruolo di medico
- La firma digitale delle terapie è una versione semplificata (basata su hash), pensata per dimostrare il concetto più che per avere valore legale reale

Restano alcuni margini di miglioramento, che terrò volentieri a mente per il futuro: un sistema di refresh del token, una firma digitale "vera" con crittografia asimmetrica, la cifratura dei dati nel database, e una configurazione più restrittiva del CORS (oggi aperto per comodità in fase di sviluppo).

Due scelte di design meritano una nota a parte:

- **Eliminazione delle terapie**: non è stata implementata volutamente. Trattandosi di dati sanitari, cancellare del tutto una terapia andrebbe in contraddizione con la tracciabilità che la firma digitale vuole garantire — nei sistemi sanitari reali, i record clinici tendono a non sparire mai fisicamente. Se in futuro servisse gestire il caso "il medico si è sbagliato", la strada più corretta sarebbe un soft-delete (un endpoint che segna la terapia come "annullata" invece di eliminarla davvero), non una `DELETE` vera e propria.
- **Chi può aggiornare lo stato di un'assunzione**: al momento questa operazione (`PUT /assunzioni/{id}`) è aperta a qualsiasi utente autenticato, medico incluso. Concettualmente avrebbe più senso riservarla al solo paziente a cui l'assunzione appartiene, dato che è lui l'unico a sapere davvero se ha preso o saltato una dose — lasciarla aperta anche al medico rende ambiguo il significato del dato registrato. Il motivo per cui ho deciso a questa operazione aperta per il momento è dovuto al fatto che in scenari reali (pazienti anziani, poco pratici di tecnologia, assistiti da un caregiver) potrebbe essere realistico che sia un infermiere o un familiare ad aggiornare lo stato per conto del paziente. È un affinamento del controllo degli accessi lasciato per una versione successiva.

---

## Cosa si potrebbe aggiungere in futuro

- Notifiche automatiche per ricordare le assunzioni;
- Una dashboard più completa lato medico;
- Una vera app mobile;
- Integrazione con sistemi sanitari già esistenti;
- Integrazione di maggiori RUOLI, come ad esempio ADMIN o INFERMIERA;

---

## In breve

TerAgenda è un piccolo prototipo che mostra come un'architettura moderna basata su API possa semplificare davvero la vita a chi segue una terapia — e a chi la prescrive. Per iniziare a usarla, il punto di partenza migliore è la [Guida Utente](./GUIDA_UTENTE.md).
