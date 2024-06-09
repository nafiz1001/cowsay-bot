FROM docker.io/library/python:3.11.9-alpine3.20

WORKDIR /usr/src/cowsay-bot

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser -HD bot
COPY --chown=bot . .
USER bot

# provide TOKEN and GUILD_IDS environment variables
CMD [ "./cowsay-bot.py" ]
