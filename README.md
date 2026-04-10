  SOAR & GRC Automation Tool

Acest proiect este un sistem de tip SOAR (Security Orchestration, Automation, and Response) dezvoltat în Python. Rolul principal al aplicației este de a monitoriza jurnalele de sistem Linux în timp real, de a bloca automat atacurile de tip Brute Force și de a genera rapoarte de incident care respectă cerințele de audit GRC.

Sistemul este împărțit în două componente principale: un daemon de monitorizare/remediere (Backend) și un dashboard interactiv pentru vizualizare (Frontend).

 Funcționalități Principale

1)Detecție în timp real (SOC): Analizarea fișierului `/var/log/auth.log` utilizând expresii regulate (Regex) pentru identificarea încercărilor eșuate de autentificare prin SSH.
2)Remediere Automată (SOAR): Izolarea atacatorilor la atingerea pragului de 5 încercări eșuate prin aplicarea automată de reguli DROP în IPTables.
3)Threat Intelligence: Geolocalizarea adreselor IP publice (via ip-api) pentru identificarea sursei atacului. Logica include fallback pentru IP-uri din clase private (RFC 1918).
4)Audit și GRC: Generarea automată a unui raport de incident în format PDF.
5)Chain of Custody: Integrarea unei semnături digitale (Hash SHA-256) pe datele brute ale atacului pentru a garanta integritatea logurilor în fața auditorilor.

 Alinierea la Standarde (Conformitate)
Proiectul a fost mapat pe următoarele standarde de securitate:
1)NIS2 (Art. 21):  Răspuns automatizat la incidente și managementul riscului.
2)ISO/IEC 27001 (A.9.1.1):  Controlul accesului și restricționarea rețelelor.

---

   Interfața Grafică (Dashboard)

Mai jos se regăsește o captură a interfeței Streamlit pentru monitorizarea incidentelor:

![Dashboard SOC](dashboard_poza.png)

## Raportare (Exemplu PDF)

Documentul generat automat pentru management și audit:

![Raport Incident](raport_poza.png)

---

## Stack Tehnologic
* **Limbaj:** Python 3
* **OS:** Linux (testat pe medii Debian/Kali)
* **Librării:** `pandas`, `streamlit` (UI), `requests` (API Call), `fpdf` (Generare Rapoarte), `hashlib` (Criptografie).

## Instrucțiuni de Utilizare

1. Clonarea repository-ului și instalarea cerințelor:
```bash
git clone [https://github.com/](https://github.com/)[NUMELE_TAU_DE_UTILIZATOR]/SOAR-GRC-Automator.git
cd SOAR-GRC-Automator
pip3 install -r requirements.txt
