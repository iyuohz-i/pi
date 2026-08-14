#!/usr/bin/env python3
"""Generate batch-4 knowledge graph output (3 parts)."""

import json
import math
import os

# Read input data
with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-4.json") as f:
    extract = json.load(f)

with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-4.json") as f:
    dispatch = json.load(f)

batch_import_data = dispatch["batchImportData"]
neighbor_map = dispatch.get("neighborMap", {})

# Build a lookup from path -> extraction result
extract_map = {r["path"]: r for r in extract["results"]}

# Sort files alphabetically
all_files = sorted([r["path"] for r in extract["results"]])

# ============================================================
# NODE DEFINITIONS
# ============================================================

# File summaries (Chinese)
file_summaries = {
    "packages/ai/src/providers/faux.ts": "模拟 LLM provider，用于测试和开发环境。提供流式响应、token 估算、消息克隆等功能，支持中断和错误模拟。",
    "packages/ai/src/providers/images/register-builtins.ts": "注册内置图片生成 API provider，包括 OpenRouter 图片生成功能的懒加载注册。",
    "packages/ai/src/session-resources.ts": "管理会话级资源的注册和清理，确保会话结束时正确释放 WebSocket 连接等资源。",
    "packages/ai/src/types.ts": "AI 包的核心类型定义文件，定义了 AssistantMessage、Context、Provider 等全局共享类型接口。",
    "packages/ai/src/utils/abort-signals.ts": "组合多个 AbortSignal 为单一信号的工具函数，支持优先级和超时控制。",
    "packages/ai/src/utils/deferred-tools.ts": "将延迟工具调用从消息内容中分离提取，用于处理异步工具执行场景。",
    "packages/ai/src/utils/diagnostics.ts": "提取和附加诊断错误信息到助手消息，用于调试和错误追踪。",
    "packages/ai/src/utils/error-body.ts": "标准化 provider 错误响应，提取 HTTP body 文本并格式化错误消息。",
    "packages/ai/src/utils/estimate.ts": "估算消息和上下文的 token 数量，结合文本和图片内容进行粗略计算。",
    "packages/ai/src/utils/event-stream.ts": "事件流和助手消息事件流的实现，提供 push/end/result 等流式操作接口。",
    "packages/ai/src/utils/hash.ts": "生成字符串的短哈希值，用于缓存键和唯一标识。",
    "packages/ai/src/utils/headers.ts": "将 Headers 对象和 provider header 配置转换为 Record 类型。",
    "packages/ai/src/utils/json-parse.ts": "JSON 解析与修复工具，支持流式 JSON 解析、控制字符转义和损坏 JSON 修复。",
    "packages/ai/src/utils/node-http-proxy.ts": "解析 HTTP/HTTPS 代理配置，根据目标 URL 解析适用的代理服务器地址。",
    "packages/ai/src/utils/overflow.ts": "检测上下文溢出错误，通过模式匹配识别各 provider 的上下文长度超限错误。",
    "packages/ai/src/utils/provider-env.ts": "获取 provider 专用环境变量值，支持 Bun 沙箱环境变量覆盖。",
    "packages/ai/src/utils/provider-retry.ts": "Provider 请求重试逻辑，包含可重试错误判断、重试延迟计算和可中断休眠。",
    "packages/ai/src/utils/retry.ts": "助手调用重试机制，支持指数退避、可重试错误判断和中断休眠错误处理。",
    "packages/ai/src/utils/sanitize-unicode.ts": "清理 Unicode 代理对，确保字符串在所有 JavaScript 环境中正确处理。",
    "packages/ai/src/utils/text.ts": "从消息内容中提取纯文本，处理文本和图片块类型。",
    "packages/ai/src/utils/typebox-helpers.ts": "TypeBox schema 辅助函数，提供 StringEnum 用于定义字符串枚举类型。",
    "packages/ai/src/utils/uuid.ts": "生成 UUIDv7 格式的唯一标识符，基于时间戳保证时序排序。",
    "packages/ai/src/utils/validation.ts": "工具调用参数验证和 JSON Schema 强制类型转换，支持联合类型和可选空值处理。",
    "packages/ai/test/abort.test.ts": "测试 AbortSignal 中断功能，验证流式和完成模式下的中断行为及后续消息处理。",
    "packages/ai/test/anthropic-adaptive-thinking-models.test.ts": "测试 Anthropic 自适应思维模型配置，验证所有模型的 thinking level 支持。",
    "packages/ai/test/anthropic-auth-token.test.ts": "测试 Anthropic auth token 认证流程，验证 SSE 响应和 token 鉴权。",
    "packages/ai/test/anthropic-cache-write-1h-cost.test.ts": "测试 Anthropic 1 小时缓存写入计费，验证 cache_creation input tokens 的费用计算。",
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts": "测试 Anthropic eager tool input 兼容性，验证工具输入 schema 的兼容模式处理。",
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts": "端到端测试 Anthropic eager tool input 流式功能，验证各 provider 的工具启用请求。",
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts": "测试 Anthropic 空 thinking signature 兼容性，验证允许空签名时的请求 payload。",
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts": "测试 Anthropic 强制自适应思维功能，验证 compat 配置对 thinking 参数的控制。",
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts": "端到端测试 Anthropic 长缓存保留功能，验证各 provider 的长缓存保留请求。",
    "packages/ai/test/anthropic-opus-4-8-smoke.test.ts": "Anthropic Opus 4.8 模型冒烟测试，验证模型基本可用性。",
    "packages/ai/test/anthropic-sse-parsing.test.ts": "测试 Anthropic SSE 事件流解析，验证各类 SSE 事件的正确处理和错误恢复。",
    "packages/ai/test/anthropic-temperature-compat.test.ts": "测试 Anthropic temperature 兼容性，验证 compat 配置对 temperature 参数的控制。",
}

