#!/usr/bin/env python3
import json

nodes = []
edges = []

def add_file_node(path, name, summary, tags, complexity, languageNotes=None):
    node = {
        "id": f"file:{path}",
        "type": "file",
        "name": name,
        "filePath": path,
        "summary": summary,
        "tags": tags,
        "complexity": complexity
    }
    if languageNotes:
        node["languageNotes"] = languageNotes
    nodes.append(node)

def add_func_node(path, name, lineRange, summary, tags, complexity):
    nodes.append({
        "id": f"function:{path}:{name}",
        "type": "function",
        "name": name,
        "filePath": path,
        "lineRange": lineRange,
        "summary": summary,
        "tags": tags,
        "complexity": complexity
    })

def add_edge(source, target, etype, direction="forward", weight=1.0):
    if source == target:
        return
    edges.append({
        "source": source,
        "target": target,
        "type": etype,
        "direction": direction,
        "weight": weight
    })

P = "packages/ai/src/providers"

# === MODEL CATALOG FILES (16) ===
model_files = [
    ("minimax.models.ts", "MINIMAX_MODELS", "MiniMax"),
    ("mistral.models.ts", "MISTRAL_MODELS", "Mistral"),
    ("moonshotai-cn.models.ts", "MOONSHOTAI_CN_MODELS", "Moonshot AI 中国"),
    ("moonshotai.models.ts", "MOONSHOTAI_MODELS", "Moonshot AI"),
    ("nvidia.models.ts", "NVIDIA_MODELS", "NVIDIA"),
    ("openai-codex.models.ts", "OPENAI_CODEX_MODELS", "OpenAI Codex"),
    ("openai.models.ts", "OPENAI_MODELS", "OpenAI"),
    ("opencode-go.models.ts", "OPENCODE_GO_MODELS", "OpenCode Go"),
    ("opencode.models.ts", "OPENCODE_MODELS", "OpenCode"),
    ("openrouter.models.ts", "OPENROUTER_MODELS", "OpenRouter"),
    ("qwen-token-plan-cn.models.ts", "QWEN_TOKEN_PLAN_CN_MODELS", "通义千问 Token 计划 中国"),
    ("qwen-token-plan-individual.models.ts", "QWEN_TOKEN_PLAN_INDIVIDUAL_MODELS", "通义千问 Token 计划 个人"),
    ("qwen-token-plan.models.ts", "QWEN_TOKEN_PLAN_MODELS", "通义千问 Token 计划"),
    ("together.models.ts", "TOGETHER_MODELS", "Together"),
    ("vercel-ai-gateway.models.ts", "VERCEL_AI_GATEWAY_MODELS", "Vercel AI Gateway"),
]

for fname, const_name, display_name in model_files:
    fpath = f"{P}/{fname}"
    add_file_node(fpath, fname,
        f"自动生成的{display_name}模型目录文件，从 JSON 数据导入并通过 flattenModelCatalog 导出 {const_name} 常量。",
        ["data-model", "model-catalog", "auto-generated"],
        "simple",
        "由 scripts/generate-models.ts 自动生成，使用 JSON import 与 flattenModelCatalog 模式。")

