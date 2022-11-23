FROM ubuntu:20.04

EXPOSE 5000/tcp

RUN apt-get update && apt-get install -y sqlite3 python3.8 curl pip

COPY project-app/ /src/project-app

RUN pip install -r /src/project-app/requirements.txt
RUN pip install /src/project-app/.

COPY Docker/entry.sh /usr/local/bin/entry.sh
RUN chmod a+x /usr/local/bin/entry.sh

ENTRYPOINT ["/bin/sh", "/usr/local/bin/entry.sh"]