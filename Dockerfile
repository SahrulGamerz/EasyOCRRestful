FROM python:3.10-buster

ENV PORT=3000 
ENV GIT_URL=https://github.com/SahrulGamerz/EasyOCRRestful
ENV RUN_SCRIPT=app.py

RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/li

RUN echo "#!/bin/sh" > /start.sh && \
	echo "[ -d \"/app/.git\" ] && echo Running git pull $""GIT_URL || echo Running git clone $""GIT_URL ." >> /start.sh && \
	echo "[ -d \"/app/.git\" ] && git pull $""GIT_URL || git clone $""GIT_URL ." >> /start.sh && \
	echo "echo Running pip install virtualenv" >> /start.sh && \
	echo "pip install virtualenv" >> /start.sh && \
	echo "echo Running python -m venv env" >> /start.sh && \
	echo "python -m venv env" >> /start.sh && \
	echo "echo Running . env/bin/activate" >> /start.sh && \
	echo ". env/bin/activate" >> /start.sh && \
	echo "echo Running pip install -r requirements.txt" >> /start.sh && \
	echo "pip install -r requirements.txt" >> /start.sh && \
	echo "echo Running python ./$""RUN_SCRIPT" >> /start.sh && \
	echo "python ./$""RUN_SCRIPT" >> /start.sh 

RUN chmod +x /start.sh && mkdir /app

WORKDIR /app 

EXPOSE $PORT 

HEALTHCHECK CMD curl --fail http://localhost:$PORT/health || exit 1

CMD ["/start.sh"] 