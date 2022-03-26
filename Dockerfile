FROM dacom/mapscript:7.4.3

RUN useradd -m cropx && echo "cropx:cropx" | chpasswd && adduser cropx sudo
ENV INSTALLDIR /opt/

# make installdir writable for user cropx
RUN mkdir ${INSTALLDIR}weather_service
RUN chown cropx ${INSTALLDIR} /var/tmp ${INSTALLDIR}weather_service

WORKDIR ${INSTALLDIR}weather_service
COPY setup/requirements.txt .
RUN pip3 install -r requirements.txt && pip3 install gunicorn==18

# write git hash to file, this is used by Sentry
ARG CROPR_GIT_HASH
RUN echo $CROPR_GIT_HASH > .cropx_git_hash
COPY --chown=cropx weather_service/ weather_service/
COPY --chown=cropx setup/ setup/
COPY --chown=cropx manage.py .

RUN mkdir -p /var/log/weather_service/

USER cropx

#ENTRYPOINT ["/bin/bash", "/opt/weather_service/setup/docker/entrypoint.sh"]
CMD ${INSTALLDIR}weather_service/setup/gunicorn/gunicorn_start.sh weather_service ${INSTALLDIR}
