FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# Create non-root user
# -----------------------------
RUN useradd -m analyst

# -----------------------------
# Install required tools
# -----------------------------
RUN apt update && apt install -y \
    python3 \
    strace \
    tcpdump \
    procps \
    net-tools \
    iproute2 \
    file \
    curl \
    ca-certificates \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Setup working directory
# -----------------------------
WORKDIR /analysis

# Copy sandbox agent + entrypoint
COPY monitor_agent.py /analysis/monitor_agent.py
COPY entrypoint.sh /analysis/entrypoint.sh

RUN chmod +x /analysis/entrypoint.sh

# Allow tcpdump without full root
RUN setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump || true

RUN chown -R analyst:analyst /analysis

USER analyst

ENTRYPOINT ["/analysis/entrypoint.sh"]