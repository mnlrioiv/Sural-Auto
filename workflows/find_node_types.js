const fs = require("fs");
const path = require("path");
const pnpmDir = "/usr/local/lib/node_modules/n8n/node_modules/.pnpm";
const dirs = fs.readdirSync(pnpmDir).filter(d => d.startsWith("n8n-nodes-base@"));
const nodeBase = path.join(pnpmDir, dirs[0], "node_modules", "n8n-nodes-base", "dist", "nodes");
const subdirs = fs.readdirSync(nodeBase);
const result = {};
subdirs.forEach(s => {
  const jsFile = path.join(nodeBase, s, s + ".node.js");
  const jsonFile = path.join(nodeBase, s, s + ".node.json");
  
  if (fs.existsSync(jsonFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(jsonFile, "utf8"));
      result[s] = data.node || "no-node-field";
    } catch(e) {
      result[s] = "json-parse-error";
    }
  }
});
Object.keys(result).sort().forEach(k => console.log(k + ": " + result[k]));
