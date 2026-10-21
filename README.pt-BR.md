<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="art/repo/banner-dark.pt-BR.svg">
    <img alt="Oniscus" src="art/repo/banner-light.pt-BR.svg" width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://github.com/arthurcvieira/oniscus/releases/latest"><img alt="Última versão" src="https://img.shields.io/github/v/release/arthurcvieira/oniscus?include_prereleases&sort=semver&style=flat-square&label=vers%C3%A3o&color=F7C948&labelColor=1C2026"></a>
  <a href="https://github.com/arthurcvieira/oniscus/releases"><img alt="Downloads" src="https://img.shields.io/github/downloads/arthurcvieira/oniscus/total?style=flat-square&label=downloads&color=F7C948&labelColor=1C2026"></a>
  <a href="https://github.com/arthurcvieira/oniscus/stargazers"><img alt="Estrelas" src="https://img.shields.io/github/stars/arthurcvieira/oniscus?style=flat-square&logo=github&label=estrelas&color=F7C948&labelColor=1C2026"></a>
  <a href="LICENSES.pt-BR.md"><img alt="Licença" src="https://img.shields.io/badge/licen%C3%A7a-GPL--3.0--or--later-4CC27A?style=flat-square&labelColor=1C2026"></a>
  <br>
  <img alt="Baseado no openSUSE Tumbleweed" src="https://img.shields.io/badge/baseado%20no-openSUSE%20Tumbleweed-73BA25?style=flat-square&labelColor=1C2026">
  <img alt="XFCE + i3" src="https://img.shields.io/badge/desktop-XFCE%20%2B%20i3-9AA4AF?style=flat-square&labelColor=1C2026">
  <a href="https://github.com/arthurcvieira/oniscus/commits/main"><img alt="Último commit" src="https://img.shields.io/github/last-commit/arthurcvieira/oniscus?style=flat-square&label=%C3%BAltimo%20commit&color=9AA4AF&labelColor=1C2026"></a>
</p>

<p align="center">
  <b>Um Linux aconchegante que simplesmente funciona.</b><br>
  <a href="https://github.com/arthurcvieira/oniscus/releases/latest">Baixar</a> ·
  <a href="docs/onis.pt-BR.md">O comando onis</a> ·
  <a href="docs/development.pt-BR.md">Compile você mesmo</a> ·
  <a href="README.md">English</a>
</p>

---

O **Oniscus** é uma distribuição Linux feita sobre o openSUSE Tumbleweed, com um
desktop retrô e acolhedor que já está pronto quando você entra. O XFCE cuida do
dia a dia (configurações, energia, notificações, Wi-Fi, discos e arquivos)
enquanto o i3 mantém suas janelas organizadas lado a lado. Sem maratona de
configuração, sem caçar arquivos de config: é ligar e se sentir em casa.

O nome vem do *Oniscus*, o tatuzinho-de-jardim: pequeno, resistente e feliz num
cantinho aconchegante. Esse isópode é o nosso mascote, e você vai encontrá-lo
acenando no botão do menu e no terminal.

## Por que Oniscus

- **Pronto desde o primeiro boot.** Painel, dock, lançador, tema, prompt e apps
  já vêm configurados. Dá para começar a trabalhar na hora.
