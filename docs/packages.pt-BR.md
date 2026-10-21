# Pacotes e repositório do Oniscus

[English](packages.md)

O Tumbleweed é rolling release, então os arquivos próprios do Oniscus precisam ser
atualizados do mesmo jeito que o resto do sistema. Eles viram pacotes RPM
construídos no [Open Build Service](https://build.opensuse.org) (OBS), o serviço
de build gratuito do openSUSE, e publicados num repositório do Oniscus. Sistemas
instalados recebem versões novas com `onis update` (que roda `zypper dup`), sem
reinstalar.

## Pacotes

| Pacote | Conteúdo |
|---|---|
| `onis` | o comando `onis` (`/usr/bin/onis`, alias `oniscus`), páginas de manual, catálogo de apps, guia dos agentes de IA |
| `oniscus-branding` | nome no os-release e o serviço de boot que o mantém, logo, ícone do menu, papel de parede, temas Xi3 Retro do GTK e do Plank |
| `oniscus-desktop` | padrões do sistema (configurações do XFCE, painel, apps padrão, Starship, Plank), a sessão do Ly, as configs copiadas para usuários novos, e `Requires` da pilha do desktop (i3, Polybar, picom, Plank, rofi...) |

O `packaging/manifest.tsv` diz qual arquivo do `kiwi/root` vai para qual pacote e
para onde. O spec (`packaging/oniscus.spec`) e o `build.sh` leem esse arquivo,
então colocar um arquivo novo num pacote é uma linha só.

### Como as atualizações chegam

- Arquivos em `/usr` (onis, temas, logo, papel de parede) são trocados a cada
  atualização.
- Arquivos em `/etc` são `%config(noreplace)`: se o admin mudou um, a atualização
  mantém o dele e salva o novo ao lado como `.rpmnew`.
- Os padrões do sistema ficam em `/etc/xdg/oniscus` em vez de `/etc/xdg`, para
  nunca bater com arquivos de pacotes do XFCE ou do openSUSE. A sessão do Oniscus
  abre o XFCE com `XDG_CONFIG_DIRS=/etc/xdg/oniscus:/etc/xdg`.
- Dependências novas também chegam: se o `oniscus-desktop` passar a exigir um
  pacote novo, o `zypper dup` instala.
- Limite: arquivos do `/etc/skel` só são copiados quando o usuário é criado.
  Mudanças neles chegam a usuários novos, não ao `~/.config` que já existe (i3,
  Polybar, picom, fastfetch). Passar esses para padrões do sistema fica para
  depois.

### Fora dos pacotes (só na imagem)

`/etc/ly/config.ini` (é do pacote `ly`), `/etc/dconf/profile/user`, os arquivos
do instalador Calamares e o atalho "Instalar o Oniscus". Continuam no
`kiwi/root`. Na imagem Release o `/etc/bash.bashrc.local` é só uma linha que
carrega `/usr/share/oniscus/shell/bashrc.sh`, do `oniscus-desktop`.

## Dois jeitos de gerar a ISO

| | `./build.sh` (Dev, padrão) | `PROFILE=Release ./build.sh` |
|---|---|---|
| Arquivos do Oniscus | copiados do `kiwi/root` | instalados do repositório do Oniscus |
| Atualização no sistema instalado | não (os arquivos não são de nenhum pacote) | sim, com `onis update` |
| Serve para | testar mudanças antes de lançar | a ISO que você publica |

O modo Release copia `kiwi/` para `out/description`, tira os arquivos listados no
manifesto, põe o `packaging/release-overlay/` e gera com o perfil `Release` do
KIWI (repositório do Oniscus + `onis`, `oniscus-branding`, `oniscus-desktop`).

## Configuração inicial (Arthur, uma vez só)

Os nomes abaixo supõem o repositório GitHub `arthurcvieira/oniscus` e o projeto
OBS `home:oniscus` (usuário `oniscus` no OBS). Se escolher outros, troque em
`packaging/obs/*`, `packaging/oniscus.spec` (URL) e `kiwi/config.kiwi` (caminho do
repositório).

1. **GitHub**: crie o repositório e envie o conteúdo de `distro/` para a raiz
   (`kiwi/`, `packaging/`, `docs/`... no topo). Marque a primeira versão:
   `git tag v0.1.0 && git push --tags`.
2. **Conta no OBS**: cadastre-se em https://build.opensuse.org (é a conta do
   openSUSE, grátis). Crie o usuário `oniscus`: o projeto pessoal dele,
   `home:oniscus`, guarda os pacotes do Oniscus.
