# Repository artwork

*English · [Português](README.pt-BR.md)*

Made from the approved mascot in `../branding/`, which is placed unchanged. All text is converted to outlines (Nunito, Noto Sans Mono, SIL OFL), so the SVGs look the same everywhere. License: **CC BY-SA 4.0**.

| File | Use |
|---|---|
| `banner-dark.svg`, `banner-light.svg` | README header (1280×400), one per GitHub theme |
| `banner-*.pt-BR.svg` | the same, with the Portuguese tagline, for `README.pt-BR.md` |
| `social-preview.png` | GitHub social preview (1280×640): Settings → General → Social preview |
| `logo-horizontal-{dark,light}.svg` | mascot + name, transparent background |
| `wordmark-{dark,light}.svg` | name only |
| `avatar.png` | 512×512 square for the GitHub organization/profile, OBS, Matrix, etc. |
| `divider.svg` | thin section divider |

"Oniscus" is always set in one colour; never highlight part of the word.

README header:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="art/repo/banner-dark.svg">
    <img alt="Oniscus" src="art/repo/banner-light.svg" width="100%">
  </picture>
</p>
```

Rebuild: `python3 make_repo_art.py FONT_DIR` (needs `fonttools`; FONT_DIR holds `Nunito.ttf` and `NotoSansMono.ttf` from github.com/google/fonts), then `NODE_PATH=$(npm root -g) node render.mjs` for the PNGs.
