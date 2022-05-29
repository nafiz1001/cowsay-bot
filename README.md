# Cowsay Bot

A cowsay discord bot written in python

## Usage

1. Create a Discord bot. You can follow tutorials such as [this](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/). You need the token of the bot for later steps. You can skip the OAuth2 part.
1. Obtain the guild ID of all the servers your bot will join. I did not test my project with bot invitation.
1. Install dependencies: `pip install -r requirements`
1. Star the bot: `TOKEN="your token" GUILD_IDS="guild IDs separated by a single space" ./cowsaw-bot`

### Docker Usage

1. `docker build -t "cowsay-bot" .`
2. `docker run -e "TOKEN=your token" -e "GUILD_IDS=guild IDs separated by a single space" cowsay-bot`