# File tags
file_tags = {
    "packages/ai/src/providers/faux.ts": ["provider", "mock", "streaming", "testing", "factory"],
    "packages/ai/src/providers/images/register-builtins.ts": ["provider", "images", "registry", "factory"],
    "packages/ai/src/session-resources.ts": ["session", "cleanup", "resource-management"],
    "packages/ai/src/types.ts": ["type-definition", "core-types", "barrel"],
    "packages/ai/src/utils/abort-signals.ts": ["utility", "abort-signal", "async"],
    "packages/ai/src/utils/deferred-tools.ts": ["utility", "deferred-tools", "message-processing"],
    "packages/ai/src/utils/diagnostics.ts": ["utility", "diagnostics", "error-handling"],
    "packages/ai/src/utils/error-body.ts": ["utility", "error-handling", "provider-error"],
    "packages/ai/src/utils/estimate.ts": ["utility", "token-estimation", "context"],
    "packages/ai/src/utils/event-stream.ts": ["utility", "event-stream", "streaming"],
    "packages/ai/src/utils/hash.ts": ["utility", "hash", "caching"],
    "packages/ai/src/utils/headers.ts": ["utility", "headers", "serialization"],
    "packages/ai/src/utils/json-parse.ts": ["utility", "json-parse", "streaming", "repair"],
    "packages/ai/src/utils/node-http-proxy.ts": ["utility", "proxy", "http"],
    "packages/ai/src/utils/overflow.ts": ["utility", "context-overflow", "error-detection"],
    "packages/ai/src/utils/provider-env.ts": ["utility", "environment", "provider-config"],
    "packages/ai/src/utils/provider-retry.ts": ["utility", "retry", "provider-error"],
    "packages/ai/src/utils/retry.ts": ["utility", "retry", "exponential-backoff"],
    "packages/ai/src/utils/sanitize-unicode.ts": ["utility", "unicode", "sanitization"],
    "packages/ai/src/utils/text.ts": ["utility", "text-extraction", "message-processing"],
    "packages/ai/src/utils/typebox-helpers.ts": ["utility", "typebox", "schema"],
    "packages/ai/src/utils/uuid.ts": ["utility", "uuid", "identifier"],
    "packages/ai/src/utils/validation.ts": ["utility", "validation", "json-schema", "coercion"],
    "packages/ai/test/abort.test.ts": ["test", "abort-signal", "streaming"],
    "packages/ai/test/anthropic-adaptive-thinking-models.test.ts": ["test", "anthropic", "thinking-models"],
    "packages/ai/test/anthropic-auth-token.test.ts": ["test", "anthropic", "auth-token", "sse"],
    "packages/ai/test/anthropic-cache-write-1h-cost.test.ts": ["test", "anthropic", "cache", "cost"],
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts": ["test", "anthropic", "tool-input", "compat"],
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts": ["test", "anthropic", "tool-input", "e2e"],
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts": ["test", "anthropic", "thinking-signature", "compat"],
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts": ["test", "anthropic", "adaptive-thinking", "compat"],
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts": ["test", "anthropic", "cache-retention", "e2e"],
    "packages/ai/test/anthropic-opus-4-8-smoke.test.ts": ["test", "anthropic", "smoke-test", "opus"],
    "packages/ai/test/anthropic-sse-parsing.test.ts": ["test", "anthropic", "sse-parsing", "streaming"],
    "packages/ai/test/anthropic-temperature-compat.test.ts": ["test", "anthropic", "temperature", "compat"],
}

# File complexity
file_complexity = {}
for r in extract["results"]:
    path = r["path"]
    nel = r.get("nonEmptyLines", 0)
    if nel > 200:
        file_complexity[path] = "complex"
    elif nel > 50:
        file_complexity[path] = "moderate"
    else:
        file_complexity[path] = "simple"

