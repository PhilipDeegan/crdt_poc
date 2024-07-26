FROM debian:latest

WORKDIR /root
COPY run.sh /root
COPY models.py /root
COPY env.py /root
COPY test_conn.py /root
COPY test_db.py /root
RUN chmod +x run.sh && ./run.sh
