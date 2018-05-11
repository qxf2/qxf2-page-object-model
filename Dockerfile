#Dockerfile to build an image which supports testing our Qxf2 Page Object Model.
#Pull ubuntu 16.04 base image
FROM ubuntu
MAINTAINER Qxf2 Services

# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
	software-properties-common \
    unzip \
    curl \
    xvfb \

	
# Chrome browser to run the tests
ARG CHROME_VERSION = "latest"
if ["${CHROME_VERSION}" = "latest"]; then
    RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
	&& echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
	&& mkdir -p /usr/share/desktop-directories \
	&& apt-get -y update && apt-get install -y google-chrome-stable
else
	RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add \
      && wget https://www.slimjet.com/chrome/download-chrome.php?file=lnx%2Fchrome64_$CHROME_VERSION.deb \
	  && dpkg -i download-chrome*.deb || true	  
    RUN apt-get install -y -f \
      && rm -rf /var/lib/apt/lists/*
fi 
	  
# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
	&& echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
	&& chmod 755 /opt/google/chrome/google-chrome

# Chrome Driver
ARG CHROME_DRIVER_VERSION="latest"
if ["${CHROME_DRIVER_VERSION}" = "latest"]; then
	RUN mkdir -p /opt/selenium \
	&& curl http://chromedriver.storage.googleapis.com/2.30/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
	&& cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;
else
	RUN mkdir -p /opt/selenium \
        && curl http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -o /opt/selenium/chromedriver_linux64.zip \
        && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;
fi	

# Firefox browser to run the tests
RUN apt-get install -y firefox

# Gecko Driver
ENV GECKODRIVER_VERSION 0.16.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GECKODRIVER_VERSION/geckodriver-v$GECKODRIVER_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GECKODRIVER_VERSION \
  && chmod 755 /opt/geckodriver-$GECKODRIVER_VERSION \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/geckodriver \
  && ln -fs /opt/geckodriver-$GECKODRIVER_VERSION /usr/bin/wires
  
# Python 2.7 and Python Pip
RUN apt-get update 
RUN apt-get install -y \
    python \
    python-setuptools \
    python-pip