# Function summaries (Chinese) - keyed by "path:functionName"
func_summaries = {
    # faux.ts
    "packages/ai/src/providers/faux.ts:fauxText": "创建文本类型的 faux 内容块。",
    "packages/ai/src/providers/faux.ts:fauxThinking": "创建思维类型的 faux 内容块。",
    "packages/ai/src/providers/faux.ts:fauxToolCall": "创建工具调用类型的 faux 内容块，包含随机 ID 和参数。",
    "packages/ai/src/providers/faux.ts:fauxAssistantMessage": "创建完整的 faux 助手消息，支持内容和选项配置。",
    "packages/ai/src/providers/faux.ts:contentToText": "将用户内容块数组转换为纯文本表示。",
    "packages/ai/src/providers/faux.ts:assistantContentToText": "将助手内容块数组转换为纯文本，处理文本、思维和工具调用块。",
    "packages/ai/src/providers/faux.ts:serializeContext": "将对话上下文序列化为文本，包含系统提示、消息历史和工具定义。",
    "packages/ai/src/providers/faux.ts:withUsageEstimate": "为 faux 消息添加 token 使用量估算，包括输入、输出和缓存 token。",
    "packages/ai/src/providers/faux.ts:splitStringByTokenSize": "按 token 大小将字符串分割为多个块，用于模拟流式输出。",
    "packages/ai/src/providers/faux.ts:cloneMessage": "克隆消息并更新其 API、provider 和 modelId 元数据。",
    "packages/ai/src/providers/faux.ts:createDeferredMessage": "创建延迟处理的消息对象，包含 model 和 handle 回调。",
    "packages/ai/src/providers/faux.ts:createErrorMessage": "创建错误消息，包含错误详情和 provider 元数据。",
    "packages/ai/src/providers/faux.ts:streamWithDeltas": "模拟流式增量输出，按 token 分块并以指定速率发送 delta 事件。",
    "packages/ai/src/providers/faux.ts:createFauxCore": "创建 faux provider 核心实现，配置流式和完成模式的完整逻辑。",
    "packages/ai/src/providers/faux.ts:fauxProvider": "创建 faux provider 实例，封装 createFauxCore 并注册到 provider 系统。",
    # register-builtins.ts
    "packages/ai/src/providers/images/register-builtins.ts:createLazyLoadErrorImages": "创建懒加载图片 provider 的错误处理函数。",
    "packages/ai/src/providers/images/register-builtins.ts:generateImagesOpenRouter": "通过 OpenRouter API 生成图片的入口函数。",
    "packages/ai/src/providers/images/register-builtins.ts:registerBuiltInImagesApiProviders": "注册所有内置图片生成 API provider 到注册表。",
    # session-resources.ts
    "packages/ai/src/session-resources.ts:registerSessionResourceCleanup": "注册会话级资源清理回调函数。",
    "packages/ai/src/session-resources.ts:cleanupSessionResources": "执行所有已注册的会话资源清理回调。",
    # abort-signals.ts
    "packages/ai/src/utils/abort-signals.ts:combineAbortSignals": "组合多个 AbortSignal 为单一信号，支持超时和优先级控制。",
    # deferred-tools.ts
    "packages/ai/src/utils/deferred-tools.ts:splitDeferredTools": "从消息内容中分离延迟工具调用，返回工具和非工具内容。",
    # diagnostics.ts
    "packages/ai/src/utils/diagnostics.ts:formatThrownValue": "格式化抛出的异常值为字符串表示。",
    "packages/ai/src/utils/diagnostics.ts:extractDiagnosticError": "从错误对象中提取诊断信息，返回结构化错误详情。",
    "packages/ai/src/utils/diagnostics.ts:createAssistantMessageDiagnostic": "创建助手消息的诊断信息对象。",
    "packages/ai/src/utils/diagnostics.ts:appendAssistantMessageDiagnostic": "向助手消息追加诊断信息。",
    # error-body.ts
    "packages/ai/src/utils/error-body.ts:normalizeProviderError": "标准化 provider 错误对象，提取 body 文本和状态码。",
    "packages/ai/src/utils/error-body.ts:formatProviderError": "格式化 provider 错误为用户友好的错误消息字符串。",
    "packages/ai/src/utils/error-body.ts:truncateErrorText": "截断错误文本到最大长度限制。",
    "packages/ai/src/utils/error-body.ts:safeJsonStringify": "安全地序列化 JSON，处理循环引用和特殊字符。",
    # estimate.ts
    "packages/ai/src/utils/estimate.ts:calculateContextTokens": "计算上下文 token 数量的辅助函数。",
    "packages/ai/src/utils/estimate.ts:estimateTextTokens": "估算文本字符串的 token 数量。",
    "packages/ai/src/utils/estimate.ts:estimateTextAndImageContentTokens": "估算文本和图片混合内容的 token 数量。",
    "packages/ai/src/utils/estimate.ts:estimateMessageTokens": "估算单条消息的 token 数量，处理各类内容块。",
    "packages/ai/src/utils/estimate.ts:getLastAssistantUsageInfo": "获取上下文中最后一条助手消息的使用量信息。",
    "packages/ai/src/utils/estimate.ts:estimateMessages": "估算消息数组的总 token 数量。",
    "packages/ai/src/utils/estimate.ts:estimateContextTokens": "估算完整上下文的 token 数量，包括系统提示和工具定义。",
    # event-stream.ts
    "packages/ai/src/utils/event-stream.ts:createAssistantMessageEventStream": "创建助手消息事件流实例的工厂函数。",
    # hash.ts
    "packages/ai/src/utils/hash.ts:shortHash": "生成字符串的短哈希值，使用 FNV-1a 算法。",
    # headers.ts
    "packages/ai/src/utils/headers.ts:headersToRecord": "将 Headers 对象转换为 Record<string, string> 类型。",
    "packages/ai/src/utils/headers.ts:providerHeadersToRecord": "将 provider header 配置转换为 Record 类型，处理大小写。",
    # json-parse.ts
    "packages/ai/src/utils/json-parse.ts:escapeControlCharacter": "转义 JSON 字符串中的控制字符。",
    "packages/ai/src/utils/json-parse.ts:repairJson": "修复损坏的 JSON 字符串，处理截断、语法错误和结构问题。",
    "packages/ai/src/utils/json-parse.ts:parseJsonWithRepair": "解析 JSON 字符串，解析失败时自动尝试修复后重试。",
    "packages/ai/src/utils/json-parse.ts:parseStreamingJson": "解析流式 JSON 片段，支持增量解析和部分 JSON 容错。",
    # node-http-proxy.ts
    "packages/ai/src/utils/node-http-proxy.ts:getProxyEnv": "从环境变量获取代理配置（HTTP_PROXY/HTTPS_PROXY）。",
    "packages/ai/src/utils/node-http-proxy.ts:parseProxyTargetUrl": "解析代理目标 URL，验证协议合法性。",
    "packages/ai/src/utils/node-http-proxy.ts:shouldProxyHostname": "判断指定主机名是否应通过代理访问，排除 localhost 等。",
    "packages/ai/src/utils/node-http-proxy.ts:getProxyForUrl": "根据目标 URL 获取适用的代理地址。",
    "packages/ai/src/utils/node-http-proxy.ts:resolveHttpProxyUrlForTarget": "为目标 URL 解析 HTTP 代理地址，返回完整代理 URL。",
    # overflow.ts
    "packages/ai/src/utils/overflow.ts:isContextOverflow": "检测错误是否为上下文溢出，匹配各 provider 的溢出错误模式。",
    "packages/ai/src/utils/overflow.ts:isRecoverableLength": "判断上下文长度是否可通过截断消息恢复。",
    "packages/ai/src/utils/overflow.ts:getOverflowPatterns": "获取所有 provider 的上下文溢出错误匹配模式。",
    # provider-env.ts
    "packages/ai/src/utils/provider-env.ts:getBunSandboxEnvValue": "获取 Bun 沙箱环境中的环境变量值。",
    "packages/ai/src/utils/provider-env.ts:getProviderEnvValue": "获取 provider 专用环境变量值，支持 Bun 沙箱覆盖。",
    # provider-retry.ts
    "packages/ai/src/utils/provider-retry.ts:isRetryableProviderError": "判断 provider 错误是否可重试（如 429、503 等）。",
    "packages/ai/src/utils/provider-retry.ts:validateServerRetryDelayMs": "验证服务器返回的重试延迟值是否在合理范围内。",
    "packages/ai/src/utils/provider-retry.ts:getRetryDelayMs": "计算重试延迟时间，优先使用服务器指定的延迟。",
    "packages/ai/src/utils/provider-retry.ts:abortableSleep": "可被 AbortSignal 中断的异步休眠函数。",
    "packages/ai/src/utils/provider-retry.ts:retryProviderRequest": "执行 provider 请求并自动重试，支持指数退避和服务器延迟。",
    # retry.ts
    "packages/ai/src/utils/retry.ts:sleep": "可被 AbortSignal 中断的异步休眠，支持指数退避延迟。",
    "packages/ai/src/utils/retry.ts:retryAssistantCall": "执行助手调用并自动重试，支持错误分类和退避策略。",
    "packages/ai/src/utils/retry.ts:isRetryableAssistantError": "判断助手错误是否可重试（如速率限制、服务器错误等）。",
    # sanitize-unicode.ts
    "packages/ai/src/utils/sanitize-unicode.ts:sanitizeSurrogates": "清理字符串中的孤立 Unicode 代理对，防止编码错误。",
    # text.ts
    "packages/ai/src/utils/text.ts:contentText": "从消息内容中提取纯文本，忽略图片等非文本块。",
    # typebox-helpers.ts
    "packages/ai/src/utils/typebox-helpers.ts:StringEnum": "创建 TypeBox 字符串枚举 schema 的辅助函数。",
    # uuid.ts
    "packages/ai/src/utils/uuid.ts:uuidv7": "生成 UUIDv7 格式的唯一标识符，基于时间戳保证时序排序。",
    # validation.ts
    "packages/ai/src/utils/validation.ts:matchesJsonType": "检查值是否匹配指定的 JSON 类型。",
    "packages/ai/src/utils/validation.ts:coercePrimitiveByType": "按 JSON Schema 类型强制转换原始值（字符串转数字等）。",
    "packages/ai/src/utils/validation.ts:applySchemaObjectCoercion": "对对象值应用 JSON Schema 类型强制转换。",
    "packages/ai/src/utils/validation.ts:applySchemaArrayCoercion": "对数组值应用 JSON Schema 类型强制转换。",
    "packages/ai/src/utils/validation.ts:coerceWithUnionSchema": "使用联合类型 schema 尝试强制转换值。",
    "packages/ai/src/utils/validation.ts:coerceWithJsonSchema": "根据完整 JSON Schema 递归强制转换值的类型。",
    "packages/ai/src/utils/validation.ts:normalizeOptionalNulls": "规范化可选字段的 null 值，移除不必要的 null 属性。",
    "packages/ai/src/utils/validation.ts:getValidator": "获取 TypeBox schema 的验证器函数，带缓存。",
    "packages/ai/src/utils/validation.ts:formatValidationPath": "格式化验证错误路径为可读字符串。",
    "packages/ai/src/utils/validation.ts:validateToolCall": "验证工具调用的参数是否符合 schema 定义。",
    "packages/ai/src/utils/validation.ts:validateToolArguments": "验证工具参数并自动执行类型强制转换，返回验证结果和错误信息。",
    # Test functions
    "packages/ai/test/abort.test.ts:testAbortSignal": "测试流式请求的 AbortSignal 中断，验证中断后仍能继续新消息。",
    "packages/ai/test/abort.test.ts:testImmediateAbort": "测试立即中断 AbortSignal 时完成请求的行为。",
    "packages/ai/test/abort.test.ts:testAbortThenNewMessage": "测试中断后发送新消息的完整流程。",
    "packages/ai/test/anthropic-cache-write-1h-cost.test.ts:eventsWithCacheCreation": "构造带 cache_creation input tokens 的 SSE 事件序列。",
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts:createModel": "创建用于测试的 Anthropic 模型实例，配置 compat 选项。",
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts:captureAnthropicRequest": "启动本地服务器捕获 Anthropic API 请求，验证 tool input schema。",
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:getProbePriority": "根据模型 ID 获取探针优先级，用于选择测试模型。",
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:selectOneCasePerProvider": "从所有用例中按 provider 选择一个代表用例。",
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:expectToolEnabledRequestAccepted": "验证带工具启用的请求被 provider 接受并返回有效响应。",
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:makeModel": "创建 Anthropic 模型实例，配置空 thinking signature 兼容选项。",
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:makeContext": "构造包含 thinking signature 的测试上下文。",
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:capturePayload": "流式发送请求并捕获实际发送的 payload。",
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts:makeCustomModel": "创建带 compat 配置的自定义 Anthropic 模型。",
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts:capturePayload": "流式发送请求并捕获 payload，验证 thinking 参数。",
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:getProbePriority": "根据模型 ID 获取探针优先级。",
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:selectOneCasePerProvider": "按 provider 选择一个代表用例。",
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:expectLongCacheRetentionAccepted": "验证长缓存保留请求被 provider 接受。",
    "packages/ai/test/anthropic-opus-4-8-smoke.test.ts:makeContext": "创建 Opus 4.8 冒烟测试的上下文。",
    "packages/ai/test/anthropic-temperature-compat.test.ts:makeCustomModel": "创建带 temperature compat 配置的自定义模型。",
    "packages/ai/test/anthropic-temperature-compat.test.ts:capturePayload": "流式发送请求并捕获 payload，验证 temperature 参数。",
}

