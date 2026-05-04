# IMPORT LIBRERIE
from fastapi import FastAPI, Depends  # framework web
from sqlalchemy.orm import Session    # tipo per il database

# IMPORT INTERNI PROGETTO 
from app.db.database import engine, SessionLocal, Base    # connessione al database
from app.models.user import User    # modello database
from app.schemas.user import UserCreate, UserLogin     # schema input API
from app.models.terapia import Terapia  # modello database
from app.schemas.terapia import TerapiaCreate   # schema input API
from app.utils.security import hash_password, verify_password      # funzione hash password
from app.models.farmaco import Farmaco
from app.schemas.farmaco import FarmacoCreate, FarmacoResponse
from app.models.assunzione import Assunzione, StatoAssunzione
from app.schemas.assunzione import AssunzioneCreate, AssunzioneUpdate
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware



# creazione applicazione FastAPI
app = FastAPI(title="TerAgenda API")

#Aggiunta CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in sviluppo ok
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# crea automaticamente le tabelle nel database
Base.metadata.create_all(bind=engine)

# DIPENDENZA DATABASE
def get_db():
    db = SessionLocal()  # apre connessione DB
    try:
        yield db         # usa DB nelle API
    finally:
        db.close()       # chiude connessione

# endpoint base per test server
@app.get("/")
def root():
    return {"message": "TerAgenda attiva"}  # risposta JSON

# ENDPOINT REGISTER

@app.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    # crea nuovo utente
    new_user = User(
        nome=user_data.nome,
        email=user_data.email,
        password_hash=hash_password(user_data.password),  # sicurezza
        ruolo=user_data.ruolo
    )

    db.add(new_user)      # aggiunge al DB
    db.commit()           # salva definitivamente
    db.refresh(new_user)  # aggiorna oggetto con ID

    return {
        "message": "Utente registrato con successo",
        "id": new_user.id
    }

@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
     # cerca utente per email
    user = db.query(User).filter(User.email == user_data.email).first()

    # se non esiste
    if not user:
        return {"error": "Utente non trovato"}

    # verifica password
    if not verify_password(user_data.password, user.password_hash):
        return {"error": "Password errata"}

    return {
        "message": "Login effettuato con successo",
        "user_id": user.id,
        "ruolo": user.ruolo
    }

@app.post("/terapie")
def crea_terapia(data: TerapiaCreate, db: Session = Depends(get_db)):

    nuova_terapia = Terapia(
        paziente_id=data.paziente_id,
        medico_id=data.medico_id,
        data_inizio=data.data_inizio,
        data_fine=data.data_fine,
        frequenza_giornaliera=data.frequenza_giornaliera,
        note=data.note
    )

    db.add(nuova_terapia)
    db.commit()
    db.refresh(nuova_terapia)

    giorni = (data.data_fine - data.data_inizio).days

    for giorno in range(giorni + 1):
        for dose in range(data.frequenza_giornaliera):

            # crea data + orario
            base_date = data.data_inizio + timedelta(days=giorno)

            orario = datetime.combine(
                base_date,
                datetime.min.time()
            ) + timedelta(hours=(24 // data.frequenza_giornaliera) * dose)

            assunzione = Assunzione(
                terapia_id=nuova_terapia.id,
                orario=orario,
                dosaggio="1 compressa",
                stato="DA_PRENDERE"
            )

            db.add(assunzione)

    db.commit()

    return {
        "message": "Terapia creata con assunzioni automatiche",
        "id": nuova_terapia.id
    }

@app.post("/assunzioni")
def crea_assunzione(data: AssunzioneCreate, db: Session = Depends(get_db)):

    nuova = Assunzione(
        terapia_id=data.terapia_id,
        orario=data.orario,
        dosaggio=data.dosaggio
    )

    db.add(nuova)
    db.commit()
    db.refresh(nuova)

    return {
        "message": "Assunzione creata",
        "id": nuova.id
    }

@app.get("/assunzioni")
def get_assunzioni(stato: str = None, oggi: bool = False,  db: Session = Depends(get_db)):

    query = db.query(Assunzione)

    #filtro per stato
    if stato:
        query = query.filter(Assunzione.stato == stato)

    #filtro per oggi
    if oggi:
        start = datetime.now().date()
        end = start + timedelta(days=1)

        query = query.filter(
            Assunzione.orario >= start,
            Assunzione.orario < end
        )

    return query.all()

@app.get("/assunzioni/oggi/non-prese")
def get_assunzioni_oggi_non_prese(db: Session = Depends(get_db)):

    # 1️⃣ calcolo range giornata
    oggi = datetime.now().date()
    domani = oggi + timedelta(days=1)

    # 2️⃣ query filtrata
    assunzioni = db.query(Assunzione).filter(
        Assunzione.orario >= oggi,
        Assunzione.orario < domani,
        Assunzione.stato == StatoAssunzione.DA_PRENDERE
    ).all()

    return assunzioni

@app.put("/assunzioni/{assunzione_id}")
def aggiorna_assunzione(
    assunzione_id: int,
    data: AssunzioneUpdate,
    db: Session = Depends(get_db)
):

    assunzione = db.query(Assunzione).filter(
        Assunzione.id == assunzione_id
    ).first()

    if not assunzione:
        raise HTTPException(status_code=404, detail="Assunzione non trovata")

    assunzione.stato = data.stato

    db.commit()

    return {"message": "Stato aggiornato"}

@app.post("/farmaci")
def crea_farmaco(data: FarmacoCreate, db: Session = Depends(get_db)):

    nuovo = Farmaco(
        nome=data.nome,
        descrizione=data.descrizione
    )

    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)

    return {
        "message": "Farmaco creato",
        "id": nuovo.id
    }

@app.get("/farmaci")
def get_farmaci(db: Session = Depends(get_db)):
    return db.query(Farmaco).all()

@app.get("/farmaci/{farmaco_id}")
def get_farmaco(farmaco_id: int, db: Session = Depends(get_db)):

    farmaco = db.query(Farmaco).filter(Farmaco.id == farmaco_id).first()

    if not farmaco:
        return {"error": "Farmaco non trovato"}

    return farmaco

@app.put("/farmaci/{farmaco_id}")
def aggiorna_farmaco(farmaco_id: int, data: FarmacoCreate, db: Session = Depends(get_db)):

    farmaco = db.query(Farmaco).filter(Farmaco.id == farmaco_id).first()

    if not farmaco:
        return {"error": "Farmaco non trovato"}

    farmaco.nome = data.nome
    farmaco.descrizione = data.descrizione

    db.commit()
    db.refresh(farmaco)

    return {
        "message": "Farmaco aggiornato"
    }

@app.delete("/farmaci/{farmaco_id}")
def elimina_farmaco(farmaco_id: int, db: Session = Depends(get_db)):

    farmaco = db.query(Farmaco).filter(Farmaco.id == farmaco_id).first()

    if not farmaco:
        return {"error": "Farmaco non trovato"}

    db.delete(farmaco)
    db.commit()

    return {
        "message": "Farmaco eliminato"
    }