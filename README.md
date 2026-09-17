#  TerAgenda

TerAgenda è un’applicazione web full-stack per la gestione digitale delle terapie farmacologiche.
Consente di pianificare, monitorare e tracciare le assunzioni giornaliere dei pazienti in modo semplice ed efficace.

---

## Obiettivo

L’applicazione nasce per risolvere un problema reale nel settore sanitario:

> migliorare l’aderenza alle terapie farmacologiche e ridurre errori o dimenticanze da parte dei pazienti.

---

##  Funzionalità principali

- Registrazione e login utenti
- Creazione terapie da parte del medico
- Generazione automatica delle assunzioni
- Visualizzazione giornaliera delle dosi
-  Aggiornamento stato:

  - DA_PRENDERE
  - PRESA
  - SALTATA
- Filtri dinamici nella dashboard
- Interfaccia semplice e intuitiva

---

## Architettura

L’applicazione segue un’architettura **full-stack basata su API REST**:

- Frontend (HTML, CSS, JavaScript)
- Backend (FastAPI - Python)
- Database (SQLite)

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
├── docs/                # Diagrammi Caso d'Uso, UML, ER
├── requirements.txt
└── README.md
```

---

## Come avviare il progetto

1- Clonare la repository

```bash
git clone https://github.com/tuo-username/TerAgenda.git
cd TerAgenda
```

---

2- Installare le dipendenze

```bash
pip install -r requirements.txt
```

---

3- Avviare il backend

```bash
uvicorn app.main:app --reload
```

---

4- Accedere all’app
- API: http://127.0.0.1:8000
- Documentazione API: http://127.0.0.1:8000/docs
- Frontend: aprire `frontend/login.html` (meglio tramite server locale)

---

## Database

Il database utilizzato è SQLite.

- Il file **viene creato automaticamente al primo avvio del backend**
- Non è incluso nella repository per motivi di portabilità

---

## API principali

| Metodo | Endpoint                | Descrizione                              | Autenticazione richiesta |
| ------ | ------------------------ | ----------------------------------------- | ------------------------- |
| POST   | /register                | Registrazione nuovo utente                | -                          |
| POST   | /login                   | Autenticazione utente, restituisce token  | -                          |
| GET    | /users/me                | Dati dell'utente autenticato              | Sì (qualsiasi ruolo)       |
| POST   | /terapie                 | Creazione terapia + assunzioni automatiche| Sì (solo `medico`)         |
| GET    | /terapie                 | Lista terapie (filtro per paziente/medico)| Sì (qualsiasi ruolo)       |
| GET    | /terapie/{id}            | Dettaglio singola terapia                 | Sì (qualsiasi ruolo)       |
| PUT    | /terapie/{id}/firma      | Firma digitale della terapia              | Sì (solo `medico` autore)  |
| GET    | /assunzioni              | Lista assunzioni                          | Sì (qualsiasi ruolo)       |
| PUT    | /assunzioni/{id}         | Aggiornamento stato (presa/saltata)       | Sì (qualsiasi ruolo)       |
| POST   | /farmaci                 | Creazione farmaco                         | Sì (solo `medico`)         |
| PUT    | /farmaci/{id}            | Modifica farmaco                          | Sì (solo `medico`)         |
| DELETE | /farmaci/{id}            | Eliminazione farmaco                      | Sì (solo `medico`)         |

Le richieste autenticate vanno effettuate inviando l'header `Authorization: Bearer <token>`, con il token ottenuto da `/login`.

---

## Testing

L’applicazione è stata testata tramite:

- Login utente
- Creazione terapia
- Generazione automatica assunzioni
- Aggiornamento stato (presa/saltata)
- Filtri frontend

---

## Documentazione

Nella cartella `docs/` sono presenti:

- Diagramma ER
- Diagramma UML
- Use Case

---

## Sicurezza

- **Autenticazione basata su token JWT**: al login viene rilasciato un `access_token` (validità 8 ore) da inviare come `Authorization: Bearer <token>` in tutte le chiamate protette.
- **Password**: salvate come hash bcrypt (mai in chiaro), tramite `passlib`.
- **Gestione ruoli**: gli endpoint di scrittura più sensibili (creazione terapie, gestione farmaci, firma) sono riservati al ruolo `medico`; un medico non può inoltre creare terapie a nome di un altro medico.
- **Firma digitale delle terapie**: implementata in forma semplificata (hash SHA-256 calcolato sui dati chiave della terapia), riservata al medico che l'ha creata. Non è una firma crittografica a chiave pubblica, ma rende l'operazione tracciabile.
- Possibili miglioramenti futuri:
  - Refresh token e logout lato server (revoca token)
  - Firma digitale con crittografia asimmetrica reale
  - Cifratura dei dati sanitari a riposo
  - CORS ristretto ai soli domini autorizzati (attualmente aperto per semplicità di sviluppo)

---

## Sviluppi futuri

- Notifiche automatiche (reminder)
- Dashboard medica avanzata
- Applicazione mobile
- Integrazione con sistemi sanitari reali

---

## Conclusione

TerAgenda rappresenta un prototipo di sistema sanitario digitale basato su architettura REST, progettato per migliorare la gestione e il monitoraggio delle terapie farmacologiche.
