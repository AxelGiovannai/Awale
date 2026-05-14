FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      python3-tk tk tcl \
      xvfb \
      x11vnc \
      libwayland-client0 libwayland-cursor0 \
      libx11-6 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x24 & export DISPLAY=:99 && x11vnc -display :99 -forever -nopw & python Main.py"]