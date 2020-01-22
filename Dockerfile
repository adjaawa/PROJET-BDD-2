FROM ubuntu:latest
RUN apt -y update 
RUN apt install -y python3 
RUN apt install -y python3-pip 
RUN pip3 install pyparsing
RUN pip3 install texttable
WORKDIR /app
COPY ./api.py /app
COPY ./sqlparsing.py /app
COPY ./function_utils.py /app
COPY ./server.py /app
COPY ./users.txt /app
COPY ./schools.json /app
COPY ./script.sh /app
CMD ["bash", "/app/script.sh"]

