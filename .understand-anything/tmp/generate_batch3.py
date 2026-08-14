#!/usr/bin/env python3
"""Generate knowledge graph nodes and edges for batch 3."""
import json, math, os

# Load extraction results
with open('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-3.json') as f:
    extract = json.load(f)

# Load dispatch data for batchImportData
with open('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-3.json') as f:
    dispatch = json.load(f)

batch_import_data = dispatch['batchImportData']
results_by_path = {r['path']: r for r in extract['results']}

nodes = []
edges = []

# ============================================================
# FILE NODES (all 35 files)
# ============================================================

file_summaries = {
    "packages/ai/scripts/generate-image-models.ts": "从 OpenRouter API 获取图像模型列表并生成 TypeScript 模型定义文件的脚本工具。",
    "packages/ai/src/api/anthropic-messages.ts": "Anthropic Messages API 适配器，实现消息转换、SSE 流解析、工具调用和 thinking 级别映射等核心功能。",
    "packages/ai/src/api/azure-openai-responses.lazy.ts": "Azure OpenAI Responses API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/azure-openai-responses.ts": "Azure OpenAI Responses API 适配器，处理 Azure 部署名称映射、base URL 规范化和请求参数构建。",
    "packages/ai/src/api/bedrock-converse-stream.lazy.ts": "AWS Bedrock Converse Stream API 的惰性加载包装器，支持运行时注入 provider 模块。",
    "packages/ai/src/api/bedrock-converse-stream.ts": "AWS Bedrock Converse Stream API 适配器，实现凭证解析、消息转换、SSE 流处理和 thinking 级别映射。",
    "packages/ai/src/api/cloudflare-gateway-binding.ts": "Cloudflare AI Gateway 绑定适配器，通过 Workers fetch binding 代理 LLM 请求并收集诊断头信息。",
    "packages/ai/src/api/constrained-sampling.ts": "约束采样工具模块，提供 JSON Schema 严格模式转换和 grammar 工具输入约束的解析逻辑。",
    "packages/ai/src/api/github-copilot-headers.ts": "GitHub Copilot 动态请求头构建器，处理 vision 输入检测和 initiator 标识推断。",
    "packages/ai/src/api/google-generative-ai.lazy.ts": "Google Generative AI API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/google-generative-ai.ts": "Google Generative AI (Gemini) API 适配器，处理流式响应、thinking 配置和 budget 管理。",
    "packages/ai/src/api/google-shared.ts": "Google API 共享工具模块，提供消息转换、工具映射、stop reason 映射和重试逻辑供 Gemini 和 Vertex 共用。",
    "packages/ai/src/api/google-vertex.lazy.ts": "Google Vertex AI API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/google-vertex.ts": "Google Vertex AI API 适配器，处理项目/区域解析、API Key 和 ADC 认证、以及 Gemini 模型参数构建。",
    "packages/ai/src/api/lazy.ts": "惰性 API 加载基础设施，提供 createSetupErrorMessage、lazyStream 和 lazyApi 工厂函数供各 provider 的 .lazy.ts 文件复用。",
    "packages/ai/src/api/mistral-conversations.lazy.ts": "Mistral Conversations API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/mistral-conversations.ts": "Mistral Conversations API 适配器，实现 chat payload 构建、流式事件解析、工具调用 ID 规范化和 HTTP 传输。",
    "packages/ai/src/api/openai-codex-responses.lazy.ts": "OpenAI Codex Responses API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/openai-codex-responses.ts": "OpenAI Codex Responses API 适配器，支持 SSE 和 WebSocket 双通道流式传输、请求体压缩、会话缓存和重试逻辑。",
    "packages/ai/src/api/openai-completions.ts": "OpenAI Completions API 适配器，实现兼容性检测、消息转换、prompt cache 控制和 chat template 参数构建。",
    "packages/ai/src/api/openai-prompt-cache.ts": "OpenAI prompt cache key 工具函数，提供 key 长度限制和截断逻辑。",
    "packages/ai/src/api/openai-responses-shared.ts": "OpenAI Responses API 共享模块，提供消息转换、工具转换、流式响应处理和 stop reason 映射供多个 Responses 变体复用。",
    "packages/ai/src/api/openai-responses.ts": "OpenAI Responses API 适配器，处理客户端创建、请求参数构建和 service tier 定价。",
    "packages/ai/src/api/openrouter-images.ts": "OpenRouter 图像生成 API 适配器，实现图像生成请求构建、usage 解析和错误处理。",
    "packages/ai/src/api/pi-messages.lazy.ts": "Pi Messages API 的惰性加载包装器，实现按需初始化模块。",
    "packages/ai/src/api/pi-messages.ts": "Pi Messages API 适配器，实现自定义事件转换、流式响应处理和 rewrite 诊断。",
    "packages/ai/src/api/simple-options.ts": "通用选项构建器，提供 max tokens 裁剪、reasoning 级别调整和基础选项构建等共享逻辑。",
    "packages/ai/src/api/transform-messages.ts": "消息转换工具，处理图像占位符替换、不支持的图像降级和 tool call ID 规范化。",
    "packages/ai/src/bedrock-provider.ts": "Bedrock provider 模块导出，将 bedrock-converse-stream API 注册为 provider 模块。",
    "packages/ai/src/compat.ts": "API 兼容层，注册内置和自定义 provider、管理 API provider 映射，并提供统一的 stream/complete 入口。",
    "packages/ai/src/env-api-keys.ts": "环境变量 API Key 解析器，支持多 provider 的 key 发现、Vertex ADC 凭证检测和 key 环境变量映射。",
    "packages/ai/src/image-models.ts": "图像模型注册表，提供图像模型和 provider 的查询接口。",
    "packages/ai/src/images-api-registry.ts": "图像 API provider 注册表，管理图像生成 API provider 的注册和查找。",
    "packages/ai/src/images.ts": "图像生成入口模块，委托给 images-api-registry 和内置 provider 注册器执行图像生成。",
    "packages/ai/src/legacy-api-aliases.ts": "旧版 API 别名模块，为各 provider 的 stream/streamSimple 函数提供向后兼容的导出别名。"
}

