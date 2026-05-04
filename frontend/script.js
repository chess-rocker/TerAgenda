const BASE_URL = "http://127.0.0.1:8000";

/* ===================== STATE ===================== */
let tutteAssunzioni = [];
let filtroAttivo = "TUTTE";

/* ===================== LOGIN ===================== */
function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const msg = document.getElementById("msg");
    const btn = document.getElementById("loginBtn");

    msg.innerText = "";
    btn.disabled = true;
    btn.innerText = "Accesso...";

    fetch(BASE_URL + "/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {

        if (data.user_id) {

            msg.style.color = "green";
            msg.innerText = "Login riuscito!";

            setTimeout(() => {
                localStorage.setItem("user", JSON.stringify(data));
                window.location.href = "dashboard.html";
            }, 800);

        } else {

            msg.style.color = "red";
            msg.innerText = "Credenziali errate";

            btn.disabled = false;
            btn.innerText = "Accedi";
        }
    })
    .catch(() => {

        msg.style.color = "red";
        msg.innerText = "Errore server";

        btn.disabled = false;
        btn.innerText = "Accedi";
    });
}

/* ===================== LOAD ASSUNZIONI ===================== */
function loadAssunzioni() {

    fetch(BASE_URL + "/assunzioni?oggi=true")
    .then(res => res.json())
    .then(data => {

        tutteAssunzioni = data;
        renderAssunzioni();
    });
}

/* ===================== RENDER CON FILTRO ===================== */
function renderAssunzioni() {

    const container = document.getElementById("container");
    container.innerHTML = "";

    let lista = tutteAssunzioni;

    if (filtroAttivo !== "TUTTE") {
        lista = tutteAssunzioni.filter(a => a.stato === filtroAttivo);
    }

    lista.forEach(a => {

        const card = document.createElement("div");
        card.className = "card";

        let color = "gray";
        if (a.stato === "PRESA") color = "green";
        if (a.stato === "SALTATA") color = "red";

        card.innerHTML = `
            <h3>Assunzione #${a.id}</h3>
            <p>Stato: <span style="color:${color}; font-weight:bold">${a.stato}</span></p>
            <p>Orario: ${a.orario}</p>

            <button onclick="update(${a.id}, 'PRESA')">✔ Presa</button>
            <button onclick="update(${a.id}, 'SALTATA')">✖ Saltata</button>
        `;

        container.appendChild(card);
    });
}

/* ===================== FILTRO ===================== */
function setFiltro(nuovoFiltro) {
    filtroAttivo = nuovoFiltro;
    renderAssunzioni();
}

/* ===================== UPDATE STATO ===================== */
function update(id, stato) {

    fetch(BASE_URL + "/assunzioni/" + id, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ stato })
    })
    .then(() => loadAssunzioni());
}

/* ===================== AUTO LOAD ===================== */
document.addEventListener("DOMContentLoaded", () => {

    if (document.getElementById("container")) {
        loadAssunzioni();
    }
});

/* ===================== LOGOUT ===================== */
function logout() {
    localStorage.removeItem("user");
    window.location.href = "login.html";
}