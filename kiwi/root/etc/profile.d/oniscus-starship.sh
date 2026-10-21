# Oniscus: Starship prompt config. Changing the accent color (onis accent)
# writes a user copy to ~/.config/oniscus/starship.toml
if [ -f "$HOME/.config/oniscus/starship.toml" ]; then
    export STARSHIP_CONFIG="$HOME/.config/oniscus/starship.toml"
else
    export STARSHIP_CONFIG=/etc/starship.toml
fi
