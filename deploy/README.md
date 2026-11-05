# Deploying ccp-engine (D75)

Nothing here runs by itself: the service goes public only when the person says so («publícalo»).

1. Commit, then `tools/package.sh` (it stamps HEAD into dist/ccp-service/VERSION, copies this Dockerfile and the
   requirements, refuses secrets, and smoke-tests the package locally).
2. Deploy to Cloud Run in the FOAAP project (always name the project: the gcloud default has changed by itself before):

       gcloud run deploy ccp-engine --project gen-lang-client-0698758883 --source dist/ccp-service \
         --region europe-southwest1 --allow-unauthenticated --set-env-vars CCP_TOKEN="$(cat deploy/.ccp-token)" \
         --memory 1Gi --cpu 1 --timeout 120 --concurrency 1 --max-instances 4 --quiet

   deploy/.ccp-token is the API key for the keyed routes (POST /v1/verificar, /v1/regras/*); it is gitignored and never
   printed. Public without a key: /v1/saude, /v1/openapi.json, /v1/lei.json, /v1/manifesto.json, /v1/exemplo/*.
3. After every law or rule change that verify passes (tools/refresh.py --apply does this daily), package and deploy again.

What the service never does is in tools/serve.py's docstring: no writes, no model, no network, no request body logged.
