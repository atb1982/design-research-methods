# Design Research Methods

A public reference of 117 design research methods, organized across the Double Diamond.
The detailed cards were researched and written by students at the College of Design,
NC State University. The first set of cards came from **D 492 Intro to Design Research**,
Spring 2026. The site itself does not name a course on its home page, so other courses can use it.

Live site: _add the GitHub Pages URL here once Pages is enabled_

## What is in this repository

| Path | Purpose |
|---|---|
| `index.html` | The entire site. Data is embedded, so it opens correctly from a file or a server. |
| `data.json` | The same content as a standalone file, for reuse or for a future dynamic version. |
| `images/` | 59 method images plus the Double Diamond diagram. |
| `overview_links.json` | Free online overview pages for the reference entries ("Where to learn more"). |
| `templates.json` | Free templates, worksheets and canvases linked from method cards ("Templates and worksheets"). |
| `build.py` | Regenerates `index.html` from `data.json`, `overview_links.json` and `templates.json`. |

## Publishing with GitHub Pages

1. Create a repository and upload every file in this folder, keeping `images/` intact.
2. Open **Settings, then Pages**.
3. Under **Source**, choose **Deploy from a branch**, select `main` and `/ (root)`, then save.
4. The site appears at `https://<username>.github.io/<repository>/` within a minute or two.

## Embedding in Google Sites

New Google Sites has no API and cannot be generated programmatically, so the site is
embedded rather than rebuilt there.

1. Publish to GitHub Pages and copy the URL.
2. In Google Sites choose **Insert, then Embed, then By URL** and paste it.
3. Stretch the embed block to the full page width and set a tall frame height so the
   page scrolls inside the frame rather than in a short window.

## Editing content

Content lives in `data.json`. Each method is one object.

Student-written cards use `"kind": "full"`:

```json
{
  "id": "card-sorting",
  "name": "Card Sorting",
  "phase": "insights",
  "kind": "full",
  "student": "Tyler Surface",
  "whatItIs": "...",
  "whenToUse": ["..."],
  "howToDoIt": ["..."],
  "whatYouNeed": ["..."],
  "tips": ["..."],
  "mistakes": ["..."],
  "example": "...",
  "sources": ["..."],
  "image": "images/card-sorting.jpg"
}
```

Methods that no student has documented use `"kind": "brief"` with a short explanation,
a `reference`, and a `referenceUrl`.

After editing `data.json`, run `python3 build.py` to regenerate `index.html`.

To add a template to a card, add an entry to `templates.json` under the method id (student or
reference card). Each entry needs `title`, `publisher`, `url` (https), `format` (for example
`PDF` or `Online whiteboard`) and `access` (what a person must do to get it, such as
`Free download` or `A free account is likely needed`). `note` is optional. Link out only; do not
copy third-party files into this repository. The build stops if an id or a field is missing.

To add or replace an image, save it as `images/<method-id>.jpg` and set these fields on
that method in `data.json`:

| Field | Purpose |
|---|---|
| `image` | Path, for example `images/card-sorting.jpg` |
| `imageAlt` | ALT text that describes what the picture shows |
| `imageCredit` | Sentence naming who provided the image, for example `Image provided by Tyler Surface.` |
| `imageSource` and `imageSourceUrl` | Original source name and, if there is one, its link |
| `imageNote` | Optional note, such as `AI-generated image.` |

Other optional fields on student cards: `expandedNote` (states that the card was expanded
from a named book), `editorNote`, and `library` (page references in the course books).

## Phase colors

| Phase | Double Diamond | Hex |
|---|---|---|
| Research | Discover | `#fdc907` |
| Insights | Define | `#eb5b54` |
| Ideation | Develop | `#83bc2c` |
| Prototyping & Testing | Deliver | `#4a8ecb` |

Core palette follows NC State brand guidance: Wolfpack Red `#CC0000`, black, and white,
set in Roboto, Roboto Condensed, and Roboto Slab.

## Credit and reuse

Each card names the student who wrote it. Images were selected by students to illustrate
their methods. The credit under every image names the student and the original source.
Confirm licensing before reusing any image outside this site.