# Class summaries (Chinese)
class_summaries = {
    "packages/ai/src/utils/event-stream.ts:EventStream": "通用事件流类，提供 push、end、result 等流式操作接口，支持异步迭代。",
    "packages/ai/src/utils/event-stream.ts:AssistantMessageEventStream": "助手消息专用事件流，继承 EventStream，扩展助手消息事件类型。",
}

# Function tags
func_tags = {
    # faux.ts
    "packages/ai/src/providers/faux.ts:fauxText": ["factory", "content-block", "text"],
    "packages/ai/src/providers/faux.ts:fauxThinking": ["factory", "content-block", "thinking"],
    "packages/ai/src/providers/faux.ts:fauxToolCall": ["factory", "content-block", "tool-call"],
    "packages/ai/src/providers/faux.ts:fauxAssistantMessage": ["factory", "assistant-message", "mock"],
    "packages/ai/src/providers/faux.ts:contentToText": ["utility", "text-extraction", "serialization"],
    "packages/ai/src/providers/faux.ts:assistantContentToText": ["utility", "text-extraction", "serialization"],
    "packages/ai/src/providers/faux.ts:serializeContext": ["utility", "serialization", "context"],
    "packages/ai/src/providers/faux.ts:withUsageEstimate": ["utility", "token-estimation", "usage"],
    "packages/ai/src/providers/faux.ts:splitStringByTokenSize": ["utility", "string-split", "token"],
    "packages/ai/src/providers/faux.ts:cloneMessage": ["utility", "clone", "message"],
    "packages/ai/src/providers/faux.ts:createDeferredMessage": ["factory", "deferred", "message"],
    "packages/ai/src/providers/faux.ts:createErrorMessage": ["factory", "error-message", "mock"],
    "packages/ai/src/providers/faux.ts:streamWithDeltas": ["streaming", "delta", "mock"],
    "packages/ai/src/providers/faux.ts:createFauxCore": ["factory", "provider-core", "mock"],
    "packages/ai/src/providers/faux.ts:fauxProvider": ["factory", "provider", "mock"],
    # register-builtins.ts
    "packages/ai/src/providers/images/register-builtins.ts:createLazyLoadErrorImages": ["utility", "error-handling", "images"],
    "packages/ai/src/providers/images/register-builtins.ts:generateImagesOpenRouter": ["api-handler", "images", "openrouter"],
    "packages/ai/src/providers/images/register-builtins.ts:registerBuiltInImagesApiProviders": ["registry", "images", "provider"],
    # session-resources.ts
    "packages/ai/src/session-resources.ts:registerSessionResourceCleanup": ["utility", "cleanup", "callback"],
    "packages/ai/src/session-resources.ts:cleanupSessionResources": ["utility", "cleanup", "resource-management"],
    # abort-signals.ts
    "packages/ai/src/utils/abort-signals.ts:combineAbortSignals": ["utility", "abort-signal", "async"],
    # deferred-tools.ts
    "packages/ai/src/utils/deferred-tools.ts:splitDeferredTools": ["utility", "deferred-tools", "message-processing"],
    # diagnostics.ts
    "packages/ai/src/utils/diagnostics.ts:formatThrownValue": ["utility", "error-formatting", "serialization"],
    "packages/ai/src/utils/diagnostics.ts:extractDiagnosticError": ["utility", "error-extraction", "diagnostics"],
    "packages/ai/src/utils/diagnostics.ts:createAssistantMessageDiagnostic": ["factory", "diagnostics", "assistant-message"],
    "packages/ai/src/utils/diagnostics.ts:appendAssistantMessageDiagnostic": ["utility", "diagnostics", "message"],
    # error-body.ts
    "packages/ai/src/utils/error-body.ts:normalizeProviderError": ["utility", "error-normalization", "provider-error"],
    "packages/ai/src/utils/error-body.ts:formatProviderError": ["utility", "error-formatting", "provider-error"],
    "packages/ai/src/utils/error-body.ts:truncateErrorText": ["utility", "truncation", "error-text"],
    "packages/ai/src/utils/error-body.ts:safeJsonStringify": ["utility", "json", "serialization"],
    # estimate.ts
    "packages/ai/src/utils/estimate.ts:calculateContextTokens": ["utility", "token-estimation", "context"],
    "packages/ai/src/utils/estimate.ts:estimateTextTokens": ["utility", "token-estimation", "text"],
    "packages/ai/src/utils/estimate.ts:estimateTextAndImageContentTokens": ["utility", "token-estimation", "image"],
    "packages/ai/src/utils/estimate.ts:estimateMessageTokens": ["utility", "token-estimation", "message"],
    "packages/ai/src/utils/estimate.ts:getLastAssistantUsageInfo": ["utility", "usage-info", "context"],
    "packages/ai/src/utils/estimate.ts:estimateMessages": ["utility", "token-estimation", "messages"],
    "packages/ai/src/utils/estimate.ts:estimateContextTokens": ["utility", "token-estimation", "context"],
    # event-stream.ts
    "packages/ai/src/utils/event-stream.ts:createAssistantMessageEventStream": ["factory", "event-stream", "assistant-message"],
    # hash.ts
    "packages/ai/src/utils/hash.ts:shortHash": ["utility", "hash", "fnv"],
    # headers.ts
    "packages/ai/src/utils/headers.ts:headersToRecord": ["utility", "headers", "conversion"],
    "packages/ai/src/utils/headers.ts:providerHeadersToRecord": ["utility", "headers", "provider-config"],
    # json-parse.ts
    "packages/ai/src/utils/json-parse.ts:escapeControlCharacter": ["utility", "escape", "control-char"],
    "packages/ai/src/utils/json-parse.ts:repairJson": ["utility", "json-repair", "parsing"],
    "packages/ai/src/utils/json-parse.ts:parseJsonWithRepair": ["utility", "json-parse", "repair"],
    "packages/ai/src/utils/json-parse.ts:parseStreamingJson": ["utility", "json-parse", "streaming"],
    # node-http-proxy.ts
    "packages/ai/src/utils/node-http-proxy.ts:getProxyEnv": ["utility", "proxy", "environment"],
    "packages/ai/src/utils/node-http-proxy.ts:parseProxyTargetUrl": ["utility", "proxy", "url-parsing"],
    "packages/ai/src/utils/node-http-proxy.ts:shouldProxyHostname": ["utility", "proxy", "hostname"],
    "packages/ai/src/utils/node-http-proxy.ts:getProxyForUrl": ["utility", "proxy", "url"],
    "packages/ai/src/utils/node-http-proxy.ts:resolveHttpProxyUrlForTarget": ["utility", "proxy", "url-resolution"],
    # overflow.ts
    "packages/ai/src/utils/overflow.ts:isContextOverflow": ["utility", "overflow-detection", "error-matching"],
    "packages/ai/src/utils/overflow.ts:isRecoverableLength": ["utility", "overflow", "recovery"],
    "packages/ai/src/utils/overflow.ts:getOverflowPatterns": ["utility", "overflow", "patterns"],
    # provider-env.ts
    "packages/ai/src/utils/provider-env.ts:getBunSandboxEnvValue": ["utility", "environment", "bun"],
    "packages/ai/src/utils/provider-env.ts:getProviderEnvValue": ["utility", "environment", "provider-config"],
    # provider-retry.ts
    "packages/ai/src/utils/provider-retry.ts:isRetryableProviderError": ["utility", "retry", "error-classification"],
    "packages/ai/src/utils/provider-retry.ts:validateServerRetryDelayMs": ["utility", "retry", "validation"],
    "packages/ai/src/utils/provider-retry.ts:getRetryDelayMs": ["utility", "retry", "delay"],
    "packages/ai/src/utils/provider-retry.ts:abortableSleep": ["utility", "sleep", "abortable"],
    "packages/ai/src/utils/provider-retry.ts:retryProviderRequest": ["utility", "retry", "provider-request"],
    # retry.ts
    "packages/ai/src/utils/retry.ts:sleep": ["utility", "sleep", "abortable"],
    "packages/ai/src/utils/retry.ts:retryAssistantCall": ["utility", "retry", "assistant-call"],
    "packages/ai/src/utils/retry.ts:isRetryableAssistantError": ["utility", "retry", "error-classification"],
    # sanitize-unicode.ts
    "packages/ai/src/utils/sanitize-unicode.ts:sanitizeSurrogates": ["utility", "unicode", "sanitization"],
    # text.ts
    "packages/ai/src/utils/text.ts:contentText": ["utility", "text-extraction", "message"],
    # typebox-helpers.ts
    "packages/ai/src/utils/typebox-helpers.ts:StringEnum": ["utility", "typebox", "schema"],
    # uuid.ts
    "packages/ai/src/utils/uuid.ts:uuidv7": ["utility", "uuid", "identifier"],
    # validation.ts
    "packages/ai/src/utils/validation.ts:matchesJsonType": ["utility", "validation", "json-type"],
    "packages/ai/src/utils/validation.ts:coercePrimitiveByType": ["utility", "coercion", "type-cast"],
    "packages/ai/src/utils/validation.ts:applySchemaObjectCoercion": ["utility", "coercion", "object"],
    "packages/ai/src/utils/validation.ts:applySchemaArrayCoercion": ["utility", "coercion", "array"],
    "packages/ai/src/utils/validation.ts:coerceWithUnionSchema": ["utility", "coercion", "union-type"],
    "packages/ai/src/utils/validation.ts:coerceWithJsonSchema": ["utility", "coercion", "json-schema"],
    "packages/ai/src/utils/validation.ts:normalizeOptionalNulls": ["utility", "normalization", "null"],
    "packages/ai/src/utils/validation.ts:getValidator": ["utility", "validator", "cache"],
    "packages/ai/src/utils/validation.ts:formatValidationPath": ["utility", "formatting", "error-path"],
    "packages/ai/src/utils/validation.ts:validateToolCall": ["utility", "validation", "tool-call"],
    "packages/ai/src/utils/validation.ts:validateToolArguments": ["utility", "validation", "tool-arguments"],
    # Test functions
    "packages/ai/test/abort.test.ts:testAbortSignal": ["test", "abort-signal", "streaming"],
    "packages/ai/test/abort.test.ts:testImmediateAbort": ["test", "abort-signal", "immediate"],
    "packages/ai/test/abort.test.ts:testAbortThenNewMessage": ["test", "abort-signal", "new-message"],
    "packages/ai/test/anthropic-cache-write-1h-cost.test.ts:eventsWithCacheCreation": ["test", "sse", "cache-creation"],
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts:createModel": ["test", "model-creation", "compat"],
    "packages/ai/test/anthropic-eager-tool-input-compat.test.ts:captureAnthropicRequest": ["test", "request-capture", "server"],
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:getProbePriority": ["test", "probe-priority", "model-selection"],
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:selectOneCasePerProvider": ["test", "case-selection", "provider"],
    "packages/ai/test/anthropic-eager-tool-input-e2e.test.ts:expectToolEnabledRequestAccepted": ["test", "tool-enabled", "e2e"],
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:makeModel": ["test", "model-creation", "thinking-signature"],
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:makeContext": ["test", "context-creation", "thinking"],
    "packages/ai/test/anthropic-empty-thinking-signature-compat.test.ts:capturePayload": ["test", "payload-capture", "streaming"],
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts:makeCustomModel": ["test", "model-creation", "compat"],
    "packages/ai/test/anthropic-force-adaptive-thinking.test.ts:capturePayload": ["test", "payload-capture", "thinking"],
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:getProbePriority": ["test", "probe-priority", "model-selection"],
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:selectOneCasePerProvider": ["test", "case-selection", "provider"],
    "packages/ai/test/anthropic-long-cache-retention-e2e.test.ts:expectLongCacheRetentionAccepted": ["test", "cache-retention", "e2e"],
    "packages/ai/test/anthropic-opus-4-8-smoke.test.ts:makeContext": ["test", "context-creation", "smoke"],
    "packages/ai/test/anthropic-temperature-compat.test.ts:makeCustomModel": ["test", "model-creation", "temperature"],
    "packages/ai/test/anthropic-temperature-compat.test.ts:capturePayload": ["test", "payload-capture", "temperature"],
}

