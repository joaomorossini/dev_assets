# ALIASES
alias python="python3"

# FUNCTIONS
## Use the latest Python version for creating virtual environments
create_venv() {
    latest_python=$(ls -1 /usr/bin/python* | grep -v "python2" | sort -V | tail -n1)
    python -m venv --python="$latest_python" "$1"
}

# ENVIRONMENT VARIABLES
## Google Cloud SDK
if [ -f '/Users/morossini/google-cloud-sdk/path.zsh.inc' ]; then 
    . '/Users/morossini/google-cloud-sdk/path.zsh.inc'
fi

if [ -f '/Users/morossini/google-cloud-sdk/completion.zsh.inc' ]; then 
    . '/Users/morossini/google-cloud-sdk/completion.zsh.inc'
fi

## Postgres
export PATH="$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin"

## Modular
export MODULAR_HOME="$HOME/.modular"
export PATH="$MODULAR_HOME/pkg/packages.modular.com_mojo/bin:$PATH"

## Python
export PATH="/Users/morossini/Library/Python/3.10/bin:$PATH"

## Pipx
export PATH="$PATH:/Users/morossini/.local/bin"

## NVM
export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm


# INITIALIZATION

## Conda Initialization
__conda_setup="$('/Users/morossini/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/Users/morossini/anaconda3/etc/profile.d/conda.sh" ]; then
        . "/Users/morossini/anaconda3/etc/profile.d/conda.sh"
    else
        export PATH="/Users/morossini/anaconda3/bin:$PATH"
    fi
fi
unset __conda_setup

## Pyenv Initialization
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init --path)"
fi

# KEYBINDINGS
bindkey '^[[1;5D' beginning-of-line ## Manually added on Jul-10-2024 by João Morossini

# OTHER

## Fabric
if [ -f "/Users/morossini/.config/fabric/fabric-bootstrap.inc" ]; then 
    . "/Users/morossini/.config/fabric/fabric-bootstrap.inc"
fi

## Jina.AI: Simplify using Jina.AI Reader with Fabric
jina () {
    curl "https://r.jina.ai/$1"
}
