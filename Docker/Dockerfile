FROM ubuntu:20.04

RUN apt-get update && apt-get install -y sqlite3 python3.8 curl pip

COPY src/ /src

RUN pip install -r /src/requirements.txt

COPY Docker/entry.sh /usr/local/bin/entry.sh
RUN chmod a+x /usr/local/bin/entry.sh

ENTRYPOINT ["/bin/sh", "/usr/local/bin/entry.sh"]