FROM frolvlad/alpine-python3

ARG babelserver_port=8087
ENV BABELSERVER_PORT=$babelserver_port

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY babelfish.py babelfish.py
COPY babelserver.py babelserver.py
COPY babel_imports.py babel_imports.py
COPY test.py test.py

EXPOSE $babelserver_port

ENTRYPOINT ["python", "test.py"]
