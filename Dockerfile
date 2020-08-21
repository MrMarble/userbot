FROM python:3.8.2-slim-buster

# Ouput to the terminal without buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /bot

WORKDIR /bot

# Install chromium fot carbonsh module, this way is cached to the image so no need to install it on every run
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends

# It won't run from the root user.
RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
    && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY userbot ./userbot

CMD ["python", "-m", "userbot"]