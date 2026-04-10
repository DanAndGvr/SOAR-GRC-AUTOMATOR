# SOAR & GRC Automation Tool

Acest proiect este un sistem de tip SOAR (Security Orchestration, Automation, and Response) dezvoltat în Python. Rolul principal al aplicației este de a monitoriza jurnalele de sistem Linux în timp real, de a bloca automat atacurile de tip Brute Force și de a genera rapoarte de incident care respectă cerințele de audit GRC.

## Componente și Flux de Lucru (Vizualizare Sistem)

Pentru a oferi o imagine clară asupra funcționalității sistemului în producție, mai jos sunt documentate etapele de detecție, monitorizare și raportare.

### 1. Engine-ul de Detecție și Remediere (Backend)
![Terminal SOAR Backend](backend_terminal.png)

*Inițializarea daemon-ului de securitate în terminalul serverului. Sistemul monitorizează stream-ul de loguri pentru anomalii de autentificare.*

### 2. Centrul de Comandă Vizual și Tabelul GRC
![Dashboard Complet](Dashboard.png)

*Interfața interactivă dezvoltată în Streamlit. Include o hartă globală populată în timp real și tabelul detaliat al incidentelor izolate, mapate pe ISO 27001.*

### 3. Raportare Executivă și Forensics
📄 **[Vezi Exemplul de Raport PDF Generat Automat Aici](Raport_Incident_192_168_1_135.pdf)**

*Raportul oficial de incident (PDF) conține detaliile tehnice ale atacului și lanțul de custodie (semnătura digitală SHA-256).*

---

## Stack Tehnologic
* **Limbaj:** Python 3
* **OS:** Linux (testat pe medii Debian/Kali)
* **Librării:** `pandas`, `streamlit`, `requests`, `fpdf`, `hashlib`.

## Instrucțiuni de Utilizare

1. Clonarea repository-ului și instalarea cerințelor:
```bash
git clone https://github.com/DanAndGvr/SOAR-GRC-Automator.git
cd SOAR-GRC-Automator
pip3 install pandas streamlit requests fpdf
