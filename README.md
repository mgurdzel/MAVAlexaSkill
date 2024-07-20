
# Alexa Skill: Project MARV

## Projektbeschreibung
Dieses Projekt zielt darauf ab, einen Flurförderroboter mithilfe von Sprachbefehlen über Alexa zu steuern. Der Alexa Skill ermöglicht es dem Benutzer, verschiedene Befehle an den Roboter zu senden, um seine Bewegungen und Aktionen zu kontrollieren.

## Vorraussetzungen
- Alexa Developer Console Zugang
- Grundkenntnisse in Python
- Kenntnisse im Umgang mit AWS-Services (Lambda, IAM, etc.)

## Projektstruktur
- **Skill Definition**
     - **Interaction Model**: Definiert die Intents, Slots und Sprachmuster. Die Daten befinden sich im Ordner `/interactionModels/custom` als exportierte JSON Datei
     - **Backend-Logik**: AWS Lambda Funktion, die die Anfragen verarbeitet und entsprechende Antworten generiert. Die Daten befinden sich im Ordner `/lambda/`. Die Backend Logik wurde in diesem Projekt mit Hilfe von Python aufgebaut.

## Importieren der vorhandenen Daten

### Schritt 1: Erstellen des Alexa Skills
 - Melde dich bei der [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) an.
   - Klicke auf "Create Skill" 
   - Wähle einen Namen für deinen Skill und die "Primary local language" aus

### Schritt 2: Experience, Model, Hosting service
 - Wähle im Schritt Choose a type of experience "Other" aus
 - Wähle das "Custom" Model sowie "Alexa-hosted (Python)" als Hosting Service aus
 - Nutze einen EU Server als "Hosting Region"

### Schritt 3: Importiere Git Repository
 - Klicke oben rechts auf den Button "Import Skill" und gebe dort die Adresse des Repositorys: [MAVAlexaSkill](https://github.com/mgurdzel/MAVAlexaSkill) an.
 - Klicke nun auf Import (die Installation dauert nun ein paar Minuten)

### Schritt 4: Vergeben eines Skill Invocation Names
 - Wechsel in den Build-Sektion der [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
 - Klappe dort den Tab "Invocations" aus und klicke auf "Skill Invocations Name"
 - Vergebe dort den "Skill Invocation Name". Dieser wird benötigt um den Skill auf der Alexa zu starten.
 - Klicke nun oben rechts auf "Build"

### Schritt 5: Testen des Skills
 - Wechsel in die Test-Sektion der [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
 - Öffne dort den Skill, z.B. mit dem Befehl: "Hey Alexa, öffne {Skill Invocation Name}"
 - Der {Skill Invocation Name} muss durch den im Schritt 4 vergebenen Namen ersetzt werden


