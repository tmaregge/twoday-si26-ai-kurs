# Oppgaver

## Introduksjon

Målet med kurset er å lage en RAG-løsning med et enkelt grensesnitt hvor man kan stille spørsmål om innholdet i dokumenter.

Vi bygger komponentene hver for seg før vi kobler dem sammen. Vi starter med å lage et veldig enkelt system som vi forbedrer iterativt når alt er på plass.

Flyten blir som følger

```
PDF
 ↓
Ingest # Hent tekst fra PDF
 ↓
Chunk # Splitt tekst i mindre bolker
 ↓
Index # Last opp chunks til søkeindeksen
 ↓
Search # Søk i chunks
 ↓
Context # Formater resultatene som LLM-kontekst
 ↓
LLM # Mat inn context og spørsmål i LLM
 ↓
Answer
```

## Prosjektstruktur

De viktigste filene i projektet er følgende:

| File            | Beskrivelse                                                 | Notat                        |
| --------------- | ----------------------------------------------------------- | ---------------------------- |
| `rag.py`        | Byggeklossene i RAG-systemet vårt                           |                              |
| `explore.ipynb` | Jupyter notebook for å jobbe iterativt                      |                              |
| `main.py`       | Kan brukes for å koble sammen komponenter                   | `uv run main.py`             |
| `ui.py`         | Grensesnitt i `streamlit`                                   | `uv run streamlit run ui.py` |
| `clients.py`    | Inneholder klienter for å koble seg mot de ulike tjenestene |

Oppgavene utføres ved å implementere funksjoner i `rag.py` som så skal kobles sammen i `ui.py` til slutt.

`explore.ipynb` kan brukes for å utvikle funksjonene iterativt før man eventuelt limer dem inn i `rag.py`. Enkelte handlinger, som å opprette indeks og laste opp dokumenter er også enklere å utføre i en notebook enn via vanlige kildefiler (etter min mening).

## Oppgaver

### Oppgave 0: Koble opp tjenestene

Vi bruker API-nøkler for å koble oss til tjenestene. Dere får tilsendt en fil med miljøvariabler.

1. Kopier .env-fil til roten av prosjektet
2. Åpne filen og endre AZURE_SEARCH_INDEX_NAME til "idx-[ditt_navn]"
3. Kjør `uv run test_connection.py` for å sjekke at ting funker

### Oppgave 1: Hent ut tekst fra et dokument

Målet med denne oppgaven er å gjøre en PDF om til ren tekst, slik at vi kan bruke den i søk. Dere får tilsendt Twodays personalhåndbok.

