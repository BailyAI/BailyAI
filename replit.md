# Baily Bot – Telegram Bot Project

## Overview

Dies ist ein deutschsprachiger Telegram-Bot namens **"Baily"**, entwickelt mit Python und der `python-telegram-bot`-Bibliothek. Der Bot bietet KI-gestützte Konversation, Admin-Steuerung und speichert den Gesprächsverlauf. Ziel ist es, eine charmante und interaktive Chat-Erfahrung zu bieten.

**Aktueller Status**: Der Bot ist funktionsfähig und verwendet einen Flask-Webserver für das Keep-Alive. Die KI-Logik basiert auf **Google Gemini API** – als kostenlose Alternative zu GPT.

---

## User Preferences

- Sprachstil: Alltagstauglich, leicht verspielt

---

## Systemarchitektur

Der Bot nutzt ein modulares Design mit klarer Trennung von Zuständigkeiten.

### Hauptkomponenten

- **Main Application** (`main.py`)  
  Startpunkt, Initialisierung der Handlers

- **Web Server** (`web_server.py`)  
  Flask-basierter Keep-Alive-Server auf Port 8080

- **Konfiguration** (`config.py`)  
  Zentrale Umgebungsvariablen (z. B. `BOT_TOKEN`, `ADMIN_ID`)

- **Handler-Module**  
  Eigene Dateien für Commands, Nachrichten, Adminfunktionen

- **Utilities**  
  Zusatzfunktionen: Logging, AI-Kommunikation, Antworten

- **Persistenz**  
  Konversationsstatus wird in JSON gespeichert (`data/conversation_states.json`)

---

## KI-Integration

### Neu: **Google Gemini API** (`utils/gemini_handler.py`)

- **Funktion**: Beantwortung von Nutzereingaben mit Kontext
- **Kontextspeicherung**: max. 10 letzte Nachrichten
- **Persönlichkeit**: Flirtend, charmant, leicht dominant (definiert durch System-Prompt)
- **Fallback**: Lokale Antwortlogik bei Fehlern

---

## Module im Überblick

### 1. `/handlers/commands.py`

- `/start`, `/help`, `/whoami` u. a.
- Personalisierte Begrüßungen mit Emojis

### 2. `/handlers/conversations.py`

- Verarbeitet alle normalen Texte
- Nutzt Gemini für intelligente Antworten
- Verwalter des Gesprächszustands pro User

### 3. `/handlers/admin.py`

- `/status`, `/admin`, `/broadcast`
- Zugriff nur für `ADMIN_ID`
- Ressourcenanzeige via `psutil`

### 4. `/data/conversation_states.py`

- Speichert den Gesprächsverlauf als JSON
- Erkennt User anhand ihrer Telegram-ID
- Merkt letzte Aktivität, Nachrichtenzähler usw.

### 5. `/utils/gemini_handler.py`

- Sendet API-Anfragen an Gemini (statt OpenAI)
- Zwei Hauptfunktionen:
  - `generate_reply()`
  - `generate_reply_with_context()`

### 6. `/utils/logging_config.py`

- Erstellt `logs/` Ordner bei Bedarf
- Schreibt Logs mit Zeitstempel & Severity

---

## Datenfluss

```plaintext
Nachricht → Handler-Auswahl → Zustand laden → Antwort generieren → Zustand speichern → Antwort senden
