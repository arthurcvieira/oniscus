# Desenvolvendo o Oniscus

[English](development.md)

Notas para quem compila, testa ou altera o Oniscus. Para saber o que é a distro,
veja o [README](../README.pt-BR.md).

## Estrutura do repositório

```
.
├── build.sh                      # gera a ISO com kiwi-ng
├── art/                          # gerador do papel de parede, mascote e artes do repositório
├── docs/                         # documentação
├── packaging/                    # spec RPM, manifesto de arquivos e serviço do OBS
└── kiwi/
    ├── config.kiwi               # pacotes, repositórios, tipo de imagem (ISO live UEFI)
    ├── config.sh                 # serviços, greeter, usuário live, idioma
    └── root/                     # arquivos copiados por cima da imagem
```

Os padrões do sistema ficam em `/etc/xdg` (valem para todo usuário novo), e as
configs de usuário (i3, Polybar, picom, fastfetch) ficam em `/etc/skel`, que é
copiado para o home de cada usuário criado. Como esses arquivos viram RPMs e chegam
aos sistemas instalados está em [packages.pt-BR.md](packages.pt-BR.md).

## Peças do desktop

| Peça | Escolha |
|---|---|
| Base | openSUSE Tumbleweed (rolling release) |
| Build da imagem | KIWI NG (a mesma ferramenta que o openSUSE usa) |
| Login | Ly (greeter no terminal, tty2) com as cores da marca; só a sessão Oniscus aparece |
| Gerenciador de janelas | i3 no lugar do xfwm4 (definido em `xfce4-session.xml`) |
| Barra superior | xfce4-panel: menu, app em foco, wifi, bateria, relógio, busca |
| Barra inferior | Polybar em pílula flutuante: áreas de trabalho, CPU e RAM |
| Dock | Plank à esquerda, some quando uma janela encosta (intellihide) |
| Área de trabalho | sem xfdesktop (ele cobriria o i3); papel de parede via feh |
| Lançador | rofi e xfce4-appfinder |
| Compositor | animações do picom 12 |
| Tema | temas GTK e Plank Xi3 Retrô, ícones Oxygen, Noto Sans |
| Áudio | PipeWire |
| Mídia | VLC (`vlc -I ncurses` no terminal); a etapa opcional do Packman adiciona `vlc-codecs` |
| Instalador | Calamares, config em `kiwi/root/etc/calamares/` |

## Onde está o design

Mockup interativo: https://claude.ai/artifact/5JJzRi9e9jw8pyLk2tnp5i

Arquivos dentro de `kiwi/`:

- `root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml`: barra superior
- `root/usr/local/bin/xi3-active-app`: nome do app em foco (plugin genmon + xdotool)
- `root/etc/skel/.config/xfce4/panel/launcher-7/`: botão de busca
- `root/usr/share/themes/Xi3-Retro/`: tema GTK (barras, botões, painel)
- `root/usr/share/plank/themes/Xi3-Retro/`: tema do dock
- `root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml`: tema, ícones e fonte padrão
- `root/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-terminal.xml`: cores do terminal
- `root/etc/skel/.config/picom/picom.conf`: animações das janelas
- `root/usr/share/wallpapers/xi3.jpg`: papel de parede (gerado por `art/wallpaper.py`)
- `root/etc/skel/.config/polybar/`: barra inferior e script que a inicia
- `root/etc/ly/config.ini` e `root/usr/share/oniscus/xsessions/`: greeter Ly e a sessão Oniscus
- `root/etc/starship.toml`, `root/etc/profile.d/oniscus-starship.sh`, `root/etc/bash.bashrc.local`: prompt e fastfetch
- `root/etc/skel/.config/fastfetch/` e `root/usr/share/oniscus/logo.ansi`: fastfetch com o mascote
- `root/usr/share/pixmaps/oniscus-menu.svg`: mascote no botão do menu
- `root/etc/xdg/mimeapps.list`: VLC como player de mídia padrão
- `root/etc/dconf/db/local.d/10-xi3-plank` e `root/etc/skel/.config/plank/`: dock

## Como gerar a ISO

Num openSUSE (pode ser uma VM ou um container `opensuse/tumbleweed` com privilégios):

```bash
sudo zypper install python3-kiwi kiwi-systemdeps
./build.sh
qemu-system-x86_64 -enable-kvm -m 4G -bios /usr/share/qemu/ovmf-x86_64.bin -cdrom out/*.iso
```

No Open Build Service, a imagem e os pacotes são gerados no projeto `home:oniscus`;
o OBS refaz tudo a cada mudança no Tumbleweed.

## Lista de testes

O que conferir a cada build novo:

- **Pacotes:** todo nome do `config.kiwi` existe (`zypper search`), incluindo os
  pacotes de tradução `-lang`, `calamares`, `vlc-qt` e `vlc-lang`.
- **Dock:** o i3 trata janelas do tipo "dock" como barras de cima/baixo. Ver se o
  Plank fica na esquerda dentro do i3; a alternativa é um painel vertical do XFCE
  com autohide.
- **Animações:** a sintaxe do picom 12 bate com a versão do Tumbleweed.
- **Ly:** o `config.ini` usa o formato de cor do Ly 1.1+ (`0xSSRRGGBB`); o serviço é
  `ly.service` ou `ly@tty2.service`.
- **Painel:** o plugin de bateria é o `xfce4-battery-plugin` (o xfce4-power-manager do Tumbleweed não tem plugin de painel).
- **Branding:** `branding-upstream`, `plymouth-branding-upstream` e
  `MozillaFirefox-branding-upstream` existem, nada traz o logo do openSUSE de volta
  (`rpm -qa '*branding*'`), e GRUB, Plymouth, `/etc/issue` e fastfetch dizem Oniscus.
- **VLC:** o VLC 3 instala `vlc.desktop` (usado em `/etc/xdg/mimeapps.list`); o VLC 4
  troca para `org.videolan.vlc.desktop`.
- **Lançadores do dock:** os nomes `.desktop` (thunar, xfce4-terminal, firefox,
  org.xfce.mousepad, xfce-settings-manager).
- **Instalador:** a ISO live sobe em inglês, teclado US e UTC. O Calamares pergunta
  idioma, teclado e fuso, cria a conta do usuário e remove o usuário live, o sudo
  sem senha e o aviso dele no Ly. A cópia do sistema live em execução (`unpackfs` a
  partir de `/`) precisa funcionar com a imagem live do KIWI. As etapas opcionais
  de NVIDIA e Packman são baixadas durante a instalação
  (`calamares/modules/contextualprocess-oniscus-extras.conf`).

Um menu global estilo Mac não está incluído: depende do vala-panel-appmenu, que não
está nos repositórios oficiais.

## Nome

As regras de marca do openSUSE não permitem usar o nome ou o logo "openSUSE" como
nome de uma distro; "baseada no openSUSE Tumbleweed" é permitido. "Oniscus" é sempre
escrito numa cor só em logos e artes.
