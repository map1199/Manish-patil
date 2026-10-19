# Upload Guide (username: map1199)

Your existing repo `Manish-patil` is empty, so you can either delete it or reuse it. For a profile page, you need **3 repos**:

| Repo name (exact) | Contents |
|---|---|
| `map1199` | `profile/README.md` (rename to README.md). Shows on your profile |
| `sales-etl-data-warehouse` | the whole `sales-etl-data-warehouse` folder |
| `aws-serverless-data-pipeline` | the whole `aws-serverless-data-pipeline` folder |

## For each repo (Git Bash / terminal)
```bash
# 1. Create the empty repo on github.com (New > name > Public), then:
cd sales-etl-data-warehouse
git init
git add .
git commit -m "Initial commit: ETL pipeline and star-schema warehouse"
git branch -M main
git remote add origin https://github.com/map1199/sales-etl-data-warehouse.git
git push -u origin main
```
Repeat with `aws-serverless-data-pipeline`, and for `map1199` copy only README.md.

## Commit like a real project (looks better than one big upload)
Split into several commits, e.g.:
```bash
git add src/generate_data.py && git commit -m "Add synthetic raw data generator"
git add sql/schema.sql        && git commit -m "Add star schema DDL"
git add src/etl.py            && git commit -m "Add extract-transform-load pipeline"
git add sql/analytics.sql src/run_analytics.py && git commit -m "Add analytical queries"
git add src/test_etl.py       && git commit -m "Add data-quality tests"
git add README.md .gitignore requirements.txt && git commit -m "Add documentation"
```

## After uploading
- Pin both project repos on your profile (Customize your pins)
- Add Topics to each repo (python, sql, etl, data-engineering, aws)
- Add a repo description and take a screenshot of the Athena results for the AWS README
