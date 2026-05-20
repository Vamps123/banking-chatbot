# TODO

## Step 1: Prevent Render deploy-time OOM
- [x] Update `backend/Dockerfile` to not run `python scripts/ingest.py` by default.
- [x] Add `RUN_INGEST` env var gate around ingestion.


## Step 2: Ensure backend starts with existing vectors
- [ ] If vectors are missing, ingestion can still be triggered manually by setting `RUN_INGEST=1`.

## Step 3: (Optional) Tune embedding to lower RAM
- [ ] If SentenceTransformer still downloads too much on first run, restrict to a smaller model or defer downloads.

## Step 4: Update Render config
- [ ] Update `render.yaml` to set `RUN_INGEST=0` (or omit ingestion env).
- [ ] Redeploy and confirm no model download during deploy and no OOM.

