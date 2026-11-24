/* OSC reference pages (they have h3.osc-command): the right-hand table of contents keeps only the h2 (group) and h3
   (command) entries; the h4/h5 entries (Argument, Timing, ...) are hidden. Group headings get .toc-group (extra.css). */
(function () {
  if (!document.querySelector("h3.osc-command")) return;
  document.querySelectorAll(".md-sidebar--secondary a.md-nav__link").forEach(function (a) {
    var id = decodeURIComponent((a.getAttribute("href") || "").replace(/^#/, ""));
    var target = id && document.getElementById(id);
    if (!target) return;
    var li = a.closest("li");
    if (target.tagName === "H2") li.classList.add("toc-group");
    else if (target.tagName !== "H3") li.classList.add("toc-hidden");
  });
})();
