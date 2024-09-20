# ======================================================================
# Programm: 
# Beschreibung: 
# Autor: Martin Jeremias Künzler (MKU)
# Version: 1.0
# Datum: 15. September 2024
#
#
# ! Critical Informaition 
# ? Question Information
# * Highlight something
# ToDo: 
# ======================================================================

# =======================================================================================
# Importierte Module und Bibliotheken:
#
# 1. Flask-Module:
# - Flask: Das Hauptframework, das für die Erstellung von Webanwendungen verwendet wird.
# - render_template: Wird verwendet, um HTML-Vorlagen zu rendern und an den Browser zu senden.
# - redirect: Leitet den Benutzer auf eine andere URL weiter.
# - url_for: Erzeugt URLs für spezifische Funktionen, die in der Anwendung definiert sind.
# - flash: Zeigt kurze Nachrichten an (z.B. Fehler- oder Erfolgsmeldungen), die nach einer Weiterleitung verfügbar sind.
# - request: Ermöglicht den Zugriff auf die Daten der aktuellen HTTP-Anfrage (z.B. Formular- und URL-Daten).
# - jsonify: Wandelt Python-Daten in JSON-Format um, das typischerweise in API-Routen verwendet wird.
# - make_response: Erstellt eine HTTP-Antwort, die angepasst werden kann (z.B. zum Setzen von Cookies).
#
# 2. Flask-SQLAlchemy:
# - SQLAlchemy: Objekt-Relationaler Mapper (ORM), der die Interaktion mit der Datenbank über Python-Objekte ermöglicht.
#
# 3. urllib:
# - quote as url_quote: Wird verwendet, um Sonderzeichen in URLs zu kodieren, sodass sie in HTTP-Links verwendet werden können.
#
# 4. Flask-WTF:
# - FlaskForm: Basisklasse für die Erstellung von Webformularen in Flask.
# - StringField, PasswordField, SubmitField: Formulareingabefelder für Zeichenketten, Passwörter und Schaltflächen.
# - DataRequired, Email, EqualTo, ValidationError: Validatoren, die sicherstellen, dass Formulardaten korrekt eingegeben werden.
#
# 5. Flask-Login:
# - LoginManager: Verwaltet die Benutzeranmeldung und Authentifizierung.
# - UserMixin: Bietet Standardmethoden für Benutzermodelle (z.B. is_authenticated).
# - login_user: Loggt den Benutzer ein, wenn die Anmeldeinformationen korrekt sind.
# - current_user: Gibt den aktuell angemeldeten Benutzer zurück.
# - logout_user: Loggt den Benutzer aus und beendet die Sitzung.
# - login_required: Dekorator, der sicherstellt, dass bestimmte Routen nur von angemeldeten Benutzern aufgerufen werden können.
#
# 6. Werkzeug:
# - generate_password_hash: Erstellt ein gehashtes Passwort, das sicher in der Datenbank gespeichert werden kann.
# - check_password_hash: Überprüft, ob das eingegebene Passwort mit dem gehashten Passwort übereinstimmt.
#
# 7. Flask-Migrate:
# - Migrate: Stellt Funktionen für die Verwaltung von Datenbankmigrationen bereit, um Änderungen an der Datenbankstruktur umzusetzen.
#
# 8. Flask-Mail:
# - Mail, Message: Stellt Funktionen für das Senden von E-Mails aus der Anwendung heraus bereit.
#
# 9. os:
# - os: Ermöglicht den Zugriff auf Umgebungsvariablen und Dateipfade auf dem Server, um sensible Informationen sicher zu handhaben.
#
# 10. hashlib:
# - hashlib: Bietet Funktionen zur Berechnung kryptografischer Hashes, die verwendet werden können, um Daten sicher zu hashen oder zu signieren.
# =======================================================================================
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote as url_quote
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os
import hashlib

# =======================================================================================
# Initialisierung der Flask-Anwendung und Konfiguration von wesentlichen Einstellungen.
#
# 1. app = Flask(__name__):
#    - Initialisiert die Flask-Anwendung. `__name__` stellt sicher, dass Flask den richtigen Pfad zu den Dateien findet.
#
# 2. app.config['SECRET_KEY'] = 'your_secret_key':
#    - Setzt den geheimen Schlüssel für die Flask-Anwendung. Dieser Schlüssel wird für Sitzungsverwaltung,
#      Formularschutz (CSRF-Schutz) und andere sicherheitsrelevante Funktionen verwendet.
#    - Der 'SECRET_KEY' sollte ein schwer zu erratender, sicherer Schlüssel sein und niemals öffentlich bekannt sein.
#
# 3. app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@ipdb/db':
#    - Setzt die URI für die SQLAlchemy-Datenbankverbindung. Hier wird MySQL über den `pymysql`-Treiber verwendet.
#    - Die URI enthält die Zugangsdaten zur Datenbank (Benutzername, Passwort), die IP-Adresse des Servers und den Datenbanknamen.
#    - Beispiel für MySQL-Datenbankverbindung: `mysql+pymysql://username:password@ipdb/db`.
#    - Achte darauf, diese Zugangsdaten sicher zu behandeln, indem du sie z.B. aus einer Umgebungsvariablen beziehst.
#
# 4. E-Mail-Konfiguration (Flask-Mail):
#    - Diese Einstellungen ermöglichen es der Flask-Anwendung, E-Mails über den SMTP-Server von Cyon zu versenden.
#
#    - app.config['MAIL_SERVER'] = 'mailserver':
#      - Gibt den SMTP-Server von mailhoster an, über den E-Mails versendet werden.
#    
#    - app.config['MAIL_PORT'] = 587:
#      - Setzt den SMTP-Port auf 587, der für TLS (Transport Layer Security) verwendet wird.
#
#    - app.config['MAIL_USE_TLS'] = True:
#      - Aktiviert TLS für die E-Mail-Kommunikation, um die Übertragung zu verschlüsseln und zu sichern.
#
#    - app.config['MAIL_USE_SSL'] = False:
#      - SSL wird in diesem Fall nicht verwendet, da TLS aktiviert ist. TLS und SSL sollten nicht gleichzeitig aktiviert werden.
#
#    - app.config['MAIL_USERNAME'] = 'your mail':
#      - Die E-Mail-Adresse, die für die Authentifizierung auf dem SMTP-Server verwendet wird. In diesem Fall deine Cyon-E-Mail-Adresse.
#
#    - app.config['MAIL_PASSWORD'] = 'your password':
#      - Das Passwort für die Cyon-E-Mail-Adresse. Es wird für die Authentifizierung auf dem SMTP-Server benötigt.
#      - Achte darauf, das Passwort sicher zu behandeln und nicht im Code offenzulegen. Nutze besser Umgebungsvariablen.
#
#    - app.config['MAIL_DEFAULT_SENDER'] = 'your default mail':
#      - Setzt die Standardabsenderadresse, die für alle E-Mails verwendet wird, falls kein spezifischer Absender angegeben wird.
#
#    - app.config['MAIL_DEBUG'] = True:
#      - Aktiviert Debugging für Flask-Mail, damit detaillierte Informationen über E-Mail-Sendevorgänge ausgegeben werden.
# =======================================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@ip/databasename'
app.config['MAIL_SERVER'] = 'mailserver'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your username'  # Deine E-Mail-Adresse
app.config['MAIL_PASSWORD'] = 'your Mail Password'  # Dein E-Mail-Passwort
app.config['MAIL_DEFAULT_SENDER'] = 'your default sender Mail'  # Deine Absenderadresse
app.config['MAIL_DEBUG'] = False

