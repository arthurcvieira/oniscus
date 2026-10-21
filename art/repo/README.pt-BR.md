# Artes do repositório

*[English](README.md) · Português*

Feitas a partir do mascote aprovado em `../branding/`, usado sem alterações. Todo texto está convertido em contornos (Nunito, Noto Sans Mono, SIL OFL), então os SVGs aparecem iguais em qualquer lugar. Licença: **CC BY-SA 4.0**.

| Arquivo | Uso |
|---|---|
| `banner-dark.svg`, `banner-light.svg` | topo do README (1280×400), um para cada tema do GitHub |
| `banner-*.pt-BR.svg` | o mesmo, com o subtítulo em português, para o `README.pt-BR.md` |
| `social-preview.png` | prévia social do GitHub (1280×640): Settings → General → Social preview |
| `logo-horizontal-{dark,light}.svg` | mascote + nome, fundo transparente |
| `wordmark-{dark,light}.svg` | só o nome |
| `avatar.png` | quadrado 512×512 para organização/perfil no GitHub, OBS, Matrix etc. |
| `divider.svg` | divisor fino entre seções |

"Oniscus" sempre numa cor só; nunca destacar parte da palavra.

Topo do README:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="art/repo/banner-dark.pt-BR.svg">
    <img alt="Oniscus" src="art/repo/banner-light.pt-BR.svg" width="100%">
  </picture>
</p>
```

Para refazer: `python3 make_repo_art.py PASTA_DAS_FONTES` (precisa de `fonttools`; a pasta tem `Nunito.ttf` e `NotoSansMono.ttf` de github.com/google/fonts), depois `NODE_PATH=$(npm root -g) node render.mjs` para os PNGs.
