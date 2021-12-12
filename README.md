# Aktivitetsplanlegger
DAT310 Eksamensprosjekt

## How to run

### 1. Run the client-side Vue app in a terminal window


```
npm install
cd aktivitetsplanlegger-cli
npm run serve
```



### 2. Run the server-side Flask app in a different terminal window

```
pip install -r requirements.txt
python3 app.py
```
If the database does not exist, run
```
python3 setup_db.py
```



* aktivitetsplanlegger-cors:  Flask API that can be accessed using Cross Origin Requests.
* aktivitetsplanlegger-cli:   VueCLI application that accesses the Flask API.



## Liste over funksjonalitet
- Applikasjonen bruker Vue-CLI sammen med Flask API.
Den er en "Single page application (SPA)" som kommuniserer med Flask serveren via AJAX kall.

- Databasen inneholder to tabeller i tillegg til users-databasen; activities og participation.

- "Homepage"-siden inneholder en banner og layout'en justeres etter vindusstørrelsen.

- "Utforsk aktiviteter"-siden justeres etter vindusstørrelsen der bildene til aktivitene blir endret. Her vises aktivitetsdataen.

- Først etter brukeren er logget inn, vises "Legg til ny aktivitet"-knappen.
Brukerens brukernavn, fornavn og etternavn lagres i sessionStorage, for å lett få tilgang på informasjon om pålogget bruker.

- Hvis man ikke er registrert som bruker kan man registrere seg ved å trykke inn på "Logg inn", og videre på "Registrer ny bruker".
Nye brukere blir lagret i databasen.

- Dersom brukeren har lagt ut aktiviteter, er det mulig å slette eller redigere dem hvis det er egne aktiviteter.
- Brukeren kan laste opp et bilde med aktiviteten.
- Det er mulig å filtrere/søke i aktivitetene etter tittel, brukernavn, sted og beskrivelsen.

- Når man registreres som ny bruker må passordet være lengre enn 6 tegn, ellers kommer det oppe en feilmelding. Det kreves at alle feltene i registreringen må fylles ut.

- Vue-Router har flere routes:
    * Home, Activities, Login, Register, NotFound


## For test av login

Kan logge inn med:
- **Brukernavn**: aase
- **Passord**: passord

