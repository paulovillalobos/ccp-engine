# Deploying ccp-engine (D75)

Nothing here runs by itself: the service goes public only when the person says so («publícalo»).

1. Commit, then `tools/package.sh` (it stamps HEAD into dist/ccp-service/VERSION, copies this Dockerfile and the
   requirements, refuses secrets, and smoke-tests the package locally).
2. Deploy to Cloud Run in the FOAAP project (always name the project: the gcloud default has changed by itself before):

       gcloud run deploy ccp-engine --project gen-lang-client-0698758883 --source dist/ccp-service \
         --region europe-southwest1 --allow-unauthenticated --set-env-vars CCP_TOKEN="$(cat deploy/.ccp-token)",CCP_COMMIT="$(git rev-parse --short=9 HEAD)" \
         --set-secrets SUPABASE_PROJECT_REF=ccp-supabase-ref:latest,SUPABASE_DB_PASSWORD=ccp-supabase-password:latest \
         --memory 2Gi --cpu 1 --cpu-boost --timeout 120 --concurrency 4 --max-instances 4 \
         --startup-probe=tcpSocket.port=8080,periodSeconds=240,timeoutSeconds=240,failureThreshold=3 --quiet

   The image has no git: CCP_COMMIT names the commit served. Loading the stores takes about 4 minutes on a cold start,
   so the startup probe allows up to 12. deploy/.ccp-token must exist and be non-empty; an empty key opens the keyed routes.

   D90: the database credentials live in Secret Manager (ccp-supabase-ref, ccp-supabase-password, created once by the
   person from .env), never in the image or in a command line. The service opens its connections read only.

   deploy/.ccp-token is the API key for the keyed routes (POST /v1/verificar, /v1/regras/*); it is gitignored and never
   printed. Public without a key: /v1/saude, /v1/openapi.json, /v1/lei.json, /v1/manifesto.json, /v1/exemplo/*, and (D90) /v1/procedimentos/*,
   /v1/veredictos, /v1/entidades/*/veredictos, /v1/estatisticas (db/api.py).
3. After every law or rule change that verify passes (tools/refresh.py --apply does this daily), package and deploy again.

What the service never does is in tools/serve.py's docstring: no writes, no model, no network, no request body logged.
