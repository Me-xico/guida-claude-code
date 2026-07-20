/* Percorso guidato: trasforma un blocco .percorso (immagine SVG + didascalie
   .percorso-step con data-highlight="id1 id2") in uno step-through navigabile.
   L'SVG viene caricato inline così il CSS può accendere/spegnere i gruppi. */
(function () {
  "use strict";

  function init(el) {
    var img = el.querySelector("img");
    var steps = Array.prototype.slice.call(el.querySelectorAll(".percorso-step"));
    if (!img || steps.length === 0) return;

    fetch(img.src)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (txt) {
        var holder = document.createElement("div");
        holder.className = "percorso-svg percorso-attivo";
        holder.innerHTML = txt;
        var svg = holder.querySelector("svg");
        if (!svg) return;
        svg.setAttribute("role", "img");
        svg.setAttribute("aria-label", img.alt || "");
        img.replaceWith(holder);
        el.classList.add("percorso-js");
        build(el, svg, steps);
      })
      .catch(function () { /* fetch fallito: resta l'immagine statica */ });
  }

  function build(el, svg, steps) {
    var i = 0;

    var nav = document.createElement("div");
    nav.className = "percorso-controlli";
    var prev = button("← Indietro");
    var next = button("Avanti →");
    var count = document.createElement("span");
    count.className = "percorso-contatore";
    nav.appendChild(prev); nav.appendChild(next); nav.appendChild(count);
    el.appendChild(nav);

    prev.addEventListener("click", function () { go(i - 1); });
    next.addEventListener("click", function () { go(i + 1); });
    el.tabIndex = 0;
    el.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { go(i + 1); e.preventDefault(); }
      if (e.key === "ArrowLeft") { go(i - 1); e.preventDefault(); }
    });

    function go(n) {
      i = Math.max(0, Math.min(steps.length - 1, n));
      var ids = (steps[i].getAttribute("data-highlight") || "").split(/\s+/);
      var groups = svg.querySelectorAll('g[id^="p-"]');
      Array.prototype.forEach.call(groups, function (g) {
        g.classList.toggle("percorso-on", ids.indexOf(g.id) !== -1);
      });
      steps.forEach(function (s, k) {
        s.classList.toggle("percorso-corrente", k === i);
      });
      prev.disabled = i === 0;
      next.disabled = i === steps.length - 1;
      count.textContent = (i + 1) + " / " + steps.length;
    }

    go(0);
  }

  function button(label) {
    var b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    return b;
  }

  function boot() {
    document.querySelectorAll(".percorso").forEach(init);
  }

  /* Material usa la navigazione instant: reinizializza a ogni cambio pagina */
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(boot);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