file_tags = {
    "packages/ai/scripts/generate-image-models.ts": ["script", "code-generation", "image-models", "openrouter"],
    "packages/ai/src/api/anthropic-messages.ts": ["api-handler", "anthropic", "streaming", "sse", "tool-calling"],
    "packages/ai/src/api/azure-openai-responses.lazy.ts": ["lazy-loader", "azure", "openai-responses", "barrel"],
    "packages/ai/src/api/azure-openai-responses.ts": ["api-handler", "azure", "openai-responses", "streaming"],
    "packages/ai/src/api/bedrock-converse-stream.lazy.ts": ["lazy-loader", "bedrock", "aws", "barrel"],
    "packages/ai/src/api/bedrock-converse-stream.ts": ["api-handler", "bedrock", "aws", "streaming", "tool-calling"],
    "packages/ai/src/api/cloudflare-gateway-binding.ts": ["api-handler", "cloudflare", "gateway", "proxy"],
    "packages/ai/src/api/constrained-sampling.ts": ["utility", "json-schema", "constrained-sampling", "grammar"],
    "packages/ai/src/api/github-copilot-headers.ts": ["utility", "github-copilot", "headers", "middleware"],
    "packages/ai/src/api/google-generative-ai.lazy.ts": ["lazy-loader", "google", "gemini", "barrel"],
    "packages/ai/src/api/google-generative-ai.ts": ["api-handler", "google", "gemini", "streaming"],
    "packages/ai/src/api/google-shared.ts": ["utility", "google", "shared", "message-conversion"],
    "packages/ai/src/api/google-vertex.lazy.ts": ["lazy-loader", "google-vertex", "barrel"],
    "packages/ai/src/api/google-vertex.ts": ["api-handler", "google-vertex", "streaming", "authentication"],
    "packages/ai/src/api/lazy.ts": ["utility", "lazy-loading", "factory", "infrastructure"],
    "packages/ai/src/api/mistral-conversations.lazy.ts": ["lazy-loader", "mistral", "barrel"],
    "packages/ai/src/api/mistral-conversations.ts": ["api-handler", "mistral", "streaming", "tool-calling"],
    "packages/ai/src/api/openai-codex-responses.lazy.ts": ["lazy-loader", "openai-codex", "barrel"],
    "packages/ai/src/api/openai-codex-responses.ts": ["api-handler", "openai-codex", "websocket", "streaming", "caching"],
    "packages/ai/src/api/openai-completions.ts": ["api-handler", "openai", "completions", "streaming", "compat"],
    "packages/ai/src/api/openai-prompt-cache.ts": ["utility", "openai", "prompt-cache"],
    "packages/ai/src/api/openai-responses-shared.ts": ["utility", "openai-responses", "shared", "streaming"],
    "packages/ai/src/api/openai-responses.ts": ["api-handler", "openai-responses", "streaming"],
    "packages/ai/src/api/openrouter-images.ts": ["api-handler", "openrouter", "image-generation"],
    "packages/ai/src/api/pi-messages.lazy.ts": ["lazy-loader", "pi-messages", "barrel"],
    "packages/ai/src/api/pi-messages.ts": ["api-handler", "pi-messages", "streaming"],
    "packages/ai/src/api/simple-options.ts": ["utility", "options-builder", "shared", "token-management"],
    "packages/ai/src/api/transform-messages.ts": ["utility", "message-conversion", "image-handling"],
    "packages/ai/src/bedrock-provider.ts": ["barrel", "bedrock", "provider-module"],
    "packages/ai/src/compat.ts": ["entry-point", "compat", "provider-registry", "streaming"],
    "packages/ai/src/env-api-keys.ts": ["utility", "api-keys", "environment-variables", "authentication"],
    "packages/ai/src/image-models.ts": ["registry", "image-models", "query"],
    "packages/ai/src/images-api-registry.ts": ["registry", "image-generation", "provider-management"],
    "packages/ai/src/images.ts": ["entry-point", "image-generation", "delegation"],
    "packages/ai/src/legacy-api-aliases.ts": ["barrel", "legacy", "aliases", "backward-compat"]
}