# === SIMPLE PROVIDER FILES (14) ===
simple_providers = [
    ("minimax.ts", "minimaxProvider", "6-15", "MiniMax",
     "anthropic-messages", ["api-handler", "provider", "factory"]),
    ("mistral.ts", "mistralProvider", "6-15", "Mistral",
     "mistral-conversations", ["api-handler", "provider", "factory"]),
    ("moonshotai-cn.ts", "moonshotaiCnProvider", "6-15", "Moonshot AI 中国",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("moonshotai.ts", "moonshotaiProvider", "6-15", "Moonshot AI",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("nvidia.ts", "nvidiaProvider", "6-15", "NVIDIA",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("openai-codex.ts", "openaiCodexProvider", "7-22", "OpenAI Codex",
     "openai-codex-responses", ["api-handler", "provider", "factory", "oauth"]),
    ("openai.ts", "openaiProvider", "6-15", "OpenAI",
     "openai-responses", ["api-handler", "provider", "factory"]),
    ("opencode-go.ts", "opencodeGoProvider", "8-20", "OpenCode Go",
     "multi-api", ["api-handler", "provider", "factory", "multi-api"]),
    ("opencode.ts", "opencodeProvider", "9-24", "OpenCode",
     "multi-api", ["api-handler", "provider", "factory", "multi-api"]),
    ("openrouter.ts", "openrouterProvider", "7-23", "OpenRouter",
     "openai-completions", ["api-handler", "provider", "factory", "oauth"]),
    ("qwen-token-plan-cn.ts", "qwenTokenPlanCnProvider", "6-15", "通义千问 Token 计划 中国",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("qwen-token-plan-individual.ts", "qwenTokenPlanIndividualProvider", "6-15", "通义千问 Token 计划 个人",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("qwen-token-plan.ts", "qwenTokenPlanProvider", "6-15", "通义千问 Token 计划",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("together.ts", "togetherProvider", "6-15", "Together",
     "openai-completions", ["api-handler", "provider", "factory"]),
    ("vercel-ai-gateway.ts", "vercelAIGatewayProvider", "6-15", "Vercel AI Gateway",
     "anthropic-messages", ["api-handler", "provider", "factory"]),
]

for fname, func_name, line_range, display_name, api_type, tags in simple_providers:
    fpath = f"{P}/{fname}"
    add_file_node(fpath, fname,
        f"{display_name} 供应商实现，使用 createProvider 创建 Provider 实例，支持 {api_type} API。",
        tags,
        "simple")
    # Parse line range
    parts = line_range.split("-")
    lr = [int(parts[0]), int(parts[1])]
    add_func_node(fpath, func_name, lr,
        f"创建 {display_name} 供应商的 Provider 实例，配置 API 类型、认证方式和模型列表。",
        tags,
        "simple")
    add_edge(f"file:{fpath}", f"function:{fpath}:{func_name}", "contains", "forward", 1.0)
    add_edge(f"file:{fpath}", f"function:{fpath}:{func_name}", "exports", "forward", 0.8)

# === OPENROUTER IMAGES (1) ===
fpath = f"{P}/openrouter-images.ts"
add_file_node(fpath, "openrouter-images.ts",
    "OpenRouter 图像生成供应商实现，使用 createImagesProvider 创建图像生成 Provider，支持 OAuth 认证。",
    ["api-handler", "provider", "factory", "image-generation", "oauth"],
    "simple")
add_func_node(fpath, "openrouterImagesProvider", [7, 22],
    "创建 OpenRouter 图像生成 Provider 实例，配置 OAuth 认证和图像模型。",
    ["api-handler", "provider", "image-generation", "oauth"],
    "simple")
add_edge(f"file:{fpath}", f"function:{fpath}:openrouterImagesProvider", "contains", "forward", 1.0)
add_edge(f"file:{fpath}", f"function:{fpath}:openrouterImagesProvider", "exports", "forward", 0.8)

# === RADIUS CONFIG (1) ===
fpath = f"{P}/radius-config.ts"
add_file_node(fpath, "radius-config.ts",
    "Radius 网关配置模块，定义网关模型类型、配置消毒、URL 规范化、凭据获取和加载模型列表等核心功能。",
    ["utility", "config", "validation", "radius-gateway", "data-model"],
    "moderate",
    "使用类型保护实现运行时配置消毒，确保从网关获取的数据符合预期格式。")

# Significant radius-config functions (10+ lines or exported)
add_func_node(fpath, "isRadiusGatewayModel", [26, 40],
    "类型保护函数，检查未知值是否符合 RadiusGatewayModel 类型结构。",
    ["validation", "type-guard", "radius-gateway"],
    "simple")
add_edge(f"file:{fpath}", f"function:{fpath}:isRadiusGatewayModel", "contains", "forward", 1.0)

add_func_node(fpath, "loadRadiusGatewayConfig", [80, 96],
    "从 Radius 网关端点异步加载配置，带有认证头部和错误处理。",
    ["async", "network", "radius-gateway", "config"],
    "moderate")
add_edge(f"file:{fpath}", f"function:{fpath}:loadRadiusGatewayConfig", "contains", "forward", 1.0)
add_edge(f"file:{fpath}", f"function:{fpath}:loadRadiusGatewayConfig", "exports", "forward", 0.8)

add_func_node(fpath, "sanitizeRadiusGatewayConfig", [42, 50],
    "消毒网关配置数据，过滤无效模型并返回规范化后的配置对象。",
    ["validation", "sanitization", "radius-gateway"],
    "simple")
add_edge(f"file:{fpath}", f"function:{fpath}:sanitizeRadiusGatewayConfig", "contains", "forward", 1.0)

add_func_node(fpath, "getRadiusModelsFromConfig", [61, 68],
    "将网关配置中的模型转换为项目内部 Model 格式，添加 provider 和 baseUrl 字段。",
    ["data-model", "transformation", "radius-gateway"],
    "simple")
add_edge(f"file:{fpath}", f"function:{fpath}:getRadiusModelsFromConfig", "contains", "forward", 1.0)
add_edge(f"file:{fpath}", f"function:{fpath}:getRadiusModelsFromConfig", "exports", "forward", 0.8)

# === RADIUS PROVIDER (1) ===
fpath = f"{P}/radius.ts"
add_file_node(fpath, "radius.ts",
    "Radius 网关供应商实现，创建具有动态模型目录刷新能力的 Provider，支持从网关实时拉取最新模型列表。",
    ["api-handler", "provider", "factory", "radius-gateway", "dynamic-models"],
    "complex",
    "使用 refreshModels 闭包实现动态模型目录更新，包含存储恢复、遗留目录导入和网络刷新三层逻辑。")
add_func_node(fpath, "radiusProvider", [20, 82],
    "创建 Radius 网关 Provider 实例，配置 OAuth 认证、动态模型刷新和流式 API 转发。",
    ["api-handler", "provider", "radius-gateway", "dynamic-models"],
    "complex")
add_edge(f"file:{fpath}", f"function:{fpath}:radiusProvider", "contains", "forward", 1.0)
add_edge(f"file:{fpath}", f"function:{fpath}:radiusProvider", "exports", "forward", 0.8)

# === IMPORT EDGES (93 total) ===
import_data = {
    "minimax.models.ts": ["packages/ai/src/model-catalog.ts"],
    "minimax.ts": ["packages/ai/src/api/anthropic-messages.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/minimax.models.ts"],
    "mistral.models.ts": ["packages/ai/src/model-catalog.ts"],
    "mistral.ts": ["packages/ai/src/api/mistral-conversations.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/mistral.models.ts"],
    "moonshotai-cn.models.ts": ["packages/ai/src/model-catalog.ts"],
    "moonshotai-cn.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/moonshotai-cn.models.ts"],
    "moonshotai.models.ts": ["packages/ai/src/model-catalog.ts"],
    "moonshotai.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/moonshotai.models.ts"],
    "nvidia.models.ts": ["packages/ai/src/model-catalog.ts"],
    "nvidia.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/nvidia.models.ts"],
    "openai-codex.models.ts": ["packages/ai/src/model-catalog.ts"],
    "openai-codex.ts": ["packages/ai/src/api/openai-codex-responses.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/auth/oauth/load.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/openai-codex.models.ts"],
    "openai.models.ts": ["packages/ai/src/model-catalog.ts"],
    "openai.ts": ["packages/ai/src/api/openai-responses.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/openai.models.ts"],
    "opencode-go.models.ts": ["packages/ai/src/model-catalog.ts"],
    "opencode-go.ts": ["packages/ai/src/api/anthropic-messages.lazy.ts", "packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/api/openai-responses.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/opencode-go.models.ts"],
    "opencode.models.ts": ["packages/ai/src/model-catalog.ts"],
    "opencode.ts": ["packages/ai/src/api/anthropic-messages.lazy.ts", "packages/ai/src/api/google-generative-ai.lazy.ts", "packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/api/openai-responses.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/opencode.models.ts"],
    "openrouter-images.ts": ["packages/ai/src/api/openrouter-images.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/auth/oauth/load.ts", "packages/ai/src/images-models.ts"],
    "openrouter.models.ts": ["packages/ai/src/model-catalog.ts"],
    "openrouter.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/auth/oauth/load.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/openrouter.models.ts"],
    "qwen-token-plan-cn.models.ts": ["packages/ai/src/model-catalog.ts"],
    "qwen-token-plan-cn.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/qwen-token-plan-cn.models.ts"],
    "qwen-token-plan-individual.models.ts": ["packages/ai/src/model-catalog.ts"],
    "qwen-token-plan-individual.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/qwen-token-plan-individual.models.ts"],
    "qwen-token-plan.models.ts": ["packages/ai/src/model-catalog.ts"],
    "qwen-token-plan.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/qwen-token-plan.models.ts"],
    "radius-config.ts": ["packages/ai/src/auth/types.ts", "packages/ai/src/types.ts"],
    "radius.ts": ["packages/ai/src/api/pi-messages.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/auth/oauth/load.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/radius-config.ts"],
    "together.models.ts": ["packages/ai/src/model-catalog.ts"],
    "together.ts": ["packages/ai/src/api/openai-completions.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/together.models.ts"],
    "vercel-ai-gateway.models.ts": ["packages/ai/src/model-catalog.ts"],
    "vercel-ai-gateway.ts": ["packages/ai/src/api/anthropic-messages.lazy.ts", "packages/ai/src/auth/helpers.ts", "packages/ai/src/models.ts", "packages/ai/src/providers/vercel-ai-gateway.models.ts"],
}

for fname, imports in import_data.items():
    fpath = f"{P}/{fname}"
    for target in imports:
        add_edge(f"file:{fpath}", f"file:{target}", "imports", "forward", 0.7)

# === CALLS edges (cross-file function calls) ===
# radius.ts calls radius-config.ts functions
add_edge(f"function:{P}/radius.ts:radiusProvider", f"function:{P}/radius-config.ts:loadRadiusGatewayConfig", "calls", "forward", 0.8)
add_edge(f"function:{P}/radius.ts:radiusProvider", f"function:{P}/radius-config.ts:getRadiusModelsFromConfig", "calls", "forward", 0.8)

# === OUTPUT ===
output = {"nodes": nodes, "edges": edges}
print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
print(f"Import edges: {sum(len(v) for v in import_data.values())}")

# Verify no self-referencing edges
self_refs = [e for e in edges if e["source"] == e["target"]]
if self_refs:
    print(f"WARNING: {len(self_refs)} self-referencing edges found!")
    for e in self_refs:
        print(f"  {e['source']} -> {e['target']}")

# Write output
with open("/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-12.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Written to batch-12.json")
