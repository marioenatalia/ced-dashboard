# Vera Candles — sito e-commerce

Sito statico (HTML/CSS/JS, nessun framework, nessun build) per la vendita di
candele artigianali d’autore. Vive nella cartella `candele/` del repository e
non tocca la dashboard CED che sta sulla root.

Online su: `https://ced.focusdataconsulting.com/candele/`
(la pubblicazione avviene con GitHub Pages, come per il resto del repo).

## Pagine

| File | Cosa contiene |
|---|---|
| `index.html` | Home: hero, manifesto, selezione, «che cosa stai pagando», rituale, su misura, newsletter |
| `shop.html` | Catalogo con filtri per collezione e ordinamento |
| `prodotto.html?id=…` | Scheda prodotto (note olfattive, lavorazione, scheda tecnica, accensione, spedizioni) |
| `atelier.html` | Storia, processo produttivo, le regole dell’atelier |
| `su-misura.html` | Edizioni private (matrimoni, boutique, regali) + modulo richiesta |
| `contatti.html` | Modulo contatti, dati atelier, FAQ |
| `ordine.html` | Riepilogo carrello e invio ordine via WhatsApp o email |

Header, footer e carrello laterale sono generati da `assets/js/app.js`: si
modificano in un punto solo e cambiano su tutte le pagine.

## Le tre cose da personalizzare subito

Tutto sta in **`assets/js/products.js`**, in cima al file:

```js
const VERA_CONFIG = {
  whatsapp: '393000000000',       // numero reale, solo cifre, con prefisso (39…)
  email: 'ordini@veracandles.it', // email dove arrivano gli ordini
  telefono: '+39 300 000 0000',
  instagram: 'https://instagram.com/veracandles',
  citta: 'Atelier · Milano',
  indirizzo: 'Via della Cera 12, 20121 Milano — su appuntamento',
  spedizioneGratisDa: 200,        // soglia spedizione offerta
  costoSpedizione: 12,
  costoConfezioneRegalo: 15,
};
```

1. **Numero WhatsApp** — finché resta `393000000000` gli ordini non arrivano a nessuno.
2. **Email ordini** — usata dal pulsante «Invia via email» e nel footer.
3. **P.IVA e dati fiscali** — nel footer c’è il segnaposto «P.IVA da inserire»
   (`assets/js/app.js`, funzione `buildFooter`).

## Come funziona l’ordine

Non c’è un pagamento online: il carrello vive nel browser della cliente
(`localStorage`) e alla fine il pulsante compone un messaggio già pronto —
prodotti, quantità, totale, dati di consegna, dedica — e apre **WhatsApp** o il
**programma di posta**. L’ordine si conferma rispondendo con disponibilità e
dati di pagamento (bonifico o link carta).

Vantaggi: zero commissioni, nessun server, si può partire subito. Se in futuro
servisse il pagamento con carta direttamente sul sito, il punto da toccare è la
funzione `initOrder()` in `assets/js/app.js`.

## Aggiungere o modificare un prodotto

Sempre in `assets/js/products.js`, dentro `VERA_PRODUCTS`. Copiare un blocco
esistente e cambiarne i campi:

```js
{
  id: 'nome-file',            // usato nell’URL e per l’immagine: assets/img/nome-file.svg
  nome: 'Nome del pezzo',
  collezione: 'Signature',    // 'Opere Uniche' | 'Signature' | 'Rituali'
  prezzo: 165,
  prezzoPieno: 195,           // facoltativo: mostra il prezzo barrato
  img: 'nome-file',
  claim: 'Una riga che descrive il pezzo.',
  edizione: 'Edizione di 18 · numerata',
  stato: 'disponibile',       // 'disponibile' | 'ultimi' | 'esaurito'
  novita: true,               // facoltativo → badge «Novità»
  bestseller: true,           // facoltativo → badge «Più amata»
  note: { testa: '…', cuore: '…', fondo: '…' },
  tech: { Cera: '…', Stoppino: '…', Durata: '…', Formato: '…', Finitura: '…' },
  storia: 'Il paragrafo sulla lavorazione, quello che giustifica il prezzo.',
}
```

Le collezioni disponibili sono elencate in `VERA_COLLECTIONS` (se se ne aggiunge
una, va aggiunto anche un pulsante filtro in `shop.html`).

## Le immagini

Le immagini attuali sono **illustrazioni vettoriali** generate da noi
(`assets/img/*.svg`): servono per andare online subito con un aspetto curato,
in attesa delle foto vere.

Per sostituirle con le fotografie:

1. tagliare le foto prodotto in **formato 4:5** (es. 1200 × 1500 px), le
   editoriali in 4:5 e l’hero in 16:10 orizzontale;
2. salvarle in `assets/img/` con lo stesso nome del file SVG che sostituiscono
   (`luna-piena.jpg`, `hero.jpg`, …);
3. cambiare l’estensione nei due punti dove viene costruita:
   - prodotti: funzione `imgOf()` in `assets/js/app.js` (`.svg` → `.jpg`);
   - editoriali/hero: i tag `<img>` nelle pagine HTML.

Le illustrazioni si possono anche rigenerare (serve solo Python 3):

```bash
cd candele/scripts
python3 genera-prodotti.py   # le 10 immagini prodotto
python3 genera-scene.py      # hero, atelier, rituale, materia, su misura
```

Colori, forme e nomi dei pezzi stanno nella lista `PIECES` in
`genera-prodotti.py`.

## Note tecniche

- Nessuna dipendenza da installare: si apre `index.html` e funziona. Per
  provarlo in locale con i percorsi giusti: `python3 -m http.server` dentro `candele/`.
- I font (Cormorant Garamond + Jost) arrivano da Google Fonts; se il caricamento
  fallisce il sito ripiega su Garamond/Century Gothic di sistema senza rompersi.
- Animazioni disattivate in automatico per chi ha «riduci movimento» attivo.
- Il carrello è salvato con la chiave `vera_cart_v1` in `localStorage`.
- Prima di andare online: sostituire i testi segnaposto (indirizzo, P.IVA,
  recensione firmata «Giulia M.») con quelli reali.
