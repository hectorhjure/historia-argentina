/* Corpus de historia argentina — interacción del sitio.
   Tres cosas: tema claro/oscuro, buscador global, filtro de fichas.
   Todo degrada con gracia: sin JS, el sitio sigue siendo navegable. */
(function () {
  "use strict";

  /* --------------------------------------------------------------- tema */
  var raiz = document.documentElement;
  var guardado = null;
  try { guardado = localStorage.getItem("tema"); } catch (e) { /* modo privado */ }
  if (guardado) { raiz.setAttribute("data-theme", guardado); }

  var btnTema = document.getElementById("tema");
  if (btnTema) {
    btnTema.addEventListener("click", function () {
      var oscuroAhora = raiz.getAttribute("data-theme") === "dark" ||
        (!raiz.getAttribute("data-theme") &&
         window.matchMedia("(prefers-color-scheme: dark)").matches);
      var nuevo = oscuroAhora ? "light" : "dark";
      raiz.setAttribute("data-theme", nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) { /* ignorar */ }
    });
  }

  /* --------------------------------------------------------- utilidades */
  function normalizar(s) {
    return (s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  }
  function escapar(s) {
    return (s || "").replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  var NOMBRE_CAPA = { capitulo: "Capítulo", ficha: "Ficha", monografia: "Monografía" };

  /* ---------------------------------------------------- buscador global */
  var caja = document.getElementById("q");
  var panel = document.getElementById("resultados");

  if (caja && panel) {
    var cargando = false;
    var seleccion = -1;

    function asegurarIndice(luego) {
      if (window.INDICE) { luego(); return; }
      if (cargando) { return; }
      cargando = true;
      var s = document.createElement("script");
      s.src = "assets/indice.js";
      s.onload = function () { cargando = false; luego(); };
      s.onerror = function () { cargando = false; };
      document.head.appendChild(s);
    }

    function buscar(termino) {
      var t = normalizar(termino).trim();
      if (t.length < 2) { panel.hidden = true; return; }
      var palabras = t.split(/\s+/);
      var hits = [];
      (window.INDICE || []).forEach(function (d) {
        var heno = normalizar(d.t + " " + d.x);
        var puntos = 0;
        for (var i = 0; i < palabras.length; i++) {
          var pos = heno.indexOf(palabras[i]);
          if (pos === -1) { return; }
          puntos += normalizar(d.t).indexOf(palabras[i]) !== -1 ? 60 : 12;
          puntos += Math.max(0, 25 - pos / 60);
        }
        var donde = heno.indexOf(palabras[0]);
        hits.push({ d: d, p: puntos, frag: d.x.substr(Math.max(0, donde - 60), 170) });
      });
      hits.sort(function (a, b) { return b.p - a.p; });
      hits = hits.slice(0, 12);
      seleccion = -1;

      if (!hits.length) {
        panel.innerHTML = '<div class="vacio">Sin resultados para «' +
          escapar(termino) + '».</div>';
      } else {
        panel.innerHTML = hits.map(function (h) {
          return '<a href="' + h.d.u + '"><strong>' + escapar(h.d.t) +
            '</strong><em>' + NOMBRE_CAPA[h.d.c] + ' · …' + escapar(h.frag) +
            '…</em></a>';
        }).join("");
      }
      panel.hidden = false;
    }

    caja.addEventListener("input", function () {
      var v = caja.value;
      asegurarIndice(function () { buscar(v); });
    });
    caja.addEventListener("focus", function () { asegurarIndice(function () {}); });

    caja.addEventListener("keydown", function (ev) {
      var opciones = panel.querySelectorAll("a");
      if (ev.key === "Escape") { panel.hidden = true; caja.blur(); return; }
      if (!opciones.length) { return; }
      if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
        ev.preventDefault();
        seleccion += ev.key === "ArrowDown" ? 1 : -1;
        if (seleccion < 0) { seleccion = opciones.length - 1; }
        if (seleccion >= opciones.length) { seleccion = 0; }
        for (var i = 0; i < opciones.length; i++) {
          opciones[i].className = i === seleccion ? "sel" : "";
        }
        opciones[seleccion].scrollIntoView({ block: "nearest" });
      } else if (ev.key === "Enter" && seleccion >= 0) {
        ev.preventDefault();
        window.location.href = opciones[seleccion].getAttribute("href");
      }
    });

    document.addEventListener("click", function (ev) {
      if (!panel.contains(ev.target) && ev.target !== caja) { panel.hidden = true; }
    });
  }

  /* ------------------------------------------------- explorador de fichas */
  var entradaF = document.getElementById("ff");
  var listaF = document.getElementById("lista-fichas");
  var chipsF = document.getElementById("chips");
  var conteoF = document.getElementById("conteo");

  if (entradaF && listaF && window.FICHAS) {
    var fichas = window.FICHAS;
    var activos = {};

    var facetas = [];
    ["actualizado", "provisional"].forEach(function (v) {
      if (fichas.some(function (f) { return (f.est || "").indexOf(v) === 0; })) {
        facetas.push({ k: "est", v: v, etiqueta: v });
      }
    });
    ["alta", "media", "baja"].forEach(function (v) {
      if (fichas.some(function (f) { return f.conf === v; })) {
        facetas.push({ k: "conf", v: v, etiqueta: "confianza " + v });
      }
    });
    if (fichas.some(function (f) { return (f.tipo || []).join().indexOf("debatido") !== -1; })) {
      facetas.push({ k: "tipo", v: "debatido", etiqueta: "debatido" });
    }
    var cuentaTemas = {};
    fichas.forEach(function (f) {
      (f.temas || []).forEach(function (t) { cuentaTemas[t] = (cuentaTemas[t] || 0) + 1; });
    });
    Object.keys(cuentaTemas)
      .sort(function (a, b) { return cuentaTemas[b] - cuentaTemas[a]; })
      .slice(0, 12)
      .forEach(function (t) { facetas.push({ k: "temas", v: t, etiqueta: t }); });

    chipsF.innerHTML = facetas.map(function (f, i) {
      return '<button class="chip" type="button" aria-pressed="false" data-i="' + i +
        '">' + escapar(f.etiqueta) + "</button>";
    }).join("");

    function pinta() {
      var t = normalizar(entradaF.value).trim();
      var visibles = fichas.filter(function (f) {
        if (t && normalizar(f.id + " " + f.af + " " + (f.temas || []).join(" ") + " " + f.per)
              .indexOf(t) === -1) { return false; }
        return Object.keys(activos).every(function (i) {
          var fa = facetas[i];
          var campo = f[fa.k];
          if (Array.isArray(campo)) {
            return campo.some(function (x) { return String(x).indexOf(fa.v) !== -1; });
          }
          return String(campo || "").indexOf(fa.v) === 0 ||
                 String(campo || "").indexOf(fa.v) !== -1;
        });
      });

      conteoF.textContent = visibles.length === fichas.length
        ? fichas.length + " fichas"
        : visibles.length + " de " + fichas.length + " fichas";

      listaF.innerHTML = visibles.length
        ? visibles.map(function (f) {
            var cls = f.conf ? " c-" + f.conf : "";
            return '<a class="item-ficha" href="' + f.url + '">' +
              '<span class="fid">' + escapar(f.id) + "</span>" +
              "<p>" + escapar(f.af) + "</p>" +
              '<span class="meta">' +
              '<span class="badge e-' + escapar((f.est || "").split(" ")[0]) + '">' +
                escapar(f.est) + "</span>" +
              (f.conf ? '<span class="badge' + cls + '">confianza ' +
                escapar(f.conf) + "</span>" : "") +
              '<span class="badge">' + escapar(f.per) + "</span>" +
              "</span></a>";
          }).join("")
        : '<p class="tenue">Ninguna ficha coincide con ese filtro.</p>';
    }

    chipsF.addEventListener("click", function (ev) {
      var b = ev.target.closest ? ev.target.closest(".chip") : null;
      if (!b) { return; }
      var i = b.getAttribute("data-i");
      if (activos[i]) { delete activos[i]; b.setAttribute("aria-pressed", "false"); }
      else { activos[i] = true; b.setAttribute("aria-pressed", "true"); }
      pinta();
    });
    entradaF.addEventListener("input", pinta);
    pinta();
  }

  /* ------------------------------------------- línea de tiempo del corpus */
  /* Los hechos y el SVG ya vienen renderizados. Acá sólo se filtran y se
     sincronizan las dos vistas del mismo dato. */
  var entradaE = document.getElementById("fe");
  var listaE = document.getElementById("lista-eventos");
  var conteoE = document.getElementById("conteo-ev");
  var vacioE = document.getElementById("vacio-ev");
  var mapa = document.querySelector(".mapa-temporal");

  if (listaE) {
    var hechos = [].slice.call(listaE.querySelectorAll("li.ev"));
    var cortes = [].slice.call(listaE.querySelectorAll("h2.corte"));
    var listas = [].slice.call(listaE.querySelectorAll("ol.eventos"));
    var totalE = hechos.length;
    var ejes = {};
    var marcas = mapa ? [].slice.call(mapa.querySelectorAll("rect.m")) : [];
    var porEv = {};
    marcas.forEach(function (m) { porEv[m.getAttribute("data-ev")] = m; });

    function pintaE() {
      var q = normalizar(entradaE ? entradaE.value : "").trim();
      var activos = Object.keys(ejes);
      var visibles = 0;

      hechos.forEach(function (li) {
        var okEje = !activos.length || ejes[li.getAttribute("data-eje")];
        var okTxt = !q || normalizar(li.getAttribute("data-busq")).indexOf(q) !== -1;
        var ok = okEje && okTxt;
        li.hidden = !ok;
        var m = porEv[li.getAttribute("data-id")];
        if (m) { m.style.display = ok ? "" : "none"; }
        if (ok) { visibles++; }
      });

      // un grupo sin hechos visibles se esconde entero
      listas.forEach(function (ol, i) {
        var algo = [].slice.call(ol.children).some(function (li) { return !li.hidden; });
        ol.hidden = !algo;
        if (cortes[i]) { cortes[i].hidden = !algo; }
      });

      // apagar el eje entero en el SVG cuando está filtrado fuera
      if (mapa) {
        [].slice.call(mapa.querySelectorAll("g.eje")).forEach(function (g) {
          var dentro = !activos.length || ejes[g.getAttribute("data-eje")];
          g.classList.toggle("apagado", !dentro);
        });
      }

      conteoE.textContent = visibles === totalE
        ? totalE + " hechos"
        : visibles + " de " + totalE + " hechos";
      if (vacioE) { vacioE.hidden = visibles !== 0; }
    }

    var chipsE = document.querySelectorAll(".chip-eje");
    [].slice.call(chipsE).forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-eje");
        if (ejes[k]) { delete ejes[k]; b.setAttribute("aria-pressed", "false"); }
        else { ejes[k] = true; b.setAttribute("aria-pressed", "true"); }
        pintaE();
      });
    });
    if (entradaE) { entradaE.addEventListener("input", pintaE); }

    // clic en el mapa -> destacar y traer el hecho a la vista
    if (mapa) {
      mapa.addEventListener("click", function (ev) {
        var r = ev.target && ev.target.getAttribute
          ? ev.target.getAttribute("data-ev") : null;
        if (!r) { return; }
        hechos.forEach(function (li) { li.classList.remove("destacada"); });
        marcas.forEach(function (m) { m.classList.remove("destacada"); });
        var li = listaE.querySelector('li.ev[data-id="' + r + '"]');
        if (li && !li.hidden) {
          li.classList.add("destacada");
          if (porEv[r]) { porEv[r].classList.add("destacada"); }
          li.scrollIntoView({ block: "center",
            behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
              ? "auto" : "smooth" });
        }
      });
    }

    pintaE();
  }

  /* ------------------------------------------------- recorrido: teclado */
  /* Las flechas avanzan y retroceden entre estaciones. El enlace ya existe en
     el HTML: acá sólo se le da un atajo, así que sin JS no se pierde nada. */
  var pasos = document.querySelector(".pasos");
  if (pasos) {
    document.addEventListener("keydown", function (ev) {
      if (ev.metaKey || ev.ctrlKey || ev.altKey) { return; }
      var t = ev.target || {};
      var tag = (t.tagName || "").toUpperCase();
      if (tag === "INPUT" || tag === "TEXTAREA" || t.isContentEditable) { return; }
      var sel = ev.key === "ArrowRight" ? 'a.nav-paso.sig'
              : ev.key === "ArrowLeft"  ? 'a.nav-paso.prev' : null;
      if (!sel) { return; }
      var a = pasos.querySelector(sel);
      if (a) { ev.preventDefault(); window.location.href = a.getAttribute("href"); }
    });
  }
})();
