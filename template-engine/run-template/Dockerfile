FROM ritclizup/rit-python3-runner

USER root

RUN mkdir /rit
COPY . /rit
RUN sed -i 's/\r//g' /rit/set_umask.sh
RUN sed -i 's/\r//g' /rit/run.sh
RUN chmod +x /rit/set_umask.sh
ENV PATH="/root/.local/bin:${PATH}"

RUN apt-get --allow-releaseinfo-change update

RUN apt-get install -y git
RUN git config --global user.email "ritchie.cloud@zup.com"
RUN git config --global user.name "ritchiecloud"
RUN git config --global credential.helper store
RUN apt-get install -y tree

RUN apt-get install -y curl \
  && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
  && apt-get install -y nodejs \
  && curl -L https://www.npmjs.com/install.sh | sh

RUN pip3 install --user --disable-pip-version-check -U /rit/framework
RUN pip3 install -r /rit/requirements.txt --user --disable-pip-version-check

WORKDIR /app
ENTRYPOINT ["/rit/set_umask.sh"]
CMD ["/rit/run.sh"]
