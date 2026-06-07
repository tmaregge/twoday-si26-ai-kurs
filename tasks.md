# Oppgaver

## Introduksjon

Målet med kurset er å lage en RAG-løsning med et enkelt grensesnitt hvor man kan stille spørsmål om innholdet i dokumenter.

Vi bygger komponentene hver for seg før hvis vi kobler dem sammen. Vi starter med å lage et veldig enkelt system som vi forbedrer iterativt når alt er på plass.

## Prosjektstruktur

De viktigste filene i projektet er følgende:

| File | Beskrivelse |Notat|
|------|-------------|-------|
| `rag.py` | Byggeklossene i RAG-systemet vårt |  |
| `explore.ipynb` | Jupyter notebook for å jobbe iterativt |  |
| `main.py` | Kan brukes for å koble sammen komponenter | `uv run main.py` |
| `ui.py` | Grensesnitt i `streamlit` | `uv run streamlit run ui.py` |
| `clients.py` | Inneholder klienter for å koble seg mot de ulike tjenestene|

Oppgavene utføres ved å implementere funksjoner i `rag.py` som så skal kobles sammen i `ui.py` til slutt.

`explore.ipynb` kan brukes for å utvikle funksjonene iterativt før man eventuelt limer dem inn i `rag.py`. Enkelte handlinger, som å opprette indeks og laste opp dokumenter er også enklere å utføre i en notebook enn via vanlige kildefiler (etter min mening).

## Oppgaver

---

### Oppgave 1: Hent ut tekst fra et dokument

Målet er å gjøre PDF-en om til ren tekst. Her kan du selv velge om du vil bruke [pypdf](https://pypi.org/project/pypdf/) eller [Document Intelligence](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python#extract-layout). Førstnevnte er en del enklere og raskere, men sistnevnte er kraftigere. 

Implementer:

`ingest_pypdf()`

eller

`ingest_di()`

Test i notebook:

```
text = ingest_pypdf(...)
print(text[:1000])
```

---

### Oppgave 2: Chunk dokumentet

Store språkmodeller og søkeindekser fungerer dårlig på svært store dokumenter. Vi trenger en måte å splitte opp teksten. I tillegg ønsker vi å kunne hente ut kun de mest relevante delene av dokumentet når brukeren stiller et spørsmål.
 
Implementer:

`chunk(document)`

Målet er å produsere en liste med chunks. Hver chunk skal være en dictionary som inneholder selve teksten pluss tilhørende metadata (f.eks. filnavn)
For eksempel:
```
{
    "document_id": "twoday-personalhandbok",
    "chunk_id": "twoday-personalhandbok_1",
    "page": 1,
    "content": "Personalhåndboken skal gi informasjon og veiledning til ansatte om de forhold som er sentrale i
ansettelsesforholdet. Håndboken skal sikre en felles plattform og praksis innen de områder som
beskrives."
}
```

Her er det veldig mange mulige måter å gjøre det på, men jeg anbefaler enkel/naiv chunking til å begynne med. For eksempel å splitte opp basert på tegn.

Test:

```python
chunks = chunk(document)

print(len(chunks))
print(chunks[0])
```

---

# Oppgave 3: Opprett en søkeindeks

Opprett en Azure AI Search-indeks.

Implementer:

```python
create_index(index_name)
```

Metoden må inneholde et schema som definerer hva slags innhold hvert dokument (chunk) som lastes opp til indeksen skal inneholde.

### Refleksjon

Hvilke felter trenger vi?

Eksempel:

- id
- document_id
- content

Hva bør være nøkkelfeltet?

---

# Oppgave 4: Indekser chunkene

Last opp chunkene til Azure AI Search.

Implementer:

```python
index_chunks(chunks, index_name)
```

Verifiser at dokumentene finnes i indeksen.

---

# Oppgave 5: Bygg søk

Implementer:

```python
search(search_text)
```

Test funksjonen:

```python
results = search("ferie")

for result in results:
    print(result)
```

Skriv ut de mest relevante chunkene.

---

# Oppgave 6: Generer svar med GPT

Implementer:

```python
chat(question, context)
```

Lag en prompt som inneholder:

- system prompt
- brukerens spørsmål
- chunkene som ble hentet fra søket (`context`)

Eksempel:

```python
answer = chat(question, context)
```

### Refleksjon

Hva skjer dersom:

- vi ikke sender med kontekst?
- vi sender med irrelevante chunks?
- vi sender med for mange chunks?

---

# Oppgave 7: Sett alt sammen

Implementer:

```python
ask(question)
```

Funksjonen skal:

1. Søke etter relevante chunks
2. Bygge kontekst
3. Kalle språkmodellen
4. Returnere svaret

Eksempel:

```python
ask("Hvor mange feriedager har jeg?")
```

Pipeline:

```text
Spørsmål
    ↓
Search
    ↓
Chunks
    ↓
Prompt
    ↓
GPT
    ↓
Svar
```

Dette er en komplett RAG-løsning.

---

# Bonus 1: Bygg et grensesnitt

Bruk Streamlit til å lage et enkelt chat-grensesnitt.

Start applikasjonen:

```bash
uv run streamlit run ui.py
```

Vis:

- spørsmål
- svar
- hvilke chunks som ble brukt

---

# Bonus 2: Forbedre kvaliteten

Eksperimenter med:

- ulike chunking-strategier
  - hei
- prompten
- metadata

### Refleksjon

Hvilke endringer gir størst effekt på kvaliteten?

Hvorfor?

---

# Bonus 3: Legg til kilder

Vis hvilke chunks eller sider som ble brukt til å generere svaret.

Eksempel:

```text
Svar:
Du har 25 feriedager.

Kilder:
- Side 14
- Side 15
```

NB: For å implementere dette må du kanskje modifisere schema og chunking, samt reindeksere dokumentene.

# Bonus 4: Filopplasting

Modifiser grensesnittet til å la brukeren laste opp dokumenter, som så blir prosessert og indeksert og gjort tilgjengelig for søk. Legg til muligheten til å velge hvilke dokumenter det søkes i (dette krever at `filterable=True` for dokumentId-feltet i index schema).