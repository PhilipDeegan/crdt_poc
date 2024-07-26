FROM debian:latest

WORKDIR /root
COPY run.sh /root
COPY test_conn.py /root
RUN chmod +x run.sh && ./run.sh
