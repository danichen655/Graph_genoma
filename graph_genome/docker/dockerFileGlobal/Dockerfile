

FROM ghcr.io/pangenome/pggb:latest
RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y git
RUN apt install -y build-essential
RUN apt install -y zlib1g-dev
RUN apt install -y python3-pandas
RUN apt install -y python3-biopython
RUN apt install -y python3-gffutils

##RUN git clone https://github.com/lh3/minigraph.git
##RUN cd minigraph && make
##ENV PATH $PATH:/minigraph
RUN mkdir /code