# Secret Key for session management
# Enable SQLAlchemy echo for debugging
app.config['SQLALCHEMY_ECHO'] = True

# =======================================================================================
# Initialisierung von Flask-Erweiterungen, die in der Anwendung verwendet werden:
#
# 1. db = SQLAlchemy(app): 
#    - Initialisiert SQLAlchemy, um die Anwendung mit einer Datenbank zu verbinden und 
#      die Datenbankoperationen (ORM) durchzuführen.
#    - SQLAlchemy vereinfacht das Arbeiten mit relationalen Datenbanken und ermöglicht die Verwendung 
#      von Python-Klassen (Modelle), um Datenbanktabellen zu definieren und Abfragen auszuführen.
#
# 2. migrate = Migrate(app, db): 
#    - Initialisiert Flask-Migrate, eine Erweiterung, die Flask und SQLAlchemy die Möglichkeit gibt,
#      Datenbankmigrationen zu verwalten. Migrationen ermöglichen das schrittweise Anpassen der Datenbankstruktur,
#      ohne Daten zu verlieren.
#    - Migrate stellt sicher, dass Änderungen an den Datenbankmodellen (z.B. Hinzufügen von Feldern) 
#      auf die Datenbank angewendet werden können.
#
# 3. login_manager = LoginManager(app):
#    - Initialisiert Flask-Login, eine Erweiterung, die für die Benutzerauthentifizierung zuständig ist.
#    - Flask-Login kümmert sich um das Verwalten von Benutzersitzungen, das Ein- und Ausloggen sowie den Schutz 
#      von Routen, die nur für angemeldete Benutzer zugänglich sind.
#    - login_manager.login_view = 'login': Definiert die Route 'login' als Standard-Login-Seite, zu der 
#      nicht-authentifizierte Benutzer umgeleitet werden, wenn sie versuchen, geschützte Bereiche zu betreten.
#
# 4. mail = Mail(app):
#    - Initialisiert Flask-Mail, eine Erweiterung, die das Senden von E-Mails aus der Anwendung heraus ermöglicht.
#    - Flask-Mail wird oft verwendet, um Benutzern E-Mails wie Passwort-Reset-Nachrichten oder Willkommensnachrichten zu senden.
# =======================================================================================
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

# ======================================================================
# Diese Klasse definiert das User-Datenbankmodell für die Anwendung. 
# Es nutzt SQLAlchemy, um die Struktur einer 'User'-Tabelle in der Datenbank zu erstellen.
# Die Klasse erweitert UserMixin, um Methoden wie is_authenticated, is_active usw. bereitzustellen, 
# die für die Benutzerverwaltung und Authentifizierung benötigt werden.
# 
# Attribute:
# - id: Eindeutiger Primärschlüssel für jeden Benutzer.
# - firstname: Vorname des Benutzers (muss eindeutig sein).
# - lastname: Nachname des Benutzers (muss eindeutig sein).
# - birthday: Geburtstag des Benutzers (muss eindeutig sein).
# - username: Benutzername des Benutzers (muss eindeutig sein).
# - email: E-Mail-Adresse des Benutzers (muss eindeutig sein).
# - password: Gehashter Passwort-String (mindestens 60 Zeichen).
# - vms: Beziehung zu den 'VM'-Datensätzen, die dieser Benutzer erstellt hat. 'lazy=True' bedeutet, 
#        dass die VM-Daten nur dann geladen werden, wenn darauf zugegriffen wird.
# ======================================================================
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20), unique=True, nullable=False)
    birthday = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    vms = db.relationship('VM', backref='author', lazy=True)

# ======================================================================
# Diese Klasse definiert das VM-Datenbankmodell (Virtual Machine) für die Anwendung.
# Es nutzt SQLAlchemy, um die Struktur einer 'VM'-Tabelle in der Datenbank zu erstellen.
#
# Attribute:
# - id: Eindeutiger Primärschlüssel für jede VM.
# - name: Der Name der VM (muss angegeben sein und darf nicht leer sein).
# - description: Beschreibung der VM (muss angegeben sein und darf nicht leer sein).
# - cpu: Anzahl der CPU-Kerne, die der VM zugewiesen sind (muss angegeben sein).
# - ram: Arbeitsspeicher (RAM) der VM in Megabyte (muss angegeben sein).
# - hdd: Festplattenspeicher der VM in Gigabyte (muss angegeben sein).
# - ipv4: Eindeutige IPv4-Adresse der VM (darf nicht leer sein und muss eindeutig sein).
#         Die Länge des Strings ist auf 16 Zeichen begrenzt, um IPv4-Adressen im Format 'xxx.xxx.xxx.xxx' zu unterstützen.
# - mac: Eindeutige MAC-Adresse der VM (darf nicht leer sein und muss eindeutig sein).
# - user_id: Fremdschlüssel, der auf die ID eines Benutzers verweist, der die VM erstellt hat (darf nicht leer sein).
#            Dieser Fremdschlüssel stellt die Beziehung zwischen der VM und dem Benutzer ('User') her.
# ======================================================================
class VM(db.Model):
    __tablename__ = 'VM'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cpu = db.Column(db.Integer, nullable=False)
    ram = db.Column(db.Integer, nullable=False)
    hdd = db.Column(db.Integer, nullable=False)
    ipv4 = db.Column(db.String(16), unique=True, nullable=False)  # String length adjusted to match varchar(16)
    mac = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

