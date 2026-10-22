# Design Research Methods, D 492

A public reference of 117 design research methods, organized across the Double Diamond.
The detailed cards were researched and written by students in **D 492 Intro to Design
Research**, College of Design, NC State University, Spring 2026.

Live site: _add the GitHub Pages URL here once Pages is enabled_

## What is in this repository

| Path | Purpose |
|---|---|
| `index.html` | The entire site. Data is embedded, so it opens correctly from a file or a server. |
| `data.json` | The same content as a standalone file, for reuse or for a future dynamic version. |
| `images/` | 59 method images plus the Double Diamond diagram. |
| `build.py` | Regenerates `index.html` from `data.json`. |
| `search.js` | Search code: word-form matching and related terms. Built into `index.html`. |
| `synonyms.json` | Word forms, spellings and related terms used by search. Editable. |
| `overview_links.json` | Free online overview pages for the reference entries, shown under "Free overviews online". Editable. |

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

## Links, search, and accessibility

- Every method has its own address, for example `index.html#draw-it`. The method id in `data.json` is the address, so the Back button and shared links work.
- Search covers every field on a card (steps, tips, examples, sources) and matches all the words typed, in any order. Matches in the name rank first.
- Search understands word forms (interview, interviews, interviewing), American and British spellings (analyze, analyse), and related terms (searching questionnaire also finds survey cards, ranked lower). The page says which related terms were included.
- To add or change a free overview link, edit `overview_links.json` (method id, then a list of title, publisher, url and an optional note) and run `python3 build.py`. The build stops if an id is not a reference entry or a link is not https.
- To change related terms, edit `synonyms.json` and run `python3 build.py`. It has three lists: `forms` (spellings and word forms), `apart` (words a simple stemmer would wrongly merge, such as experience and experiment) and `related` (different terms for the same idea). The matching code is in `search.js`.
- Text on the phase colors is dark (`#1a1a1a`) so it meets WCAG AA contrast. The brand colors themselves are unchanged.
- The page has a skip link, visible keyboard focus, a polite status message for search and filter results, and a print layout for single cards.

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
