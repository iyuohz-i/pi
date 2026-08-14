import json, math, os, sys

# Load extraction results
with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-14.json") as f:
    extract = json.load(f)

# Load dispatch data for batchImportData
with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-14.json") as f:
    dispatch = json.load(f)

batch_import_data = dispatch.get("batchImportData", {})
results = {r["path"]: r for r in extract["results"]}
batch_files = dispatch.get("batchFiles", dispatch.get("files", []))

nodes = []
edges = []


# Step 1: Create file nodes
for fpath, (summary, tags, complexity, notes) in file_meta.items():
    fname = os.path.basename(fpath)
    node = {
        "id": f"file:{fpath}",
        "type": "file",
        "name": fname,
        "filePath": fpath,
        "summary": summary,
        "tags": tags,
        "complexity": complexity,
    }
    if notes:
        node["languageNotes"] = notes
    nodes.append(node)


# Step 2: Create function nodes for significant functions
for fpath, rdata in results.items():
    for fn in rdata.get("functions", []):
        fn_name = fn["name"]
        start = fn["startLine"]
        end = fn["endLine"]
        line_count = end - start + 1
        
        # Significance filter: 10+ lines OR exported
        is_exported = any(e["name"] == fn_name for e in rdata.get("exports", []))
        if line_count < 10 and not is_exported:
            continue
        
        key = (fpath, fn_name)
        if key in func_meta:
            fsummary, ftags = func_meta[key]
        else:
            # Generate generic summary from function name
            fsummary = f"{fn_name} 函数，位于 {os.path.basename(fpath)}。"
            ftags = ["function"]
        
        fcomplexity = "simple"
        if line_count >= 100:
            fcomplexity = "complex"
        elif line_count >= 30:
            fcomplexity = "moderate"
        
        nodes.append({
            "id": f"function:{fpath}:{fn_name}",
            "type": "function",
            "name": fn_name,
            "filePath": fpath,
            "lineRange": [start, end],
            "summary": fsummary,
            "tags": ftags,
            "complexity": fcomplexity,
        })


# Step 3: Create class nodes for significant classes
for fpath, rdata in results.items():
    for cls in rdata.get("classes", []):
        cls_name = cls["name"]
        start = cls["startLine"]
        end = cls["endLine"]
        line_count = end - start + 1
        methods = cls.get("methods", [])
        
        # Significance filter: 2+ methods OR 20+ lines OR exported
        is_exported = any(e["name"] == cls_name for e in rdata.get("exports", []))
        if len(methods) < 2 and line_count < 20 and not is_exported:
            continue
        
        key = (fpath, cls_name)
        if key in class_meta:
            csummary, ctags = class_meta[key]
        else:
            csummary = f"{cls_name} 类，位于 {os.path.basename(fpath)}。"
            ctags = ["class"]
        
        ccomplexity = "simple"
        if line_count >= 200:
            ccomplexity = "complex"
        elif line_count >= 50:
            ccomplexity = "moderate"
        
        nodes.append({
            "id": f"class:{fpath}:{cls_name}",
            "type": "class",
            "name": cls_name,
            "filePath": fpath,
            "lineRange": [start, end],
            "summary": csummary,
            "tags": ctags,
            "complexity": ccomplexity,
        })


# Step 4: Create edges
# 4a: contains edges (file -> function/class)
file_node_ids = set()
for n in nodes:
    if n["type"] == "file":
        file_node_ids.add(n["id"])

func_class_paths = set()
for n in nodes:
    if n["type"] in ("function", "class"):
        fpath = n["filePath"]
        func_class_paths.add(fpath)

for n in nodes:
    if n["type"] in ("function", "class"):
        fpath = n["filePath"]
        source = f"file:{fpath}"
        edges.append({
            "source": source,
            "target": n["id"],
            "type": "contains",
            "direction": "forward",
            "weight": 1.0,
        })


# 4b: import edges (1:1 from batchImportData)
for fpath, imports in batch_import_data.items():
    source = f"file:{fpath}"
    for imp_path in imports:
        edges.append({
            "source": source,
            "target": f"file:{imp_path}",
            "type": "imports",
            "direction": "forward",
            "weight": 0.7,
        })


# 4c: export edges (file -> exported function/class)
export_names = {}
for fpath, rdata in results.items():
    for e in rdata.get("exports", []):
        export_names[(fpath, e["name"])] = True

for n in nodes:
    if n["type"] in ("function", "class"):
        fpath = n["filePath"]
        name = n["name"]
        if (fpath, name) in export_names:
            edges.append({
                "source": f"file:{fpath}",
                "target": n["id"],
                "type": "exports",
                "direction": "forward",
                "weight": 0.8,
            })


# Step 5: Partition into parts
node_count = len(nodes)
edge_count = len(edges)
parts = max(1, math.ceil(max(node_count / 60, edge_count / 120)))

# Get sorted file paths
sorted_paths = sorted(file_meta.keys())
files_per_part = math.ceil(len(sorted_paths) / parts)

# Assign files to parts
part_files = {}
for i, fpath in enumerate(sorted_paths):
    part_idx = i // files_per_part
    if part_idx not in part_files:
        part_files[part_idx] = set()
    part_files[part_idx].add(fpath)

# Assign nodes to parts
part_nodes = {k: [] for k in range(parts)}
for n in nodes:
    fpath = n.get("filePath", "")
    for pidx, fset in part_files.items():
        if fpath in fset:
            part_nodes[pidx].append(n)
            break

# Assign edges to parts (based on source node)
part_node_ids = {k: set() for k in range(parts)}
for pidx, pnodes in part_nodes.items():
    for n in pnodes:
        part_node_ids[pidx].add(n["id"])

part_edges = {k: [] for k in range(parts)}
for e in edges:
    src = e["source"]
    for pidx, ids in part_node_ids.items():
        if src in ids:
            part_edges[pidx].append(e)
            break

# Write output files
out_dir = "/Users/zhouyi/AiHub/pi/.understand-anything/intermediate"
total_nodes = 0
total_edges = 0
for pidx in range(parts):
    pnodes = part_nodes[pidx]
    pedges = part_edges[pidx]
    total_nodes += len(pnodes)
    total_edges += len(pedges)
    fname = f"batch-14-part-{pidx + 1}.json"
    fpath_out = os.path.join(out_dir, fname)
    with open(fpath_out, "w") as f:
        json.dump({"nodes": pnodes, "edges": pedges}, f, ensure_ascii=False, indent=2)
    print(f"Part {pidx + 1}: {len(pnodes)} nodes, {len(pedges)} edges -> {fname}")

print(f"\nTotal: {total_nodes} nodes, {total_edges} edges across {parts} parts")
print(f"Import edges: {sum(1 for e in edges if e['type'] == 'imports')}")
print(f"Contains edges: {sum(1 for e in edges if e['type'] == 'contains')}")
print(f"Export edges: {sum(1 for e in edges if e['type'] == 'exports')}")