# ======================================================================
# Diese Klasse definiert das Registrierungsformular für neue Benutzer in der Anwendung.
# Es nutzt Flask-WTF, um Formularfelder und Validierungen zu erstellen, die für die
# Benutzerregistrierung erforderlich sind.
#
# Felder:
# - firstname: Textfeld für den Vornamen des Benutzers (Pflichtfeld).
# - lastname: Textfeld für den Nachnamen des Benutzers (Pflichtfeld).
# - birthday: Textfeld für das Geburtsdatum des Benutzers (Pflichtfeld).
# - username: Textfeld für den Benutzernamen des Benutzers (Pflichtfeld). Dieses Feld muss einzigartig sein.
# - email: Textfeld für die E-Mail-Adresse des Benutzers (Pflichtfeld). Die E-Mail-Adresse muss gültig und einzigartig sein.
# - password: Passwortfeld für das Passwort des Benutzers (Pflichtfeld).
# - confirm_password: Passwortfeld zur Bestätigung des Passworts (Pflichtfeld). Muss mit dem ersten Passwort übereinstimmen.
# - submit: Schaltfläche zum Absenden des Formulars.
#
# Validierungsmethoden:
# - validate_username: Prüft, ob der eingegebene Benutzername bereits existiert. Falls ja, wird eine Fehlermeldung ausgegeben.
# - validate_email: Prüft, ob die eingegebene E-Mail-Adresse bereits existiert. Falls ja, wird eine Fehlermeldung ausgegeben.
# ======================================================================
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    birthday = StringField('Birthday', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        print(user)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        print(user)
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

# ======================================================================
# Diese Klasse definiert das Login-Formular für die Benutzeranmeldung in der Anwendung.
# Es nutzt Flask-WTF, um Formularfelder und Validierungen zu erstellen, die für die 
# Benutzeranmeldung erforderlich sind.
#
# Felder:
# - email: Textfeld für die E-Mail-Adresse des Benutzers (Pflichtfeld). Die E-Mail muss gültig sein.
# - password: Passwortfeld für das Passwort des Benutzers (Pflichtfeld).
# - submit: Schaltfläche zum Absenden des Formulars.
# ======================================================================
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# ======================================================================
# Diese Route versendet eine Test-E-Mail über Flask-Mail.
# 
# Ablauf:
# - Es wird eine Nachricht erstellt, die einen Absender, Empfänger und den Nachrichteninhalt enthält.
# - Die Nachricht wird mit Flask-Mail über den SMTP-Server gesendet.
# - Bei erfolgreichem Versand wird eine Erfolgsmeldung ausgegeben.
# - Falls ein Fehler auftritt (z.B. Verbindungsfehler oder falsche SMTP-Daten), wird eine Fehlermeldung angezeigt.
#
# Ablauf der Funktionsweise:
# - msg = Message: Erstellt die E-Mail-Nachricht mit Betreff, Absender und Empfänger.
# - mail.send(msg): Sendet die Nachricht über den konfigurierten E-Mail-Server.
# - flash('Email sent successfully!'): Informiert den Benutzer über den erfolgreichen Versand.
# - flash(f'Failed to send email: {str(e)}'): Informiert den Benutzer, falls ein Fehler auftritt.
# - redirect(url_for('some_route')): Leitet den Benutzer nach dem E-Mail-Versand zu einer anderen Route um.
# ======================================================================
@app.route("/sendmail")
def sendmail():
    try:
        # Erstelle die Nachricht
        msg = Message('Hello from Flask', 
                    sender='sender mail',  # Absender explizit angeben
                    recipients=['recipiant'])  # Empfängeradresse einfügen
        msg.body = 'This is a test email sent from a Flask app!'
        mail.send(msg)  # E-Mail versenden

        flash('Email sent successfully!', 'success')
        return redirect(url_for('some_route'))  # Weiterleitung nach dem Senden der Mail
    except Exception as e:
        flash(f'Failed to send email: {str(e)}', 'danger')
        return redirect(url_for('home'))  # Falls etwas schiefgeht


# ======================================================================
# Diese Funktion wird von Flask-Login verwendet, um den aktuell angemeldeten Benutzer
# anhand der Benutzer-ID zu laden. 
#
# Ablauf:
# - @login_manager.user_loader: Ein Dekorator, der angibt, dass diese Funktion verwendet wird, um den Benutzer zu laden.
# - load_user(user_id): Die Funktion lädt den Benutzer aus der Datenbank basierend auf der übergebenen Benutzer-ID.
# - User.query.get(int(user_id)): Sucht den Benutzer anhand der Benutzer-ID in der Datenbank. Die ID wird in einen Integer umgewandelt.
# 
# Rückgabewert:
# - Gibt das User-Objekt zurück, das zur angegebenen ID gehört. Falls kein
# ======================================================================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ======================================================================
# Diese Funktion versendet eine Willkommens-E-Mail an den neuen Benutzer nach der Registrierung.
#
# Ablauf:
# - msg = Message: Erstellt eine E-Mail-Nachricht mit einem Betreff, Absender und Empfänger.
# - Der E-Mail-Text enthält eine persönliche Begrüßung, den Benutzernamen und einen Link zur Login-Seite.
# - mail.send(msg): Sendet die E-Mail über den konfigurierten E-Mail-Server.
#
# Parameter:
# - user: Das User-Objekt des neu registrierten Benutzers. Es enthält den Benutzernamen und die E-Mail-Adresse.
# 
# E-Mail-Inhalt:
# - Eine Begrüßung mit dem Benutzernamen.
# - Ein Link zur Login-Seite, über den der Benutzer auf sein Konto zugreifen kann.
# - Informationen darüber, wie der Benutzer den Support kontaktieren kann.
# ======================================================================
def send_welcome_email(user):
    msg = Message('Welcome to Our Service', 
                  sender="sendermail", 
                  recipients=[user.email])
    msg.body = f'''Hi {user.username},

Welcome to our platform! We are thrilled to have you join our community. 

To get started, you can log in to your account using the link below:
http://mkuvcid.ddns.net/login

If you have any questions or need assistance, feel free to reach out to our support team.

Thank you for choosing us, and we look forward to supporting you on your journey!

Best regards,
Martin Jeremias Künzler
'''

    mail.send(msg)

# ======================================================================
# Diese Funktion definiert die Route für die Startseite der Anwendung.
# Sie wird sowohl für die Haupt-URL ("/") als auch für die URL "/home" verwendet.
#
# Ablauf:
# - @app.route("/"): Definiert die Route für die Startseite (Haupt-URL).
# - @app.route("/home"): Definiert eine alternative Route, die ebenfalls zur Startseite führt.
# 
# Rückgabewert:
# - Die Funktion rendert das Template "index.html", das die Startseite der Anwendung darstellt.
# ======================================================================
@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

# =======================================================================================
# Diese Route ermöglicht es einem neuen Benutzer, ein Konto zu erstellen (Registrierung).
# Die Route unterstützt sowohl GET- als auch POST-Anfragen.
#
# Ablauf:
# - @app.route("/register", methods=['GET', 'POST']): Diese Route akzeptiert GET-Anfragen, um das Registrierungsformular 
#   anzuzeigen, und POST-Anfragen, um die übermittelten Registrierungsdaten zu verarbeiten.
#
# Ablauf der Funktion:
# - form = RegistrationForm(): Initialisiert das Registrierungsformular.
# - form.validate_on_submit(): Überprüft, ob das Formular korrekt ausgefüllt wurde und eine POST-Anfrage vorliegt.
# - generate_password_hash(form.password.data, method='pbkdf2:sha256'): Hashes das eingegebene Passwort, bevor es in der 
#   Datenbank gespeichert wird.
# - user = User(...): Erstellt ein neues Benutzerobjekt mit den Formulardaten (Benutzername, E-Mail, Passwort, Vorname, Nachname, Geburtstag).
# - db.session.add(user): Fügt den neuen Benutzer zur Datenbank hinzu.
# - db.session.commit(): Speichert den neuen Benutzer in der Datenbank.
# - send_welcome_email(user): Versendet eine Begrüßungs-E-Mail an den neuen Benutzer.
# - flash('Your account has been created! You are now able to log in', 'success'): Zeigt eine Erfolgsmeldung nach erfolgreicher Registrierung an.
# - return redirect(url_for('login')): Leitet den Benutzer nach erfolgreicher Registrierung zur Login-Seite weiter.
#
# Rückgabewert:
# - Bei einer GET-Anfrage: Gibt die HTML-Seite mit dem Registrierungsformular zurück.
# - Bei einer erfolgreichen POST-Anfrage: Leitet den Benutzer nach erfolgreicher Registrierung zur Login-Seite weiter.
# =======================================================================================
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        print(hashed_password)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, firstname=form.firstname.data, lastname=form.lastname.data, birthday=form.birthday.data)
        db.session.add(user)
        db.session.commit()
        send_welcome_email(user)
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# =======================================================================================
# Diese Route ermöglicht es einem Benutzer, sich in der Anwendung anzumelden.
# Die Route unterstützt sowohl GET- als auch POST-Anfragen.
#
# Ablauf:
# - @app.route("/login", methods=['GET', 'POST']): Diese Route akzeptiert GET-Anfragen zum Anzeigen 
#   des Login-Formulars und POST-Anfragen zur Verarbeitung der Login-Daten.
#
# Ablauf der Funktion:
# - current_user.is_authenticated: Wenn der Benutzer bereits eingeloggt ist, wird er zur Startseite umgeleitet.
# - form = LoginForm(): Initialisiert das Login-Formular.
# - form.validate_on_submit(): Überprüft, ob das Formular korrekt ausgefüllt wurde und eine POST-Anfrage vorliegt.
# - user = User.query.filter_by(email=form.email.data).first(): Sucht den Benutzer anhand der E-Mail-Adresse.
# - check_password_hash(user.password, form.password.data): Überprüft, ob das eingegebene Passwort mit dem in der Datenbank
#   gespeicherten Passwort übereinstimmt.
# - login_user(user): Loggt den Benutzer ein, wenn die E-Mail und das Passwort korrekt sind.
# - flash('Login Unsuccessful. Please check email and password', 'danger'): Zeigt eine Fehlermeldung an, wenn die E-Mail 
#   oder das Passwort falsch sind.
# - return render_template('login.html', form=form): Zeigt bei einer GET-Anfrage oder einem fehlgeschlagenen Login-Versuch das 
#   Login-Formular an.
#
# Rückgabewert:
# - Bei einem erfolgreichen Login: Leitet den Benutzer zur Startseite um.
# - Bei einer GET-Anfrage oder einem fehlgeschlagenen Login: Zeigt das Login-Formular mit einer möglichen Fehlermeldung an.
# =======================================================================================
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print("User found:", user.email)
            if check_password_hash(user.password, form.password.data):
                print("Password matches")
                login_user(user)
                return redirect(url_for('home'))
            else:
                print("Password does not match",user.password ,form.password.data)
        else:
            print("User not found")
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


