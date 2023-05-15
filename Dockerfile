#Dockerfile to build an image for running Selenium tests
#Pull ubuntu 22.04 base image
FROM ubuntu:22.04
LABEL maintainer = "Qxf2 Services"

ENV DISPLAY=:20

# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip=6.00 \
    wget=1.21.2 \
    bzip2=1.0.8 \
    xvfb \
    x11vnc=0.9.16 \
    fluxbox=1.3.5 \
    xterm

# Chrome browser to run the tests
ARG CHROME_VERSION=113.0.5672.92
RUN wget -qO /tmp/google.pub https://dl-ssl.google.com/linux/linux_signing_key.pub && apt-key add /tmp/google.pub && rm /tmp/google.pub && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list && mkdir -p /usr/share/desktop-directories && apt-get -y update && apt-get install -y google-chrome-stable=${CHROME_VERSION}-1 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome && printf "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome && chmod 755 /opt/google/chrome/google-chrome

# Chrome Driver
ARG CHROME_DRIVER_VERSION=113.0.5672.63
RUN CD_VERSION="$(if [ "${CHROME_DRIVER_VERSION:-latest}" = "latest" ]; then echo "$(wget -qO- 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE')"; else echo "${CHROME_DRIVER_VERSION}"; fi)" \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CD_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-"$CD_VERSION" \
  && chmod 755 /opt/selenium/chromedriver-"$CD_VERSION" \
  && ln -fs /opt/selenium/chromedriver-"$CD_VERSION" /usr/bin/chromedriver

RUN if [ "${CHROME_DRIVER_VERSION}" != "113.0.5672.63" ]; then \
  mkdir -p /opt/selenium && \
  wget -qO /opt/selenium/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
  unzip /opt/selenium/chromedriver_linux64.zip -d /opt/selenium && \
  rm -rf /opt/selenium/chromedriver_linux64.zip && \
  ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver; \
  fi

#Firefox browser to run the tests
ARG FIREFOX_VERSION=109.0
RUN FIREFOX_DOWNLOAD_URL="$(if [ "$FIREFOX_VERSION" = "latest" ]; then echo "https://download.mozilla.org/?product=firefox-"$FIREFOX_VERSION"-ssl&os=linux64&lang=en-US"; else echo "https://download-installer.cdn.mozilla.net/pub/firefox/releases/"$FIREFOX_VERSION"/linux-x86_64/en-US/firefox-"$FIREFOX_VERSION".tar.bz2"; fi)" \
  && apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install firefox \
  && apt-get install libdbus-glib-1-2 \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 "$FIREFOX_DOWNLOAD_URL" \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
  && ln -fs /opt/firefox-"$FIREFOX_VERSION"/firefox /usr/bin/firefox \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#Geckodriver
ARG GECKODRIVER_VERSION=0.32.2
RUN GK_VERSION="$(if [ "${GECKODRIVER_VERSION:-latest}" = "latest" ]; then echo "$(wget -qO- 'https://api.github.com/repos/mozilla/geckodriver/releases/latest' | grep '\"tag_name\":' | sed -E 's/.*\"v([0-9.]+)\".*/\1/')"; else echo "$GECKODRIVER_VERSION"; fi)" \
  && echo "Using GeckoDriver version: ""$GK_VERSION" \
  && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-"$GK_VERSION" \
  && chmod 755 /opt/geckodriver-"$GK_VERSION" \
  && ln -fs /opt/geckodriver-"$GK_VERSION" /usr/bin/geckodriver

# Python 3.5 and Python Pip
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    python3.10 \
    python3-setuptools=59.6.0-1.2ubuntu0.22.04.1 \
    python3-pip=22.0.2+dfsg-1ubuntu0.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Creating a new directory
RUN mkdir /shell_script

# Copying shell script to directory
COPY entrypoint.sh /shell_script

# Setting the working directory
WORKDIR /shell_script

# Setting the entry point
ENTRYPOINT ["/bin/bash", "/shell_script/entrypoint.sh"]

# Setting the default command to be run in the container
CMD ["sh", "-c", "Xvfb :20 -screen 0 1366x768x16 & x11vnc -passwd password -display :20 -N -forever"]
