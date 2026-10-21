# Oniscus: AI agent installers (onis install) put their commands in
# ~/.local/bin, so it must be on PATH
case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *) export PATH="$HOME/.local/bin:$PATH" ;;
esac
