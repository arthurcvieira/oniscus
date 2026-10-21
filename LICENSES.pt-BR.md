# Licenças do Oniscus

[English](LICENSES.md)

Tudo o que o Oniscus distribui pode ser publicado e redistribuído livremente.

## Arquivos criados para o Oniscus

| O quê | Licença |
|---|---|
| Configs, scripts, descrição KIWI, tema GTK "Xi3 Retrô", tema do Plank | GPL-3.0-or-later (texto em `COPYING`) |
| Papel de parede `xi3.jpg` e o script que o gera (`art/wallpaper.py`) | CC BY-SA 4.0 |
| Mascote, ícone do menu e logo do terminal (`art/branding/`), incluindo a foto de referência | CC BY-SA 4.0 |

O visual retrô é **inspirado** na era Aqua/Tiger, mas é desenhado do zero com
gradientes em CSS. Nenhum ícone, imagem, fonte ou nome da Apple é usado. Os
nomes "Aqua", "Mac OS X", "Tiger" e o logo da Apple não aparecem em nenhum arquivo
distribuído.

## Componentes de terceiros (todos dos repositórios oficiais do Tumbleweed)

| Componente | Licença |
|---|---|
| i3 | BSD-3-Clause |
| XFCE (painel, sessão, Thunar etc.) | GPL-2.0-or-later / LGPL |
| picom | MPL-2.0 e MIT |
| Polybar | MIT |
| Plank | GPL-3.0-or-later |
| rofi | MIT |
| Ly | WTFPL |
| Starship | ISC |
| fastfetch | MIT |
| gum (Boas-vindas) | MIT |
| Flatpak | LGPL-2.1-or-later (apps instalados do Flathub têm licenças próprias e não vão na ISO) |
| Ícones Oxygen | LGPL-3.0-or-later |
| Fontes Noto | SIL Open Font License 1.1 |
| VLC | GPL-2.0-or-later (a libVLC é LGPL-2.1-or-later). Só a versão do openSUSE vai na ISO; o `vlc-codecs` vem do Packman durante a instalação, nunca na ISO |
| Firefox | MPL-2.0 (a marca Firefox tem regras próprias, mas o pacote do openSUSE pode ser redistribuído como está) |

## Marcas registradas

- "openSUSE" e o logo do openSUSE são marcas da SUSE. O Oniscus pode dizer
  "baseado no openSUSE Tumbleweed" (diz no `PRETTY_NAME`, nos READMEs e no app de
  Boas-vindas), mas nunca usa o nome ou o logo como marca própria. O que a imagem faz:
  - instala `branding-upstream`, `plymouth-branding-upstream` e
    `MozillaFirefox-branding-upstream` no lugar das variantes do openSUSE;
  - remove e trava `grub2-`, `wallpaper-`, `xfce4-`, `calamares-` e os outros
    pacotes `*-branding-openSUSE`, para que atualizações não os tragam de volta;
  - define `NAME="Oniscus"` e `ID=oniscus` (com `ID_LIKE=opensuse-tumbleweed`) no
    `/etc/os-release`, mantido pelo `oniscus-os-release.service` porque o
    `openSUSE-release` reescreve esse arquivo nas atualizações;
  - não usa tema no GRUB (`GRUB_DISTRIBUTOR="Oniscus"`) e tem branding próprio no
    Calamares, papel de parede, ícone do menu e greeter Ly próprios.
  - Os nomes de repositórios e pacotes (`repo-oss`, `openSUSE-release`,
    `download.opensuse.org`) ficam como estão: eles descrevem de onde vêm os
    pacotes, o que as diretrizes permitem.
- Antes de publicar, confirmar com `rpm -qa --qf '%{NAME} %{LICENSE}\n'` na
  imagem que nenhum pacote do repositório `non-oss` impede a redistribuição. Se
  houver dúvida, remover o `repo-non-oss` do `config.kiwi`.