file_complexity = {}
for r in extract['results']:
    path = r['path']
    ne = r.get('nonEmptyLines', 0)
    fn_count = r.get('metrics', {}).get('functionCount', 0)
    if ne > 200 or fn_count > 15:
        file_complexity[path] = "complex"
    elif ne > 50:
        file_complexity[path] = "moderate"
    else:
        file_complexity[path] = "simple"

# Create file nodes
all_files = sorted(results_by_path.keys())
for path in all_files:
    name = path.rsplit('/', 1)[-1]
    node = {
        "id": f"file:{path}",
        "type": "file",
        "name": name,
        "filePath": path,
        "summary": file_summaries.get(path, ""),
        "tags": file_tags.get(path, ["code"]),
        "complexity": file_complexity.get(path, "moderate")
    }
    nodes.append(node)

# ============================================================
# FUNCTION AND CLASS NODES
# ============================================================

# Function summaries (curated for key functions)
fn_summaries = {
    # generate-image-models.ts
    "packages/ai/scripts/generate-image-models.ts:parseOpenRouterImageModels": "解析 OpenRouter 图像模型 API 响应，提取模型 ID、名称和定价信息。",
    "packages/ai/scripts/generate-image-models.ts:fetchOpenRouterImageModels": "从 OpenRouter API 获取图像模型列表，支持严格模式校验。",
    "packages/ai/scripts/generate-image-models.ts:generateImageModelsFile": "将解析后的模型数据生成为 TypeScript 源文件。",

    # anthropic-messages.ts
    "packages/ai/src/api/anthropic-messages.ts:stream": "Anthropic Messages API 核心流式入口，处理 SSE 解析、内容块分发和工具调用。",
    "packages/ai/src/api/anthropic-messages.ts:streamSimple": "Anthropic 简化流式接口，委托给 stream 函数并处理简单选项。",
    "packages/ai/src/api/anthropic-messages.ts:createClient": "创建 Anthropic API 客户端，配置 base URL、headers 和 OAuth token。",
    "packages/ai/src/api/anthropic-messages.ts:buildParams": "构建 Anthropic API 请求参数，包括 model、messages、tools 和 thinking 配置。",
    "packages/ai/src/api/anthropic-messages.ts:convertMessages": "将内部消息格式转换为 Anthropic API 消息格式，处理 cache control 和签名。",
    "packages/ai/src/api/anthropic-messages.ts:convertTools": "将工具定义转换为 Anthropic API 格式，支持 eager tool input 和延迟加载。",
    "packages/ai/src/api/anthropic-messages.ts:convertContentBlocks": "转换内容块，处理文本、图像和 tool use/tool result。",
    "packages/ai/src/api/anthropic-messages.ts:decodeSseLine": "解析 SSE 数据行，处理多行数据和事件边界。",
    "packages/ai/src/api/anthropic-messages.ts:mapStopReason": "将 Anthropic stop reason 映射为统一的停止原因枚举。",
    "packages/ai/src/api/anthropic-messages.ts:convertToolResult": "转换工具结果消息为 Anthropic 格式，处理延迟工具和名称规范化。",
    "packages/ai/src/api/anthropic-messages.ts:mapThinkingLevelToEffort": "将 thinking 级别映射为 Anthropic effort 参数。",

    # azure-openai-responses.ts
    "packages/ai/src/api/azure-openai-responses.ts:stream": "Azure OpenAI Responses API 流式入口，委托给共享的 openai-responses-shared 逻辑。",
    "packages/ai/src/api/azure-openai-responses.ts:streamSimple": "Azure OpenAI Responses 简化流式接口。",
    "packages/ai/src/api/azure-openai-responses.ts:buildParams": "构建 Azure OpenAI Responses API 请求参数，包含 deployment name 和 grammar 配置。",
    "packages/ai/src/api/azure-openai-responses.ts:normalizeAzureBaseUrl": "规范化 Azure OpenAI base URL，处理 deployment 路径和 API 版本。",
    "packages/ai/src/api/azure-openai-responses.ts:resolveAzureConfig": "解析 Azure OpenAI 配置，提取 API key、base URL 和 deployment name。",
    "packages/ai/src/api/azure-openai-responses.ts:createClient": "创建 Azure OpenAI API 客户端，配置认证头和 base URL。",

    # bedrock-converse-stream.ts
    "packages/ai/src/api/bedrock-converse-stream.ts:stream": "Bedrock Converse Stream API 核心流式入口，处理凭证解析和事件分发。",
    "packages/ai/src/api/bedrock-converse-stream.ts:streamSimple": "Bedrock 简化流式接口，委托给 stream 函数。",
    "packages/ai/src/api/bedrock-converse-stream.ts:convertMessages": "将内部消息格式转换为 Bedrock Converse 格式，处理 system prompt 和 cache control。",
    "packages/ai/src/api/bedrock-converse-stream.ts:handleContentBlockDelta": "处理 Bedrock 内容块增量事件，分发 text、tool use 和 thinking delta。",
    "packages/ai/src/api/bedrock-converse-stream.ts:mapStopReason": "将 Bedrock stop reason 映射为统一的停止原因枚举。",
    "packages/ai/src/api/bedrock-converse-stream.ts:supportsPromptCaching": "检测 Bedrock 模型是否支持 prompt caching。",
    "packages/ai/src/api/bedrock-converse-stream.ts:buildAdditionalModelRequestFields": "构建 Bedrock 额外模型请求字段，包括 thinking 配置。",
    "packages/ai/src/api/bedrock-converse-stream.ts:convertToolConfig": "将工具定义转换为 Bedrock tool config 格式。",
    "packages/ai/src/api/bedrock-converse-stream.ts:mapThinkingLevelToEffort": "将 thinking 级别映射为 Bedrock 模型对应的 effort 参数。",

    # cloudflare-gateway-binding.ts
    "packages/ai/src/api/cloudflare-gateway-binding.ts:createGatewayBindingFetch": "创建 Cloudflare Gateway binding fetch 函数，代理请求并收集诊断头。",
    "packages/ai/src/api/cloudflare-gateway-binding.ts:readBodyText": "读取请求 body 文本内容用于诊断日志。",

    # constrained-sampling.ts
    "packages/ai/src/api/constrained-sampling.ts:makeJsonSchemaNodeStrict": "将 JSON Schema 节点转换为严格模式，添加 additionalProperties: false。",
    "packages/ai/src/api/constrained-sampling.ts:resolveJsonSchemaStrictSampling": "解析 JSON Schema 严格采样配置，返回工具参数 schema。",
    "packages/ai/src/api/constrained-sampling.ts:resolveGrammarConstrainedSampling": "解析 grammar 约束采样配置，提取工具输入属性。",
    "packages/ai/src/api/constrained-sampling.ts:appendGrammarToolInputJsonDelta": "将 grammar 工具输入 JSON 增量追加到缓冲区。",

    # github-copilot-headers.ts
    "packages/ai/src/api/github-copilot-headers.ts:buildCopilotDynamicHeaders": "构建 GitHub Copilot 动态请求头，包含 editor version 和 initiative 信息。",
    "packages/ai/src/api/github-copilot-headers.ts:hasCopilotVisionInput": "检测消息中是否包含 Copilot vision 输入内容。",

    # google-generative-ai.ts
    "packages/ai/src/api/google-generative-ai.ts:stream": "Google Generative AI API 流式入口，处理 Gemini 响应流和 thinking 配置。",
    "packages/ai/src/api/google-generative-ai.ts:streamSimple": "Google Generative AI 简化流式接口。",
    "packages/ai/src/api/google-generative-ai.ts:buildParams": "构建 Google Generative AI API 请求参数。",
    "packages/ai/src/api/google-generative-ai.ts:getThinkingLevel": "根据 effort 和模型解析 Gemini thinking 级别配置。",
    "packages/ai/src/api/google-generative-ai.ts:getGoogleBudget": "计算 Google 模型的 thinking budget token 数量。",

    # google-shared.ts
    "packages/ai/src/api/google-shared.ts:convertMessages": "将内部消息格式转换为 Google API 格式，处理 tool call 和 thinking 签名。",
    "packages/ai/src/api/google-shared.ts:convertTools": "将工具定义转换为 Google function calling 格式。",
    "packages/ai/src/api/google-shared.ts:mapStopReason": "将 Google finish reason 映射为统一的停止原因枚举。",
    "packages/ai/src/api/google-shared.ts:retryGoogleRequest": "Google API 请求重试逻辑，处理速率限制和服务器错误。",

    # google-vertex.ts
    "packages/ai/src/api/google-vertex.ts:stream": "Google Vertex AI API 流式入口，处理认证和 Gemini 响应流。",
    "packages/ai/src/api/google-vertex.ts:streamSimple": "Google Vertex AI 简化流式接口。",
    "packages/ai/src/api/google-vertex.ts:createClient": "创建 Vertex AI 客户端，支持 ADC 和 API Key 认证。",
    "packages/ai/src/api/google-vertex.ts:buildParams": "构建 Vertex AI API 请求参数。",
    "packages/ai/src/api/google-vertex.ts:resolveProject": "从选项中解析 Google Cloud 项目 ID。",

    # lazy.ts
    "packages/ai/src/api/lazy.ts:lazyApi": "创建惰性加载 API 工厂函数，延迟加载实际 API 模块。",
    "packages/ai/src/api/lazy.ts:lazyStream": "创建惰性加载 stream 函数，首次调用时加载模块。",

    # mistral-conversations.ts
    "packages/ai/src/api/mistral-conversations.ts:stream": "Mistral Conversations API 流式入口，处理 HTTP 流和事件解析。",
    "packages/ai/src/api/mistral-conversations.ts:streamSimple": "Mistral 简化流式接口。",
    "packages/ai/src/api/mistral-conversations.ts:consumeChatStream": "消费 Mistral chat 流，解析 SSE 事件并分发到 output stream。",
    "packages/ai/src/api/mistral-conversations.ts:toChatMessages": "将内部消息格式转换为 Mistral chat 消息格式。",
    "packages/ai/src/api/mistral-conversations.ts:buildChatPayload": "构建 Mistral chat 请求 payload。",
    "packages/ai/src/api/mistral-conversations.ts:toMistralWirePayload": "将 payload 转换为 Mistral wire 格式。",

    # openai-codex-responses.ts
    "packages/ai/src/api/openai-codex-responses.ts:stream": "OpenAI Codex Responses API 流式入口，支持 SSE 和 WebSocket 通道选择。",
    "packages/ai/src/api/openai-codex-responses.ts:streamSimple": "OpenAI Codex Responses 简化流式接口。",
    "packages/ai/src/api/openai-codex-responses.ts:buildRequestBody": "构建 Codex Responses API 请求体，包含 session cache 和 grammar 配置。",
    "packages/ai/src/api/openai-codex-responses.ts:connectWebSocket": "建立 WebSocket 连接，处理超时和错误。",
    "packages/ai/src/api/openai-codex-responses.ts:acquireWebSocket": "获取或复用 WebSocket 连接，实现会话级连接池。",
    "packages/ai/src/api/openai-codex-responses.ts:processWebSocketStream": "处理 WebSocket 流式响应，解析事件并分发到 output stream。",
    "packages/ai/src/api/openai-codex-responses.ts:closeOpenAICodexWebSocketSessions": "关闭指定会话的所有 WebSocket 连接。",

    # openai-completions.ts
    "packages/ai/src/api/openai-completions.ts:stream": "OpenAI Completions API 核心流式入口，处理 SSE 解析和兼容性逻辑。",
    "packages/ai/src/api/openai-completions.ts:streamSimple": "OpenAI Completions 简化流式接口。",
    "packages/ai/src/api/openai-completions.ts:buildParams": "构建 OpenAI Completions API 请求参数，包含 cache control 和 chat template。",
    "packages/ai/src/api/openai-completions.ts:convertMessages": "将内部消息格式转换为 OpenAI Completions 格式，处理兼容性和图像内容。",
    "packages/ai/src/api/openai-completions.ts:convertTools": "将工具定义转换为 OpenAI Completions 格式。",
    "packages/ai/src/api/openai-completions.ts:detectCompat": "检测模型的兼容性配置，包括 cache control、thinking 和 tool calling 支持。",
    "packages/ai/src/api/openai-completions.ts:mapStopReason": "将 OpenAI finish reason 映射为统一的停止原因枚举。",
    "packages/ai/src/api/openai-completions.ts:createClient": "创建 OpenAI Completions API 客户端，配置认证和 base URL。",

    # openai-responses-shared.ts
    "packages/ai/src/api/openai-responses-shared.ts:convertResponsesMessages": "将内部消息格式转换为 OpenAI Responses API 格式。",
    "packages/ai/src/api/openai-responses-shared.ts:convertResponsesTools": "将工具定义转换为 OpenAI Responses API 格式。",
    "packages/ai/src/api/openai-responses-shared.ts:processResponsesStream": "处理 OpenAI Responses 流式响应，解析事件并分发到 output stream。",
    "packages/ai/src/api/openai-responses-shared.ts:mapStopReason": "将 Responses API status 映射为统一的停止原因枚举。",

    # openai-responses.ts
    "packages/ai/src/api/openai-responses.ts:stream": "OpenAI Responses API 流式入口，委托给共享逻辑处理。",
    "packages/ai/src/api/openai-responses.ts:streamSimple": "OpenAI Responses 简化流式接口。",
    "packages/ai/src/api/openai-responses.ts:buildParams": "构建 OpenAI Responses API 请求参数。",
    "packages/ai/src/api/openai-responses.ts:createClient": "创建 OpenAI Responses API 客户端。",

    # openrouter-images.ts
    "packages/ai/src/api/openrouter-images.ts:generateImages": "通过 OpenRouter API 生成图像，处理请求构建和响应解析。",

    # pi-messages.ts
    "packages/ai/src/api/pi-messages.ts:stream": "Pi Messages API 流式入口，处理自定义事件转换和错误恢复。",
    "packages/ai/src/api/pi-messages.ts:streamSimple": "Pi Messages 简化流式接口。",
    "packages/ai/src/api/pi-messages.ts:createEventConverter": "创建 Pi Messages 事件转换器，将原始 SSE 事件转换为统一格式。",

    # simple-options.ts
    "packages/ai/src/api/simple-options.ts:buildBaseOptions": "构建基础选项对象，提取 API key、max tokens 和 reasoning 配置。",
    "packages/ai/src/api/simple-options.ts:adjustMaxTokensForThinking": "根据 thinking 级别调整 max tokens 预算。",

    # transform-messages.ts
    "packages/ai/src/api/transform-messages.ts:transformMessages": "转换消息列表，处理图像占位符、不支持的图像降级和 tool call ID 规范化。",

    # compat.ts
    "packages/ai/src/compat.ts:registerApiProvider": "注册 API provider 到全局注册表。",
    "packages/ai/src/compat.ts:registerFauxProvider": "注册 faux（模拟）provider 用于测试。",
    "packages/ai/src/compat.ts:stream": "兼容层统一流式入口，根据 model 查找对应 provider 并调用其 stream 函数。",
    "packages/ai/src/compat.ts:streamSimple": "兼容层统一简化流式入口。",

    # env-api-keys.ts
    "packages/ai/src/env-api-keys.ts:getEnvApiKey": "从环境变量获取指定 provider 的 API key。",
    "packages/ai/src/env-api-keys.ts:getApiKeyEnvVars": "获取 provider 对应的所有 API key 环境变量名。",
    "packages/ai/src/env-api-keys.ts:hasVertexAdcCredentials": "检测是否存在 Vertex AI ADC（应用默认凭证）。",

    # images-api-registry.ts
    "packages/ai/src/images-api-registry.ts:registerImagesApiProvider": "注册图像 API provider 到全局注册表。",

    # openai-prompt-cache.ts
    "packages/ai/src/api/openai-prompt-cache.ts:clampOpenAIPromptCacheKey": "截断 OpenAI prompt cache key 到最大长度限制。",
}

