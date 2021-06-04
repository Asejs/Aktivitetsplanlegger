# Aktivitetsplanlegger
Eksamensprosjekt DAT

## Project setup
```
1. Run the client-side Vue app in a terminal window

    Commands:
    cd aktivitetsplanlegger-cli
    npm run serve

    

2. Run the server-side Flask app in a different terminal window

    Commands:
    cd aktivitetsplanlegger-cors
    pip install -r requirements.txt
    python3 app.py
```


## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

```

## Liste over funksjonalitet
- Applikasjonen bruker Flask WebServer med SQLite som database (med eksempeldata).
Den er en "Single page application (SPA)" som kommuniserer med Flask serveren via AJAX kall.
- Databasen inneholder to tabeller i tillegg til users-databasen; activities og participation.

- "Homepage"-siden inneholder en banner og layout'en justeres etter vindusstørrelsen.

- "Utforsk aktiviteter"-siden justeres etter vindusstørrelsen der bildene til aktivitene blir endret. Her vises aktivitetsdataen.

- Først etter brukeren er logget inn, vises "Legg til ny aktivitet"-knappen.
Brukerens brukernavn, fornavn og etternavn lagres i sessionStorage.

- Hvis man ikke er registrert som bruker kan man registrere seg ved å trykke inn på "Logg inn", og videre på "Registrer ny bruker".
Nye brukere blir lagret i databasen.
- Dersom brukeren har lagt ut aktiviteter, er det mulig å slette dem hvis det er egne aktiviteter.
- Det lastes opp et "default-bilde" når en ny aktivitet blir lagt til.
- Det er mulig å filtrere/søke i aktivitetene etter tittel, brukernavn, sted og beskrivelsen.

- Når man registreres som ny bruker må passordet være lengre enn 6 tegn, ellers kommer det oppe en feilmelding. Alle feltene kreves å bli fylt ut.

- Vue-Router brukes og har flere routes:
    - Home, Activities, Login, Register, NotFound

