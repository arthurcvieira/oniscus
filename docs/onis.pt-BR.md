# onis: Boas-vindas e canivete suíço do sistema

[English](onis.md) (versão principal)

O `onis` é um app de terminal (bash + [gum](https://github.com/charmbracelet/gum))
com um menu para as tarefas do dia a dia. Cada item do menu também é um subcomando em inglês.
`oniscus` é um apelido mais longo para o mesmo comando.
Telas: https://claude.ai/artifact/QfMMoxgQ4zfsemw85F8gTq

## Arquivos

| Arquivo | O quê |
|---|---|
| `kiwi/root/usr/local/bin/onis` | o app |
| `kiwi/root/usr/share/oniscus/catalog.tsv` | catálogo de instalação por categoria (formato descrito no arquivo) |
| `kiwi/root/usr/share/oniscus/agent/AGENTS.md` | guia para agentes de IA (mapa das configs, regras de segurança, receitas), em inglês |
| `kiwi/root/usr/share/oniscus/agent/skills/oniscus/SKILL.md` | o mesmo guia como skill de agente |
| `kiwi/root/etc/profile.d/oniscus-local-bin.sh` | põe `~/.local/bin` no PATH (usado pelos instaladores dos agentes) |
| `kiwi/root/etc/profile.d/oniscus-starship.sh` | usa a cópia do prompt do usuário depois de trocar o realce |

Pacotes acrescentados ao `config.kiwi`: `gum`, `xdg-utils`, `libnotify-tools`, `flatpak`.

## Como abre

- A cada login, no terminal da sessão, que vira um shell normal depois de
  "Sair" (`exec onis welcome --autostart` no i3 config). Desliga em Preferências ou
  com `onis welcome off`; aí o terminal abre sem o menu.
- `Super+Alt+Espaço` abre o mesmo menu no rofi (`onis menu`); ações que precisam
  de terminal abrem um flutuante. `Super+Espaço` é o lançador de apps.
- Na ISO live, o primeiro item é "Instalar o Oniscus neste computador" (`oniscus-install`, que abre o Calamares como root).

## Idioma

Inglês é o padrão. Quando a `LANG` da sessão começa com `pt`, o texto do menu
aparece em português do Brasil. Comandos, nomes de arquivos, comentários de
código, o guia dos agentes e a saída do `onis doctor` são sempre em inglês.
Cada texto fica no script como `t "English" "Português"`.

## Comandos

```
onis                           Boas-vindas
onis menu                      o mesmo menu no rofi
onis install [app]             catálogo por categoria, ou busca no Tumbleweed + Flathub
onis uninstall [--purge] [app]   remove um app; --purge também tira dependências órfãs, dados do usuário e cache
onis uninstall --cleanup       remove pacotes órfãos, runtimes Flatpak sem uso e caches de pacotes
onis agent [ask "tarefa"]      agente de IA padrão com o guia do Oniscus
onis agent default [comando]   claude, codex, gemini, opencode ou hermes
onis agent crashes on|off      oferecer o agente quando um programa travar
onis doctor                    relatório do sistema, só leitura
onis accent [#hex|default]     cor de realce no tema todo
onis wallpaper [--apply]       escolher ou aplicar o papel de parede
onis keys [show|change|new|remove|restore]
onis update [--yes]            zypper dup (com ponto de restauração do snapper) + apps Flatpak (usuário e sistema)
onis drivers [nvidia|codecs]   driver da NVIDIA e codecs do Packman (opcionais, mesmos comandos do instalador)
onis snapshot [list|create|diff|delete|rollback]  pontos de restauração do snapper
onis restart-bars | about | welcome on|off
onis help [comando]            ajuda completa; também onis <comando> --help
```

## Ajuda e manual

- `onis help` lista todos os comandos por área; `onis help <comando>` e
  `onis <comando> --help` mostram os detalhes de um comando, no idioma do menu.
- `man onis` (inglês) e, numa sessão em português, `man onis` em pt_BR.
  Arquivos: `kiwi/root/usr/local/share/man/man1/onis.1` e
  `kiwi/root/usr/local/share/man/pt_BR/man1/onis.1` (mais os aliases `oniscus.1`).
  O pacote `man` entrou no `config.kiwi`.

## Snapshots

`onis snapshot` é uma interface para o snapper em `/` (o `/home` do usuário é
um subvolume separado e nunca é mexido):

- `list` mostra os snapshots do mais novo ao mais antigo, `*` em uso, `+` próximo boot.
- `create [descrição]`, `diff <n> [m]` (arquivos que mudaram, por padrão contra agora),
  `delete <n>` (recusa o snapshot em uso e o padrão).
- `rollback <n>` roda `snapper rollback`, explica que o sistema volta àquele
  snapshot no próximo reinício e que o estado atual fica guardado, e oferece reiniciar.
- Tudo usa sudo; na ISO live não há snapshots e o onis avisa.

## Instalação

- Categorias: Agentes de IA, Navegadores, Pacote Office, Design, Desenvolvimento,
   Comunicação, Multimídia, Jogos, Utilitários. As linhas vêm do `catalog.tsv`.
- Origens, em ordem de preferência: repositórios do Tumbleweed (`zypper`),
  Flathub (`flatpak --user`, sem sudo; o remote flathub é adicionado por usuário
  no primeiro uso) e, para agentes de IA, o instalador oficial do projeto ou npm
  em `~/.local`. O comando exato aparece antes de rodar.
- "Instalar outro pacote" busca com `zypper search` e `flatpak search` juntos.
- O Claude Desktop não está na lista: a versão Linux só existe como `.deb` para Ubuntu/Debian.

## Desinstalar

- Mostra agentes de IA, apps Flatpak e pacotes do sistema numa lista só, com filtro.
- "Remover só o app" ou "Remover e limpar tudo": a limpeza usa `zypper remove --clean-deps`
  (dependências órfãs), `flatpak uninstall --delete-data` + `--unused` e oferece
  apagar as pastas do app em `~/.config`, `~/.local/share` e `~/.cache`.
- Antes de remover um pacote do sistema, roda um teste do zypper (dry run), mostra
  a lista e recusa se algo da lista protegida (kernel, systemd, zypper, i3, XFCE,
  Ly, gum, flatpak...) for junto.
- "Limpar" remove os `zypper packages --unneeded`, roda `zypper clean --all`,
  `flatpak uninstall --unused` e apaga cópias antigas da config do i3.

## Agentes de IA no nível do sistema

Os agentes podem cuidar da própria máquina:

- O guia é ligado como `AGENTS.md`, `CLAUDE.md` e `GEMINI.md` em
  `~/.local/share/oniscus/agent/` (a pasta onde o agente abre), e a skill em
  `~/.claude/skills`, `~/.codex/skills`, `~/.agents/skills`,
  `~/.config/opencode/skills` e `~/.hermes/skills` (`onis agent link`, a cada login).
- `Super+Ctrl+Shift+a` ou `onis agent` abre o agente padrão e pergunta o que resolver.
- `onis agent watch-crashes` (iniciado pelo i3) acompanha o journal do usuário e
  mostra a notificação "Pedir ao agente" quando um programa gera core dump.
- Segurança: os agentes rodam como o usuário, nunca como root. O guia exige um sim
  antes de qualquer `sudo`, snapshot do snapper antes de mudar o sistema e só
  fontes oficiais. O Oniscus não abre os agentes no modo "sem
  perguntar". Na ISO live o usuário `live` tem sudo sem senha, então ali o sim do
  usuário dentro do agente é a única trava.

## Cor de realce

Troca Amarelo/Mel/Âmbar pela chave, não pelo valor (o amarelo ANSI e as outras
cores da paleta ficam como estão), nas cópias do usuário: linha `client.focused`
do i3, `accent` da Polybar, cores do fastfetch, `~/.config/oniscus/starship.toml`,
cópia do tema GTK em `~/.local/share/themes/Xi3-Retro`, cópia do tema do rofi em
`~/.local/share/rofi/themes/oniscus.rasi` (chaves `accent`, `accent-light`,
`accent-dark`) e cursor do terminal
(xfconf). A tela de login Ly só muda se o usuário aceitar (sudo). O estado fica
em `~/.config/oniscus/`.

## Atalhos do i3

Edita `~/.config/i3/config`, guarda uma cópia `config.oniscus-<data>`, recusa
combinação já usada, valida com `i3 -C` e volta a cópia se o i3 recusar.

## A conferir no primeiro build real

- Nomes de pacotes do catálogo (`zypper info`), principalmente `ollama`, `steam`
  (non-oss), `xournalpp`, `docker`, `chromium`.
- `zypper install /usr/bin/npm` resolve o pacote do npm.
- `journalctl --user` recebe as mensagens do systemd-coredump; `notify-send --action`
  funciona com o xfce4-notifyd.
- Gemini CLI e Hermes leem as pastas de skills acima.
- O rofi aceita os `-theme-str` usados pelo `onis menu`.