# Class summaries
cls_summaries = {
    "packages/ai/src/api/mistral-conversations.ts:MistralHttpError": "Mistral HTTP 错误类，封装状态码和响应体。",
    "packages/ai/src/api/openai-codex-responses.ts:CodexApiError": "Codex API 错误类，封装错误代码和 payload。",
    "packages/ai/src/api/openai-codex-responses.ts:CodexProtocolError": "Codex 协议错误类，表示 WebSocket 通信协议异常。",
    "packages/ai/src/api/openai-codex-responses.ts:WebSocketCloseError": "WebSocket 关闭错误类，封装关闭码、原因和是否正常关闭。",
    "packages/ai/src/api/pi-messages.ts:PiMessagesResponseError": "Pi Messages 响应错误类，封装错误代码和诊断详情。",
}

# Function tags
fn_tags_default = {
    "stream": ["api-handler", "streaming", "entry-point"],
    "streamSimple": ["api-handler", "streaming"],
    "buildParams": ["api-handler", "request-builder"],
    "convertMessages": ["utility", "message-conversion"],
    "convertTools": ["utility", "tool-conversion"],
    "createClient": ["utility", "client-creation"],
    "mapStopReason": ["utility", "stop-reason-mapping"],
}

# Skip these files for function extraction (trivial re-export wrappers)
skip_fn_files = {
    "packages/ai/src/api/azure-openai-responses.lazy.ts",
    "packages/ai/src/api/bedrock-converse-stream.lazy.ts",
    "packages/ai/src/api/google-generative-ai.lazy.ts",
    "packages/ai/src/api/google-vertex.lazy.ts",
    "packages/ai/src/api/mistral-conversations.lazy.ts",
    "packages/ai/src/api/openai-codex-responses.lazy.ts",
    "packages/ai/src/api/pi-messages.lazy.ts",
    "packages/ai/src/bedrock-provider.ts",
    "packages/ai/src/legacy-api-aliases.ts",
    "packages/ai/src/image-models.ts",
    "packages/ai/src/images.ts",
}

