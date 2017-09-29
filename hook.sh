#------------------------------------------------------------------------------
# Autocorrect hooks.
#------------------------------------------------------------------------------

# Add hook for autocorrect.
if [ -n "$ZSH_VERSION" ]; then
  alias __hist_last_cmd__="fc -ln -1"
else
  alias __hist_last_cmd__="history 1 | cut -c 8-"
fi

__prompt_command() {
  local EXIT="$?"

  local HISTTIMEFORMAT=""
  HISTCMD_previous=$(__hist_last_cmd__)

  # Only consider errors where the exit status of 127 indicates
  # "Command not found".
  if [[ $EXIT -eq "127" ]]; then
    if [[ $HISTCMD_previous != "$HISTCMD_last" ]]; then
      HISTCMD_last=$HISTCMD_previous
      source autocorrect "$HISTCMD_previous" "$EXIT"
    fi
  fi

  HISTCMD_last=$HISTCMD_previous
}
export PROMPT_COMMAND="__prompt_command"

# Zsh-specific hooks
precmd() {
  eval "$PROMPT_COMMAND"
  RPROMPT=""
}