# =======================================================================================
# Diese Route ermöglicht es einem Benutzer, sich abzumelden (Logout).
#
# Ablauf:
# - @app.route("/logout"): Diese Route akzeptiert GET-Anfragen, um den Benutzer abzumelden.
#
# Ablauf der Funktion:
# - logout_user(): Flask-Login-Funktion, die die aktuelle Benutzersitzung beendet.
# - response = make_response(redirect(url_for('home'))): Erstellt eine Antwort, die den Benutzer zur Startseite umleitet.
# - response.set_cookie('username', '', expires=0): Löscht das 'username'-Cookie, indem es dessen Wert leert und es sofort ablaufen lässt.
# - response.set_cookie('auth', '', expires=0): Löscht das 'auth'-Cookie, indem es dessen Wert leert und es sofort ablaufen lässt.
#
# Rückgabewert:
# - Gibt eine Antwort zurück, die den Benutzer zur Startseite umleitet und gleichzeitig die Cookies 'username' und 'auth' löscht.
# =======================================================================================
@app.route("/logout")
def logout():
    logout_user()
    response = make_response(redirect(url_for('home')))
    response.set_cookie('username', '', expires=0)
    response.set_cookie('auth', '', expires=0)
    return response

# =======================================================================================
# Diese Route ermöglicht es einem angemeldeten Benutzer, eine neue virtuelle Maschine (VM) zu erstellen.
# Die Route unterstützt sowohl GET- als auch POST-Anfragen, um das Formular anzuzeigen und die eingegebenen Daten zu verarbeiten.
#
# Ablauf:
# - @app.route("/vm/new", methods=['GET', 'POST']): Diese Route akzeptiert GET-Anfragen, um das Formular für die VM-Erstellung
#   anzuzeigen und POST-Anfragen, um die übermittelten Daten zu verarbeiten und die VM in der Datenbank zu speichern.
# - @login_required: Stellt sicher, dass nur angemeldete Benutzer diese Route aufrufen können.
#
# Ablauf der Funktion:
# - GET-Anfrage: Zeigt das Formular zur Erstellung einer neuen VM an.
# - POST-Anfrage: 
#     - Liest die vom Benutzer eingegebenen Daten (Name, CPU, Beschreibung, RAM, MAC-Adresse, IPv4-Adresse, Festplattenspeicher).
#     - Erstellt ein neues VM-Objekt mit den eingegebenen Daten und dem aktuell angemeldeten Benutzer als Autor (current_user).
#     - Fügt die neue VM zur Datenbank hinzu und speichert die Änderungen.
#     - Leitet den Benutzer nach erfolgreicher Erstellung zur VM-Übersicht weiter.
# - return render_template('vms.html'): Zeigt das Formular zur Erstellung einer VM an, wenn es sich um eine GET-Anfrage handelt.
#
# Rückgabewert:
# - Bei GET: Gibt die HTML-Seite mit dem Formular zur Erstellung einer neuen VM zurück.
# - Bei POST: Leitet den Benutzer nach erfolgreicher VM-Erstellung zur VM-Übersicht weiter.
# =======================================================================================

