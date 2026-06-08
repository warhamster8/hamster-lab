# Configurare Gumroad per l'offerta libera

Questa guida spiega come trasformare Gumroad da "negozio a prezzo fisso" a strumento di
**sostegno volontario** (offerta libera, *pay what you want*), in modo che sia coerente con
il sito: nessuna vendita, nessun prezzo obbligatorio, nessun paywall.

L'idea: i template e i software restano **gratuiti e scaricabili direttamente dal sito**.
Gumroad serve **solo** come "cassetta delle offerte" — chi vuole, lascia un contributo libero.

---

## 1. Crea un prodotto "Support / Offerta libera"

1. Entra su [gumroad.com](https://gumroad.com) → **Products** → **New product**.
2. Tipo di prodotto: scegli **"Digital product"** (oppure **"Membership"** se in futuro vuoi
   contributi ricorrenti; per iniziare va benissimo il prodotto singolo).
3. Nome suggerito: **"Support Hamster Lab"** o **"Buy me a coffee ☕"**.
4. Descrizione suggerita (copiala e adatta):

   > Everything on Hamster Lab is free — templates and apps, no purchase required.
   > If something here saved you time, you can leave a voluntary contribution of any amount.
   > Thank you for keeping the lab running. 🐹

---

## 2. Attiva il prezzo libero ("Pay what you want")

Questo è il passaggio chiave per l'**offerta libera**:

1. Nella pagina del prodotto, vai alla sezione **Pricing**.
2. Attiva l'opzione **"Allow customers to pay what they want"** (a volte indicata come
   *"Let customers name a fair price"*).
3. Imposta il **prezzo minimo a 0** (`€0`) — così nessuno è obbligato a pagare.
   - Se Gumroad non accetta `0`, imposta il minimo più basso consentito (es. `€1`) e scrivilo
     chiaramente nella descrizione come "minimo tecnico, non obbligatorio".
4. (Opzionale) Imposta un **prezzo suggerito** (es. `€3`) come gentile indicazione, **non**
   come prezzo richiesto. Serve solo a dare un riferimento a chi non sa quanto lasciare.

> ⚠️ Importante: **non** impostare un prezzo fisso obbligatorio. Sarebbe di nuovo "vendita".

---

## 3. Niente file a pagamento dietro al contributo

Per restare coerente con "tutto gratis":

- **NON** mettere i template/software come *contenuto sbloccabile solo dopo il pagamento*.
  I file devono restare scaricabili gratis dal sito.
- Nel prodotto "Support" puoi:
  - non allegare alcun file (è un puro ringraziamento), **oppure**
  - allegare un piccolo "extra di ringraziamento" facoltativo (es. un PDF "grazie", uno
    sfondo, un template bonus) — purché ciò che è promesso sul sito resti gratuito comunque.

---

## 4. Disattiva la logica da e-commerce

Nelle impostazioni del prodotto e dell'account, rendi tutto coerente con l'offerta libera:

- **Call to action / pulsante**: se Gumroad lo permette, cambia il testo da "Buy this" /
  "I want this!" in qualcosa come **"Support"** o **"Leave a tip"**.
- **Receipt / email di conferma**: personalizza il messaggio con un ringraziamento, non con un
  tono da "acquisto effettuato".
- **Recensioni/Ratings**: puoi disattivarle — non si tratta di un prodotto da recensire.
- **Tasse/IVA**: per i contributi volontari valgono comunque le regole fiscali di Gumroad
  (Gumroad gestisce l'IVA come *merchant of record* nella UE). Verifica la tua situazione
  fiscale personale per le donazioni/contributi ricevuti.

---

## 5. Collega Gumroad al sito

Il sito è già predisposto. Devi solo sostituire il link segnaposto con il tuo link reale.

1. Copia l'URL del tuo prodotto Gumroad. Avrà una forma tipo:

   ```
   https://hamsterlab.gumroad.com/l/support
   ```

2. Apri `index.html` e cerca il commento:

   ```html
   <!-- Replace the href with your real Gumroad "pay what you want" link (see GUMROAD_SETUP.md) -->
   <a href="https://hamsterlab.gumroad.com/l/support" class="btn btn-primary gumroad-button" ...>
   ```

3. Sostituisci `https://hamsterlab.gumroad.com/l/support` con il **tuo** URL reale.

Il sito carica già lo script ufficiale di Gumroad:

```html
<script src="https://gumroad.com/js/gumroad.js" defer></script>
```

Grazie alle classi `gumroad-button` e `data-gumroad-overlay-checkout="true"` sul pulsante, il
contributo si apre in un **overlay** sopra il sito (l'utente non lascia la pagina). Se preferisci
che si apra in una nuova scheda, basta rimuovere la classe `gumroad-button` dal pulsante.

---

## 6. Checklist finale (coerenza con l'offerta libera)

- [ ] Il prodotto Gumroad ha **prezzo minimo 0** (o il minimo tecnico, dichiarato come tale).
- [ ] **Nessun** prezzo fisso obbligatorio da nessuna parte.
- [ ] I template e i software restano **scaricabili gratis** dal sito, senza paywall.
- [ ] Il testo parla di **contributo / supporto**, mai di "acquisto" o "prezzo".
- [ ] Il link nel sito punta al tuo prodotto Gumroad reale.
- [ ] Email di conferma personalizzata come ringraziamento.

---

## Alternative a Gumroad (se ti servono in futuro)

Tutte supportano l'offerta libera e sono pensate proprio per il sostegno volontario:

| Servizio        | Punti di forza                                              |
|-----------------|-------------------------------------------------------------|
| **Ko-fi**       | Nato per le donazioni, "buy me a coffee", 0% commissioni base |
| **Buy Me a Coffee** | Semplicissimo, orientato ai contributi una tantum/ricorrenti |
| **Liberapay**   | Open source, contributi ricorrenti, no profit               |
| **PayPal.me**   | Link diretto per donazioni, conosciuto da tutti             |
| **GitHub Sponsors** | Ottimo se il tuo pubblico è tecnico/dev                 |

Puoi anche affiancarne più di uno: ad esempio Gumroad per i contributi + un link PayPal.me
come alternativa rapida.
