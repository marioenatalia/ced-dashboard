/* ============================================================
   VERA CANDLES — logica del sito
   Header/footer/carrello sono iniettati da qui per restare
   identici su tutte le pagine. Il catalogo arriva da products.js.
   ============================================================ */
(function () {
  'use strict';

  const CFG = window.VERA_CONFIG || VERA_CONFIG;
  const PRODUCTS = window.VERA_PRODUCTS || VERA_PRODUCTS;
  const CART_KEY = 'vera_cart_v1';

  /* ----------------------------------------------------- utility -- */
  const $  = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

  const money = (n) =>
    CFG.valuta + ' ' + Number(n).toLocaleString('it-IT', { minimumFractionDigits: 0 });

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  const imgOf = (p) => 'assets/img/' + p.img + '.svg';
  const byId  = (id) => PRODUCTS.find((p) => p.id === id);
  const stato = (p) => VERA_STATI[p.stato] || VERA_STATI.disponibile;

  /* -------------------------------------------------- carrello -- */
  function cartRead() {
    try {
      const raw = JSON.parse(localStorage.getItem(CART_KEY) || '[]');
      return raw.filter((r) => byId(r.id)).map((r) => ({ id: r.id, qty: Math.max(1, r.qty | 0) }));
    } catch (e) { return []; }
  }
  function cartWrite(items) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(items)); } catch (e) {}
    renderCart();
    document.dispatchEvent(new CustomEvent('vera:cart'));
  }
  function cartAdd(id, qty) {
    const items = cartRead();
    const row = items.find((r) => r.id === id);
    if (row) row.qty += (qty || 1); else items.push({ id: id, qty: qty || 1 });
    cartWrite(items);
    toast('Aggiunto al carrello');
    openDrawer();
  }
  function cartSet(id, qty) {
    let items = cartRead();
    if (qty <= 0) items = items.filter((r) => r.id !== id);
    else { const row = items.find((r) => r.id === id); if (row) row.qty = qty; }
    cartWrite(items);
  }
  const cartCount = () => cartRead().reduce((s, r) => s + r.qty, 0);
  const cartLines = () => cartRead().map((r) => ({ p: byId(r.id), qty: r.qty }));
  const cartSubtotal = () => cartLines().reduce((s, l) => s + l.p.prezzo * l.qty, 0);
  function shippingFor(sub) {
    if (sub <= 0) return 0;
    return sub >= CFG.spedizioneGratisDa ? 0 : CFG.costoSpedizione;
  }

  window.VeraCart = {
    add: cartAdd, set: cartSet, read: cartRead, lines: cartLines,
    subtotal: cartSubtotal, shipping: shippingFor, count: cartCount, money: money,
  };

  /* ------------------------------------------------------ toast -- */
  let toastTimer;
  function toast(msg) {
    let el = $('.toast');
    if (!el) { el = document.createElement('div'); el.className = 'toast'; document.body.appendChild(el); }
    el.textContent = msg;
    requestAnimationFrame(() => el.classList.add('is-on'));
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => el.classList.remove('is-on'), 2600);
  }

  /* --------------------------------------------- header e footer -- */
  const NAV = [
    { href: 'shop.html',      label: 'Collezione' },
    { href: 'atelier.html',   label: 'Atelier' },
    { href: 'su-misura.html', label: 'Su misura' },
    { href: 'contatti.html',  label: 'Contatti' },
  ];

  const LOGO = (href) =>
    '<a class="logo" href="' + href + '" aria-label="' + esc(CFG.brand) + ' — home">' +
      '<span class="logo__mark">VERA</span>' +
      '<span class="logo__sub">Candles · Atelier</span>' +
    '</a>';

  function buildHeader() {
    const over = document.body.dataset.header === 'over';
    const here = (location.pathname.split('/').pop() || 'index.html');
    const links = NAV.map((n) =>
      '<a href="' + n.href + '"' + (n.href === here ? ' aria-current="page"' : '') + '>' + n.label + '</a>'
    ).join('');

    const header = document.createElement('header');
    header.className = 'header' + (over ? ' is-over' : ' is-solid');
    header.innerHTML =
      '<div class="header__inner">' +
        LOGO('index.html') +
        '<nav class="nav">' + links + '</nav>' +
        '<div class="header__actions">' +
          '<button class="icon-btn js-cart" aria-label="Apri il carrello">' +
            '<svg viewBox="0 0 24 24"><path d="M6 8h12l1 12H5L6 8Z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>' +
            '<span class="cart-count" data-cart-count>0</span>' +
          '</button>' +
          '<button class="icon-btn burger js-menu" aria-label="Apri il menu"><span></span></button>' +
        '</div>' +
      '</div>';
    document.body.prepend(header);

    const menu = document.createElement('div');
    menu.className = 'mobile-menu';
    menu.innerHTML =
      '<button class="mobile-menu__close" aria-label="Chiudi il menu">&times;</button>' +
      NAV.map((n) => '<a href="' + n.href + '">' + n.label + '</a>').join('');
    document.body.appendChild(menu);

    $('.js-menu').addEventListener('click', () => menu.classList.add('is-open'));
    $('.mobile-menu__close').addEventListener('click', () => menu.classList.remove('is-open'));

    const onScroll = () => {
      if (!over) return;
      header.classList.toggle('is-solid', window.scrollY > 60);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  function buildFooter() {
    const f = document.createElement('footer');
    f.className = 'footer';
    f.innerHTML =
      '<div class="wrap">' +
        '<div class="footer__grid">' +
          '<div>' + LOGO('index.html') +
            '<p style="max-width:34ch;font-size:.9rem;margin:0">Candele d’autore colate a mano in atelier. Piccole edizioni, materiali nobili, nessuna produzione in serie.</p>' +
          '</div>' +
          '<div><h4>Collezione</h4><ul>' +
            VERA_COLLECTIONS.map((c) => '<li><a href="shop.html?c=' + encodeURIComponent(c) + '">' + c + '</a></li>').join('') +
            '<li><a href="shop.html">Tutte le candele</a></li>' +
          '</ul></div>' +
          '<div><h4>Atelier</h4><ul>' +
            '<li><a href="atelier.html">La nostra storia</a></li>' +
            '<li><a href="su-misura.html">Progetti su misura</a></li>' +
            '<li><a href="contatti.html">Contatti e visite</a></li>' +
            '<li><a href="contatti.html#faq">Domande frequenti</a></li>' +
          '</ul></div>' +
          '<div><h4>Scrivici</h4><ul>' +
            '<li><a href="https://wa.me/' + CFG.whatsapp + '" target="_blank" rel="noopener">WhatsApp</a></li>' +
            '<li><a href="mailto:' + CFG.email + '">' + CFG.email + '</a></li>' +
            '<li><a href="' + CFG.instagram + '" target="_blank" rel="noopener">Instagram</a></li>' +
            '<li>' + esc(CFG.citta) + '</li>' +
          '</ul></div>' +
        '</div>' +
        '<div class="footer__bottom">' +
          '<span>© ' + new Date().getFullYear() + ' ' + esc(CFG.brand) + ' — P.IVA da inserire</span>' +
          '<span>Spedizione assicurata in tutta Italia · Confezione regalo su richiesta</span>' +
        '</div>' +
      '</div>';
    document.body.appendChild(f);
  }

  /* ------------------------------------------------ cart drawer -- */
  function buildDrawer() {
    const ov = document.createElement('div');
    ov.className = 'overlay js-overlay';
    const d = document.createElement('aside');
    d.className = 'drawer';
    d.setAttribute('aria-label', 'Carrello');
    d.innerHTML =
      '<div class="drawer__head">' +
        '<span class="drawer__title">Il tuo carrello</span>' +
        '<button class="drawer__close" aria-label="Chiudi il carrello">&times;</button>' +
      '</div>' +
      '<div class="drawer__body" data-cart-body></div>' +
      '<div class="drawer__foot" data-cart-foot></div>';
    document.body.append(ov, d);

    ov.addEventListener('click', closeDrawer);
    $('.drawer__close', d).addEventListener('click', closeDrawer);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDrawer(); });
    $$('.js-cart').forEach((b) => b.addEventListener('click', openDrawer));
  }
  function openDrawer() { $('.drawer').classList.add('is-open'); $('.js-overlay').classList.add('is-on'); }
  function closeDrawer() {
    const d = $('.drawer'); if (d) d.classList.remove('is-open');
    const o = $('.js-overlay'); if (o) o.classList.remove('is-on');
    const m = $('.mobile-menu'); if (m) m.classList.remove('is-open');
  }

  function renderCart() {
    const n = cartCount();
    $$('[data-cart-count]').forEach((el) => {
      el.textContent = n;
      el.classList.toggle('is-on', n > 0);
    });

    const body = $('[data-cart-body]');
    const foot = $('[data-cart-foot]');
    if (!body || !foot) return;

    const lines = cartLines();
    if (!lines.length) {
      body.innerHTML =
        '<div class="drawer__empty"><p>Il carrello è vuoto.</p>' +
        '<a class="link-under" href="shop.html">Scopri la collezione</a></div>';
      foot.innerHTML = '';
      return;
    }

    body.innerHTML = lines.map((l) =>
      '<div class="line-item">' +
        '<a href="prodotto.html?id=' + l.p.id + '"><img src="' + imgOf(l.p) + '" alt="' + esc(l.p.nome) + '"></a>' +
        '<div>' +
          '<a href="prodotto.html?id=' + l.p.id + '"><span class="line-item__name">' + esc(l.p.nome) + '</span></a>' +
          '<div class="line-item__meta">' + esc(l.p.collezione) + '</div>' +
          '<div class="line-item__row">' +
            '<span class="qty">' +
              '<button data-dec="' + l.p.id + '" aria-label="Riduci">−</button>' +
              '<span>' + l.qty + '</span>' +
              '<button data-inc="' + l.p.id + '" aria-label="Aumenta">+</button>' +
            '</span>' +
            '<span class="line-item__price">' + money(l.p.prezzo * l.qty) + '</span>' +
          '</div>' +
          '<div style="margin-top:8px"><button class="remove" data-del="' + l.p.id + '">Rimuovi</button></div>' +
        '</div>' +
      '</div>'
    ).join('');

    const sub = cartSubtotal();
    const ship = shippingFor(sub);
    const manca = Math.max(0, CFG.spedizioneGratisDa - sub);
    foot.innerHTML =
      '<div class="totals">' +
        '<div class="totals__row"><span>Subtotale</span><span>' + money(sub) + '</span></div>' +
        '<div class="totals__row"><span>Spedizione assicurata</span><span>' + (ship ? money(ship) : 'Offerta') + '</span></div>' +
        (manca > 0 ? '<div class="totals__row"><small>Mancano ' + money(manca) + ' alla spedizione offerta</small></div>' : '') +
        '<div class="totals__row totals__row--big"><span>Totale</span><span>' + money(sub + ship) + '</span></div>' +
      '</div>' +
      '<a class="btn btn--block" href="ordine.html">Completa l’ordine</a>' +
      '<p style="text-align:center;margin:14px 0 0"><a class="link-under" href="shop.html">Continua a scegliere</a></p>';

    $$('[data-inc]', foot.parentElement).forEach((b) =>
      b.addEventListener('click', () => {
        const id = b.dataset.inc;
        cartSet(id, (cartRead().find((r) => r.id === id) || {}).qty + 1);
      }));
    $$('[data-dec]', foot.parentElement).forEach((b) =>
      b.addEventListener('click', () => {
        const id = b.dataset.dec;
        cartSet(id, (cartRead().find((r) => r.id === id) || {}).qty - 1);
      }));
    $$('[data-del]', foot.parentElement).forEach((b) =>
      b.addEventListener('click', () => cartSet(b.dataset.del, 0)));
  }

  /* ------------------------------------------------- card e liste -- */
  function cardHTML(p) {
    const st = stato(p);
    const badge = p.novita ? 'Novità' : (p.bestseller ? 'Più amata' : st.label);
    const badgeDark = !p.novita && !p.bestseller && p.stato === 'esaurito';
    return '' +
      '<article class="card reveal' + (st.vendibile ? '' : ' card--sold') + '">' +
        '<a href="prodotto.html?id=' + p.id + '" class="card__media">' +
          '<img src="' + imgOf(p) + '" alt="' + esc(p.nome) + ' — candela artigianale ' + esc(p.collezione) + '" loading="lazy">' +
          (badge ? '<span class="card__badge' + (badgeDark ? ' card__badge--dark' : '') + '">' + badge + '</span>' : '') +
          (st.vendibile
            ? '<div class="card__quick"><button class="btn btn--light btn--block" data-add="' + p.id + '">Aggiungi</button></div>'
            : '') +
        '</a>' +
        '<a href="prodotto.html?id=' + p.id + '" class="card__body">' +
          '<span class="card__coll">' + esc(p.collezione) + '</span>' +
          '<span class="card__name">' + esc(p.nome) + '</span>' +
          '<span class="card__note">' + esc(p.note.cuore) + '</span>' +
          '<span class="card__price">' +
            (p.prezzoPieno ? '<s>' + money(p.prezzoPieno) + '</s>' : '') + money(p.prezzo) +
          '</span>' +
        '</a>' +
      '</article>';
  }

  function bindAdd(root) {
    $$('[data-add]', root).forEach((b) =>
      b.addEventListener('click', (e) => {
        e.preventDefault(); e.stopPropagation();
        cartAdd(b.dataset.add, 1);
      }));
  }

  function renderGrid(el, list) {
    el.innerHTML = list.map(cardHTML).join('');
    bindAdd(el);
    observeReveals(el);
  }

  /* ------------------------------------------------------ reveal -- */
  let io;
  function observeReveals(root) {
    const els = $$('.reveal:not(.is-in)', root || document);
    if (!('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-in')); return; }
    if (!io) {
      io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: .12 });
    }
    els.forEach((e) => io.observe(e));
  }

  /* ------------------------------------------------- pagina home -- */
  function initHome() {
    const grid = $('[data-home-grid]');
    if (grid) {
      const picks = PRODUCTS.filter((p) => p.stato !== 'esaurito').slice(0, 4);
      renderGrid(grid, picks);
    }
  }

  /* ------------------------------------------------- pagina shop -- */
  function initShop() {
    const grid = $('[data-shop-grid]');
    if (!grid) return;
    const chips = $$('.chip');
    const sort = $('[data-sort]');
    const count = $('[data-count]');

    const params = new URLSearchParams(location.search);
    let filtro = params.get('c') || 'Tutte';
    if (!VERA_COLLECTIONS.includes(filtro)) filtro = 'Tutte';

    function apply() {
      let list = PRODUCTS.filter((p) => filtro === 'Tutte' || p.collezione === filtro);
      const s = sort ? sort.value : 'curata';
      if (s === 'prezzo-asc') list = list.slice().sort((a, b) => a.prezzo - b.prezzo);
      if (s === 'prezzo-desc') list = list.slice().sort((a, b) => b.prezzo - a.prezzo);
      if (s === 'nome') list = list.slice().sort((a, b) => a.nome.localeCompare(b.nome, 'it'));
      chips.forEach((c) => c.classList.toggle('is-on', c.dataset.filter === filtro));
      if (count) count.textContent = list.length + (list.length === 1 ? ' pezzo' : ' pezzi');
      renderGrid(grid, list);
    }

    chips.forEach((c) => c.addEventListener('click', () => {
      filtro = c.dataset.filter;
      const u = new URL(location.href);
      if (filtro === 'Tutte') u.searchParams.delete('c'); else u.searchParams.set('c', filtro);
      history.replaceState({}, '', u);
      apply();
    }));
    if (sort) sort.addEventListener('change', apply);
    apply();
  }

  /* --------------------------------------------- scheda prodotto -- */
  function initPDP() {
    const root = $('[data-pdp]');
    if (!root) return;
    const id = new URLSearchParams(location.search).get('id');
    const p = byId(id) || PRODUCTS[0];
    const st = stato(p);
    document.title = p.nome + ' · ' + CFG.brand;

    const techRows = Object.keys(p.tech)
      .map((k) => '<dt>' + esc(k) + '</dt><dd>' + esc(p.tech[k]) + '</dd>').join('');

    root.innerHTML =
      '<div class="wrap">' +
        '<nav class="breadcrumb"><a href="index.html">Home</a> · <a href="shop.html">Collezione</a> · ' +
          '<a href="shop.html?c=' + encodeURIComponent(p.collezione) + '">' + esc(p.collezione) + '</a> · ' + esc(p.nome) +
        '</nav>' +
        '<div class="pdp__grid">' +
          '<div class="pdp__media reveal">' +
            '<img src="' + imgOf(p) + '" alt="' + esc(p.nome) + '" data-main>' +
          '</div>' +
          '<div class="pdp__info reveal delay-1">' +
            '<p class="eyebrow">' + esc(p.collezione) + (st.label ? ' · ' + st.label : '') + '</p>' +
            '<h1 style="font-size:clamp(2.4rem,5vw,3.6rem)">' + esc(p.nome) + '</h1>' +
            '<p class="pdp__price">' + (p.prezzoPieno ? '<s style="color:var(--ink-3);margin-right:10px">' + money(p.prezzoPieno) + '</s>' : '') + money(p.prezzo) + '</p>' +
            '<hr class="rule">' +
            '<p class="lede">' + esc(p.claim) + '</p>' +
            '<p style="font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--gold)">' + esc(p.edizione) + '</p>' +
            '<div class="pdp__buy">' +
              (st.vendibile
                ? '<span class="qty"><button data-q="-1" aria-label="Riduci">−</button><span data-qty>1</span><button data-q="1" aria-label="Aumenta">+</button></span>' +
                  '<button class="btn" data-buy>Aggiungi al carrello · ' + money(p.prezzo) + '</button>'
                : '<button class="btn" disabled>Esaurito</button>' +
                  '<a class="btn btn--ghost" href="https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent('Vorrei essere avvisata quando ' + p.nome + ' torna disponibile.') + '" target="_blank" rel="noopener">Avvisami</a>') +
            '</div>' +
            '<div class="notes">' +
              '<div class="note-row"><span>Testa</span><p>' + esc(p.note.testa) + '</p></div>' +
              '<div class="note-row"><span>Cuore</span><p>' + esc(p.note.cuore) + '</p></div>' +
              '<div class="note-row"><span>Fondo</span><p>' + esc(p.note.fondo) + '</p></div>' +
            '</div>' +
            '<div class="accordion" style="margin-top:34px">' +
              accItem('La lavorazione', '<p>' + esc(p.storia) + '</p>', true) +
              accItem('Scheda tecnica', '<dl>' + techRows + '</dl>') +
              accItem('Come si accende', '<p>Alla prima accensione lascia sciogliere la cera fino al bordo: servono circa due ore e serve a evitare il cratere centrale. Accorcia lo stoppino a 5 mm prima di ogni accensione e non superare le quattro ore per volta. Non lasciare mai una fiamma incustodita.</p>') +
              accItem('Spedizione e reso', '<p>Spedizione assicurata in Italia in 2–4 giorni lavorativi, offerta sopra ' + money(CFG.spedizioneGratisDa) + '. Ogni pezzo viaggia in scatola rigida con imbottitura in carta di cotone. Reso entro 14 giorni sui pezzi integri e non accesi; i progetti su misura non sono rendibili.</p>') +
            '</div>' +
          '</div>' +
        '</div>' +
      '</div>';

    // quantita' + acquisto
    let q = 1;
    const qEl = $('[data-qty]', root);
    $$('[data-q]', root).forEach((b) => b.addEventListener('click', () => {
      q = Math.max(1, q + Number(b.dataset.q));
      qEl.textContent = q;
    }));
    const buy = $('[data-buy]', root);
    if (buy) buy.addEventListener('click', () => cartAdd(p.id, q));

    bindAccordions(root);

    // correlati
    const rel = $('[data-related]');
    if (rel) {
      const list = PRODUCTS.filter((x) => x.id !== p.id && x.collezione === p.collezione)
        .concat(PRODUCTS.filter((x) => x.id !== p.id && x.collezione !== p.collezione))
        .slice(0, 4);
      renderGrid(rel, list);
    }
    observeReveals(root);
  }

  /* --------------------------------------------------- accordion -- */
  function bindAccordions(root) {
    $$('.accordion__btn', root || document).forEach((b) => {
      if (b.dataset.bound) return;
      b.dataset.bound = '1';
      b.addEventListener('click', () => {
        const item = b.parentElement;
        const open = item.classList.toggle('is-open');
        const panel = $('.accordion__panel', item);
        panel.style.maxHeight = open ? panel.scrollHeight + 'px' : 0;
      });
    });
    $$('.accordion__item.is-open .accordion__panel', root || document).forEach((pn) => {
      pn.style.maxHeight = pn.scrollHeight + 'px';
    });
  }

  /* ------------------------------------- segnaposto dai contatti -- */
  function fillContacts() {
    $$('[data-wa]').forEach((a) => {
      if (!a.getAttribute('href')) a.setAttribute('href', 'https://wa.me/' + CFG.whatsapp);
    });
    $$('[data-email]').forEach((a) => {
      a.setAttribute('href', 'mailto:' + CFG.email);
      if (!a.textContent.trim()) a.textContent = CFG.email;
    });
    $$('[data-telefono]').forEach((el) => { if (!el.textContent.trim()) el.textContent = CFG.telefono; });
    $$('[data-indirizzo]').forEach((el) => { if (!el.textContent.trim()) el.textContent = CFG.indirizzo; });
  }

  function accItem(titolo, html, open) {
    return '<div class="accordion__item' + (open ? ' is-open' : '') + '">' +
      '<button class="accordion__btn">' + titolo + '<i>+</i></button>' +
      '<div class="accordion__panel"><div>' + html + '</div></div>' +
    '</div>';
  }

  /* ---------------------------------------------------- ordine -- */
  function initOrder() {
    const root = $('[data-order]');
    if (!root) return;
    const form = $('#order-form');
    const riepilogo = $('[data-riepilogo]');

    function draw() {
      const lines = cartLines();
      if (!lines.length) {
        riepilogo.innerHTML = '<p class="drawer__empty">Il carrello è vuoto.<br><a class="link-under" href="shop.html" style="margin-top:14px">Scopri la collezione</a></p>';
        $$('button[type=submit], .js-wa', form).forEach((b) => b.setAttribute('disabled', 'disabled'));
        return;
      }
      const gift = $('#gift') && $('#gift').checked;
      const sub = cartSubtotal();
      const ship = shippingFor(sub);
      const giftCost = gift ? CFG.costoConfezioneRegalo : 0;
      riepilogo.innerHTML =
        lines.map((l) =>
          '<div class="line-item" style="grid-template-columns:64px 1fr">' +
            '<img src="' + imgOf(l.p) + '" alt="' + esc(l.p.nome) + '">' +
            '<div><span class="line-item__name">' + esc(l.p.nome) + '</span>' +
            '<div class="line-item__meta">' + esc(l.p.collezione) + ' · quantità ' + l.qty + '</div>' +
            '<div class="line-item__row"><span></span><span class="line-item__price">' + money(l.p.prezzo * l.qty) + '</span></div></div>' +
          '</div>').join('') +
        '<div class="totals" style="margin-top:22px">' +
          '<div class="totals__row"><span>Subtotale</span><span>' + money(sub) + '</span></div>' +
          (giftCost ? '<div class="totals__row"><span>Confezione regalo</span><span>' + money(giftCost) + '</span></div>' : '') +
          '<div class="totals__row"><span>Spedizione assicurata</span><span>' + (ship ? money(ship) : 'Offerta') + '</span></div>' +
          '<div class="totals__row totals__row--big"><span>Totale</span><span>' + money(sub + ship + giftCost) + '</span></div>' +
        '</div>';
      $$('button[type=submit], .js-wa', form).forEach((b) => b.removeAttribute('disabled'));
    }

    function messaggio() {
      const d = Object.fromEntries(new FormData(form).entries());
      const lines = cartLines();
      const sub = cartSubtotal();
      const ship = shippingFor(sub);
      const giftCost = ($('#gift') && $('#gift').checked) ? CFG.costoConfezioneRegalo : 0;
      const L = [];
      L.push('Nuovo ordine · ' + CFG.brand);
      L.push('');
      lines.forEach((l) => L.push('• ' + l.p.nome + ' (' + l.p.collezione + ') × ' + l.qty + ' — ' + money(l.p.prezzo * l.qty)));
      L.push('');
      L.push('Subtotale: ' + money(sub));
      if (giftCost) L.push('Confezione regalo: ' + money(giftCost));
      L.push('Spedizione: ' + (ship ? money(ship) : 'offerta'));
      L.push('TOTALE: ' + money(sub + ship + giftCost));
      L.push('');
      L.push('Cliente: ' + (d.nome || '') + ' ' + (d.cognome || ''));
      L.push('Email: ' + (d.email || ''));
      L.push('Telefono: ' + (d.telefono || ''));
      L.push('Consegna: ' + (d.indirizzo || '') + ', ' + (d.cap || '') + ' ' + (d.citta || '') + ' (' + (d.provincia || '') + ')');
      L.push('Pagamento preferito: ' + (d.pagamento || '—'));
      if (d.dedica) L.push('Dedica: ' + d.dedica);
      if (d.note) L.push('Note: ' + d.note);
      return L.join('\n');
    }

    function valida() {
      if (!form.reportValidity()) return false;
      if (!cartLines().length) { toast('Il carrello è vuoto'); return false; }
      return true;
    }

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!valida()) return;
      const body = encodeURIComponent(messaggio());
      window.location.href = 'mailto:' + CFG.email + '?subject=' +
        encodeURIComponent('Ordine ' + CFG.brand) + '&body=' + body;
      confermato();
    });

    const wa = $('.js-wa', form);
    if (wa) wa.addEventListener('click', () => {
      if (!valida()) return;
      window.open('https://wa.me/' + CFG.whatsapp + '?text=' + encodeURIComponent(messaggio()), '_blank', 'noopener');
      confermato();
    });

    function confermato() {
      const box = $('[data-conferma]');
      if (box) { box.hidden = false; box.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    }

    const gift = $('#gift');
    if (gift) gift.addEventListener('change', draw);
    document.addEventListener('vera:cart', draw);
    draw();
  }

  /* ------------------------------------------------ form contatti -- */
  function initContact() {
    const form = $('#contact-form');
    if (!form) return;
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const d = Object.fromEntries(new FormData(form).entries());
      const testo = [
        (d.oggetto || 'Richiesta') + ' · ' + CFG.brand, '',
        'Nome: ' + (d.nome || ''), 'Email: ' + (d.email || ''),
        'Telefono: ' + (d.telefono || ''), '', (d.messaggio || ''),
      ].join('\n');
      window.location.href = 'mailto:' + CFG.email +
        '?subject=' + encodeURIComponent((d.oggetto || 'Richiesta') + ' — ' + CFG.brand) +
        '&body=' + encodeURIComponent(testo);
      toast('Apro il tuo client di posta');
    });
  }

  /* ------------------------------------------------ newsletter -- */
  function initNewsletter() {
    $$('.newsletter__form').forEach((f) => f.addEventListener('submit', (e) => {
      e.preventDefault();
      if (!f.reportValidity()) return;
      f.reset();
      toast('Grazie · ti scriveremo presto');
    }));
  }

  /* ------------------------------------------------------- boot -- */
  document.addEventListener('DOMContentLoaded', function () {
    buildHeader();
    buildDrawer();
    buildFooter();
    renderCart();
    initHome();
    initShop();
    initPDP();
    initOrder();
    initContact();
    initNewsletter();
    bindAccordions(document);
    fillContacts();
    observeReveals(document);
    $$('a[href="#carrello"], .js-open-cart').forEach((a) =>
      a.addEventListener('click', (e) => { e.preventDefault(); openDrawer(); }));
  });
})();