# Class tags
class_tags = {
    "packages/ai/src/utils/event-stream.ts:EventStream": ["event-stream", "streaming", "async"],
    "packages/ai/src/utils/event-stream.ts:AssistantMessageEventStream": ["event-stream", "assistant-message", "streaming"],
}

# Function complexity
def func_complexity(start, end):
    lines = end - start + 1
    if lines > 200:
        return "complex"
    elif lines > 50:
        return "moderate"
    else:
        return "simple"

def class_complexity(start, end, methods):
    lines = end - start + 1
    if lines > 200 or len(methods) > 5:
        return "complex"
    elif lines > 50 or len(methods) >= 2:
        return "moderate"
    else:
        return "simple"

# ============================================================
# BUILD NODES
# ============================================================

all_nodes = []
# Map: node_id -> file_path (for partitioning)
node_to_file = {}

for path in all_files:
    result = extract_map[path]
    export_names = [e["name"] for e in result.get("exports", [])]
    is_test = ".test." in path

    # File node
    file_id = f"file:{path}"
    file_name = path.split("/")[-1]
    tags = list(file_tags.get(path, ["utility"]))
    if is_test and "test" not in tags:
        tags.insert(0, "test")

    file_node = {
        "id": file_id,
        "type": "file",
        "name": file_name,
        "filePath": path,
        "summary": file_summaries.get(path, f"源文件: {file_name}"),
        "tags": tags[:5],
        "complexity": file_complexity.get(path, "moderate"),
    }
    all_nodes.append(file_node)
    node_to_file[file_id] = path

    # Function nodes
    for fn in result.get("functions", []):
        fn_name = fn["name"]
        line_count = fn["endLine"] - fn["startLine"] + 1
        is_exported = fn_name in export_names

        if line_count < 10 and not is_exported:
            continue

        fn_id = f"function:{path}:{fn_name}"
        fn_key = f"{path}:{fn_name}"
        fn_node = {
            "id": fn_id,
            "type": "function",
            "name": fn_name,
            "filePath": path,
            "lineRange": [fn["startLine"], fn["endLine"]],
            "summary": func_summaries.get(fn_key, f"函数 {fn_name}"),
            "tags": func_tags.get(fn_key, ["utility"])[:5],
            "complexity": func_complexity(fn["startLine"], fn["endLine"]),
        }
        all_nodes.append(fn_node)
        node_to_file[fn_id] = path

    # Class nodes
    for cls in result.get("classes", []):
        cls_name = cls["name"]
        line_count = cls["endLine"] - cls["startLine"] + 1
        method_count = len(cls.get("methods", []))
        is_exported = cls_name in export_names

        if method_count < 2 and line_count < 20 and not is_exported:
            continue

        cls_id = f"class:{path}:{cls_name}"
        cls_key = f"{path}:{cls_name}"
        cls_node = {
            "id": cls_id,
            "type": "class",
            "name": cls_name,
            "filePath": path,
            "lineRange": [cls["startLine"], cls["endLine"]],
            "summary": class_summaries.get(cls_key, f"类 {cls_name}"),
            "tags": class_tags.get(cls_key, ["class"])[:5],
            "complexity": class_complexity(cls["startLine"], cls["endLine"], cls.get("methods", [])),
        }
        all_nodes.append(cls_node)
        node_to_file[cls_id] = path