# Track which function/class nodes are created and their exports
created_fn_nodes = set()
created_cls_nodes = set()
exported_fns = {}  # path -> set of exported fn names
exported_cls = {}  # path -> set of exported cls names

for path in all_files:
    r = results_by_path[path]
    exports = r.get('exports', [])
    exported_fns[path] = set()
    exported_cls[path] = set()
    for e in exports:
        exported_fns[path].add(e['name'])
        exported_cls[path].add(e['name'])

# Create function nodes
for path in all_files:
    if path in skip_fn_files:
        continue
    r = results_by_path[path]
    for fn in r.get('functions', []):
        fn_name = fn.get('name', '')
        start = fn.get('startLine', 0)
        end = fn.get('endLine', 0)
        line_count = end - start + 1
        is_exported = fn_name in exported_fns.get(path, set())

        # Significance filter: 10+ lines OR exported
        if line_count < 10 and not is_exported:
            continue
        # Skip trivial one-liners even if exported
        if line_count < 4:
            continue

        node_id = f"function:{path}:{fn_name}"
        if node_id in created_fn_nodes:
            continue

        summary = fn_summaries.get(f"{path}:{fn_name}", f"{fn_name} 函数。")
        tags = fn_tags_default.get(fn_name, ["utility"]).copy()
        if is_exported:
            if "entry-point" not in tags:
                tags.append("exported")
        # Ensure at least 3 tags
        if len(tags) < 3:
            tags.extend(["function", "internal"])
        tags = tags[:5]

        complexity = "simple"
        if line_count >= 100:
            complexity = "complex"
        elif line_count >= 30:
            complexity = "moderate"

        nodes.append({
            "id": node_id,
            "type": "function",
            "name": fn_name,
            "filePath": path,
            "lineRange": [start, end],
            "summary": summary,
            "tags": tags[:5],
            "complexity": complexity
        })
        created_fn_nodes.add(node_id)

