// The Tally feedback form behind every feedback page (English, 繁體中文, 简体中文).
// THIS IS THE ONLY PLACE ITS ID LIVES. Set it to the ID at the end of the form's share link
// (https://tally.so/r/<ID>), for example "wAbCdE". While it's empty, each page shows its
// "not available yet" note instead of the form. See README.md, "Feedback form".
var LUNE_TALLY_FORM_ID = "vGQ89l";

(function () {
  var holder = document.getElementById("feedback-form");
  if (!holder || !LUNE_TALLY_FORM_ID) return;

  // The page's language goes to the form's hidden field "language" (en, zh-Hant or zh-Hans).
  var language = document.documentElement.lang || "en";
  var iframe = document.createElement("iframe");
  iframe.setAttribute("data-tally-src", "https://tally.so/embed/" + encodeURIComponent(LUNE_TALLY_FORM_ID) +
    "?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1&language=" + encodeURIComponent(language));
  iframe.setAttribute("loading", "lazy");
  iframe.setAttribute("height", "760");
  iframe.setAttribute("title", holder.getAttribute("data-title") || "Feedback");
  holder.replaceChildren(iframe);

  // Tally's own embed script sizes the form to its content; without it, the form still loads.
  var load = function () {
    if (typeof Tally !== "undefined") {
      Tally.loadEmbeds();
    } else {
      iframe.src = iframe.getAttribute("data-tally-src");
    }
  };
  var script = document.createElement("script");
  script.src = "https://tally.so/widgets/embed.js";
  script.onload = load;
  script.onerror = load;
  document.body.appendChild(script);
})();
