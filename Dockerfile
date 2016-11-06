# Dockerfile
FROM python:2-onbuild
COPY start.sh /start.sh
EXPOSE 8000
CMD ["/start.sh"]