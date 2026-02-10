# bathscurl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install -g @anthropic-ai/claude-code
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
claude


1
211