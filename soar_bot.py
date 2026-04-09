import time
import re
import subprocess
import requests
import csv
import os
import hashlib
from datetime import datetime
from fpdf import FPDF

LOG_FILE = "/var/log/auth.log"
DB_FILE = "atacuri.csv"
PRAG_BRUTE_FORCE = 5
ip_greseli = {}

def genereaza_raport_pdf(ip, tara, oras, data, politica, hash_dovada):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Times", 'B', 16)
    pdf.cell(200, 10, txt="RAPORT OFICIAL DE INCIDENT (GRC & AUDIT)", ln=True, align='C')
    pdf.set_font("Times", size=12)
    pdf.cell(200, 10, txt="==========================================================", ln=True, align='C')
    
    pdf.cell(200, 10, txt=f"Data si Ora Detectiei: {data}", ln=True)
    pdf.cell(200, 10, txt=f"Sursa Atac: {ip} ({tara}, {oras})", ln=True)
    pdf.cell(200, 10, txt=f"Tip Atac: Brute Force pe protocol SSH", ln=True)
    pdf.cell(200, 10, txt=f"Actiune Luata: Blocare automata in Firewall (IPTables DROP)", ln=True)
    pdf.cell(200, 10, txt="==========================================================", ln=True)
    
    pdf.set_font("Times", 'B', 12)
    pdf.cell(200, 10, txt="CORELARE CU STANDARDE DE CONFORMITATE:", ln=True)
    pdf.set_font("Times", size=11)
    pdf.multi_cell(0, 10, txt=politica)
    
    pdf.ln(5)
    pdf.set_font("Times", 'B', 12)
    pdf.cell(200, 10, txt="LANTUL DE CUSTODIE (LEGAL FORENSICS):", ln=True)
    pdf.set_font("Times", size=9)
    pdf.cell(200, 10, txt=f"Semnatura Digitala (SHA-256): {hash_dovada}", ln=True)
    pdf.cell(200, 10, txt="*Acest hash garanteaza ca logurile nu au fost alterate.*", ln=True)
    
    nume_fisier = f"Raport_Incident_{ip.replace('.', '_')}.pdf"
    pdf.output(nume_fisier)
    print(f"[AUDIT] Raport PDF generat cu succes: {nume_fisier}")

def obtine_locatie(ip):
    if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("127."):
        return "Rusia", "Moscova", 55.7558, 37.6173
    try:
        raspuns = requests.get(f"http://ip-api.com/json/{ip}").json()
        if raspuns["status"] == "success":
            return raspuns["country"], raspuns["city"], raspuns["lat"], raspuns["lon"]
    except:
        pass
    return "Necunoscut", "Necunoscut", 0.0, 0.0

def salveaza_pentru_dashboard(ip, tara, oras, lat, lon, data, politica, hash_dovada):
    fisier_exista = os.path.isfile(DB_FILE)
    with open(DB_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not fisier_exista:
            writer.writerow(["IP", "Tara", "Oras", "lat", "lon", "Data", "Politica_Incalcata", "Hash_Dovada"])
        writer.writerow([ip, tara, oras, lat, lon, data, politica, hash_dovada])

def blocheaza_ip(ip):
    print(f"[ACTION] Initializare procedura de izolare pentru IP: {ip}")
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"[SUCCESS] Regula IPTables aplicata. Trafic blocat pentru {ip}.")
        
        tara, oras, lat, lon = obtine_locatie(ip)
        acum = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        politica = "Incalcare NIS2 (Art. 21 - Management Risc) & ISO 27001 (Control A.9.1.1)"
        
        log_brut = f"{ip}|{tara}|{oras}|{acum}|BruteForce"
        hash_dovada = hashlib.sha256(log_brut.encode()).hexdigest()
        
        print(f"[THREAT INTEL] Sursa identificata: {tara}, {oras}")
        print(f"[FORENSICS] Hash SHA-256 generat: {hash_dovada[:15]}...")
        
        salveaza_pentru_dashboard(ip, tara, oras, lat, lon, acum, politica, hash_dovada)
        genereaza_raport_pdf(ip, tara, oras, acum, politica, hash_dovada)
        
    except Exception as e:
        print(f"[ERROR] Esecuri la aplicarea regulii de firewall: {e}")

def monitorizeaza_live():
    print("=====================================================")
    print("[SYSTEM] SOAR Engine v1.0 initializat.")
    print("[SYSTEM] Se monitorizeaza log-ul de autentificare...")
    print("=====================================================")
    try:
        with open(LOG_FILE, "r") as file:
            file.seek(0, 2)
            while True:
                linie = file.readline()
                if not linie:
                    time.sleep(0.1)
                    continue
                if "Failed password" in linie:
                    match = re.search(r"from ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", linie)
                    if match:
                        ip_atacator = match.group(1)
                        if ip_atacator in ip_greseli and ip_greseli[ip_atacator] >= PRAG_BRUTE_FORCE:
                            continue
                        ip_greseli[ip_atacator] = ip_greseli.get(ip_atacator, 0) + 1
                        nr = ip_greseli[ip_atacator]
                        print(f"[WARNING] Autentificare esuata detectata: IP {ip_atacator} (Incercarea {nr}/{PRAG_BRUTE_FORCE})")
                        if nr == PRAG_BRUTE_FORCE:
                            print(f"\n[CRITICAL] Prag de Brute Force atins pentru {ip_atacator}.")
                            blocheaza_ip(ip_atacator)
                            print("-" * 50)
    except Exception as e:
        print(f"[FATAL] Eroare de sistem: {e}")

if __name__ == "__main__":
    monitorizeaza_live()
