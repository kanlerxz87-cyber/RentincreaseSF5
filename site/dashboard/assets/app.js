
document.addEventListener('DOMContentLoaded', function () {
  // table filter: <div class="filter" data-table="#id">
  document.querySelectorAll('.filter').forEach(function (f) {
    var sel = f.getAttribute('data-table');
    var table = document.querySelector(sel);
    if (!table) return;
    var input = f.querySelector('input');
    var select = f.querySelector('select');
    function apply() {
      var q = (input && input.value || '').toLowerCase();
      var s = (select && select.value || '');
      var shown = 0;
      table.querySelectorAll('tbody tr').forEach(function (tr) {
        var txt = tr.textContent.toLowerCase();
        var ok = (!q || txt.indexOf(q) > -1) && (!s || tr.getAttribute('data-group') === s);
        tr.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      var out = f.querySelector('.count');
      if (out) out.textContent = shown + ' row' + (shown === 1 ? '' : 's');
    }
    if (input) input.addEventListener('input', apply);
    if (select) select.addEventListener('change', apply);
    apply();
  });
});
