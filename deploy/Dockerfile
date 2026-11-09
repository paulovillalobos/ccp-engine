# The ccp-engine service: build from the package tools/package.sh writes (dist/ccp-service).
#   tools/package.sh && docker build -t ccp-engine dist/ccp-service
#   docker run --rm -p 8080:8080 -e PORT=8080 -e CCP_HOST=0.0.0.0 -e CCP_TOKEN=<secret> \
#     -e SUPABASE_PROJECT_REF=<ref> -e SUPABASE_DB_PASSWORD=<password> ccp-engine
# D90: the image runs db/api.py (tools/serve.py's routes plus the stored verdicts, read only from Supabase).
FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt && useradd -r -u 10001 ccp && chown -R ccp /app
USER ccp
ENV PORT=8080 CCP_HOST=0.0.0.0 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s CMD python3 -c "import urllib.request,os; urllib.request.urlopen('http://127.0.0.1:%s/v1/saude' % os.environ['PORT'])" || exit 1
CMD ["sh", "-c", "python3 -I db/api.py --host \"$CCP_HOST\" --port \"$PORT\""]
