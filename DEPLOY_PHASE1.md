# 🚀 Deploy Phase 1 Updates

## Files Created/Updated

### New Files:
- ✅ `vector_store.py` - Semantic search engine
- ✅ `document_processor.py` - PDF/Excel/Word handler
- ✅ `PHASE1_COMPLETE.md` - Documentation
- ✅ `DEPLOY_PHASE1.md` - This file

### Updated Files:
- ✅ `requirements.txt` - Added vector search libraries
- ✅ `database.py` - Enhanced schema + new functions

## Deployment Steps

### Step 1: Upload to GitHub

**Option A: Via GitHub Website**
1. Go to your repository: `github.com/YOUR-USERNAME/intelligence-agent`
2. For each NEW file:
   - Click "Add file" → "Create new file"
   - Copy filename and content
   - Commit
3. For UPDATED files:
   - Click on file → Edit (pencil icon)
   - Replace content
   - Commit

**Option B: Via Git (if installed)**
```bash
cd intelligence-agent
git add .
git commit -m "Phase 1: Vector search foundation"
git push
```

### Step 2: Railway Auto-Deploy

Railway will automatically:
1. Detect changes
2. Rebuild with new requirements
3. Download embedding model (~80MB, one-time)
4. Initialize enhanced database
5. Restart services

**Expected Deploy Time:** 4-6 minutes

### Step 3: Verify Deployment

**Check Web Service Logs:**
```
🔧 Initializing Vector Store...
📦 Loading embedding model...
✅ Embedding model loaded (384 dimensions)
✅ Vector store initialized
✅ Database initialized successfully
```

**Check Scheduler Service Logs:**
```
🤖 Personal Intelligence Agent Scheduler Started
✅ Database initialized successfully
```

### Step 4: Test Vector Store (Optional)

**In Railway Shell (Web Service):**
```bash
python vector_store.py
```

Should see:
```
Testing Vector Store...
✅ Found: AI in Healthcare
   Similarity: 0.847
```

## What Happens on First Deploy?

### 1. Model Download (Automatic)
```
Downloading sentence-transformers model...
model.safetensors: 100%|███| 90.9M/90.9M
✅ Model cached at /mnt/data/
```

### 2. Database Migration (Automatic)
```
ALTER TABLE articles ADD COLUMN full_content TEXT
ALTER TABLE articles ADD COLUMN vector_indexed BOOLEAN
CREATE TABLE uploaded_documents...
CREATE TABLE system_config...
✅ Schema upgraded
```

### 3. Existing Data Preserved
- All your existing articles remain
- New fields added with default values
- No data loss

## Troubleshooting

### Issue: Build Failed - Memory Error
**Solution:** Vector model needs RAM
- Railway free tier: 512MB RAM
- Upgrade to Hobby tier: $5/month (512MB → 1GB)

### Issue: Model Download Timeout
**Solution:** Railway build timeout
- Retry deployment (model caches after first success)
- Or pre-download model locally and upload

### Issue: Database Locked
**Solution:** Services accessing DB simultaneously
- Restart scheduler service first
- Then restart web service
- This happens only once during migration

## Post-Deployment Checklist

- [ ] Web service running (check logs)
- [ ] Scheduler service running (check logs)
- [ ] Dashboard loads (visit Railway URL)
- [ ] No errors in logs
- [ ] Database migration complete

## Next: Phase 2 Implementation

Once deployed successfully, we'll add:
1. Vector search to chatbot
2. Document upload API
3. System prompt editor
4. Full content scraping

---

## Need Help?

**Check these first:**
1. Web service logs for errors
2. Scheduler service logs
3. Railway build logs

**Common fixes:**
- Restart services (Settings → Restart)
- Redeploy (Deployments → Redeploy)
- Check environment variables still set

---

**Ready?** Upload files to GitHub and watch Railway deploy! 🎉