# Create class nodes
for path in all_files:
    if path in skip_fn_files:
        continue
    r = results_by_path[path]
    for cls in r.get('classes', []):
        cls_name = cls.get('name', '')
        start = cls.get('startLine', 0)
        end = cls.get('endLine', 0)
        line_count = end - start + 1
        methods = cls.get('methods', [])
        is_exported = cls_name in exported_cls.get(path, set())

        # Significance filter: 2+ methods or 20+ lines OR exported
        if len(methods) < 2 and line_count < 20 and not is_exported:
            continue
        # Skip trivial one-liners
        if line_count < 5 and not is_exported:
            continue

        node_id = f"class:{path}:{cls_name}"
        if node_id in created_cls_nodes:
            continue

        summary = cls_summaries.get(f"{path}:{cls_name}", f"{cls_name} 类。")
        tags = ["error-class", "exception"]
        if is_exported:
            tags.append("exported")
        # Ensure at least 3 tags
        if len(tags) < 3:
            tags.extend(["class", "internal"])
        tags = tags[:5]

        complexity = "simple"
        if line_count >= 50:
            complexity = "complex"
        elif line_count >= 15:
            complexity = "moderate"

        nodes.append({
            "id": node_id,
            "type": "class",
            "name": cls_name,
            "filePath": path,
            "lineRange": [start, end],
            "summary": summary,
            "tags": tags[:5],
            "complexity": complexity
        })
        created_cls_nodes.add(node_id)

