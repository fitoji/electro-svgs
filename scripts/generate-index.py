#!/usr/bin/env python3
"""Regenerate index.html from every SVG directory in the repository."""
from pathlib import Path
import html
import re

ROOT = Path(__file__).resolve().parent.parent
SVG_DIRS = (
    ROOT / "symbols" / "componentes",
    ROOT / "icons",
    ROOT / "illustrations",
)
OUTPUT = ROOT / "index.html"

NAMES = {
    "icon-bolt.svg": "Icono rayo de la app",
    "icon-rebt.svg": "Icono REBT de la app",
    "placeholder-logo.svg": "Logo placeholder de la app",
    "placeholder.svg": "Imagen placeholder de la app",
}

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
    files = []
    for directory in SVG_DIRS:
        files.extend(sorted(directory.glob("*.svg"), key=natural_key))
    rows = []
    for path in files:
        ident = path.stem
        title = NAMES.get(path.name) or title_of(path)
        rel = path.relative_to(ROOT).as_posix()
        search = html.escape(f"{title} {path.name} {ident} {rel}".lower(), quote=True)
        rows.append(
            f'        <tr data-search="{search}">\n'
            f'          <td class="preview-cell"><span class="preview"><img src="{rel}" alt="Vista previa de {html.escape(title, quote=True)}" loading="lazy" width="36" height="36"></span></td>\n'
            f'          <td class="name">{html.escape(title)}</td>\n'
            f'          <td class="id">{ident}</td>\n'
            f'          <td class="file"><a href="{rel}" target="_blank" rel="noopener">{html.escape(rel)}</a></td>\n'
            f'        </tr>'
        )
    OUTPUT.write_text(
        TEMPLATE.replace("__ROWS__", "\n".join(rows)).replace("__COUNT__", str(len(files))),
        encoding="utf-8",
    )
    print(f"Generado {OUTPUT.name} con {len(files)} simbolos")


if __name__ == "__main__":
    main()