@app.route("/vm/new", methods=['GET', 'POST'])
@login_required
def new_vm():
    if request.method == 'POST':
        name = request.form['name']
        cpu = request.form['cpu']
        description = request.form['description']
        ram = request.form['ram']
        mac = request.form['mac']
        ipv4 = request.form['ipv4']
        hdd = request.form['hdd']
        vm = VM(name=name, description=description, author=current_user, cpu=cpu, ram=ram, mac=mac, ipv4=ipv4, hdd=hdd)
        db.session.add(vm)
        db.session.commit()
        return redirect(url_for('view_vms'))  # Redirect to the VM list page or desired page
    return render_template('vms.html')

# =======================================================================================
# Diese API-Route gibt eine Liste aller virtuellen Maschinen (VMs) mit detaillierten Informationen in JSON-Format zurück.
#
# Ablauf:
# - @app.route("/api/vms", methods=['GET']): Diese Route akzeptiert GET-Anfragen und gibt eine JSON-Liste 
#   der virtuellen Maschinen mit detaillierten Informationen zurück.
#
# Ablauf der Funktion:
# - vms = VM.query.all(): Ruft alle VMs aus der Datenbank ab.
# - vms_list = [{"1_id": vm.id, "2_name": vm.name, "3_cpu": vm.cpu, "4_ram": vm.ram, "5_hdd": vm.hdd, "6_ipv4": vm.ipv4,
#                "7_description": vm.description, "8_author": vm.author.username} for vm in vms]:
#   Erstellt eine Liste von Wörterbüchern, in denen detaillierte Informationen für jede VM enthalten sind, 
#   einschließlich ID, Name, CPU, RAM, HDD, IPv4, Beschreibung und Benutzername des Erstellers.
# - return jsonify(vms_list): Konvertiert die Liste der VMs in JSON und gibt sie als API-Antwort zurück.
#
# Rückgabewert:
# - Gibt eine JSON-Liste zurück, die alle VMs mit ihrer ID, ihrem Namen, CPU, RAM, Festplattenspeicher (HDD),
#   IPv4-Adresse, Beschreibung und dem Benutzernamen des Erstellers enthält.
# =======================================================================================
@app.route("/api/vms", methods=['GET'])
def get_vms():
    vms = VM.query.all()
    vms_list = [{"1_id":vm.id,"2_name": vm.name,"3_cpu":vm.cpu,"4_ram":vm.ram,"5_hdd":vm.hdd,"6_ipv4":vm.ipv4, "7_description": vm.description, "8_author": vm.author.username} for vm in vms]
    return jsonify(vms_list)