# ============================================================
# EDGES
# ============================================================

# 1. contains edges (file -> function/class)
for node in nodes:
    if node['type'] in ('function', 'class'):
        file_id = f"file:{node['filePath']}"
        edges.append({
            "source": file_id,
            "target": node['id'],
            "type": "contains",
            "direction": "forward",
            "weight": 1.0
        })

# 2. exports edges (file -> exported function/class)
for node in nodes:
    if node['type'] == 'function':
        path = node['filePath']
        fn_name = node['name']
        if fn_name in exported_fns.get(path, set()):
            edges.append({
                "source": f"file:{path}",
                "target": node['id'],
                "type": "exports",
                "direction": "forward",
                "weight": 0.8
            })
    elif node['type'] == 'class':
        path = node['filePath']
        cls_name = node['name']
        if cls_name in exported_cls.get(path, set()):
            edges.append({
                "source": f"file:{path}",
                "target": node['id'],
                "type": "exports",
                "direction": "forward",
                "weight": 0.8
            })

# 3. imports edges (from batchImportData)
for path, imports in batch_import_data.items():
    file_id = f"file:{path}"
    for imp_path in imports:
        target_id = f"file:{imp_path}"
        if file_id == target_id:
            continue
        edges.append({
            "source": file_id,
            "target": target_id,
            "type": "imports",
            "direction": "forward",
            "weight": 0.7
        })

