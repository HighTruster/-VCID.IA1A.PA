
# VM-Management Anwendung

Dieses Repository enthält den Quellcode und die Dokumentation für die **VM-Management**-Anwendung. Das Projekt ist Teil einer Praxisarbeit und zielt darauf ab, den Benutzern eine benutzerfreundliche Plattform zur Verwaltung von virtuellen Maschinen (VMs) bereitzustellen. Im Folgenden werden die Hauptfunktionen, verwendete Technologien und Anweisungen zur Bereitstellung der Anwendung beschrieben.

## Überblick

Die **VM-Management**-Anwendung ermöglicht es Benutzern, virtuelle Maschinen zu erstellen, zu bearbeiten und zu löschen. Dabei können Ressourcen wie CPU, RAM, Festplattenspeicher und Netzwerkeinstellungen über eine benutzerfreundliche Oberfläche konfiguriert werden. Die Anwendung wurde mit dem Flask-Framework entwickelt und verwendet MySQL als Datenbank zur Speicherung von VM- und Benutzerdaten.

## Funktionen

- **VM-Erstellung**: Benutzer können virtuelle Maschinen erstellen, indem sie Einstellungen wie CPU, RAM, Speicher und Netzwerkeinstellungen konfigurieren.
- **VM-Bearbeitung**: Benutzer können bestehende virtuelle Maschinen bearbeiten und deren Konfigurationen aktualisieren.
- **Benutzerverwaltung**: Die Anwendung unterstützt die Registrierung, Anmeldung und Verwaltung von Benutzerkonten.
- **API-Integration**: Eine RESTful API ermöglicht es externen Anwendungen, mit dem System zu interagieren, einschließlich des Abrufs von VM-Daten im JSON-Format.

## Verwendete Technologien

- **Flask (Python)**: Web-Framework zur Entwicklung der Anwendung.
- **MySQL**: Relationale Datenbank zur Speicherung von Benutzer- und VM-Daten.
- **Docker**: Containerisierungsplattform zur Bereitstellung der Anwendung.
- **NGINX**: Wird als Reverse Proxy verwendet, um HTTP/HTTPS-Anfragen zu verarbeiten und SSL-Unterstützung zu bieten.

## Bereitstellungsanweisungen

Die Anwendung ist mit Docker verpackt und ermöglicht eine einfache Bereitstellung in verschiedenen Umgebungen.

### Voraussetzungen

- Docker und Docker Compose installiert.
- MySQL-Datenbank mit den erforderlichen Anmeldeinformationen konfiguriert.

### Schritte zur Bereitstellung

1. Klonen Sie dieses Repository:
   ```bash
   git clone https://github.com/HighTruster/VCID.IA1A-MJK.git
   ```

2. Wechseln Sie in das Projektverzeichnis:
   ```bash
   cd VCID.IA1A-MJK
   ```

3. Aktualisieren Sie die Umgebungsvariablen und Konfigurationsdateien (`conf.env`):
   ```bash
   export MAIL_USERNAME='Ihre Mail'
   export MAIL_PASSWORD='Ihr Passwort'
   export MAIL_DEFAULT_SENDER='Ihre Mail'
   ```

4. Bauen und starten Sie die Docker-Container:
   ```bash
   docker compose up --build
   ```

5. Greifen Sie über Ihren Browser auf die Anwendung unter `http://localhost` oder Ihrer konfigurierten Domain zu.

## API-Endpunkte

Die folgenden API-Endpunkte stehen für die externe Integration zur Verfügung:

- **GET /api/vms**: Gibt eine Liste aller virtuellen Maschinen zurück.
- **GET /api/users**: Gibt eine Liste aller registrierten Benutzer zurück.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Weitere Informationen finden Sie in der [LICENSE](LICENSE) Datei.

## Autor

- Martin Jeremias Künzler
