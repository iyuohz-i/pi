#!/usr/bin/env python3
"""Generate batch-20-part-2.json for the file-analyzer batch 20."""

import json

nodes = [
    {
        "id": "file:packages/ai/test/github-copilot-oauth.test.ts",
        "type": "file",
        "name": "github-copilot-oauth.test.ts",
        "filePath": "packages/ai/test/github-copilot-oauth.test.ts",
        "summary": "测试 GitHub Copilot OAuth 流程，包括设备码登录、令牌刷新以及模型列表更新，通过 mock fetch 模拟完整交互。",
        "tags": ["test", "oauth", "github-copilot"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/images-models.test.ts",
        "type": "file",
        "name": "images-models.test.ts",
        "filePath": "packages/ai/test/images-models.test.ts",
        "summary": "测试图像模型供应商的创建与调用流程，验证内置图像供应商列表的正确性。",
        "tags": ["test", "images-models", "provider"],
        "complexity": "moderate"
    },
    {
        "id": "file:packages/ai/test/kimi-coding-oauth.test.ts",
        "type": "file",
        "name": "kimi-coding-oauth.test.ts",
        "filePath": "packages/ai/test/kimi-coding-oauth.test.ts",
        "summary": "测试 Kimi Coding OAuth 设备码授权流程，通过 mock 响应模拟设备授权和令牌轮询。",
        "tags": ["test", "oauth", "kimi-coding"],
        "complexity": "moderate"
    },
    {
        "id": "file:packages/ai/test/model-catalog-types.test.ts",
        "type": "file",
        "name": "model-catalog-types.test.ts",
        "filePath": "packages/ai/test/model-catalog-types.test.ts",
        "summary": "对模型目录类型进行编译期类型检查测试，确保 GitHub Copilot 和 xAI 模型定义符合类型约束。",
        "tags": ["test", "type-definition", "model-catalog"],
        "complexity": "simple"
    },
    {
        "id": "file:packages/ai/test/models-runtime.test.ts",
        "type": "file",
        "name": "models-runtime.test.ts",
        "filePath": "packages/ai/test/models-runtime.test.ts",
        "summary": "Models 运行时的综合测试套件，覆盖供应商创建、模型列表获取、动态供应商注册、OAuth 认证以及成本计算等核心功能。",
        "tags": ["test", "models", "runtime", "integration"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/oauth-auth.test.ts",
        "type": "file",
        "name": "oauth-auth.test.ts",
        "filePath": "packages/ai/test/oauth-auth.test.ts",
        "summary": "测试多个供应商的 OAuth 认证集成，验证凭据存储与令牌刷新在 Anthropic、GitHub Copilot、Kimi、OpenAI Codex、OpenRouter 和 xAI 间的一致性。",
        "tags": ["test", "oauth", "integration", "auth"],
        "complexity": "moderate"
    },
    {
        "id": "file:packages/ai/test/oauth-device-code.test.ts",
        "type": "file",
        "name": "oauth-device-code.test.ts",
        "filePath": "packages/ai/test/oauth-device-code.test.ts",
        "summary": "测试 OAuth 设备码流程的通用轮询逻辑，包括 pending 状态轮询、授权完成和错误处理。",
        "tags": ["test", "oauth", "device-code"],
        "complexity": "moderate"
    },
    {
        "id": "file:packages/ai/test/openai-codex-oauth.test.ts",
        "type": "file",
        "name": "openai-codex-oauth.test.ts",
        "filePath": "packages/ai/test/openai-codex-oauth.test.ts",
        "summary": "测试 OpenAI Codex OAuth 设备码登录流程，包括 JWT 令牌生成、pending 轮询和令牌交换。",
        "tags": ["test", "oauth", "openai-codex"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/openrouter-oauth.test.ts",
        "type": "file",
        "name": "openrouter-oauth.test.ts",
        "filePath": "packages/ai/test/openrouter-oauth.test.ts",
        "summary": "测试 OpenRouter OAuth 流程和图像供应商集成，验证 PKCE 认证和令牌刷新机制。",
        "tags": ["test", "oauth", "openrouter", "images-models"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/providers.test.ts",
        "type": "file",
        "name": "providers.test.ts",
        "filePath": "packages/ai/test/providers.test.ts",
        "summary": "供应商集成测试套件，覆盖所有内置供应商的创建、API 挂载、认证配置和流式响应功能。",
        "tags": ["test", "providers", "integration"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/radius-oauth.test.ts",
        "type": "file",
        "name": "radius-oauth.test.ts",
        "filePath": "packages/ai/test/radius-oauth.test.ts",
        "summary": "测试 Radius OAuth 设备码登录和令牌刷新流程。",
        "tags": ["test", "oauth", "radius"],
        "complexity": "moderate"
    },
    {
        "id": "file:packages/ai/test/scratch.ts",
        "type": "file",
        "name": "scratch.ts",
        "filePath": "packages/ai/test/scratch.ts",
        "summary": "临时实验脚本，用于手动验证 Anthropic 供应商的流式调用功能。",
        "tags": ["test", "scratch", "experimental"],
        "complexity": "simple"
    },
    {
        "id": "file:packages/ai/test/text.test.ts",
        "type": "file",
        "name": "text.test.ts",
        "filePath": "packages/ai/test/text.test.ts",
        "summary": "测试从包入口导出的文本处理工具函数（如 contentText），验证公共 API 的可用性。",
        "tags": ["test", "utility", "text"],
        "complexity": "simple"
    },
    {
        "id": "file:packages/ai/test/xai-oauth.test.ts",
        "type": "file",
        "name": "xai-oauth.test.ts",
        "filePath": "packages/ai/test/xai-oauth.test.ts",
        "summary": "测试 xAI OAuth 设备码登录和令牌刷新流程，通过 mock fetch 模拟完整授权交互。",
        "tags": ["test", "oauth", "xai"],
        "complexity": "complex"
    },
    {
        "id": "file:packages/ai/test/xai-responses.test.ts",
        "type": "file",
        "name": "xai-responses.test.ts",
        "filePath": "packages/ai/test/xai-responses.test.ts",
        "summary": "测试 xAI 供应商通过 OpenAI Responses API 的流式调用，验证请求格式和响应解析。",
        "tags": ["test", "xai", "responses-api"],
        "complexity": "moderate"
    },
    {
        "id": "file:scripts/generate-thinking-capabilities.mjs",
        "type": "file",
        "name": "generate-thinking-capabilities.mjs",
        "filePath": "scripts/generate-thinking-capabilities.mjs",
        "summary": "代码生成脚本，从 models.ts 中提取模型定义并生成 thinking capabilities 配置数据。",
        "tags": ["script", "code-generation", "build-system"],
        "complexity": "simple"
    },
    # Function nodes
    {
        "id": "function:packages/ai/test/github-copilot-oauth.test.ts:getUrl",
        "type": "function",
        "name": "getUrl",
        "filePath": "packages/ai/test/github-copilot-oauth.test.ts",
        "lineRange": [18, 29],
        "summary": "从 fetch 请求输入中提取 URL 字符串，用于测试中的请求断言。",
        "tags": ["test", "utility"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/github-copilot-oauth.test.ts:loginGitHubCopilotForTest",
        "type": "function",
        "name": "loginGitHubCopilotForTest",
        "filePath": "packages/ai/test/github-copilot-oauth.test.ts",
        "lineRange": [31, 56],
        "summary": "执行 GitHub Copilot OAuth 登录的测试辅助函数，模拟设备码显示和用户交互回调。",
        "tags": ["test", "oauth", "helper"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/github-copilot-oauth.test.ts:refreshGitHubCopilotModelsForTest",
        "type": "function",
        "name": "refreshGitHubCopilotModelsForTest",
        "filePath": "packages/ai/test/github-copilot-oauth.test.ts",
        "lineRange": [58, 94],
        "summary": "测试 GitHub Copilot 模型列表刷新流程，mock fetch 响应并验证令牌刷新请求头。",
        "tags": ["test", "oauth", "models"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/images-models.test.ts:testImageModel",
        "type": "function",
        "name": "testImageModel",
        "filePath": "packages/ai/test/images-models.test.ts",
        "lineRange": [14, 25],
        "summary": "验证单个图像模型的 ID 和供应商信息是否符合预期。",
        "tags": ["test", "images-models", "validation"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/images-models.test.ts:testProvider",
        "type": "function",
        "name": "testProvider",
        "filePath": "packages/ai/test/images-models.test.ts",
        "lineRange": [43, 69],
        "summary": "创建图像供应商实例并测试其图像生成调用，记录调用参数并返回模拟结果。",
        "tags": ["test", "images-models", "provider"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/kimi-coding-oauth.test.ts:deviceAuthorizationResponse",
        "type": "function",
        "name": "deviceAuthorizationResponse",
        "filePath": "packages/ai/test/kimi-coding-oauth.test.ts",
        "lineRange": [22, 32],
        "summary": "生成 Kimi Coding 设备授权响应的 mock 数据，支持自定义覆盖字段。",
        "tags": ["test", "oauth", "mock"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/models-runtime.test.ts:testModel",
        "type": "function",
        "name": "testModel",
        "filePath": "packages/ai/test/models-runtime.test.ts",
        "lineRange": [9, 22],
        "summary": "验证模型 ID 和供应商信息是否符合预期，并检查模型成本和 thinking 级别配置。",
        "tags": ["test", "models", "validation"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/models-runtime.test.ts:doneMessage",
        "type": "function",
        "name": "doneMessage",
        "filePath": "packages/ai/test/models-runtime.test.ts",
        "lineRange": [24, 42],
        "summary": "生成测试用的完成消息事件流，包含助手文本和结束标记。",
        "tags": ["test", "models", "mock"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/models-runtime.test.ts:testProvider",
        "type": "function",
        "name": "testProvider",
        "filePath": "packages/ai/test/models-runtime.test.ts",
        "lineRange": [55, 82],
        "summary": "创建测试用供应商实例，配置 mock API 响应并返回供应商和事件流引用。",
        "tags": ["test", "models", "provider", "mock"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/models-runtime.test.ts:testOAuth",
        "type": "function",
        "name": "testOAuth",
        "filePath": "packages/ai/test/models-runtime.test.ts",
        "lineRange": [97, 107],
        "summary": "生成测试用 OAuth 配置对象，支持自定义覆盖字段。",
        "tags": ["test", "oauth", "mock"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/openai-codex-oauth.test.ts:createAccessToken",
        "type": "function",
        "name": "createAccessToken",
        "filePath": "packages/ai/test/openai-codex-oauth.test.ts",
        "lineRange": [20, 30],
        "summary": "生成无签名 JWT 测试令牌，包含 OpenAI Codex 账户 ID 声明。",
        "tags": ["test", "oauth", "jwt", "mock"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/openai-codex-oauth.test.ts:deviceAuthPendingResponse",
        "type": "function",
        "name": "deviceAuthPendingResponse",
        "filePath": "packages/ai/test/openai-codex-oauth.test.ts",
        "lineRange": [32, 44],
        "summary": "生成设备授权 pending 状态的 mock 响应，模拟用户尚未完成授权的场景。",
        "tags": ["test", "oauth", "mock"],
        "complexity": "simple"
    },
    {
        "id": "function:packages/ai/test/openai-codex-oauth.test.ts:loginOpenAICodexDeviceCodeForTest",
        "type": "function",
        "name": "loginOpenAICodexDeviceCodeForTest",
        "filePath": "packages/ai/test/openai-codex-oauth.test.ts",
        "lineRange": [46, 68],
        "summary": "执行 OpenAI Codex 设备码登录的测试辅助函数，模拟设备码显示和交互回调。",
        "tags": ["test", "oauth", "helper"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/xai-oauth.test.ts:loginXaiForTest",
        "type": "function",
        "name": "loginXaiForTest",
        "filePath": "packages/ai/test/xai-oauth.test.ts",
        "lineRange": [53, 69],
        "summary": "执行 xAI OAuth 设备码登录的测试辅助函数，模拟设备码显示和交互回调。",
        "tags": ["test", "oauth", "helper"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/xai-responses.test.ts:completedResponse",
        "type": "function",
        "name": "completedResponse",
        "filePath": "packages/ai/test/xai-responses.test.ts",
        "lineRange": [14, 34],
        "summary": "生成 OpenAI Responses API 完成状态的 mock 响应 JSON。",
        "tags": ["test", "responses-api", "mock"],
        "complexity": "moderate"
    },
    {
        "id": "function:packages/ai/test/xai-responses.test.ts:captureRequest",
        "type": "function",
        "name": "captureRequest",
        "filePath": "packages/ai/test/xai-responses.test.ts",
        "lineRange": [36, 56],
        "summary": "通过 spy 拦截 fetch 请求，调用 xAI 供应商流式 API 并捕获实际发送的请求体。",
        "tags": ["test", "responses-api", "validation"],
        "complexity": "moderate"
    }
]

# Build edges
edges = []

# Import edges (1:1 from batchImportData)
import_data = {
    "packages/ai/test/github-copilot-oauth.test.ts": [
        "packages/ai/src/auth/credential-store.ts",
        "packages/ai/src/auth/oauth/github-copilot.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/providers/github-copilot.ts"
    ],
    "packages/ai/test/images-models.test.ts": [
        "packages/ai/src/auth/types.ts",
        "packages/ai/src/images-models.ts",
        "packages/ai/src/providers/all.ts",
        "packages/ai/src/types.ts"
    ],
    "packages/ai/test/kimi-coding-oauth.test.ts": [
        "packages/ai/src/auth/oauth/kimi-coding.ts",
        "packages/ai/src/auth/types.ts"
    ],
    "packages/ai/test/model-catalog-types.test.ts": [
        "packages/ai/src/providers/github-copilot.models.ts",
        "packages/ai/src/providers/xai.models.ts"
    ],
    "packages/ai/test/models-runtime.test.ts": [
        "packages/ai/src/auth/credential-store.ts",
        "packages/ai/src/auth/types.ts",
        "packages/ai/src/models-store.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/types.ts",
        "packages/ai/src/utils/event-stream.ts"
    ],
    "packages/ai/test/oauth-auth.test.ts": [
        "packages/ai/src/auth/credential-store.ts",
        "packages/ai/src/auth/oauth/anthropic.ts",
        "packages/ai/src/auth/oauth/github-copilot.ts",
        "packages/ai/src/auth/oauth/kimi-coding.ts",
        "packages/ai/src/auth/oauth/openai-codex.ts",
        "packages/ai/src/auth/oauth/openrouter.ts",
        "packages/ai/src/auth/oauth/xai.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/oauth.ts",
        "packages/ai/src/providers/anthropic.ts",
        "packages/ai/src/providers/github-copilot.ts"
    ],
    "packages/ai/test/oauth-device-code.test.ts": [
        "packages/ai/src/auth/oauth/device-code.ts"
    ],
    "packages/ai/test/openai-codex-oauth.test.ts": [
        "packages/ai/src/auth/oauth/openai-codex.ts"
    ],
    "packages/ai/test/openrouter-oauth.test.ts": [
        "packages/ai/src/auth/credential-store.ts",
        "packages/ai/src/auth/oauth/openrouter.ts",
        "packages/ai/src/images-models.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/providers/openrouter-images.ts",
        "packages/ai/src/providers/openrouter.ts"
    ],
    "packages/ai/test/providers.test.ts": [
        "packages/ai/src/api/lazy.ts",
        "packages/ai/src/auth/helpers.ts",
        "packages/ai/src/auth/types.ts",
        "packages/ai/src/models-store.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/providers/all.ts",
        "packages/ai/src/providers/amazon-bedrock.ts",
        "packages/ai/src/providers/anthropic.ts",
        "packages/ai/src/providers/cloudflare-ai-gateway.ts",
        "packages/ai/src/providers/cloudflare-workers-ai.ts",
        "packages/ai/src/providers/faux.ts",
        "packages/ai/src/providers/google-vertex.ts",
        "packages/ai/src/types.ts",
        "packages/ai/src/utils/event-stream.ts"
    ],
    "packages/ai/test/radius-oauth.test.ts": [
        "packages/ai/src/auth/oauth/radius.ts",
        "packages/ai/src/auth/types.ts"
    ],
    "packages/ai/test/scratch.ts": [
        "packages/ai/src/models.ts",
        "packages/ai/src/providers/anthropic.ts",
        "packages/ai/src/types.ts"
    ],
    "packages/ai/test/text.test.ts": [
        "packages/ai/src/index.ts"
    ],
    "packages/ai/test/xai-oauth.test.ts": [
        "packages/ai/src/auth/oauth/xai.ts",
        "packages/ai/src/auth/types.ts"
    ],
    "packages/ai/test/xai-responses.test.ts": [
        "packages/ai/src/api/openai-responses.ts",
        "packages/ai/src/models.ts",
        "packages/ai/src/providers/xai.models.ts",
        "packages/ai/src/providers/xai.ts",
        "packages/ai/src/types.ts"
    ],
    "scripts/generate-thinking-capabilities.mjs": [
        "packages/ai/src/models.ts"
    ]
}

for file_path, targets in import_data.items():
    for target in targets:
        edges.append({
            "source": f"file:{file_path}",
            "target": f"file:{target}",
            "type": "imports",
            "direction": "forward",
            "weight": 0.7
        })

# Contains edges (file -> function)
contains = [
    ("packages/ai/test/github-copilot-oauth.test.ts", "getUrl"),
    ("packages/ai/test/github-copilot-oauth.test.ts", "loginGitHubCopilotForTest"),
    ("packages/ai/test/github-copilot-oauth.test.ts", "refreshGitHubCopilotModelsForTest"),
    ("packages/ai/test/images-models.test.ts", "testImageModel"),
    ("packages/ai/test/images-models.test.ts", "testProvider"),
    ("packages/ai/test/kimi-coding-oauth.test.ts", "deviceAuthorizationResponse"),
    ("packages/ai/test/models-runtime.test.ts", "testModel"),
    ("packages/ai/test/models-runtime.test.ts", "doneMessage"),
    ("packages/ai/test/models-runtime.test.ts", "testProvider"),
    ("packages/ai/test/models-runtime.test.ts", "testOAuth"),
    ("packages/ai/test/openai-codex-oauth.test.ts", "createAccessToken"),
    ("packages/ai/test/openai-codex-oauth.test.ts", "deviceAuthPendingResponse"),
    ("packages/ai/test/openai-codex-oauth.test.ts", "loginOpenAICodexDeviceCodeForTest"),
    ("packages/ai/test/xai-oauth.test.ts", "loginXaiForTest"),
    ("packages/ai/test/xai-responses.test.ts", "completedResponse"),
    ("packages/ai/test/xai-responses.test.ts", "captureRequest"),
]
for file_path, func_name in contains:
    edges.append({
        "source": f"file:{file_path}",
        "target": f"function:{file_path}:{func_name}",
        "type": "contains",
        "direction": "forward",
        "weight": 1.0
    })

# tested_by edges (production -> test). Source is production file (in neighborMap/batchImportData), target is test file (in our nodes)
tested_by = [
    ("packages/ai/src/auth/oauth/github-copilot.ts", "packages/ai/test/github-copilot-oauth.test.ts"),
    ("packages/ai/src/images-models.ts", "packages/ai/test/images-models.test.ts"),
    ("packages/ai/src/auth/oauth/kimi-coding.ts", "packages/ai/test/kimi-coding-oauth.test.ts"),
    ("packages/ai/src/providers/xai.models.ts", "packages/ai/test/model-catalog-types.test.ts"),
    ("packages/ai/src/models.ts", "packages/ai/test/models-runtime.test.ts"),
    ("packages/ai/src/oauth.ts", "packages/ai/test/oauth-auth.test.ts"),
    ("packages/ai/src/auth/oauth/device-code.ts", "packages/ai/test/oauth-device-code.test.ts"),
    ("packages/ai/src/auth/oauth/openai-codex.ts", "packages/ai/test/openai-codex-oauth.test.ts"),
    ("packages/ai/src/auth/oauth/openrouter.ts", "packages/ai/test/openrouter-oauth.test.ts"),
    ("packages/ai/src/providers/all.ts", "packages/ai/test/providers.test.ts"),
    ("packages/ai/src/auth/oauth/radius.ts", "packages/ai/test/radius-oauth.test.ts"),
    ("packages/ai/src/index.ts", "packages/ai/test/text.test.ts"),
    ("packages/ai/src/auth/oauth/xai.ts", "packages/ai/test/xai-oauth.test.ts"),
    ("packages/ai/src/providers/xai.ts", "packages/ai/test/xai-responses.test.ts"),
]
for prod_path, test_path in tested_by:
    edges.append({
        "source": f"file:{prod_path}",
        "target": f"file:{test_path}",
        "type": "tested_by",
        "direction": "forward",
        "weight": 0.5
    })

output = {"nodes": nodes, "edges": edges}

with open("/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-20-part-2.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
print(f"Import edges: {sum(len(v) for v in import_data.values())}")
print(f"Contains edges: {len(contains)}")
print(f"Tested_by edges: {len(tested_by)}")
