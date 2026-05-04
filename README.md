#  TerAgenda

TerAgenda è un’applicazione web full-stack per la gestione digitale delle terapie farmacologiche.
Consente di pianificare, monitorare e tracciare le assunzioni giornaliere dei pazienti in modo semplice ed efficace.

---

## Obiettivo

L’applicazione nasce per risolvere un problema reale nel settore sanitario:

> migliorare l’aderenza alle terapie farmacologiche e ridurre errori o dimenticanze da parte dei pazienti.

---

##  Funzionalità principali

* ✔ Registrazione e login utenti
* ✔ Creazione terapie da parte del medico
* ✔ Generazione automatica delle assunzioni
* ✔ Visualizzazione giornaliera delle dosi
* ✔ Aggiornamento stato:

  * DA_PRENDERE
  * PRESA
  * SALTATA
* ✔ Filtri dinamici nella dashboard
* ✔ Interfaccia semplice e intuitiva

---

## Architettura

L’applicazione segue un’architettura **full-stack basata su API REST**:

Frontend (HTML, CSS, JavaScript)
⬇
Backend (FastAPI - Python)
⬇
Database (SQLite)

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
├── docs/                # Diagrammi UML e ER
├── requirements.txt
└── README.md
```

---

## Come avviare il progetto

### 1- Clonare la repository

```bash
git clone https://github.com/tuo-username/TerAgenda.git
cd TerAgenda
```

---

### 2- Installare le dipendenze

```bash
pip install -r requirements.txt
```

---

### 3- Avviare il backend

```bash
uvicorn app.main:app --reload
```

---

### 4- Accedere all’app

* API: http://127.0.0.1:8000
* Documentazione API: http://127.0.0.1:8000/docs
* Frontend: aprire `frontend/login.html` (meglio tramite server locale)

---

## Database

Il database utilizzato è SQLite.

👉 Il file **viene creato automaticamente al primo avvio del backend**
👉 Non è incluso nella repository per motivi di portabilità

---

## 📡 API principali

| Metodo | Endpoint         | Descrizione           |
| ------ | ---------------- | --------------------- |
| POST   | /login           | Autenticazione utente |
| POST   | /terapie         | Creazione terapia     |
| GET    | /assunzioni      | Lista assunzioni      |
| PUT    | /assunzioni/{id} | Aggiornamento stato   |

---

## Testing

L’applicazione è stata testata tramite:

* ✔ Login utente
* ✔ Creazione terapia
* ✔ Generazione automatica assunzioni
* ✔ Aggiornamento stato (presa/saltata)
* ✔ Filtri frontend

(Screenshot disponibili nella documentazione)

---

## Documentazione

Nella cartella `docs/` sono presenti:

* Diagramma ER
* Diagramma UML
* Use Case

---

## Sicurezza

Versione base con autenticazione semplice.
Possibili miglioramenti futuri:

* JWT authentication
* Cifratura dati
* Gestione ruoli avanzata

---

## Sviluppi futuri

* Notifiche automatiche (reminder)
* Dashboard medica avanzata
* Applicazione mobile
* Integrazione con sistemi sanitari reali

---

## Conclusione

TerAgenda rappresenta un prototipo di sistema sanitario digitale basato su architettura REST, progettato per migliorare la gestione e il monitoraggio delle terapie farmacologiche.

---