# ============================================================
# BUILD EDGES
# ============================================================

all_edges = []

# 1. imports edges (1:1 from batchImportData)
for path in all_files:
    imports = batch_import_data.get(path, [])
    file_id = f"file:{path}"
    for imp_path in imports:
        edge = {
            "source": file_id,
            "target": f"file:{imp_path}",
            "type": "imports",
            "direction": "forward",
            "weight": 0.7,
        }
        all_edges.append(edge)

# 2. contains edges (file -> function/class)
for node in all_nodes:
    if node["type"] in ("function", "class"):
        path = node["filePath"]
        file_id = f"file:{path}"
        edge = {
            "source": file_id,
            "target": node["id"],
            "type": "contains",
            "direction": "forward",
            "weight": 1.0,
        }
        all_edges.append(edge)

# 3. exports edges (file -> exported function/class)
for path in all_files:
    result = extract_map[path]
    export_names = [e["name"] for e in result.get("exports", [])]
    file_id = f"file:{path}"

    for fn in result.get("functions", []):
        fn_name = fn["name"]
        if fn_name not in export_names:
            continue
        line_count = fn["endLine"] - fn["startLine"] + 1
        if line_count < 10 and not fn_name in export_names:
            continue
        # Check if node was created
        fn_id = f"function:{path}:{fn_name}"
        # Verify node exists
        if any(n["id"] == fn_id for n in all_nodes):
            edge = {
                "source": file_id,
                "target": fn_id,
                "type": "exports",
                "direction": "forward",
                "weight": 0.8,
            }
            all_edges.append(edge)

    for cls in result.get("classes", []):
        cls_name = cls["name"]
        if cls_name not in export_names:
            continue
        cls_id = f"class:{path}:{cls_name}"
        if any(n["id"] == cls_id for n in all_nodes):
            edge = {
                "source": file_id,
                "target": cls_id,
                "type": "exports",
                "direction": "forward",
                "weight": 0.8,
            }
            all_edges.append(edge)