# 4. calls edges (cross-file function calls inferred from imports + call graph)
# Build a map of exported function names to their file paths
fn_to_file = {}
for node in nodes:
    if node['type'] == 'function':
        fn_to_file.setdefault(node['name'], set()).add(node['filePath'])

# For each file's call graph, check if called functions exist in imported files
for path in all_files:
    r = results_by_path[path]
    call_graph = r.get('callGraph', [])
    imported_files = set(batch_import_data.get(path, []))
    for call in call_graph:
        caller = call.get('caller', '')
        callee = call.get('callee', '')
        if callee in fn_to_file:
            callee_files = fn_to_file[callee]
            for cf in callee_files:
                if cf != path and cf in imported_files:
                    caller_id = f"function:{path}:{caller}"
                    callee_id = f"function:{cf}:{callee}"
                    if caller_id in created_fn_nodes and callee_id in created_fn_nodes:
                        edges.append({
                            "source": caller_id,
                            "target": callee_id,
                            "type": "calls",
                            "direction": "forward",
                            "weight": 0.8
                        })

# ============================================================
# SPLIT INTO PARTS
# ============================================================

node_count = len(nodes)
edge_count = len(edges)
parts = max(1, math.ceil(max(node_count / 60, edge_count / 120)))

print(f"Total nodes: {node_count}, Total edges: {edge_count}, Parts: {parts}")

# Sort files alphabetically
sorted_files = sorted(all_files)
chunk_size = math.ceil(len(sorted_files) / parts)

# Assign files to parts
part_files = []
for i in range(parts):
    start_idx = i * chunk_size
    end_idx = min((i + 1) * chunk_size, len(sorted_files))
    part_files.append(set(sorted_files[start_idx:end_idx]))

# Assign nodes to parts
part_nodes = [[] for _ in range(parts)]
for node in nodes:
    fp = node.get('filePath', '')
    for i, pf in enumerate(part_files):
        if fp in pf:
            part_nodes[i].append(node)
            break

# Assign edges to parts (based on source node's file)
part_edges = [[] for _ in range(parts)]
for edge in edges:
    source = edge['source']
    # Extract file path from source id
    if source.startswith('file:'):
        fp = source[5:]
    elif source.startswith('function:') or source.startswith('class:'):
        # format: function:path:name  or  class:path:name
        parts_id = source.split(':')
        if len(parts_id) >= 3:
            fp = ':'.join(parts_id[1:-1])
        else:
            fp = ''
    else:
        fp = ''

    for i, pf in enumerate(part_files):
        if fp in pf:
            part_edges[i].append(edge)
            break

# Write parts
output_dir = '/Users/zhouyi/AiHub/pi/.understand-anything/intermediate'
for i in range(parts):
    part_num = i + 1
    filename = f"batch-3-part-{part_num}.json" if parts > 1 else "batch-3.json"
    filepath = os.path.join(output_dir, filename)
    part_data = {
        "nodes": part_nodes[i],
        "edges": part_edges[i]
    }
    with open(filepath, 'w') as f:
        json.dump(part_data, f, ensure_ascii=False, indent=2)
    print(f"Written {filename}: {len(part_nodes[i])} nodes, {len(part_edges[i])} edges")

# Verify import edge count
import_edge_count = sum(1 for e in edges if e['type'] == 'imports')
expected_import_count = sum(len(v) for v in batch_import_data.values())
print(f"Import edges: {import_edge_count}, Expected: {expected_import_count}")
