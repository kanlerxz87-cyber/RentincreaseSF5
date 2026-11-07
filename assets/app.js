/* Tiny dashboard helpers: per-table row filtering + visible row counts. No external dependencies. */
(function () {
  "use strict";
  document.querySelectorAll("table[data-filterable]").forEach(function (table) {
    var bar = document.createElement("div");
    bar.className = "filterbar";
    var input = document.createElement("input");
    input.type = "search";
    input.setAttribute("aria-label", "Filter table rows");
    input.placeholder = "Filter rows (type a topic, value, source id, or status)…";
    var count = document.createElement("span");
    count.className = "count";
    bar.appendChild(input);
    bar.appendChild(count);
    var host = table.parentNode;
    if (host && host.classList && host.classList.contains("tablewrap")) {
      host.parentNode.insertBefore(bar, host);
    } else {
      host.insertBefore(bar, table);
    }

    var rows = Array.prototype.slice.call(table.querySelectorAll("tbody tr"));
    function refresh() {
      var q = input.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (r) {
        var match = !q || (r.textContent || "").toLowerCase().indexOf(q) !== -1;
        r.style.display = match ? "" : "none";
        if (match) shown++;
      });
      count.textContent = shown + " of " + rows.length + " rows";
    }
    input.addEventListener("input", refresh);
    refresh();
  });
})();