# 4. tested_by edges
# Intra-batch: types.ts is imported by all test files in this batch
test_files_in_batch = [p for p in all_files if ".test." in p]
production_files_in_batch = [p for p in all_files if ".test." not in p]

for test_file in test_files_in_batch:
    test_imports = set(batch_import_data.get(test_file, []))
    for prod_file in production_files_in_batch:
        if prod_file in test_imports:
            edge = {
                "source": f"file:{prod_file}",
                "target": f"file:{test_file}",
                "type": "tested_by",
                "direction": "forward",
                "weight": 0.5,
            }
            all_edges.append(edge)

# Cross-batch tested_by: from neighborMap
for prod_path in production_files_in_batch:
    neighbors = neighbor_map.get(prod_path, [])
    for neighbor in neighbors:
        neighbor_path = neighbor["path"]
        if ".test." in neighbor_path:
            edge = {
                "source": f"file:{prod_path}",
                "target": f"file:{neighbor_path}",
                "type": "tested_by",
                "direction": "forward",
                "weight": 0.5,
            }
            all_edges.append(edge)

# ============================================================
# PARTITION INTO PARTS
# ============================================================

node_count = len(all_nodes)
edge_count = len(all_edges)
parts = max(1, math.ceil(max(node_count / 60, edge_count / 120)))