3. **osc** (linha de comando do OBS), numa máquina openSUSE:
   `sudo zypper install osc obs-service-obs_scm obs-service-tar obs-service-recompress obs-service-set_version`
4. **Projeto e pacote**:
   ```sh
   osc meta prj home:oniscus -F packaging/obs/project-meta.xml
   osc meta pkg home:oniscus oniscus -F packaging/obs/package-meta.xml
   osc checkout home:oniscus/oniscus && cd home:oniscus/oniscus
   cp <repo>/packaging/obs/_service .
   osc add _service && osc commit -m "Build from GitHub"
   ```
   O OBS roda o serviço (busca o GitHub, pega o spec) e constrói. Acompanhe em
   https://build.opensuse.org/package/show/home:oniscus/oniscus
5. **Reconstruir a cada push**: crie um token e cadastre como webhook no GitHub.
   ```sh
   osc token --create --operation runservice home:oniscus oniscus
   ```
   No GitHub: Settings, Webhooks, Add webhook. Payload URL
   `https://build.opensuse.org/trigger/webhook?id=<id do token>`, content type
   `application/json`, secret = o texto do token, evento "Just the push event".
6. **Chave do repositório** para a ISO Release (o OBS assina o repositório):
   `osc signkey home:oniscus > packaging/oniscus-repo.asc` e faça
   commit. O `build.sh` passa a chave para o KIWI, que confia nela dentro da
   imagem.

O repositório fica em
`https://download.opensuse.org/repositories/home:/oniscus/openSUSE_Tumbleweed/`.

## Lançar uma atualização

1. Mude os arquivos em `kiwi/root` (e o manifesto, se o arquivo for novo).
2. Escreva uma entrada em `packaging/oniscus.changes` (`osc vc` faz o cabeçalho).
3. Faça push. O webhook reconstrói; a versão é a última tag mais os commits
   (`0.1.0+git3.abc1234`). Crie a tag `vX.Y.Z` para uma versão com nome.
4. Os usuários recebem com `onis update`. O OBS reconstrói os pacotes sozinho
   quando sai snapshot novo do Tumbleweed.

## Pôr o repositório num sistema já instalado

Sistemas instalados por uma ISO Dev têm os arquivos mas não o repositório. Para
trocar:

```sh
sudo zypper addrepo -f https://download.opensuse.org/repositories/home:/oniscus/openSUSE_Tumbleweed/ oniscus
sudo zypper refresh   # aceite a chave do Oniscus
sudo zypper install --force-resolution onis oniscus-branding oniscus-desktop
```

Os pacotes passam a ser donos dos arquivos em `/usr`. As cópias antigas em
`/usr/local/bin` precisam sair (`sudo rm /usr/local/bin/{onis,oniscus,xi3-active-app}`),
senão continuam na frente das do pacote.

## O que já foi conferido

O spec gera os pacotes com `rpmbuild` (noarch, três pacotes, listas de arquivos e
`%config` como descrito). Ainda não conferido num Tumbleweed de verdade: o build
no OBS (macros do openSUSE, rpmlint), conflitos de arquivo com pacotes do
Tumbleweed (`/etc/starship.toml`, `/etc/profile.d/oniscus-*`) e o build de uma
ISO Release.
