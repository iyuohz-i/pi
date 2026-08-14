import fs from 'fs';

const data = JSON.parse(fs.readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/batch8-full.json','utf8'));

// Sort files alphabetically by path
const fileNodes = data.nodes.filter(n => n.type === 'file').sort((a,b) => a.filePath.localeCompare(b.filePath));
const filePaths = fileNodes.map(n => n.filePath);

const N = filePaths.length;
const parts = Math.ceil(Math.max(data.nodes.length / 60, data.edges.length / 120));
const filesPerPart = Math.ceil(N / parts);

const outDir = '/Users/zhouyi/AiHub/pi/.understand-anything/intermediate';

for (let p = 0; p < parts; p++) {
  const partFiles = filePaths.slice(p * filesPerPart, (p + 1) * filesPerPart);
  const partFileSet = new Set(partFiles);

  // Nodes whose filePath is in this part's files
  const partNodes = data.nodes.filter(n => {
    const fp = n.filePath || '';
    return partFileSet.has(fp);
  });

  // Edges whose source is in this part's nodes
  const partNodeIds = new Set(partNodes.map(n => n.id));
  const partEdges = data.edges.filter(e => partNodeIds.has(e.source));

  const partData = { nodes: partNodes, edges: partEdges };
  const partNum = p + 1;
  const outPath = `${outDir}/batch-8-part-${partNum}.json`;
  fs.writeFileSync(outPath, JSON.stringify(partData, null, 2));

  console.log(`Part ${partNum}: ${partNodes.length} nodes, ${partEdges.length} edges -> ${outPath}`);

  // Validate
  try {
    JSON.parse(fs.readFileSync(outPath, 'utf8'));
    console.log(`  Valid JSON: true`);
  } catch(e) {
    console.log(`  VALID JSON: FALSE - ${e.message}`);
  }
}