# =======================================================================================
# Diese API-Route gibt eine Liste aller Benutzer in JSON-Format zurück.
#
# Ablauf:
# - @app.route("/api/users", methods=['GET']): Diese Route akzeptiert GET-Anfragen und gibt eine JSON-Liste 
#   der Benutzer zurück.
#
# Ablauf der Funktion:
# - users = User.query.all(): Ruft alle Benutzer aus der Datenbank ab.
# - user_list = [{"id": user.id, "author": user.username} for user in users]: Erstellt eine Liste von 
#   Wörterbüchern, in denen die Benutzer-ID und der Benutzername für jeden Benutzer enthalten sind.
# - return jsonify(user_list): Konvertiert die Liste der Benutzer in JSON und gibt sie als API-Antwort zurück.
#
# Rückgabewert:
# - Gibt eine JSON-Liste zurück, die alle Benutzer mit ihrer ID und ihrem Benutzernamen enthält.
# =======================================================================================
@app.route("/api/users", methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id":user.id, "Username": user.username, "Firstname": user.firstname, "Lastname": user.lastname, "E-Mail": user.email, "Birthday": user.birthday} for user in users]
    return jsonify(user_list)
 

# ======================================================================
# Diese Route behandelt den Endpunkt '/url_map'.
#  Wenn darauf zugegriffen wird, gibt sie die URL-Map der Flask-Anwendung aus und liefert sie als JSON zurück.
# ======================================================================
@app.route('/api/url_map')
def work():
    print(app.url_map)
    # Return the url_map as JSON
    urls = {}
    for rule in app.url_map.iter_rules():
        urls[str(rule)] = {
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "defaults": rule.defaults,
            "subdomain": rule.subdomain,
        }   
    # Die URL Map wird mittels eines JSON zurückgegeben und im Browser oder zum Beispiel Postman angezeigt
    return jsonify(url_map=urls)

# =======================================================================================
# Diese Route zeigt eine Liste aller Benutzer aus der Datenbank an.
#
# Ablauf:
# - @app.route("/user"): Diese Route akzeptiert GET-Anfragen, um die Liste der Benutzer anzuzeigen.
#
# Ablauf der Funktion:
# - users_data = User.query.all(): Diese Abfrage ruft alle in der Datenbank gespeicherten Benutzer ab.
# - return render_template("user.html", users_data=users_data): Rendert das HTML-Template 'user.html'
#   und übergibt die Liste der Benutzer als Variable 'users_data', damit diese in der Ansicht angezeigt 
#   werden kann.
#
# Rückgabewert:
# - Gibt die gerenderte HTML-Seite mit der Liste aller Benutzer zurück.
# =======================================================================================
@app.route("/user")
def user():
    users_data = User.query.all()
    return render_template("user.html", users_data=users_data)

# =======================================================================================
# Diese Route zeigt die Details eines einzelnen Benutzers basierend auf der übergebenen Benutzer-ID.
#
# Ablauf:
# - @app.route("/showUser/<int:user>"): Diese Route akzeptiert GET-Anfragen und erwartet eine Benutzer-ID 
#   als Parameter, um den spezifischen Benutzer abzurufen und seine Details anzuzeigen.
#
# Ablauf der Funktion:
# - cuser = User.query.filter_by(id=user): Sucht nach dem Benutzer mit der angegebenen ID in der Datenbank.
#   - Wichtig: Hier fehlt das `.first()`, um das erste Ergebnis der Abfrage zurückzugeben. Andernfalls wird 
#     eine Abfrage (Query) zurückgegeben und nicht der tatsächliche Benutzer.
# - return render_template('showUser.html', showUser=cuser): Rendert das HTML-Template 'showUser.html' und 
#   übergibt die Benutzerdaten als Variable 'showUser', damit die Details des Benutzers auf der Seite angezeigt 
#   werden können.
#
# Rückgabewert:
# - Gibt die gerenderte HTML-Seite mit den Details des gefundenen Benutzers zurück.
# =======================================================================================
@app.route("/showUser/<int:user>")
def userShow(user):
    cuser = User.query.filter_by(id=user)
    return render_template('showUser.html',showUser=cuser)

# =======================================================================================
# Diese Route zeigt die Details einer einzelnen virtuellen Maschine (VM) basierend auf der übergebenen ID.
#
# Ablauf:
# - @app.route("/showVM/<int:id>"): Diese Route akzeptiert GET-Anfragen und erwartet eine VM-ID als Parameter,
#   um die spezifische VM abzurufen und anzuzeigen.
#
# Ablauf der Funktion:
# - cuser = VM.query.filter_by(id=id): Sucht nach der VM mit der angegebenen ID in der Datenbank.
#   - Wichtig: Hier fehlt das `.first()`, um das erste Ergebnis der Abfrage zurückzugeben. Andernfalls wird eine Abfrage (Query) zurückgegeben und nicht die eigentliche VM.
# - return render_template('showVM.html', showVM=cuser): Rendert das HTML-Template 'showVM.html' und übergibt
#   die VM-Daten als Variable 'showVM', damit die Details der VM auf der Seite angezeigt werden können.
#
# Rückgabewert:
# - Gibt die gerenderte HTML-Seite mit den Details der gefundenen VM zurück.
# =======================================================================================
@app.route("/showVM/<int:id>")
def showVM(id):
    cuser = VM.query.filter_by(id=id)
    return render_template('showVM.html',showVM=cuser)

# =======================================================================================
# Diese Route ermöglicht es dem Benutzer, eine Liste aller virtuellen Maschinen (VMs) anzuzeigen.
#
# Ablauf:
# - @app.route("/view_vms"): Diese Route akzeptiert GET-Anfragen, um die Liste der VMs anzuzeigen.
#
# Ablauf der Funktion:
# - vms = VM.query.all(): Diese Abfrage ruft alle in der Datenbank gespeicherten VMs ab.
# - render_template("view_vms.html", vms=vms): Rendert das HTML-Template 'view_vms.html' und übergibt
#   die Liste der VMs als Variable 'vms' an das Template, damit diese in der Ansicht angezeigt werden kann.
#
# Rückgabewert:
# - Gibt die gerenderte HTML-Seite mit allen VMs zurück.
# =======================================================================================

@app.route("/view_vms")
def view_vms():
    vms = VM.query.all()
    return render_template("view_vms.html",vms=vms)

# =======================================================================================
# Diese Route ermöglicht es einem Benutzer, die Details eines vorhandenen Benutzers zu bearbeiten.
# Die Route unterstützt sowohl GET- als auch POST-Anfragen, um Benutzerdaten zu laden und zu aktualisieren.
#
# Ablauf:
# - @app.route('/edit_user/<int:id>', methods=['GET', 'POST']): Diese Route akzeptiert GET- und POST-Anfragen.
#   - GET: Lädt die Benutzerdaten zur Bearbeitung.
#   - POST: Nimmt die vom Benutzer geänderten Daten entgegen und speichert sie in der Datenbank.
#
# Ablauf der Funktion:
# - cuser = User.query.filter_by(id=id).first(): Sucht den Benutzer mit der angegebenen ID in der Datenbank.
#   Falls kein Benutzer gefunden wird, gibt die Funktion eine 404-Fehlerseite zurück.
# - Wenn die Anfrage eine POST-Anfrage ist, werden die im Formular übermittelten Daten verwendet, um die
#   Benutzerdaten zu aktualisieren (E-Mail, Vorname, Nachname und Geburtstag).
# - Der Benutzername wird nicht aktualisiert, da dieses Feld im Formular deaktiviert ist.
# - db.session.commit(): Speichert die Änderungen in der Datenbank.
# - Falls ein Fehler auftritt, wird die Datenbankoperation zurückgesetzt (Rollback) und eine Fehlermeldung ausgegeben.
# - flash(f'User {cuser.username} updated successfully!'): Zeigt eine Erfolgsmeldung an, wenn der Benutzer erfolgreich aktualisiert wurde.
# - redirect(url_for('user')): Leitet den Benutzer nach erfolgreicher Bearbeitung zur Benutzerübersicht weiter.
#
# Parameter:
# - id: Die ID des zu bearbeitenden Benutzers. Diese wird als URL-Parameter übergeben.
# =======================================================================================

@app.route('/edit_user/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cuser = User.query.filter_by(id=id).first()  # Get the user from the database by ID
    if not cuser:
        return "User not found", 404

    if request.method == 'POST':
        # Update user details with form data, but don't update the username as it is disabled
        cuser.email = request.form['email']
        cuser.firstname = request.form['firstname']
        cuser.lastname = request.form['lastname']
        cuser.birthday = request.form['birthday']

        try:
            db.session.commit()  # Commit the changes to the database
            flash(f'User {cuser.username} updated successfully!', 'success')
            return redirect(url_for('user'))  # Redirect to the user list page
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash(f'Error updating user: {str(e)}', 'danger')

    return render_template('edit_user.html', showUser=cuser)

# =======================================================================================
# Diese Route ermöglicht es einem Benutzer, eine bestehende virtuelle Maschine (VM) zu bearbeiten.
# Die Route unterstützt sowohl GET- als auch POST-Anfragen, um die VM-Daten abzurufen und zu aktualisieren.
#
# Ablauf:
# - @app.route('/edit_vm/<int:id>', methods=['GET', 'POST']): Diese Route akzeptiert GET- und POST-Anfragen.
#   - GET: Lädt die VM-Daten für die Bearbeitung.
#   - POST: Nimmt die vom Benutzer geänderten Daten entgegen und speichert sie in der Datenbank.
#
# Ablauf der Funktion:
# - cuser = VM.query.filter_by(id=id).first(): Sucht die VM mit der angegebenen ID in der Datenbank.
#   Falls keine VM gefunden wird, wird eine 404-Fehlermeldung zurückgegeben.
# - Wenn die Anfrage eine POST-Anfrage ist, werden die im Formular übermittelten Daten verwendet, um die
#   VM-Daten zu aktualisieren (z.B. Name, CPU, RAM, Festplattenspeicher, MAC-Adresse, IPv4-Adresse und Beschreibung).
# - db.session.commit(): Speichert die Änderungen in der Datenbank.
# - Falls ein Fehler auftritt, wird die Datenbankoperation zurückgesetzt (Rollback) und eine Fehlermeldung ausgegeben.
# - flash('VM updated successfully!'): Zeigt eine Erfolgsmeldung an, wenn die VM erfolgreich aktualisiert wurde.
# - redirect(url_for('view_vms')): Leitet den Benutzer nach erfolgreicher Bearbeitung zur VM-Übersicht oder einer anderen Seite weiter.
#
# Parameter:
# - id: Die ID der zu bearbeitenden virtuellen Maschine. Diese wird als URL-Parameter übergeben.
# =======================================================================================
@app.route('/edit_vm/<int:id>', methods=['GET', 'POST'])
def edit_vm(id):
    cuser = VM.query.filter_by(id=id).first()
    if not cuser:
        return "VM not found", 404

    if request.method == 'POST':
        # Update the existing VM object with form data
        cuser.name = request.form['name']
        cuser.cpu = request.form['cpu']
        cuser.description = request.form['description']
        cuser.ram = request.form['ram']
        cuser.mac = request.form['mac']
        cuser.ipv4 = request.form['ipv4']
        cuser.hdd = request.form['hdd']
        
        try:
            db.session.commit()  # Commit the changes to the database
            flash('VM updated successfully!', 'success')
            return redirect(url_for('view_vms'))  # Redirect to the VM list page or desired page
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of an error
            flash(f'Error updating VM: {str(e)}', 'danger')

    return render_template('edit_vm.html', showVM=cuser)



# =======================================================================================
# Diese Route ermöglicht es einem autorisierten Benutzer (erfordert Anmeldung),
# eine virtuelle Maschine (VM) aus der Datenbank zu löschen.
#
# Ablauf:
# - @app.route('/delete_vm/<int:vm_id>', methods=['POST']): Diese Route wird über eine POST-Anfrage
#   aufgerufen, um eine VM basierend auf der übergebenen VM-ID zu löschen.
# - @login_required: Stellt sicher, dass nur authentifizierte Benutzer diese Aktion ausführen können.
#
# Ablauf der Funktion:
# - vm_to_delete = VM.query.get_or_404(vm_id): Sucht nach der VM mit der angegebenen ID.
#   Falls keine VM mit dieser ID gefunden wird, wird eine 404-Fehlerseite angezeigt.
# - db.session.delete(vm_to_delete): Löscht die gefundene VM aus der Datenbank.
# - db.session.commit(): Speichert die Änderungen (Löschung) in der Datenbank.
# - flash('VM has been deleted!'): Zeigt eine Erfolgsmeldung an, dass die VM erfolgreich gelöscht wurde.
# - redirect(url_for('view_vms')): Leitet den Benutzer nach dem Löschen zur Seite mit der VM-Übersicht weiter.
#
# Parameter:
# - vm_id: Die ID der zu löschenden virtuellen Maschine. Diese wird als URL-Parameter übergeben.
# =======================================================================================

@app.route('/delete_vm/<int:vm_id>', methods=['POST'])
@login_required
def delete_vm(vm_id):
    vm_to_delete = VM.query.get_or_404(vm_id)
    db.session.delete(vm_to_delete)
    db.session.commit()
    flash('VM has been deleted!', 'success')
    return redirect(url_for('view_vms'))

# =======================================================================================
# Diese Route ermöglicht es einem autorisierten Benutzer (erfordert Anmeldung),
# einen Benutzer aus der Datenbank zu löschen.
#
# Ablauf:
# - @app.route('/delete_user/<int:user_id>', methods=['POST']): Diese Route wird über eine POST-Anfrage
#   aufgerufen, um einen Benutzer basierend auf der übergebenen Benutzer-ID zu löschen.
# - @login_required: Stellt sicher, dass nur authentifizierte Benutzer diese Aktion ausführen können.
#
# Ablauf der Funktion:
# - user_to_delete = User.query.get_or_404(user_id): Sucht nach dem Benutzer mit der angegebenen ID.
#   Falls kein Benutzer mit dieser ID gefunden wird, wird eine 404-Fehlerseite angezeigt.
# - db.session.delete(user_to_delete): Löscht den gefundenen Benutzer aus der Datenbank.
# - db.session.commit(): Speichert die Änderungen (Löschung) in der Datenbank.
# - flash('User has been deleted!'): Zeigt eine Erfolgsmeldung an, dass der Benutzer erfolgreich gelöscht wurde.
# - redirect(url_for('user')): Leitet den Benutzer nach dem Löschen auf die Seite mit der Benutzerübersicht weiter.
#
# Parameter:
# - user_id: Die ID des Benutzers, der gelöscht werden soll. Diese wird als URL-Parameter übergeben.
# =======================================================================================
@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('user'))

# =======================================================================================
# Diese Funktion hilft dabei,
# benutzerdefinierte Fehlermeldungen für den HTTP Error Code 400 (Bad Request)
# anzuzeigen. Der Fehler 400 bedeutet, dass der Server die Anfrage aufgrund eines
# fehlerhaften oder ungültigen Syntaxverständnisses nicht verarbeiten konnte. 
# Dies kann passieren, wenn die Anfrage fehlerhafte Daten enthält oder 
# das Anforderungsformat nicht den erwarteten Spezifikationen entspricht.
#
# Mit dieser Funktion wird dem Benutzer eine benutzerfreundliche Fehlermeldungsseite 
# angezeigt, anstatt eine generische oder leere Fehlerseite. Diese Seite informiert 
# den Benutzer darüber, dass die Anfrage nicht korrekt war und erklärt möglicherweise,
# welche Schritte unternommen werden sollten, um die Anfrage zu korrigieren.
# =======================================================================================

@app.errorhandler(400)
def page_not_found(e):
    return render_template("error_400.html"), 400

# =======================================================================================
# Diese Funktion hilft dabei,
# benutzerdefinierte Fehlermeldungen für den HTTP Error Code 404 (Not Found)
# anzuzeigen. Der Fehler 404 bedeutet, dass die angeforderte Ressource 
# auf dem Server nicht gefunden wurde. Dies kann passieren, wenn die URL falsch ist 
# oder die Ressource entfernt wurde.
#
# Mit dieser Funktion wird dem Benutzer eine benutzerfreundliche Fehlermeldungsseite 
# angezeigt, anstatt eine generische oder leere Fehlerseite. Die Seite informiert 
# den Benutzer darüber, dass die angeforderte Seite oder Ressource nicht existiert 
# und bietet möglicherweise eine Rückkehr zur Startseite oder andere Navigationsoptionen an.
# =======================================================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error_404.html"), 404

# =======================================================================================
# Diese Funktion hilft dabei, 
# benutzerdefinierte Fehlermeldungen für den HTTP Error Code 403 (Forbidden)
# anzuzeigen. Der Fehler 403 bedeutet, dass der Server die Anfrage des Benutzers 
# verstanden hat, aber die Berechtigung fehlt, um auf die angeforderte Ressource zuzugreifen.
# Dies kann passieren, wenn der Benutzer keine ausreichenden Rechte hat 
# oder wenn bestimmte Inhalte nur für bestimmte Benutzergruppen zugänglich sind.
#
# Mit dieser Funktion wird dem Benutzer eine benutzerfreundliche Fehlermeldungsseite 
# angezeigt, anstatt eine generische oder leere Fehlerseite. Diese Seite informiert 
# den Benutzer darüber, dass der Zugriff verweigert wurde, und bietet möglicherweise 
# weitere Informationen oder Anweisungen.
# =======================================================================================
@app.errorhandler(403)
def page_not_found(e):
    return render_template("error_403.html"), 403

# =======================================================================================
# Diese Funktion hilft dabei, 
# benutzerdefinierte Fehlermeldungen für den HTTP Error Code 405 (Method Not Allowed)
# "Anfrage darf nur mit anderen HTTP-Methoden (zum Beispiel GET statt POST)
# gestellt werden. Gültige Methoden für die betreffende Ressource werden 
# im „Allow“-Header-Feld der Antwort übermittelt.)"
# anzuzeigen und dem Benutzer 
# eine benutzerfreundliche Fehlermeldungsseite zu präsentieren, 
# anstatt eine generische oder leere Fehlerseite.
# =======================================================================================
@app.errorhandler(405)
def page_not_found(e):
    return render_template("error_405.html"), 405

# =======================================================================================
# Diese Funktion hilft dabei, 
# benutzerdefinierte Fehlermeldungen für den HTTPS Error Code 500 (Internal Server Error)
# "Dies ist ein „Sammel-Statuscode“ für unerwartete Serverfehler."
# anzuzeigen und dem Benutzer 
# eine benutzerfreundliche Fehlermeldungsseite zu präsentieren, 
# anstatt eine generische oder leere Fehlerseite.
# =======================================================================================
@app.errorhandler(500)  # Dekorator, der Flask anweist, diese Funktion bei einem HTTP 500 Fehler aufzurufen
def page_not_found(e):  # Definiert eine Funktion, die bei einem 500 Fehler ausgeführt wird
    return render_template("error_500.html"), 500  # Rendert die HTML-Vorlage 'error_500.html' und gibt den HTTP-Statuscode 500 zurück

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True,host='0.0.0.0',port=port)

