# Docker file for development
FROM ubuntu:20.04

WORKDIR /app

RUN pip install pandas
RUN pip install openpyxl
RUN pip install dash
RUN pip install plotly
RUN pip install geopandas
RUN pip install dash
RUN pip install dash-bootstrap-components
RUN pip install dash-bootstrap-templates
RUN pip install dash-leaflet
RUN pip install dash-labs
RUN pip install dash-renderer

#--------------------------------------------------------
# Docker file for deployment
#FROM python:3.8-slim-buster

#WORKDIR /app

#RUN pip install pandas
#RUN pip install openpyxl
#RUN pip install dash
#RUN pip install plotly
#RUN pip install geopandas
#RUN pip install dash
#RUN pip install dash-bootstrap-components
#RUN pip install dash-bootstrap-templates
#RUN pip install dash-leaflet
#RUN pip install dash-labs
#RUN pip install dash-renderer

#ADD . /app/

#ENTRYPOINT [ "python3" ]
#CMD ["dashboard/app.py"]
