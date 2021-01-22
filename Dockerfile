FROM debian:stable-slim
ARG godot_url 

RUN apt update && apt install -y curl unzip && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/local/bin/server/
RUN cd /usr/local/bin/server/ && curl -o godot.zip $godot_url && unzip godot.zip && rm godot.zip && mv Godot* server && chmod +x server
COPY server.pck /usr/local/bin/server/

WORKDIR /usr/local/bin/server/
CMD ["/usr/local/bin/server/server"]