print(f"Total nodes: {node_count}, Total edges: {edge_count}, Parts: {parts}")

# Sort files alphabetically and chunk
files_per_part = math.ceil(len(all_files) / parts)
file_groups = []
for i in range(parts):
    start = i * files_per_part
    end = min(start + files_per_part, len(all_files))
    file_groups.append(set(all_files[start:end]))

# Assign nodes to parts
for part_idx, file_group in enumerate(file_groups):
    part_nodes = []
    part_edges = []

    for node in all_nodes:
        node_file = node.get("filePath", "")
        if node_file in file_group:
            part_nodes.append(node)

    # Get all node IDs in this part
    part_node_ids = {n["id"] for n in part_nodes}

    # Also include file IDs that are in this part's file group
    part_file_ids = {f"file:{p}" for p in file_group}

    for edge in all_edges:
        source_file = node_to_file.get(edge["source"], "")
        if source_file in file_group:
            part_edges.append(edge)

    # Write part
    part_num = part_idx + 1
    output = {"nodes": part_nodes, "edges": part_edges}

    output_path = f"/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-4-part-{part_num}.json"
    with open(output_path, "w") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Part {part_num}: {len(part_nodes)} nodes, {len(part_edges)} edges -> {output_path}")

# Verify import edge count
import_edge_count = sum(1 for e in all_edges if e["type"] == "imports")
print(f"\nImport edges: {import_edge_count}")

# Verify by summing batchImportData
expected_imports = sum(len(v) for v in batch_import_data.values())
print(f"Expected imports: {expected_imports}")
print(f"Match: {import_edge_count == expected_imports}")

# Print edge type breakdown
from collections import Counter
edge_types = Counter(e["type"] for e in all_edges)
print(f"\nEdge type breakdown: {dict(edge_types)}")
