#!/usr/bin/env python3
"""Regenerate index.html from every SVG directory in the repository."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent.parent
SVG_DIRS = (
    ROOT / "symbols" / "componentes",
    ROOT / "illustrations",
)
OUTPUT = ROOT / "index.html"

TEMPLATE = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catálogo de símbolos · electro-svgs</title>
<meta name="description" content="Galería de los símbolos eléctricos SVG del repositorio electro-svgs.">
<style>
  :root {
    color-scheme: light;
    --bg: #f5f4f0;
    --surface: #ffffff;
    --ink: #17191d;
    --ink-soft: #4a4e57;
    --line: #dcdad2;
    --line-strong: #c7c4ba;
    --head: #eeeae1;
    --accent: #1b4bb7;
    --hover: #f2f6fd;
    --zebra: #fbfaf7;
    --selection: #cddcff;
  }
  * { box-sizing: border-box; }
  html { -webkit-text-size-adjust: 100%; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 15px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-variant-numeric: tabular-nums;
  }
  ::selection { background: var(--selection); color: var(--ink); }
  :focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  [hidden] { display: none !important; }
  .wrap { width: min(1120px, 100% - 3rem); margin-inline: auto; }

  .page-header { padding: 3.25rem 0 1.75rem; border-bottom: 1px solid var(--line); }
  h1 { font-size: clamp(1.9rem, 4vw, 2.6rem); line-height: 1.1; letter-spacing: -0.035em; margin: 0 0 .55rem; }
  .lede { color: var(--ink-soft); max-width: 64ch; margin: 0 0 1.75rem; }
  .search { display: block; max-width: 30rem; }
  .search span { display: block; font-size: .8rem; font-weight: 650; margin-bottom: .4rem; }
  .search input {
    width: 100%; padding: .65rem .8rem; font: inherit; color: var(--ink);
    background: var(--surface); border: 1px solid var(--line-strong); border-radius: 8px;
  }
  .search input::placeholder { color: var(--ink-soft); opacity: 1; }
  .search input:focus { border-color: var(--accent); }

  .count { margin: 1.5rem 0 .6rem; font-size: .8rem; font-weight: 650; color: var(--ink-soft); letter-spacing: .02em; }
  .table-wrap {
    margin-bottom: 2.5rem; max-height: min(72vh, 900px); overflow: auto;
    background: var(--surface); border: 1px solid var(--line); border-radius: 10px;
    scrollbar-width: thin; scrollbar-color: var(--line-strong) transparent;
  }
  .table-wrap::-webkit-scrollbar { width: 10px; height: 10px; }
  .table-wrap::-webkit-scrollbar-thumb { background: var(--line-strong); border: 2px solid var(--surface); border-radius: 6px; }
  table { width: 100%; min-width: 620px; border-collapse: collapse; }
  caption { text-align: left; padding: .9rem 1.1rem; color: var(--ink-soft); font-size: .85rem; border-bottom: 1px solid var(--line); }
  th, td { padding: .5rem 1.1rem; text-align: left; border-bottom: 1px solid var(--line); vertical-align: middle; }
  thead th {
    position: sticky; top: 0; z-index: 1; background: var(--head);
    font-size: .72rem; text-transform: uppercase; letter-spacing: .07em; font-weight: 700;
    white-space: nowrap;
  }
  tbody tr:nth-child(even) { background: var(--zebra); }
  tbody tr { transition: background-color 120ms ease-out; }
  tbody tr:hover { background: var(--hover); }
  tbody tr:last-child td { border-bottom: 0; }
  .preview-cell { width: 4.75rem; }
  .preview {
    display: grid; place-items: center; width: 3rem; height: 3rem;
    background: #fff; border: 1px solid var(--line); border-radius: 6px;
  }
  .preview img { display: block; width: 2.5rem; height: 2.5rem; object-fit: contain; }
  .name { font-weight: 600; }
  .id, .file a { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86rem; }
  .id { color: var(--ink-soft); }
  .file a { color: var(--accent); text-decoration: none; }
  .file a:hover { text-decoration: underline; text-underline-offset: 3px; }
  .empty { padding: 2.5rem 1rem; text-align: center; color: var(--ink-soft); }
  tbody tr { cursor: pointer; }
  tbody tr:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
  dialog {
    width: min(560px, 100% - 2rem); max-height: min(85vh, 760px); padding: 0;
    border: 1px solid var(--line-strong); border-radius: 12px;
    background: var(--surface); color: var(--ink);
    box-shadow: 0 18px 48px rgba(23, 25, 29, .18);
  }
  dialog::backdrop { background: rgba(23, 25, 29, .55); }
  dialog[open] { animation: dialog-in 160ms ease-out; }
  @keyframes dialog-in { from { opacity: 0; transform: translateY(8px) scale(.98); } }
  .dialog-head {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem;
    padding: 1.25rem 1.4rem 1rem; border-bottom: 1px solid var(--line);
  }
  .dialog-head h2 { margin: 0; font-size: 1.25rem; letter-spacing: -0.02em; line-height: 1.25; }
  .dialog-head p { margin: .25rem 0 0; font-size: .82rem; color: var(--ink-soft); }
  .close {
    flex: none; width: 2rem; height: 2rem; display: grid; place-items: center;
    font: inherit; font-size: 1.3rem; line-height: 1; color: var(--ink); cursor: pointer;
    background: var(--surface); border: 1px solid var(--line-strong); border-radius: 6px;
  }
  .close:hover { background: var(--head); }
  .dialog-body { padding: 1.4rem; overflow: auto; }
  .canvas {
    display: grid; place-items: center; min-height: 220px; padding: 1.5rem;
    background: #fff; border: 1px solid var(--line); border-radius: 8px;
  }
  .canvas img { display: block; max-width: 100%; max-height: 320px; width: auto; height: auto; object-fit: contain; }
  .dialog-meta { display: flex; flex-wrap: wrap; gap: .5rem 2rem; margin: 1rem 0 0; }
  .dialog-meta dt { color: var(--ink-soft); font-size: .72rem; text-transform: uppercase; letter-spacing: .06em; }
  .dialog-meta dd { margin: .15rem 0 0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .85rem; }
  .dialog-foot { padding: 0 1.4rem 1.4rem; }
  .dialog-foot a { color: var(--accent); font-size: .875rem; text-decoration: none; }
  .dialog-foot a:hover { text-decoration: underline; text-underline-offset: 3px; }
  @media (prefers-reduced-motion: reduce) {
    dialog[open] { animation: none; }
    tbody tr { transition: none; }
  }
  footer {
    display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; justify-content: space-between;
    padding: 1.4rem 0 3rem; border-top: 1px solid var(--line);
    color: var(--ink-soft); font-size: .85rem;
  }
  footer a { color: var(--accent); text-decoration: none; }
  footer a:hover { text-decoration: underline; text-underline-offset: 3px; }
  @media (max-width: 600px) {
    .wrap { width: min(1120px, 100% - 2rem); }
    .page-header { padding-top: 2.25rem; }
    th, td { padding-inline: .8rem; }
  }
</style>
</head>
<body>
  <header class="page-header">
    <div class="wrap">
      <h1>Catálogo de símbolos</h1>
      <p class="lede">Todos los SVG del repositorio, con su nombre, identificador y vista previa. Los códigos numéricos de los esquemáticos corresponden a la librería CADe_SIMU.</p>
      <label class="search">
        <span>Buscar por nombre, código o archivo</span>
        <input id="filter" type="search" placeholder="Ej.: motor, contactor, 1000" autocomplete="off" spellcheck="false">
      </label>
    </div>
  </header>

  <main class="wrap">
    <p class="count" id="count">__COUNT__ símbolos</p>
    <div class="table-wrap">
      <table id="catalog">
        <caption>Vista previa, nombre, código y archivo de cada símbolo SVG.</caption>
        <thead>
          <tr>
            <th scope="col">Vista previa</th>
            <th scope="col">Símbolo</th>
            <th scope="col">Código</th>
            <th scope="col">Archivo</th>
          </tr>
        </thead>
        <tbody>
__ROWS__
        </tbody>
      </table>
      <p class="empty" id="empty" hidden>Ningún símbolo coincide con la búsqueda.</p>
    </div>
  </main>

  <footer class="wrap">
    <span>electro-svgs · licencia MIT</span>
    <a href="README.md">Ver el README del repositorio</a>
  </footer>

  <dialog id="preview" aria-labelledby="preview-title">
    <div class="dialog-head">
      <div>
        <h2 id="preview-title"></h2>
        <p>Vista previa del símbolo</p>
      </div>
      <button type="button" class="close" id="preview-close" aria-label="Cerrar vista previa">&times;</button>
    </div>
    <div class="dialog-body">
      <div class="canvas"><img id="preview-image" src="__FIRST__" alt=""></div>
      <dl class="dialog-meta">
        <div><dt>Código</dt><dd id="preview-code"></dd></div>
        <div><dt>Archivo</dt><dd id="preview-file"></dd></div>
      </dl>
    </div>
    <div class="dialog-foot">
      <a id="preview-link" href="#" target="_blank" rel="noopener">Abrir SVG en una pestaña nueva</a>
    </div>
  </dialog>

  <script>
    const input = document.getElementById('filter');
    const rows = Array.from(document.querySelectorAll('#catalog tbody tr'));
    const count = document.getElementById('count');
    const empty = document.getElementById('empty');
    input.addEventListener('input', () => {
      const q = input.value.trim().toLocaleLowerCase();
      let visible = 0;
      for (const row of rows) {
        const hit = !q || row.dataset.search.includes(q);
        row.hidden = !hit;
        if (hit) visible++;
      }
      count.textContent = visible === rows.length
        ? rows.length + ' símbolos'
        : visible + ' de ' + rows.length + ' símbolos';
      empty.hidden = visible !== 0;
    });

    const dialog = document.getElementById('preview');
    const previewTitle = document.getElementById('preview-title');
    const previewImage = document.getElementById('preview-image');
    const previewCode = document.getElementById('preview-code');
    const previewFile = document.getElementById('preview-file');
    const previewLink = document.getElementById('preview-link');

    function openPreview(row) {
      const name = row.querySelector('.name').textContent;
      const file = row.querySelector('.file a');
      previewTitle.textContent = name;
      previewImage.src = row.querySelector('img').getAttribute('src');
      previewImage.alt = 'Renderizado de ' + name;
      previewCode.textContent = row.querySelector('.id').textContent;
      previewFile.textContent = file.textContent;
      previewLink.href = file.href;
      dialog.showModal();
    }

    for (const row of rows) {
      row.tabIndex = 0;
      row.addEventListener('click', (event) => {
        if (event.target.closest('a')) return;
        openPreview(row);
      });
      row.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          openPreview(row);
        }
      });
    }

    document.getElementById('preview-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => {
      if (event.target === dialog) dialog.close();
    });
  </script>
</body>
</html>
'''


def natural_key(path):
    """Sort numerically inside digit runs: 1000, 1001, ..., 1050."""
    return [(1, int(x)) if x.isdigit() else (0, x) for x in re.split(r"(\d+)", path.name)]


def title_of(path):
    match = re.search(r"<title>(.*?)</title>", path.read_text(encoding="utf-8"), re.S)
    return html.unescape(match.group(1)).strip() if match else path.stem


def main():
    catalog = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    files = []
    for directory in SVG_DIRS:
        files.extend(sorted(directory.glob("*.svg"), key=natural_key))

    listed = {entry["file"] for entry in catalog["entries"]}
    items = []
    for entry in catalog["entries"]:
        if not (ROOT / entry["file"]).exists():
            continue
        items.append(
            {
                "code": entry["code"],
                "name": entry["name"],
                "file": entry["file"],
                "search": " ".join(
                    str(value)
                    for value in (
                        entry["name"],
                        entry["code"],
                        entry["file"],
                        entry.get("designator", ""),
                        entry.get("category_label", ""),
                    )
                ),
            }
        )
    # Un SVG nuevo sin entrada en el catálogo se muestra igual, con su <title>.
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        if rel not in listed:
            title = title_of(path)
            items.append(
                {
                    "code": path.stem,
                    "name": title,
                    "file": rel,
                    "search": f"{title} {path.stem} {rel}",
                }
            )

    items.sort(key=lambda item: natural_key(Path(item["file"])))
    rows = []
    for item in items:
        rel = item["file"]
        name = item["name"]
        search = html.escape(item["search"].lower(), quote=True)
        rows.append(
            f'        <tr data-search="{search}">\n'
            f'          <td class="preview-cell"><span class="preview"><img src="{rel}" alt="Vista previa de {html.escape(name, quote=True)}" loading="lazy" width="36" height="36"></span></td>\n'
            f'          <td class="name">{html.escape(name)}</td>\n'
            f'          <td class="id">{item["code"]}</td>\n'
            f'          <td class="file"><a href="{rel}" target="_blank" rel="noopener">{html.escape(rel)}</a></td>\n'
            f'        </tr>'
        )
    first = items[0]["file"] if items else ""
    OUTPUT.write_text(
        TEMPLATE.replace("__ROWS__", "\n".join(rows))
        .replace("__COUNT__", str(len(items)))
        .replace("__FIRST__", first),
        encoding="utf-8",
    )
    print(f"Generado {OUTPUT.name} con {len(items)} simbolos")


if __name__ == "__main__":
    main()
