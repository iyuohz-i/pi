const fs = require("fs");
const path = require("path");

const extractData = JSON.parse(fs.readFileSync("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-6.json", "utf8"));
const dispatchData = JSON.parse(fs.readFileSync("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-6.json", "utf8"));

// File metadata: summaries, tags, complexity
const fileMeta = {
  "packages/ai/test/google-shared-gemini3-unsigned-tool-call.test.ts": {
    summary: "测试 Gemini 3 模型在未签名 tool call 场景下的消息转换与 stop reason 映射，验证 google-shared API 层的容错能力。",
    tags: ["test", "google", "tool-call", "gemini"],
    complexity: "moderate"
  },
  "packages/ai/test/google-shared-image-tool-result-routing.test.ts": {
    summary: "验证 Google 共享 API 层对图片类型 tool result 的消息路由与转换逻辑是否正确。",
    tags: ["test", "google", "image", "tool-result"],
    complexity: "moderate"
  },
  "packages/ai/test/google-shared-retry.test.ts": {
    summary: "测试 Google API 请求的重试逻辑，验证 retryGoogleRequest 在不同错误状态码下的行为。",
    tags: ["test", "google", "retry", "error-handling"],
    complexity: "simple"
  },
  "packages/ai/test/google-shared-signed-empty-blocks.test.ts": {
    summary: "测试 Google 共享 API 对签名空 thinking block 的处理，确保 retainThoughtSignature 逻辑正确。",
    tags: ["test", "google", "thinking", "signature"],
    complexity: "moderate"
  },
  "packages/ai/test/google-thinking-disable.test.ts": {
    summary: "端到端测试 Google 模型禁用 thinking/reasoning 功能后的行为，验证输出不含 thinking 事件且 token 消耗降低。",
    tags: ["test", "google", "thinking", "e2e"],
    complexity: "moderate"
  },
  "packages/ai/test/google-thinking-signature.test.ts": {
    summary: "测试 Google thinking signature 保留逻辑，验证 retainThoughtSignature 函数的行为。",
    tags: ["test", "google", "thinking", "signature"],
    complexity: "simple"
  },
  "packages/ai/test/google-vertex-api-key-resolution.test.ts": {
    summary: "测试 Google Vertex AI 的 API Key 解析逻辑，使用 mock 验证不同凭据配置下的密钥选取策略。",
    tags: ["test", "google-vertex", "api-key", "authentication"],
    complexity: "moderate"
  },
  "packages/ai/test/image-model-data.test.ts": {
    summary: "验证图像模型数据生成脚本的输出是否符合预期格式，测试 parseOpenRouterImageModels 的解析能力。",
    tags: ["test", "image-models", "data-validation"],
    complexity: "simple"
  },
  "packages/ai/test/image-tool-result.test.ts": {
    summary: "端到端测试各 LLM provider 对包含图片的 tool result 的处理能力，验证模型能正确识别并描述图片内容。",
    tags: ["test", "image", "tool-result", "e2e", "multi-provider"],
    complexity: "complex"
  },
  "packages/ai/test/images.test.ts": {
    summary: "测试图像生成功能，涵盖基本生成、文本+图片混合输出、图片输入处理三种场景。",
    tags: ["test", "image-generation", "multi-provider"],
    complexity: "moderate"
  },
  "packages/ai/test/interleaved-thinking.test.ts": {
    summary: "测试 LLM 在工具调用间的交错思考能力，验证第二次 tool call 前仍能产生 thinking block。",
    tags: ["test", "thinking", "tool-call", "interleaved"],
    complexity: "moderate"
  },
  "packages/ai/test/lax-message-content.test.ts": {
    summary: "测试宽松消息内容转换逻辑，验证 transformMessages 对仅文本消息的兼容处理。",
    tags: ["test", "message-transform", "validation"],
    complexity: "simple"
  },
  "packages/ai/test/max-thinking.test.ts": {
    summary: "测试 OpenAI Codex 模型的 thinking token 上限配置，使用 mock token 验证 max thinking budget 限制。",
    tags: ["test", "openai-codex", "thinking", "token-budget"],
    complexity: "moderate"
  },
  "packages/ai/test/mistral-http-transport.test.ts": {
    summary: "测试 Mistral Conversations API 的 HTTP 传输层，使用 mock SSE 响应验证流式解析、分块传输与错误处理。",
    tags: ["test", "mistral", "http-transport", "sse", "streaming"],
    complexity: "complex"
  },
  "packages/ai/test/mistral-raw-stop-reason.test.ts": {
    summary: "测试 Mistral API 原始 stop reason 的映射逻辑，验证不同 finishReason 到统一 stopReason 的转换。",
    tags: ["test", "mistral", "stop-reason", "mapping"],
    complexity: "simple"
  },
  "packages/ai/test/mistral-reasoning-mode.test.ts": {
    summary: "测试 Mistral 模型的 reasoning mode 配置，验证 streamSimple 请求中 reasoning 参数的正确传递。",
    tags: ["test", "mistral", "reasoning", "streaming"],
    complexity: "moderate"
  },
  "packages/ai/test/mistral-tool-schema.test.ts": {
    summary: "测试 Mistral 模型的 tool schema 转换，验证工具定义格式在 compat 层的正确映射。",
    tags: ["test", "mistral", "tool-schema", "validation"],
    complexity: "simple"
  },
  "packages/ai/test/node-http-proxy.test.ts": {
    summary: "测试 Node.js HTTP 代理 URL 解析逻辑，验证 resolveHttpProxyUrlForTarget 在不同环境变量配置下的行为。",
    tags: ["test", "http-proxy", "network", "configuration"],
    complexity: "moderate"
  },
  "packages/ai/test/oauth.ts": {
    summary: "OAuth 认证工具模块，提供 API Key 解析、auth storage 读写与 token 刷新功能，供多个 E2E 测试共享使用。",
    tags: ["test", "oauth", "authentication", "utility", "shared"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-codex-cache-affinity-e2e.test.ts": {
    summary: "端到端测试 OpenAI Codex 的 cache affinity 功能，验证连续请求的缓存命中行为。",
    tags: ["test", "openai-codex", "cache", "e2e"],
    complexity: "simple"
  },
  "packages/ai/test/openai-codex-stream.test.ts": {
    summary: "全面测试 OpenAI Codex Responses API 的流式传输，使用 mock SSE 验证 WebSocket 会话管理、工具调用、thinking 与错误处理等多种场景。",
    tags: ["test", "openai-codex", "streaming", "websocket", "sse"],
    complexity: "complex"
  },
  "packages/ai/test/openai-completions-cache-control-format.test.ts": {
    summary: "测试 OpenAI Completions API 的 cache control 格式，验证 Anthropic cache marker 在请求中的正确注入。",
    tags: ["test", "openai-completions", "cache-control", "anthropic"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-empty-tools.test.ts": {
    summary: "测试 OpenAI Completions API 在空工具列表场景下的行为，验证兼容层对 empty tools 的正确处理。",
    tags: ["test", "openai-completions", "tools", "edge-case"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-prompt-cache.test.ts": {
    summary: "测试 OpenAI Completions API 的 prompt cache 功能，验证缓存控制参数的正确传递与命中率。",
    tags: ["test", "openai-completions", "prompt-cache", "caching"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-raw-stop-reason.test.ts": {
    summary: "测试 OpenAI Completions API 原始 stop reason 的映射逻辑，验证不同 finish_reason 到统一 stopReason 的转换。",
    tags: ["test", "openai-completions", "stop-reason", "mapping"],
    complexity: "simple"
  },
  "packages/ai/test/openai-completions-reasoning-details.test.ts": {
    summary: "测试 OpenAI Completions API 的 reasoning details 输出，验证流式事件中 reasoning 内容的正确解析。",
    tags: ["test", "openai-completions", "reasoning", "streaming"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-response-model.test.ts": {
    summary: "测试 OpenAI Completions 响应中 model 字段的正确性，验证 OpenRouter Auto 路由场景下模型标识的透传。",
    tags: ["test", "openai-completions", "response-model", "openrouter"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-retry.test.ts": {
    summary: "测试 OpenAI Completions API 的重试逻辑，验证在可重试错误下的自动重发与流消费行为。",
    tags: ["test", "openai-completions", "retry", "streaming"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-thinking-as-text.test.ts": {
    summary: "测试 OpenAI Completions API 将 thinking 内容作为文本输出的模式，验证事件收集与 thinking block 的正确转换。",
    tags: ["test", "openai-completions", "thinking", "text-mode"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-thinking-token-budget.test.ts": {
    summary: "测试 OpenAI Completions API 的 thinking token budget 配置，验证 thinking budget 参数在请求中的正确传递。",
    tags: ["test", "openai-completions", "thinking", "token-budget"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-completions-tool-choice.test.ts": {
    summary: "全面测试 OpenAI Completions API 的 tool choice 功能，覆盖 auto/none/required/特定函数等多种工具选择策略。",
    tags: ["test", "openai-completions", "tool-choice", "comprehensive"],
    complexity: "complex"
  },
  "packages/ai/test/openai-completions-tool-result-images.test.ts": {
    summary: "测试 OpenAI Completions API 处理包含图片的 tool result，验证图片数据在工具结果消息中的正确封装。",
    tags: ["test", "openai-completions", "tool-result", "image"],
    complexity: "moderate"
  },
  "packages/ai/test/openai-responses-cache-affinity-e2e.test.ts": {
    summary: "端到端测试 OpenAI Responses API 的 cache affinity 功能，验证连续请求的缓存命中行为。",
    tags: ["test", "openai-responses", "cache", "e2e"],
    complexity: "simple"
  },
  "packages/ai/test/openai-responses-compat.test.ts": {
    summary: "全面测试 OpenAI Responses API 的兼容层，验证响应头捕获、流式事件转换与多种模型配置的正确性。",
    tags: ["test", "openai-responses", "compat", "streaming"],
    complexity: "complex"
  },
  "packages/ai/test/openai-responses-empty-tool-result.test.ts": {
    summary: "测试 OpenAI Responses API 对空 tool result 的处理，验证 convertResponsesMessages 对空结果的兼容转换。",
    tags: ["test", "openai-responses", "tool-result", "edge-case"],
    complexity: "simple"
  }
};

// Function metadata: summary and tags for significant functions
const funcMeta = {
  "packages/ai/test/google-shared-gemini3-unsigned-tool-call.test.ts:makeGemini3Model": {
    summary: "构建 Gemini 3 模型配置对象，封装 API、provider 和 model ID 参数。",
    tags: ["test-helper", "factory", "model-config"]
  },
  "packages/ai/test/google-shared-gemini3-unsigned-tool-call.test.ts:makeContext": {
    summary: "构建测试上下文，包含消息历史与 thought signature，用于 Gemini 3 未签名 tool call 测试。",
    tags: ["test-helper", "context-builder"]
  },
  "packages/ai/test/google-shared-image-tool-result-routing.test.ts:makeModel": {
    summary: "构建 Google 模型配置对象，用于图片 tool result 路由测试。",
    tags: ["test-helper", "factory", "model-config"]
  },
  "packages/ai/test/google-shared-image-tool-result-routing.test.ts:makeContext": {
    summary: "构建包含图片 tool result 的测试上下文，用于验证消息路由逻辑。",
    tags: ["test-helper", "context-builder", "image"]
  },
  "packages/ai/test/google-shared-signed-empty-blocks.test.ts:makeModel": {
    summary: "构建 Google 模型配置对象，用于签名空 block 测试。",
    tags: ["test-helper", "factory", "model-config"]
  },
  "packages/ai/test/google-shared-signed-empty-blocks.test.ts:makeContext": {
    summary: "构建包含签名空 block 内容的测试上下文，验证 thinking signature 保留逻辑。",
    tags: ["test-helper", "context-builder", "thinking"]
  },
  "packages/ai/test/google-thinking-disable.test.ts:makeContext": {
    summary: "构建禁用 thinking 的测试上下文，生成简单的 pong 问答消息。",
    tags: ["test-helper", "context-builder"]
  },
  "packages/ai/test/google-thinking-disable.test.ts:runWithoutReasoning": {
    summary: "执行禁用 reasoning 的流式请求，收集响应并统计 thinking 事件数、字符数与输出 token 数。",
    tags: ["test-runner", "streaming", "thinking"]
  },
  "packages/ai/test/google-thinking-disable.test.ts:expectThinkingDisabledE2E": {
    summary: "端到端验证 thinking 已被禁用，断言无 thinking 事件、pong 响应正常且 token 消耗在阈值内。",
    tags: ["test-assertion", "e2e", "thinking"]
  },
  "packages/ai/test/image-tool-result.test.ts:handleToolWithImageResult": {
    summary: "端到端测试：发送含图片的 tool result 给模型，验证模型能识别图片内容并生成后续文本响应。",
    tags: ["test-runner", "e2e", "image", "tool-result"]
  },
  "packages/ai/test/image-tool-result.test.ts:handleToolWithTextAndImageResult": {
    summary: "端到端测试：发送含文本与图片混合的 tool result，验证模型对多模态工具结果的处理能力。",
    tags: ["test-runner", "e2e", "image", "multimodal"]
  },
  "packages/ai/test/images.test.ts:basicImageGeneration": {
    summary: "测试基本图像生成流程，调用 generateImages 并验证输出包含图片类型。",
    tags: ["test-runner", "image-generation"]
  },
  "packages/ai/test/images.test.ts:handleTextAndImageOutput": {
    summary: "测试文本与图片混合输出场景，验证 generateImages 返回结果中同时包含图片和文本内容。",
    tags: ["test-runner", "image-generation", "multimodal"]
  },
  "packages/ai/test/images.test.ts:handleImageInput": {
    summary: "测试图片输入处理场景，读取本地图片文件并传入 generateImages，验证模型能处理图片输入。",
    tags: ["test-runner", "image-generation", "image-input"]
  },
  "packages/ai/test/interleaved-thinking.test.ts:asCalculatorArguments": {
    summary: "将计算器工具调用参数解析为结构化对象，提取操作数与运算符。",
    tags: ["test-helper", "parser", "calculator"]
  },
  "packages/ai/test/interleaved-thinking.test.ts:evaluateCalculatorCall": {
    summary: "评估计算器工具调用，解析参数并执行算术运算返回结果。",
    tags: ["test-helper", "calculator", "evaluator"]
  },
  "packages/ai/test/interleaved-thinking.test.ts:assertSecondToolCallWithInterleavedThinking": {
    summary: "验证第二次 tool call 前存在交错 thinking block，执行两轮工具调用并断言每轮均产生 thinking 事件。",
    tags: ["test-runner", "thinking", "tool-call", "interleaved"]
  },
  "packages/ai/test/lax-message-content.test.ts:makeTextOnlyModel": {
    summary: "构建仅返回文本内容的 mock 模型，用于宽松消息内容转换测试。",
    tags: ["test-helper", "mock", "model-config"]
  },
  "packages/ai/test/mistral-http-transport.test.ts:createBytewiseSseResponse": {
    summary: "创建逐字节的 SSE 响应流，模拟 Mistral API 的分块传输场景。",
    tags: ["test-helper", "sse", "mock", "streaming"]
  },
  "packages/ai/test/mistral-raw-stop-reason.test.ts:createFetch": {
    summary: "创建 mock fetch 函数，返回指定 finishReason 的 Mistral SSE 响应，用于 stop reason 映射测试。",
    tags: ["test-helper", "mock", "fetch", "sse"]
  },
  "packages/ai/test/mistral-reasoning-mode.test.ts:capturePayload": {
    summary: "捕获 streamSimple 发送的请求 payload，验证 reasoning mode 参数的正确传递。",
    tags: ["test-runner", "streaming", "payload-capture"]
  },
  "packages/ai/test/oauth.ts:loadAuthStorage": {
    summary: "从本地 auth storage 文件加载认证信息，读取并解析 JSON 格式的存储数据。",
    tags: ["utility", "auth", "storage", "file-io"]
  },
  "packages/ai/test/oauth.ts:resolveApiKey": {
    summary: "解析指定 provider 的 API Key，优先从 auth storage 读取 OAuth token，过期时自动刷新并持久化。",
    tags: ["utility", "auth", "api-key", "oauth", "token-refresh"]
  },
  "packages/ai/test/openai-codex-stream.test.ts:buildSSEPayload": {
    summary: "构建 OpenAI Codex SSE 响应 payload，支持自定义 status、done 标志与 endTurn 事件，模拟流式传输。",
    tags: ["test-helper", "sse", "mock", "openai-codex"]
  },
  "packages/ai/test/openai-completions-cache-control-format.test.ts:capturePayload": {
    summary: "捕获 OpenAI Completions 请求 payload，提取并返回 cache control 相关的请求体内容。",
    tags: ["test-runner", "payload-capture", "cache-control"]
  },
  "packages/ai/test/openai-completions-cache-control-format.test.ts:expectAnthropicCacheMarkers": {
    summary: "断言请求 payload 中包含 Anthropic cache marker 标记，验证 cache control 格式的正确注入。",
    tags: ["test-assertion", "cache-control", "anthropic"]
  },
  "packages/ai/test/openai-completions-reasoning-details.test.ts:model": {
    summary: "构建 mock OpenAI Completions 响应模型，返回包含 reasoning details 的流式 chunk。",
    tags: ["test-helper", "mock", "reasoning"]
  },
  "packages/ai/test/openai-completions-reasoning-details.test.ts:toolCallChunk": {
    summary: "构建包含 tool call 内容的流式 chunk 对象，模拟工具调用的流式传输。",
    tags: ["test-helper", "mock", "tool-call", "streaming"]
  },
  "packages/ai/test/openai-completions-response-model.test.ts:openRouterAuto": {
    summary: "构建 OpenRouter Auto 路由模型配置，验证响应中 model 字段的正确透传。",
    tags: ["test-helper", "openrouter", "model-config"]
  },
  "packages/ai/test/openai-completions-thinking-as-text.test.ts:buildModel": {
    summary: "构建将 thinking 内容作为文本输出的 mock 模型配置，用于 thinking-as-text 模式测试。",
    tags: ["test-helper", "mock", "thinking", "model-config"]
  },
  "packages/ai/test/openai-completions-thinking-as-text.test.ts:buildAssistant": {
    summary: "构建包含 thinking 文本的 assistant 消息对象，模拟 thinking-as-text 模式的响应内容。",
    tags: ["test-helper", "mock", "thinking", "message-builder"]
  },
  "packages/ai/test/openai-completions-thinking-token-budget.test.ts:capture": {
    summary: "捕获 streamSimple 请求中的 thinking token budget 参数，验证 budget 配置的正确传递。",
    tags: ["test-runner", "thinking", "token-budget", "payload-capture"]
  },
  "packages/ai/test/openai-completions-tool-choice.test.ts:captureSimpleParams": {
    summary: "捕获 streamSimple 请求参数中的 tool_choice 配置，用于验证不同工具选择策略的传递。",
    tags: ["test-runner", "tool-choice", "payload-capture"]
  },
  "packages/ai/test/openai-completions-tool-result-images.test.ts:buildToolResult": {
    summary: "构建包含图片数据的 tool result 消息对象，用于图片 tool result 测试。",
    tags: ["test-helper", "tool-result", "image", "message-builder"]
  },
  "packages/ai/test/openai-completions-tool-result-images.test.ts:buildEmptyToolResult": {
    summary: "构建空的 tool result 消息对象，用于验证空结果与图片结果的混合处理。",
    tags: ["test-helper", "tool-result", "message-builder"]
  },
  "packages/ai/test/openai-responses-compat.test.ts:getHeader": {
    summary: "从 fetch 请求中提取指定 header 值，用于验证 OpenAI Responses API 的响应头。",
    tags: ["test-helper", "http-headers", "fetch"]
  },
  "packages/ai/test/openai-responses-compat.test.ts:captureOpenAIResponseHeaders": {
    summary: "捕获 OpenAI Responses API 的响应头信息，验证 cache、rate-limit 等 header 的正确返回。",
    tags: ["test-runner", "http-headers", "response-capture"]
  },
  "packages/ai/test/openai-responses-empty-tool-result.test.ts:buildEmptyToolResult": {
    summary: "构建空的 tool result 消息对象，用于测试 OpenAI Responses API 对空工具结果的处理。",
    tags: ["test-helper", "tool-result", "message-builder"]
  }
};

// Determine which functions are significant (10+ lines or exported)
function isSignificant(func, filePath, exports) {
  const lines = func.endLine - func.startLine + 1;
  if (lines >= 10) return true;
  if (exports && exports.some(e => e.name === func.name)) return true;
  return false;
}

// Build nodes
const nodes = [];
const extractMap = {};
for (const r of extractData.results) {
  extractMap[r.path] = r;
}

for (const r of extractData.results) {
  const meta = fileMeta[r.path] || { summary: "测试文件", tags: ["test"], complexity: "simple" };
  const fileName = r.path.split("/").pop();

  // File node
  nodes.push({
    id: `file:${r.path}`,
    type: "file",
    name: fileName,
    filePath: r.path,
    summary: meta.summary,
    tags: meta.tags,
    complexity: meta.complexity
  });

  // Function nodes
  if (r.functions) {
    for (const func of r.functions) {
      if (!isSignificant(func, r.path, r.exports)) continue;
      const funcKey = `${r.path}:${func.name}`;
      const fmeta = funcMeta[funcKey] || { summary: `测试辅助函数 ${func.name}`, tags: ["test-helper"] };
      nodes.push({
        id: `function:${r.path}:${func.name}`,
        type: "function",
        name: func.name,
        filePath: r.path,
        lineRange: [func.startLine, func.endLine],
        summary: fmeta.summary,
        tags: fmeta.tags,
        complexity: func.endLine - func.startLine > 50 ? "moderate" : "simple"
      });
    }
  }
}

// Build edges
const edges = [];

// 1. imports edges (from batchImportData)
for (const [filePath, importPaths] of Object.entries(dispatchData.batchImportData)) {
  for (const importPath of importPaths) {
    edges.push({
      source: `file:${filePath}`,
      target: `file:${importPath}`,
      type: "imports",
      direction: "forward",
      weight: 0.7
    });
  }
}

// 2. contains edges (file → function)
for (const r of extractData.results) {
  if (!r.functions) continue;
  for (const func of r.functions) {
    if (!isSignificant(func, r.path, r.exports)) continue;
    edges.push({
      source: `file:${r.path}`,
      target: `function:${r.path}:${func.name}`,
      type: "contains",
      direction: "forward",
      weight: 1.0
    });
  }
}

// 3. exports edges (for exported functions)
for (const r of extractData.results) {
  if (!r.exports || !r.functions) continue;
  for (const exp of r.exports) {
    const func = r.functions.find(f => f.name === exp.name);
    if (func && isSignificant(func, r.path, r.exports)) {
      edges.push({
        source: `file:${r.path}`,
        target: `function:${r.path}:${exp.name}`,
        type: "exports",
        direction: "forward",
        weight: 0.8
      });
    }
  }
}

// 4. tested_by edges (production file → test file)
// For each import where target is a production file (src/ or scripts/), emit tested_by
for (const [filePath, importPaths] of Object.entries(dispatchData.batchImportData)) {
  for (const importPath of importPaths) {
    // Only emit tested_by for production files (not test helpers)
    if (importPath.includes("/src/") || importPath.includes("/scripts/")) {
      edges.push({
        source: `file:${importPath}`,
        target: `file:${filePath}`,
        type: "tested_by",
        direction: "forward",
        weight: 0.5
      });
    }
  }
}

// Remove duplicate edges
const edgeSet = new Set();
const uniqueEdges = [];
for (const e of edges) {
  const key = `${e.source}|${e.target}|${e.type}`;
  if (!edgeSet.has(key)) {
    edgeSet.add(key);
    uniqueEdges.push(e);
  }
}

console.log(`Total nodes: ${nodes.length}`);
console.log(`Total edges: ${uniqueEdges.length}`);
console.log(`  imports: ${uniqueEdges.filter(e => e.type === "imports").length}`);
console.log(`  contains: ${uniqueEdges.filter(e => e.type === "contains").length}`);
console.log(`  exports: ${uniqueEdges.filter(e => e.type === "exports").length}`);
console.log(`  tested_by: ${uniqueEdges.filter(e => e.type === "tested_by").length}`);

// Split into parts
// Sort files alphabetically
const allFiles = extractData.results.map(r => r.path).sort();
const parts = Math.ceil(Math.max(nodes.length / 60, uniqueEdges.length / 120));
const filesPerPart = Math.ceil(allFiles.length / parts);
console.log(`Parts: ${parts}, files per part: ${filesPerPart}`);

for (let p = 0; p < parts; p++) {
  const partFiles = new Set(allFiles.slice(p * filesPerPart, (p + 1) * filesPerPart));
  // All nodes whose filePath is in this part's files
  const partNodes = nodes.filter(n => n.filePath && partFiles.has(n.filePath));
  const partNodeIds = new Set(partNodes.map(n => n.id));

  // Edges whose source is in this part's nodes
  // For tested_by edges (source = production file not in batch), assign to part containing target
  const partEdges = uniqueEdges.filter(e => {
    if (partNodeIds.has(e.source)) return true;
    // For tested_by edges where source is external, check if target is in this part
    if (e.type === "tested_by" && partNodeIds.has(e.target)) return true;
    return false;
  });

  const partData = { nodes: partNodes, edges: partEdges };
  const partNum = p + 1;
  const outPath = `/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-6-part-${partNum}.json`;
  fs.writeFileSync(outPath, JSON.stringify(partData, null, 2));
  console.log(`Part ${partNum}: ${partData.nodes.length} nodes, ${partData.edges.length} edges → ${outPath}`);
}
