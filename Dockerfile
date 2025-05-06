# lightweight base image
FROM httpd:alpine
# install jq for json file proceessing and bash, remove tmp packages to reduce image size
RUN apk add --no-cache jq bash && rm -rf /var/cache/apk/*

# copy the script with execute permission file and json file that contains the data
COPY --chmod=755 generate_oscar_html.sh /usr/local/bin/
COPY oscar_age_gender.json /usr/local/bin/

# the working diretory
WORKDIR /usr/local/bin

# run the script and copy the genrated directories to the apache server and then clean up
RUN ./generate_oscar_html.sh && \
    cp -r Years/ Names/ /usr/local/apache2/htdocs/ && \
    chown -R www-data:www-data /usr/local/apache2/htdocs/ && \
    rm -rf Years/ Names/ generate_oscar_html.sh oscar_age_gender.json

# apache hardening configurations to reduce amount of info server send to production env
RUN sed -i \
    -e 's/^Listen 80/Listen 8090/' \
    -e 's/^#ServerName www.example.com:80/ServerName localhost:8090/' \
    -e 's/^#ServerSignature On/ServerSignature Off/' \
    -e 's/^ServerTokens OS/ServerTokens Prod/' \
    /usr/local/apache2/conf/httpd.conf && \
    echo -e "\n\
# security headers\n\
FileETag None\n\
TraceEnable Off\n\
\n\
# directory access\n\
<Directory \"/usr/local/apache2/htdocs\">\n\
    Options Indexes FollowSymLinks\n\
    AllowOverride None\n\
    Require all granted\n\
</Directory>" >> /usr/local/apache2/conf/httpd.conf

# the port that the container will be use
EXPOSE 8090

# command to run when start the container 
CMD ["httpd-foreground"]

# ENTRYPOINT: we can not override it unless we use --entrypoint flage, where CMD we can by adding commands after "run"
