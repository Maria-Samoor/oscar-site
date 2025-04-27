FROM httpd:latest
# update to insure having latest packages, install jq for json proceessing, remove tmp packages to reduce image size
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

# copy the sh file and json file that contains the data
COPY generate_oscar_html.sh /usr/local/bin/
COPY oscar_age_gender.json /usr/local/bin/

# the working diretory
WORKDIR /usr/local/bin

# make the script executable
RUN chmod +x generate_oscar_html.sh

# run the script and copy the genrated directories to the apache server
RUN ./generate_oscar_html.sh && cp -r Years/ Names/ /usr/local/apache2/htdocs/

#change apache defult port from 80 for 8090
RUN sed -i 's/Listen 80/Listen 8090/' /usr/local/apache2/conf/httpd.conf

# the port that the container will be use
EXPOSE 8090

# command to run when start the container 
CMD ["httpd-foreground"]


# ENTRYPOINT: we can not override it unless we use --entrypoint flage, where CMD we can by adding commands after "run"