Bruk biblioteket [pypdf](https://pypi.org/project/pypdf/) for å lese innholdet fra PDF-filen.

Implementer:

`ingest_pypdf()`

Test i notebook:

```
text = ingest_pypdf(...)
print(text[:1000])
```

#### Refleksjon

Hva slags metadata kan være nyttig å ta vare på?

### Oppgave 2: Chunk dokumentet

Store språkmodeller og søkeindekser fungerer dårlig på svært store dokumenter. Vi trenger en måte å splitte opp teksten. I tillegg ønsker vi å kunne hente ut kun de mest relevante delene av dokumentet når brukeren stiller et spørsmål.

Implementer:

`chunk(document)`

Målet er å produsere en liste med chunks. Hver chunk skal være en dictionary som inneholder selve teksten pluss tilhørende metadata (f.eks. filnavn)
For eksempel:

```json
{
    "document_id": "twoday-personalhandbok",
    "chunk_id": "twoday-personalhandbok_1",
    "content": "Personalhåndboken skal gi informasjon og veiledning til ansatte om de forhold som er sentrale i
ansettelsesforholdet. Håndboken skal sikre en felles plattform og praksis innen de områder som
beskrives."
}
```

Her er det veldig mange mulige måter å gjøre det på, men jeg anbefaler enkel/naiv chunking til å begynne med. For eksempel å splitte opp basert på tegn.

Test:

```python
chunks = chunk(document) # Document er det scannede PDF-dokumentet

print(len(chunks))
print(chunks[0])
```

#### Refleksjon

Er det noen flere felter som bør inkluderes?

# Oppgave 3: Opprett en søkeindeks

Teorioppgave! Med mindre du har gjort noe spennende i de tidligere oppgavene og må modifisere schema-et `;)`

Undersøk funksjonen `create_index`. Funksjonen oppretter en søkeindeks med følgende schema

```python
    fields = [
        SimpleField(name="chunk_id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
    ]
```

NB: Husk å kalle metoden med index-navnet ditt! For eksempel:

```
create_index("idx-torstein")
```

### Nyttige lenker

https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python#creating-an-index

https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python

### Refleksjon

Hvilke felter trenger vi?

Eksempel:

- id
- document_id
- content

Hva bør være nøkkelfeltet?

# Oppgave 4: Last opp chunkene

Last opp chunkene til Azure AI Search.

Implementer:

```python
upload_chunks(chunks, index_name)
```

Verifiser at dokumentene finnes i indeksen. Du kan sjekke via kode, eller spørre meg om å sjekke i Azure.

### Nyttige lenker

Her kan du finne metoden for å laste opp dokumenter:
https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python

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

# Oppgave 6: Generer svar

Implementer:

```python
generate_answer(question, context)
```

Funksjonen tar inn et spørsmål og tilhørende context (søkeresultater) og genererer et svar.

NB: Bruk `model="gpt-5.4-mini"`

Lag en prompt som inneholder:

- system prompt
- brukerens spørsmål
- chunkene som ble hentet fra søket (`context`)

Eksempel:

```python
answer = generate_answer(question, context)
```

### Nyttige lenker

https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/responses?tabs=python#generate-a-text-response

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
Prompt
    ↓
LLM
    ↓
Svar
```

Etter denne oppgaven har vi en komplett RAG-løsning!

# Bonusoppgaver

Nå som vi har det grunnleggende systemet på plass kan vi jobbe med å forbedre det. Hva du gjør er opp til deg. Under er noen eksempler på ting man kan gjøre.

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

# Bonus 2: Legg til vektorsøk

Bruk modellen `text-embedding-3-large` for å lage en vektor-embedding av chunk-innholdet. Modifiser indeksen til å ta i bruk dette feltet for vektorsøk/semantisk søk.

# Bonus 3: Forbedre chunking

Ta en titt på dokumentasjonen og implementer en ny chunking-metode
https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents

Man kan for eksempel eksperimentere med

- Ulike chunk sizes
- Overlap mellom chunks (f.eks. 25%)
- Semantisk chunking

### Refleksjon

Hvilke endringer gir størst effekt på kvaliteten?

Hvorfor?

# Bonus 4: Legg til kilder

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

# Bonus 5: Filopplasting

Modifiser grensesnittet til å la brukeren laste opp dokumenter, som så blir prosessert og indeksert og gjort tilgjengelig for søk. Legg til muligheten til å velge hvilke dokumenter det søkes i (dette krever at `filterable=True` for dokumentId-feltet i index schema).

# Bonus 6: Bruk Document Intelligence for tekstekstraksjon

Bytt ut `ingest_pypdf()` med [Document Intelligence](https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme?view=azure-python#extract-layout) for kraftigere tekstekstraksjon, spesielt nyttig for scannede dokumenter eller komplekse layouter.

Implementer:

`ingest_di()`

# Bonus 7: Blob storage for lagring av dokumenter

Koble opp systemet til blob storage, slik at dokumenter lastet opp havner der. Legg til en referanse til blob-en for et gitt dokument i schema i indeksen. Bruk blob storage som "knowledge source" i

Gjør så PDF-en til vises i grensesnittet når man får resultatene (`st.pdf`).
