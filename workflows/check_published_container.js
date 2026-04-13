const sqlite3 = require('/usr/local/lib/node_modules/n8n/node_modules/.pnpm/sqlite3@5.1.7/node_modules/sqlite3/lib/sqlite3.js');
const db = new sqlite3.Database('/home/node/.n8n/database.sqlite');

db.all("SELECT workflowId, publishedVersionId FROM workflow_published_version", [], (err, rows) => {
    if (err) {
        console.error(err);
    } else {
        rows.forEach(r => {
            console.log(`wfId=${r.workflowId} pvid=${r.publishedVersionId}`);
        });
    }
    db.close();
});