- **Rolling release, mas seguro.** O Tumbleweed traz o software mais novo, e toda
  atualização do sistema cria antes um ponto de restauração do
  [snapper](https://github.com/openSUSE/snapper). Se algo parecer estranho, volte
  com um comando.
- **Janelas lado a lado sem lição de casa.** O i3 organiza as janelas e o XFCE
  cuida do resto. Você tem a agilidade de um gerenciador tiling com o conforto de
  um desktop completo.
- **Um comando amigo.** O `onis` é a tela de boas-vindas e o canivete suíço do
  sistema: instale apps, atualize, crie pontos de restauração, troque cores e mais.
- **Só fontes oficiais.** Os pacotes vêm dos repositórios oficiais do Tumbleweed,
  e as peças próprias do Oniscus são RPMs comuns do
  [Open Build Service](https://build.opensuse.org/project/show/home:oniscus), que
  se atualizam junto com o resto do sistema.
- **Fala a sua língua.** Inglês por padrão, com português do Brasil incluído. As
  ferramentas do Oniscus seguem o seu `LANG`.

## Um passeio

| | |
|---|---|
| **Login** | Ly, uma tela de entrada tranquila no estilo terminal, nas cores do Oniscus |
| **Barra de cima** | menu, app em foco, Wi-Fi, bateria, relógio e busca |
| **Barra de baixo** | uma pílula flutuante com áreas de trabalho, CPU e RAM |
| **Dock** | Plank à esquerda, que sai da frente quando uma janela chega perto |
| **Lançador** | rofi, a uma tecla de distância |
| **Visual** | Xi3 Retrô: tema escuro inspirado nos anos 2000, com realce amarelo quente, ícones Oxygen e Noto Sans |
| **Movimento** | animações do picom ao abrir, fechar e redimensionar janelas |
| **Terminal** | prompt Starship e fastfetch com o mascote |
| **Mídia** | VLC para vídeo e música, PipeWire para o som |
| **Instalador** | Calamares, com drivers NVIDIA e codecs extras opcionais |

## Conheça o `onis`

O `onis` abre quando você entra e fica a um atalho de distância
(<kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>Espaço</kbd>). Todo item do menu também é
um comando:

```bash
onis install gimp        # apps do Tumbleweed e do Flathub, por categoria
onis update              # sistema + Flatpak, com ponto de restauração antes
onis snapshot list       # veja e volte pontos de restauração
onis accent "#7FB4CA"    # troca a cor de realce em todo o sistema
onis drivers nvidia      # driver NVIDIA ou codecs extras, quando quiser
onis agent               # peça ajuda ao seu agente de IA com o sistema
onis doctor              # um relatório rápido do sistema, só leitura
```

Prefere o nome longo? `oniscus` também funciona. Veja o
[guia completo](docs/onis.pt-BR.md) ou rode `onis help`.

## Atalhos úteis

| Teclas | O que faz |
|---|---|
| <kbd>Super</kbd>+<kbd>Espaço</kbd> | abrir um app |
| <kbd>Super</kbd>+<kbd>Alt</kbd>+<kbd>Espaço</kbd> | menu do `onis` |
| <kbd>Super</kbd>+<kbd>Enter</kbd> | terminal |
| <kbd>Super</kbd>+<kbd>E</kbd> | arquivos (Thunar) |
| <kbd>Super</kbd>+<kbd>1</kbd>…<kbd>9</kbd> | trocar de área de trabalho |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>Q</kbd> | fechar a janela |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>Espaço</kbd> | soltar ou encaixar a janela |
| <kbd>Super</kbd>+<kbd>F</kbd> | tela cheia |
| <kbd>Super</kbd>+<kbd>Shift</kbd>+<kbd>X</kbd> | bloquear a tela |

`onis keys` mostra todos e deixa você trocar.

## Como ter o Oniscus

1. Baixe a ISO mais recente em
   [Releases](https://github.com/arthurcvieira/oniscus/releases/latest).
2. Grave num pendrive com o Fedora Media Writer, o balenaEtcher ou
   `sudo dd if=oniscus.iso of=/dev/sdX bs=4M status=progress`.
3. Inicie pelo pendrive (UEFI) e entre com o usuário `live`, senha `live`. A tela
   de login lembra você.
4. Escolha **Instalar o Oniscus** no `onis` ou no menu. O instalador pergunta
   idioma, teclado e fuso horário, e oferece drivers NVIDIA e codecs extras se
   você quiser.

Já instalou? O `onis update` mantém tudo em dia, inclusive o próprio Oniscus.

Quer gerar a ISO você mesmo ou mexer no desktop? Veja
[docs/development.pt-BR.md](docs/development.pt-BR.md) e
[docs/packages.pt-BR.md](docs/packages.pt-BR.md).

## Licença

Os arquivos próprios do Oniscus são [GPL-3.0-or-later](COPYING), e a arte
(mascote, logos, papel de parede) é CC BY-SA 4.0. O resto vem dos repositórios
oficiais do openSUSE Tumbleweed, cada um com sua licença. Detalhes em
[LICENSES.pt-BR.md](LICENSES.pt-BR.md).

<sub>O Oniscus é um projeto independente, baseado no openSUSE Tumbleweed e sem
vínculo ou endosso do Projeto openSUSE.</sub>
