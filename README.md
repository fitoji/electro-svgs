# electro-svgs

Biblioteca de símbolos eléctricos en formato SVG: esquemáticos (IEC 60617 / UNE), iconos de panel e ilustraciones para documentación técnica.

## Propósito

Centralizar los SVG eléctricos que hoy están repartidos entre proyectos (simulador, calculistas e interfaces) en un único lugar, con convenciones consistentes de nombre, dimensiones y trazos. El objetivo es que cualquier herramienta del ecosistema pueda consumir los mismos símbolos sin duplicarlos ni convertirlos.

Esto **no** es un editor ni un simulador: solo contiene los recursos gráficos y su inventario.

## Origen y estado actual

Los 227 archivos de `symbols/componentes/` son una **copia** de `REA-ing-inversa/docs/img/componentes/`. Por ahora conviven en ambos repositorios: REA-ing-inversa sigue usando su original (hay referencias en `app/scripts/make-component-docs.ts` y `docs/componentes.md`), así que no se rompe nada. Esta duplicación es intencional y temporal.

### Migración futura

Cuando esta librería esté madura, el plan es convertirla en la fuente única de verdad:

1. Versionar este repo y decidir cómo lo consume REA-ing-inversa (submodule, subtree o paquete publicado).
2. Actualizar las referencias en REA-ing-inversa para que apunten a este repo.
3. Recién entonces borrar `docs/img/componentes/` de REA-ing-inversa y consolidar todo acá.

Hasta ese momento, **no borrar la copia de REA-ing-inversa**.

## Estructura

```
electro-svgs/
├── README.md
├── LICENSE
├── symbols/
│   └── componentes/   # 227 símbolos CADe_SIMU con nombre numérico
├── icons/             # iconos para interfaces y paneles (vacío)
├── illustrations/     # diagramas para documentación (vacío)
└── catalog.json       # inventario: id, nombre, categoría, ruta y tags (pendiente)
```

Los archivos se agrupan por categoría dentro de cada carpeta. Si un símbolo procede de una librería externa (por ejemplo, los códigos numéricos de CADe_SIMU), se conserva su identificador original como nombre de archivo (`1000.svg`, `1050.svg`, …) y se documenta su equivalente legible en `catalog.json`.

## Convenciones de los SVG

Todo archivo que entre al repositorio debe cumplir esto:

- **ViewBox, no dimensiones fijas.** Usar `viewBox` y evitar `width`/`height` rígidos, para que escale en cualquier contexto.
- **Trazos vectoriales.** Formas con `stroke` y `fill` limpios; sin imágenes incrustadas ni `base64`.
- **Tamaño de trazo coherente.** Mantener un mismo grosor dentro de una categoría para que los símbolos se vean uniformes al composarlos.
- **Sin estilos globales.** Los colores se definen por `currentColor` o variables CSS, para poder cambiarlos desde el consumidor.
- **Accesibilidad.** Incluir `<title>` con el nombre del símbolo; cuando aporte contexto, también `<desc>`.
- **Sin scripts ni elementos externos.** SVG estático, seguro de embeber.

Ejemplo mínimo:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-labelledby="title">
  <title id="title">Contacto normalmente abierto</title>
  <path d="M3 12h5m8 0h5M8 12l8-6" fill="none" stroke="currentColor" stroke-width="1.5"/>
</svg>
```

## Uso

Como imagen:

```html
<img src="symbols/contactores/na.svg" alt="Contacto normalmente abierto" width="32" />
```

En CSS, usando `currentColor`:

```css
.icon {
  width: 1.5rem;
  color: #0f172a;
}
```

En React (Vite), importando el SVG como componente:

```tsx
import ContactoNA from './symbols/contactores/na.svg?react';

<ContactoNA aria-label="Contacto normalmente abierto" />;
```

Si tu bundler no soporta el sufijo `?react`, importá la URL y usala con `<img>`.

## Cómo agregar un símbolo

1. Guardá el archivo en la carpeta correspondiente, con nombre en minúsculas y guiones (`contacto-na.svg`).
2. Verificá las convenciones de la sección anterior.
3. Agregá una entrada a `catalog.json` con `id`, `nombre`, `categoría`, `ruta` y `tags`.
4. Confirmá que el símbolo sea de autoría propia para que quede cubierto por la licencia MIT del repositorio.
5. Revisá que el SVG se vea bien sobre fondo claro y oscuro antes de abrir el PR.

## Licencia

MIT. Todos los SVG son de autoría propia y se distribuyen bajo la licencia MIT del repositorio. El texto completo está en [`LICENSE`](LICENSE).
