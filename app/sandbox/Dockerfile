FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Create non-root user
RUN useradd -m analyst

# Install required tools (including libcap2-bin for setcap)
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    strace \
    tcpdump \
    procps \
    net-tools \
    iproute2 \
    inotify-tools \
    file \
    curl \
    ca-certificates \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /analysis

COPY monitor_agent.py /analysis/monitor_agent.py
COPY entrypoint.sh /analysis/entrypoint.sh

RUN chmod +x /analysis/entrypoint.sh

# Correct dynamic capability assignment
RUN setcap cap_net_raw,cap_net_admin=eip $(which tcpdump)

RUN chown -R analyst:analyst /analysis

USER analyst
ENTRYPOINT ["/analysis/entrypoint.sh"]