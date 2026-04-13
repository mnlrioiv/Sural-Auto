const fs = require('fs');
const workflows = JSON.parse(fs.readFileSync('/home/node/n8n_wf_fixed.json', 'utf8'));
workflows.forEach((wf, i) => {
  fs.writeFileSync('/home/node/workflows/wf' + (i+1) + '.json', JSON.stringify(wf, null, 2));
  console.log('Created wf' + (i+1) + '.json: ' + wf.name);
});
