# Kali Linux is the base image
FROM kalilinux/kali-rolling:latest

# Install necessary tools
RUN apt-get update && \
	apt-get -y upgrade && \
	DEBIAN_FRONTEND=noninteractive apt-get install -y \
	build-essential \
	git \
	python3 \
	python3-pip \
	python3.11-venv \
	golang \
	golang-go \
	whois \
	inetutils-ping \
	wafw00f \
	dnsutils \
	nmap \
	traceroute \
	masscan \
	wget \
	curl \
	ncat \
	exploitdb \
	netcat-traditional \
	metasploit-framework \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install subfinder
RUN go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
RUN cp /root/go/bin/subfinder  /usr/bin/

# Install LinkFinder
RUN git clone https://github.com/GerbenJavado/LinkFinder.git

# Copy the project into root directory
WORKDIR /root
COPY . .

# Setting port for Flask
EXPOSE 5000
