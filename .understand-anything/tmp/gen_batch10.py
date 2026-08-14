#!/usr/bin/env python3
"""Generate batch-10.json knowledge graph output (2 parts)."""
import json
import os
import math

BASE = "packages/ai/src"
OUT_DIR = "/Users/zhouyi/AiHub/pi/.understand-anything/intermediate"

# ============================================================
# FILE NODES (33 files) - all summaries in Chinese
# ============================================================
file_nodes = []

def add_file(path, name, summary, tags, complexity, languageNotes=None):
    node = {
        "id": f"file:{path}",
        "type": "file",
        "name": name,
        "filePath": path,
        "summary": summary,
        "tags": tags,
        "complexity": complexity,
    }
    if languageNotes:
        node["languageNotes"] = languageNotes
    file_nodes.append(node)
    return node

add_file(f"{BASE}/api/anthropic-messages.lazy.ts", "anthropic-messages.lazy.ts",
    "Anthropic Messages API 的延迟加载包装器，通过动态导入减少启动时的模块加载开销。",
    ["lazy-loading", "api-wrapper", "anthropic"], "simple",
    "使用动态 import() 实现按需加载，避免将整个 API 模块打包到启动路径中。")

add_file(f"{BASE}/api/openai-completions.lazy.ts", "openai-completions.lazy.ts",
    "OpenAI Completions API 的延迟加载包装器，按需动态导入 API 实现。",
    ["lazy-loading", "api-wrapper", "openai"], "simple")

add_file(f"{BASE}/api/openai-responses.lazy.ts", "openai-responses.lazy.ts",
    "OpenAI Responses API 的延迟加载包装器，按需动态导入 API 实现。",
    ["lazy-loading", "api-wrapper", "openai"], "simple")

add_file(f"{BASE}/api/openrouter-images.lazy.ts", "openrouter-images.lazy.ts",
    "OpenRouter Images API 的延迟加载包装器，按需动态导入图像生成 API 实现。",
    ["lazy-loading", "api-wrapper", "openrouter", "image-generation"], "simple")

add_file(f"{BASE}/auth/context.ts", "context.ts",
    "提供默认的供应商认证上下文工厂函数，封装环境变量读取与 Node.js 模块加载逻辑。",
    ["auth", "factory", "context"], "simple")

add_file(f"{BASE}/auth/credential-store.ts", "credential-store.ts",
    "基于链式异步序列化的内存凭证存储，提供读写、修改和删除操作的互斥访问控制。",
    ["auth", "credential-store", "serialization", "in-memory"], "moderate",
    "通过 Promise 链实现异步操作的串行化，避免凭证并发写入冲突。")

add_file(f"{BASE}/auth/helpers.ts", "helpers.ts",
    "提供环境变量 API Key 认证和延迟 OAuth 加载两个辅助函数，供供应商认证流程复用。",
    ["auth", "utility", "api-key", "oauth"], "simple")

add_file(f"{BASE}/auth/oauth/anthropic.ts", "anthropic.ts",
    "实现 Anthropic 的 OAuth 认证流程，包括 PKCE 授权码交换、回调服务器和令牌刷新。",
    ["auth", "oauth", "anthropic", "pkce", "callback-server"], "complex",
    "使用本地 HTTP 回调服务器接收授权码，配合 PKCE 流程增强安全性。")

add_file(f"{BASE}/auth/oauth/device-code.ts", "device-code.ts",
    "提供 OAuth 设备码流程的通用轮询机制，支持可中止的 sleep 和设备码状态轮询。",
    ["auth", "oauth", "device-code", "polling"], "moderate",
    "abortableSleep 结合 AbortSignal 实现可取消的等待，避免轮询过程中资源泄漏。")

add_file(f"{BASE}/auth/oauth/github-copilot.ts", "github-copilot.ts",
    "实现 GitHub Copilot 的设备码 OAuth 认证流程，包含企业域名支持、令牌刷新和模型启用管理。",
    ["auth", "oauth", "github-copilot", "device-code"], "complex",
    "支持企业域名自动检测和 Copilot 模型列表获取与启用。")

add_file(f"{BASE}/auth/oauth/kimi-coding.ts", "kimi-coding.ts",
    "实现 Kimi Coding 的设备码 OAuth 认证流程，包含设备授权、令牌轮询和刷新逻辑。",
    ["auth", "oauth", "kimi", "device-code"], "complex",
    "支持可配置的 OAuth 主机地址和令牌刷新重试机制。")

add_file(f"{BASE}/auth/oauth/load.ts", "load.ts",
    "提供所有内置 OAuth 流程的延迟加载入口，按需动态导入各供应商的 OAuth 模块。",
    ["auth", "oauth", "lazy-loading", "factory"], "simple",
    "每个 load 函数封装一个动态 import()，减少未使用 OAuth 流量的启动开销。")

add_file(f"{BASE}/auth/oauth/oauth-page.ts", "oauth-page.ts",
    "生成 OAuth 回调页面的 HTML 渲染逻辑，提供成功和错误两种页面模板。",
    ["auth", "oauth", "html", "callback-page"], "moderate",
    "使用模板字符串生成 HTML，通过 escapeHtml 防止 XSS 注入。")

add_file(f"{BASE}/auth/oauth/openai-codex.ts", "openai-codex.ts",
    "实现 OpenAI Codex 的 OAuth 认证流程，支持设备码和本地回调服务器两种授权方式。",
    ["auth", "oauth", "openai", "pkce", "device-code"], "complex",
    "同时支持设备码流程和 PKCE 本地服务器流程，根据交互方式自动选择。")

add_file(f"{BASE}/auth/oauth/openrouter.ts", "openrouter.ts",
    "实现 OpenRouter 的 OAuth 认证流程，使用 PKCE 和本地回调服务器完成授权码交换。",
    ["auth", "oauth", "openrouter", "pkce", "callback-server"], "complex",
    "回调服务器处理授权码接收并自动关闭，支持错误状态页面的 HTML 响应。")

add_file(f"{BASE}/auth/oauth/pkce.ts", "pkce.ts",
    "提供 PKCE（Proof Key for Code Exchange）验证器和挑战码的生成工具。",
    ["auth", "oauth", "pkce", "utility", "crypto"], "simple",
    "使用 Web Crypto API 的 randomValues 生成加密安全的 PKCE 参数。")

add_file(f"{BASE}/auth/oauth/radius.ts", "radius.ts",
    "实现 Radius 平台的 OAuth 认证流程，支持浏览器和设备码两种授权方式，并通过工厂函数配置。",
    ["auth", "oauth", "radius", "device-code", "factory"], "complex",
    "通过 createRadiusOAuth 工厂函数动态创建 OAuth 配置，支持 OIDC 发现端点。")

add_file(f"{BASE}/auth/oauth/xai.ts", "xai.ts",
    "实现 xAI 的设备码 OAuth 认证流程，包含设备码请求、令牌轮询和刷新逻辑。",
    ["auth", "oauth", "xai", "device-code"], "complex",
    "使用表单 POST 请求与 xAI OAuth 端点交互，支持令牌刷新令牌轮换。")

add_file(f"{BASE}/auth/resolve.ts", "resolve.ts",
    "解析供应商认证信息，按优先级依次尝试存储的 OAuth、API Key 和环境变量认证方式。",
    ["auth", "resolver", "oauth", "api-key"], "complex",
    "支持 AbortSignal 取消认证解析，并通过 ModelsError 提供结构化错误码。")

add_file(f"{BASE}/auth/types.ts", "types.ts",
    "定义认证系统的核心类型，包括认证上下文、凭证存储接口、OAuth 回调和提示类型。",
    ["auth", "type-definition", "oauth", "interface"], "moderate",
    "纯类型定义文件，无运行时代码，为整个认证模块提供类型契约。")

add_file(f"{BASE}/bun-oauth.ts", "bun-oauth.ts",
    "为 Bun 运行时注册所有内置 OAuth 流程的加载器入口。",
    ["auth", "oauth", "bun", "registration"], "simple",
    "通过 registerBunOAuthFlows 将所有延迟加载的 OAuth 模块注册到 Bun 运行时。")

add_file(f"{BASE}/cli.ts", "cli.ts",
    "命令行工具入口，提供供应商登录和模型列表查看功能。",
    ["entry-point", "cli", "auth", "interactive"], "moderate")

add_file(f"{BASE}/compat/extension-oauth-types.ts", "extension-oauth-types.ts",
    "兼容性类型定义文件，为 VS Code 扩展提供 OAuth 凭证类型的重新导出。",
    ["type-definition", "compat", "oauth"], "simple",
    "用于向后兼容扩展程序的 OAuth 类型定义。")

add_file(f"{BASE}/images-models.ts", "images-models.ts",
    "实现图像生成模型的供应商管理和认证解析，支持多供应商图像 API 的统一接口。",
    ["image-generation", "service", "auth", "multi-provider"], "complex",
    "ImagesModelsImpl 管理多个图像供应商，提供统一的 generateImages 接口。")

add_file(f"{BASE}/index.ts", "index.ts",
    "包的入口 barrel 文件，重新导出所有公开的类型、接口和工厂函数。",
    ["entry-point", "barrel", "exports"], "simple",
    "纯 re-export barrel 文件，28 个导出，无运行时逻辑。")

add_file(f"{BASE}/model-catalog.ts", "model-catalog.ts",
    "提供模型目录扁平化工具函数，将分组模型列表转换为扁平的模型 ID 列表。",
    ["utility", "model-catalog", "flatten"], "simple")

add_file(f"{BASE}/models-store.ts", "models-store.ts",
    "内存模型存储实现，提供供应商模型数据的读写和删除操作。",
    ["data-model", "in-memory", "store"], "simple",
    "InMemoryModelsStore 使用 Map 存储模型数据，实现 ModelsStore 接口。")

add_file(f"{BASE}/models.ts", "models.ts",
    "核心模型管理实现，提供多供应商模型注册、认证、流式补全和刷新等全部功能。",
    ["service", "multi-provider", "model-management", "streaming"], "complex",
    "ModelsImpl 类包含 28 个方法，涵盖供应商管理、认证解析、模型刷新和流式 API 调用。")

add_file(f"{BASE}/oauth.ts", "oauth.ts",
    "OAuth 模块的 barrel 文件，重新导出所有 OAuth 相关的公开类型。",
    ["barrel", "oauth", "type-definition", "exports"], "simple",
    "纯 re-export barrel 文件，7 个类型导出，无运行时代码。")

add_file(f"{BASE}/providers/all.ts", "all.ts",
    "汇总所有内置 LLM 供应商的定义，提供供应商列表、模型目录和图像供应商的统一入口。",
    ["barrel", "multi-provider", "registry", "entry-point"], "moderate",
    "导入 44 个供应商模块并聚合为统一的 builtinProviders 和 builtinModels 接口。")

add_file(f"{BASE}/providers/amazon-bedrock.models.ts", "amazon-bedrock.models.ts",
    "定义 Amazon Bedrock 供应商的内置模型目录常量。",
    ["model-catalog", "amazon-bedrock", "constant"], "simple")

add_file(f"{BASE}/providers/amazon-bedrock.ts", "amazon-bedrock.ts",
    "实现 Amazon Bedrock 供应商的创建函数，配置认证方式和 API 端点。",
    ["provider", "amazon-bedrock", "factory"], "moderate")

add_file(f"{BASE}/providers/ant-ling.models.ts", "ant-ling.models.ts",
    "定义 Ant Ling 供应商的内置模型目录常量。",
    ["model-catalog", "ant-ling", "constant"], "simple")

print(f"Created {len(file_nodes)} file nodes")

# ============================================================
# FUNCTION AND CLASS NODES (significant sub-nodes)
# ============================================================
sub_nodes = []

def add_fn(path, name, start, end, summary, tags, complexity):
    sub_nodes.append({
        "id": f"function:{path}:{name}",
        "type": "function",
        "name": name,
        "filePath": path,
        "lineRange": [start, end],
        "summary": summary,
        "tags": tags,
        "complexity": complexity,
    })

def add_cls(path, name, start, end, summary, tags, complexity):
    sub_nodes.append({
        "id": f"class:{path}:{name}",
        "type": "class",
        "name": name,
        "filePath": path,
        "lineRange": [start, end],
        "summary": summary,
        "tags": tags,
        "complexity": complexity,
    })

# --- auth/context.ts ---
add_fn(f"{BASE}/auth/context.ts", "defaultProviderAuthContext", 23, 45,
    "创建默认的供应商认证上下文，封装环境变量读取和 Node.js 模块加载能力。",
    ["auth", "factory", "context"], "simple")

# --- auth/credential-store.ts ---
add_cls(f"{BASE}/auth/credential-store.ts", "InMemoryCredentialStore", 9, 67,
    "内存凭证存储类，通过 Promise 链实现异步操作串行化，提供凭证的读写、修改和删除。",
    ["auth", "credential-store", "serialization", "in-memory"], "moderate")

# --- auth/helpers.ts ---
add_fn(f"{BASE}/auth/helpers.ts", "envApiKeyAuth", 9, 31,
    "从环境变量读取 API Key 并创建认证信息，支持多个环境变量名称的优先级查找。",
    ["auth", "api-key", "utility"], "simple")
add_fn(f"{BASE}/auth/helpers.ts", "lazyOAuth", 40, 59,
    "创建延迟加载的 OAuth 认证模块，在首次使用时才动态导入 OAuth 实现。",
    ["auth", "oauth", "lazy-loading"], "simple")

# --- auth/oauth/anthropic.ts ---
add_fn(f"{BASE}/auth/oauth/anthropic.ts", "startCallbackServer", 99, 168,
    "启动本地 HTTP 回调服务器接收 Anthropic OAuth 授权码，处理 CSRF 状态验证。",
    ["auth", "oauth", "callback-server", "anthropic"], "moderate")
add_fn(f"{BASE}/auth/oauth/anthropic.ts", "exchangeAuthorizationCode", 190, 232,
    "使用 PKCE 验证器将授权码交换为 Anthropic 的访问令牌和刷新令牌。",
    ["auth", "oauth", "token-exchange", "pkce"], "moderate")
add_fn(f"{BASE}/auth/oauth/anthropic.ts", "loginAnthropic", 234, 312,
    "执行 Anthropic OAuth 登录流程，包括生成 PKCE 参数、打开浏览器和交换令牌。",
    ["auth", "oauth", "login", "anthropic"], "complex")
add_fn(f"{BASE}/auth/oauth/anthropic.ts", "refreshAnthropicToken", 317, 353,
    "使用刷新令牌获取新的 Anthropic 访问令牌。",
    ["auth", "oauth", "token-refresh", "anthropic"], "moderate")

# --- auth/oauth/device-code.ts ---
add_fn(f"{BASE}/auth/oauth/device-code.ts", "abortableSleep", 26, 44,
    "可中止的延迟函数，支持通过 AbortSignal 取消等待。",
    ["utility", "async", "abort"], "simple")
add_fn(f"{BASE}/auth/oauth/device-code.ts", "pollOAuthDeviceCodeFlow", 46, 98,
    "轮询 OAuth 设备码授权流程，按指定间隔查询令牌状态直到完成或超时。",
    ["auth", "oauth", "device-code", "polling"], "moderate")

# --- auth/oauth/github-copilot.ts ---
add_fn(f"{BASE}/auth/oauth/github-copilot.ts", "startDeviceFlow", 146, 201,
    "启动 GitHub Copilot 设备码授权流程，请求设备码并返回用户验证信息。",
    ["auth", "oauth", "device-code", "github-copilot"], "moderate")
add_fn(f"{BASE}/auth/oauth/github-copilot.ts", "refreshGitHubCopilotAccessToken", 253, 288,
    "使用刷新令牌获取新的 GitHub Copilot 访问令牌，支持企业域名。",
    ["auth", "oauth", "token-refresh", "github-copilot"], "moderate")
add_fn(f"{BASE}/auth/oauth/github-copilot.ts", "loginGitHubCopilot", 357, 395,
    "执行 GitHub Copilot OAuth 登录流程，通过设备码方式获取访问令牌。",
    ["auth", "oauth", "login", "github-copilot"], "moderate")

# --- auth/oauth/kimi-coding.ts ---
add_fn(f"{BASE}/auth/oauth/kimi-coding.ts", "startDeviceAuthorization", 69, 117,
    "向 Kimi Coding 发起设备授权请求，获取设备码和用户验证 URI。",
    ["auth", "oauth", "device-code", "kimi"], "moderate")
add_fn(f"{BASE}/auth/oauth/kimi-coding.ts", "pollForToken", 141, 207,
    "轮询 Kimi Coding 令牌端点，等待用户完成设备授权后获取访问令牌。",
    ["auth", "oauth", "polling", "kimi"], "complex")
add_fn(f"{BASE}/auth/oauth/kimi-coding.ts", "refreshToken", 228, 279,
    "使用刷新令牌获取新的 Kimi Coding 访问令牌，支持重试机制。",
    ["auth", "oauth", "token-refresh", "kimi"], "complex")
add_fn(f"{BASE}/auth/oauth/kimi-coding.ts", "loginKimiCoding", 281, 293,
    "执行 Kimi Coding OAuth 登录流程，通过设备码方式获取访问令牌。",
    ["auth", "oauth", "login", "kimi"], "simple")

# --- auth/oauth/oauth-page.ts ---
add_fn(f"{BASE}/auth/oauth/oauth-page.ts", "renderPage", 12, 92,
    "渲染 OAuth 回调页面的完整 HTML，支持自定义标题、图标和重定向逻辑。",
    ["auth", "oauth", "html", "rendering"], "moderate")
add_fn(f"{BASE}/auth/oauth/oauth-page.ts", "oauthSuccessHtml", 94, 100,
    "生成 OAuth 认证成功页面的 HTML，显示成功消息。",
    ["auth", "oauth", "html"], "simple")
add_fn(f"{BASE}/auth/oauth/oauth-page.ts", "oauthErrorHtml", 102, 109,
    "生成 OAuth 认证错误页面的 HTML，显示错误消息和详情。",
    ["auth", "oauth", "html", "error"], "simple")

# --- auth/oauth/openai-codex.ts ---
add_fn(f"{BASE}/auth/oauth/openai-codex.ts", "createAuthorizationFlow", 293, 312,
    "创建 OpenAI Codex 的 PKCE 授权流程参数，生成验证器和挑战码。",
    ["auth", "oauth", "pkce", "openai"], "simple")
add_fn(f"{BASE}/auth/oauth/openai-codex.ts", "startLocalOAuthServer", 320, 394,
    "启动本地 HTTP 服务器处理 OpenAI Codex 的 OAuth 回调，接收授权码。",
    ["auth", "oauth", "callback-server", "openai"], "complex")
add_fn(f"{BASE}/auth/oauth/openai-codex.ts", "loginOpenAICodex", 445, 506,
    "执行 OpenAI Codex OAuth 登录流程，支持浏览器和设备码两种方式。",
    ["auth", "oauth", "login", "openai"], "complex")

# --- auth/oauth/openrouter.ts ---
add_fn(f"{BASE}/auth/oauth/openrouter.ts", "exchangeAuthorizationCode", 80, 133,
    "使用 PKCE 验证器将授权码交换为 OpenRouter 的访问令牌。",
    ["auth", "oauth", "token-exchange", "pkce"], "moderate")
add_fn(f"{BASE}/auth/oauth/openrouter.ts", "startCallbackServer", 135, 240,
    "启动本地回调服务器接收 OpenRouter OAuth 授权码，处理状态验证和错误页面。",
    ["auth", "oauth", "callback-server", "openrouter"], "complex")
add_fn(f"{BASE}/auth/oauth/openrouter.ts", "loginOpenRouter", 242, 299,
    "执行 OpenRouter OAuth 登录流程，包括 PKCE 生成、浏览器授权和令牌交换。",
    ["auth", "oauth", "login", "openrouter"], "complex")

# --- auth/oauth/pkce.ts ---
add_fn(f"{BASE}/auth/oauth/pkce.ts", "generatePKCE", 21, 34,
    "生成 PKCE 验证器和挑战码，使用加密安全的随机数。",
    ["auth", "oauth", "pkce", "crypto"], "simple")

# --- auth/oauth/radius.ts ---
add_cls(f"{BASE}/auth/oauth/radius.ts", "OAuthResponseError", 68, 82,
    "OAuth 响应错误类，封装 HTTP 状态码和 OAuth 错误信息。",
    ["auth", "oauth", "error", "radius"], "simple")
add_fn(f"{BASE}/auth/oauth/radius.ts", "requestOAuthToken", 102, 140,
    "向 Radius OAuth 令牌端点发送请求，处理响应并返回令牌信息。",
    ["auth", "oauth", "token-request", "radius"], "moderate")
add_fn(f"{BASE}/auth/oauth/radius.ts", "startOAuthCallbackServer", 147, 218,
    "启动本地回调服务器接收 Radius OAuth 授权码，处理状态验证。",
    ["auth", "oauth", "callback-server", "radius"], "complex")
add_fn(f"{BASE}/auth/oauth/radius.ts", "loginWithBrowser", 220, 269,
    "通过浏览器方式执行 Radius OAuth 登录，启动回调服务器并打开浏览器。",
    ["auth", "oauth", "login", "radius"], "moderate")
add_fn(f"{BASE}/auth/oauth/radius.ts", "loginWithDeviceCode", 305, 350,
    "通过设备码方式执行 Radius OAuth 登录，轮询令牌端点。",
    ["auth", "oauth", "device-code", "radius"], "moderate")
add_fn(f"{BASE}/auth/oauth/radius.ts", "createRadiusOAuth", 357, 403,
    "Radius OAuth 工厂函数，根据配置创建支持浏览器和设备码的 OAuth 模块。",
    ["auth", "oauth", "factory", "radius"], "moderate")

# --- auth/oauth/xai.ts ---
add_fn(f"{BASE}/auth/oauth/xai.ts", "postForm", 64, 98,
    "向 xAI 端点发送表单 POST 请求，处理错误响应并返回 JSON。",
    ["auth", "oauth", "http", "xai"], "moderate")
add_fn(f"{BASE}/auth/oauth/xai.ts", "pollForTokens", 161, 199,
    "轮询 xAI 令牌端点，等待用户完成设备授权后获取访问令牌。",
    ["auth", "oauth", "polling", "xai"], "moderate")
add_fn(f"{BASE}/auth/oauth/xai.ts", "loginXai", 201, 211,
    "执行 xAI OAuth 登录流程，通过设备码方式获取访问令牌。",
    ["auth", "oauth", "login", "xai"], "simple")
add_fn(f"{BASE}/auth/oauth/xai.ts", "refreshXaiToken", 213, 227,
    "使用刷新令牌获取新的 xAI 访问令牌。",
    ["auth", "oauth", "token-refresh", "xai"], "simple")

# --- auth/resolve.ts ---
add_cls(f"{BASE}/auth/resolve.ts", "ModelsError", 26, 34,
    "模型认证错误类，携带结构化错误码用于区分不同认证失败场景。",
    ["auth", "error", "model"], "simple")
add_fn(f"{BASE}/auth/resolve.ts", "resolveProviderAuth", 50, 61,
    "解析供应商认证信息，按优先级依次尝试 OAuth、API Key 和环境变量。",
    ["auth", "resolver", "provider"], "simple")
add_fn(f"{BASE}/auth/resolve.ts", "resolveProviderAuthWithSignal", 63, 110,
    "带 AbortSignal 的供应商认证解析，支持取消长时间运行的认证操作。",
    ["auth", "resolver", "abort"], "complex")
add_fn(f"{BASE}/auth/resolve.ts", "resolveStoredOAuth", 127, 179,
    "解析存储的 OAuth 凭证，检查令牌有效期并在需要时触发刷新。",
    ["auth", "oauth", "resolver", "token-refresh"], "complex")

# --- bun-oauth.ts ---
add_fn(f"{BASE}/bun-oauth.ts", "registerBunOAuthFlows", 11, 21,
    "为 Bun 运行时注册所有内置 OAuth 流程的延迟加载器。",
    ["auth", "oauth", "bun", "registration"], "simple")

# --- cli.ts ---
add_fn(f"{BASE}/cli.ts", "login", 45, 77,
    "CLI 登录命令，引导用户选择供应商并执行 OAuth 认证流程。",
    ["cli", "auth", "login", "interactive"], "moderate")
add_fn(f"{BASE}/cli.ts", "main", 79, 114,
    "CLI 主入口函数，解析命令行参数并分发到登录或列表子命令。",
    ["entry-point", "cli", "main"], "moderate")

# --- images-models.ts ---
add_cls(f"{BASE}/images-models.ts", "ImagesModelsImpl", 97, 225,
    "图像模型管理实现类，管理多个图像供应商并提供统一的认证解析和图像生成接口。",
    ["image-generation", "service", "multi-provider"], "complex")
add_fn(f"{BASE}/images-models.ts", "createImagesProvider", 251, 275,
    "创建图像供应商定义，封装模型列表和图像生成 API 调用。",
    ["image-generation", "factory", "provider"], "moderate")

# --- model-catalog.ts ---
add_fn(f"{BASE}/model-catalog.ts", "flattenModelCatalog", 22, 27,
    "将分组模型目录扁平化为模型 ID 列表，去除分组层级。",
    ["utility", "model-catalog", "flatten"], "simple")

# --- models-store.ts ---
add_cls(f"{BASE}/models-store.ts", "InMemoryModelsStore", 27, 45,
    "内存模型存储实现，使用 Map 存储供应商模型数据，提供读写和删除操作。",
    ["data-model", "in-memory", "store"], "simple")

# --- models.ts ---
add_cls(f"{BASE}/models.ts", "ModelsImpl", 254, 733,
    "核心模型管理类，提供多供应商注册、认证解析、模型刷新、流式补全和批量完成等全部功能。",
    ["service", "multi-provider", "model-management", "streaming"], "complex")
add_fn(f"{BASE}/models.ts", "mergeHeaders", 238, 252,
    "合并 HTTP 请求头，覆盖重复的键值。",
    ["utility", "http", "headers"], "simple")
add_fn(f"{BASE}/models.ts", "createProvider", 762, 862,
    "根据供应商输入创建供应商定义，配置认证方式、API 端点和模型列表。",
    ["factory", "provider", "multi-provider"], "complex")
add_fn(f"{BASE}/models.ts", "calculateCost", 878, 898,
    "根据模型定价和使用量计算 API 调用费用。",
    ["utility", "cost", "calculation"], "moderate")
add_fn(f"{BASE}/models.ts", "clampThinkingLevel", 913, 932,
    "将思考级别限制在模型支持的范围内。",
    ["utility", "validation", "thinking"], "simple")

# --- providers/all.ts ---
add_fn(f"{BASE}/providers/all.ts", "builtinProviders", 89, 132,
    "返回所有内置 LLM 供应商的定义列表，聚合 44 个供应商模块。",
    ["registry", "multi-provider", "barrel"], "moderate")
add_fn(f"{BASE}/providers/all.ts", "builtinModels", 135, 141,
    "返回所有内置供应商的模型目录，支持供应商过滤。",
    ["registry", "model-catalog", "multi-provider"], "simple")

# --- providers/amazon-bedrock.ts ---
add_fn(f"{BASE}/providers/amazon-bedrock.ts", "amazonBedrockProvider", 82, 90,
    "创建 Amazon Bedrock 供应商定义，配置认证和 API 端点。",
    ["provider", "amazon-bedrock", "factory"], "simple")

print(f"Created {len(sub_nodes)} sub-nodes (functions + classes)")

# ============================================================
# EDGES
# ============================================================
edges = []

def add_edge(source, target, etype, weight, direction="forward"):
    if source == target:
        return
    edges.append({
        "source": source,
        "target": target,
        "type": etype,
        "direction": direction,
        "weight": weight,
    })

# --- batchImportData: 1:1 import edges ---
batch_import_data = {
    f"{BASE}/api/anthropic-messages.lazy.ts": [f"{BASE}/api/lazy.ts", f"{BASE}/types.ts"],
    f"{BASE}/api/openai-completions.lazy.ts": [f"{BASE}/api/lazy.ts", f"{BASE}/types.ts"],
    f"{BASE}/api/openai-responses.lazy.ts": [f"{BASE}/api/lazy.ts", f"{BASE}/types.ts"],
    f"{BASE}/api/openrouter-images.lazy.ts": [f"{BASE}/types.ts"],
    f"{BASE}/auth/context.ts": [f"{BASE}/auth/types.ts"],
    f"{BASE}/auth/credential-store.ts": [f"{BASE}/auth/types.ts", f"{BASE}/utils/abort.ts"],
    f"{BASE}/auth/helpers.ts": [f"{BASE}/auth/types.ts"],
    f"{BASE}/auth/oauth/anthropic.ts": [f"{BASE}/auth/oauth/oauth-page.ts", f"{BASE}/auth/oauth/pkce.ts", f"{BASE}/auth/types.ts", f"{BASE}/utils/provider-env.ts"],
    f"{BASE}/auth/oauth/device-code.ts": [],
    f"{BASE}/auth/oauth/github-copilot.ts": [f"{BASE}/auth/oauth/device-code.ts", f"{BASE}/auth/types.ts", f"{BASE}/providers/github-copilot.models.ts"],
    f"{BASE}/auth/oauth/kimi-coding.ts": [f"{BASE}/auth/oauth/device-code.ts", f"{BASE}/auth/types.ts", f"{BASE}/utils/provider-env.ts"],
    f"{BASE}/auth/oauth/load.ts": [f"{BASE}/auth/types.ts"],
    f"{BASE}/auth/oauth/oauth-page.ts": [],
    f"{BASE}/auth/oauth/openai-codex.ts": [f"{BASE}/auth/oauth/device-code.ts", f"{BASE}/auth/oauth/oauth-page.ts", f"{BASE}/auth/oauth/pkce.ts", f"{BASE}/auth/types.ts", f"{BASE}/utils/provider-env.ts"],
    f"{BASE}/auth/oauth/openrouter.ts": [f"{BASE}/auth/oauth/oauth-page.ts", f"{BASE}/auth/oauth/pkce.ts", f"{BASE}/auth/types.ts", f"{BASE}/utils/provider-env.ts"],
    f"{BASE}/auth/oauth/pkce.ts": [],
    f"{BASE}/auth/oauth/radius.ts": [f"{BASE}/auth/oauth/device-code.ts", f"{BASE}/auth/oauth/oauth-page.ts", f"{BASE}/auth/oauth/pkce.ts", f"{BASE}/auth/types.ts", f"{BASE}/providers/radius-config.ts"],
    f"{BASE}/auth/oauth/xai.ts": [f"{BASE}/auth/oauth/device-code.ts", f"{BASE}/auth/types.ts"],
    f"{BASE}/auth/resolve.ts": [f"{BASE}/auth/types.ts", f"{BASE}/types.ts", f"{BASE}/utils/abort.ts", f"{BASE}/utils/diagnostics.ts"],
    f"{BASE}/auth/types.ts": [f"{BASE}/types.ts"],
    f"{BASE}/bun-oauth.ts": [f"{BASE}/auth/oauth/anthropic.ts", f"{BASE}/auth/oauth/github-copilot.ts", f"{BASE}/auth/oauth/kimi-coding.ts", f"{BASE}/auth/oauth/load.ts", f"{BASE}/auth/oauth/openai-codex.ts", f"{BASE}/auth/oauth/openrouter.ts", f"{BASE}/auth/oauth/radius.ts", f"{BASE}/auth/oauth/xai.ts"],
    f"{BASE}/cli.ts": [f"{BASE}/index.ts", f"{BASE}/providers/all.ts"],
    f"{BASE}/compat/extension-oauth-types.ts": [f"{BASE}/auth/types.ts"],
    f"{BASE}/images-models.ts": [f"{BASE}/auth/context.ts", f"{BASE}/auth/credential-store.ts", f"{BASE}/auth/resolve.ts", f"{BASE}/auth/types.ts", f"{BASE}/models.ts", f"{BASE}/types.ts"],
    f"{BASE}/index.ts": [],
    f"{BASE}/model-catalog.ts": [f"{BASE}/types.ts"],
    f"{BASE}/models-store.ts": [f"{BASE}/types.ts"],
    f"{BASE}/models.ts": [f"{BASE}/api/lazy.ts", f"{BASE}/auth/context.ts", f"{BASE}/auth/credential-store.ts", f"{BASE}/auth/resolve.ts", f"{BASE}/auth/types.ts", f"{BASE}/models-store.ts", f"{BASE}/types.ts", f"{BASE}/utils/abort.ts"],
    f"{BASE}/oauth.ts": [],
    f"{BASE}/providers/all.ts": [
        f"{BASE}/images-models.ts", f"{BASE}/models.ts", f"{BASE}/providers/amazon-bedrock.ts",
        f"{BASE}/providers/ant-ling.ts", f"{BASE}/providers/anthropic.ts", f"{BASE}/providers/azure-openai-responses.ts",
        f"{BASE}/providers/baseten.ts", f"{BASE}/providers/cerebras.ts", f"{BASE}/providers/cloudflare-ai-gateway.ts",
        f"{BASE}/providers/cloudflare-workers-ai.ts", f"{BASE}/providers/deepseek.ts", f"{BASE}/providers/fireworks.ts",
        f"{BASE}/providers/github-copilot.ts", f"{BASE}/providers/google-vertex.ts", f"{BASE}/providers/google.ts",
        f"{BASE}/providers/groq.ts", f"{BASE}/providers/huggingface.ts", f"{BASE}/providers/kimi-coding.ts",
        f"{BASE}/providers/minimax-cn.ts", f"{BASE}/providers/minimax.ts", f"{BASE}/providers/mistral.ts",
        f"{BASE}/providers/moonshotai-cn.ts", f"{BASE}/providers/moonshotai.ts", f"{BASE}/providers/nvidia.ts",
        f"{BASE}/providers/openai-codex.ts", f"{BASE}/providers/openai.ts", f"{BASE}/providers/opencode-go.ts",
        f"{BASE}/providers/opencode.ts", f"{BASE}/providers/openrouter-images.ts", f"{BASE}/providers/openrouter.ts",
        f"{BASE}/providers/qwen-token-plan-cn.ts", f"{BASE}/providers/qwen-token-plan-individual.ts",
        f"{BASE}/providers/qwen-token-plan.ts", f"{BASE}/providers/radius.ts", f"{BASE}/providers/together.ts",
        f"{BASE}/providers/vercel-ai-gateway.ts", f"{BASE}/providers/xai.ts",
        f"{BASE}/providers/xiaomi-token-plan-ams.ts", f"{BASE}/providers/xiaomi-token-plan-cn.ts",
        f"{BASE}/providers/xiaomi-token-plan-sgp.ts", f"{BASE}/providers/xiaomi.ts",
        f"{BASE}/providers/zai-coding-cn.ts", f"{BASE}/providers/zai.ts", f"{BASE}/types.ts",
    ],
    f"{BASE}/providers/amazon-bedrock.models.ts": [f"{BASE}/model-catalog.ts"],
    f"{BASE}/providers/amazon-bedrock.ts": [f"{BASE}/api/bedrock-converse-stream.lazy.ts", f"{BASE}/auth/types.ts", f"{BASE}/models.ts", f"{BASE}/providers/amazon-bedrock.models.ts"],
    f"{BASE}/providers/ant-ling.models.ts": [f"{BASE}/model-catalog.ts"],
}

import_count = 0
for fpath, imports in batch_import_data.items():
    for imp in imports:
        add_edge(f"file:{fpath}", f"file:{imp}", "imports", 0.7)
        import_count += 1

print(f"Created {import_count} import edges (expected 120)")

# --- contains edges: file -> sub-node ---
# Map sub_nodes to their parent files
for sn in sub_nodes:
    fpath = sn["filePath"]
    add_edge(f"file:{fpath}", sn["id"], "contains", 1.0)

# --- exports edges: file -> exported sub-node ---
# Only for sub-nodes that are exported
exported_subs = {
    f"{BASE}/auth/context.ts": ["defaultProviderAuthContext"],
    f"{BASE}/auth/credential-store.ts": ["InMemoryCredentialStore"],
    f"{BASE}/auth/helpers.ts": ["envApiKeyAuth", "lazyOAuth"],
    f"{BASE}/auth/oauth/radius.ts": ["createRadiusOAuth", "OAuthResponseError"],
    f"{BASE}/auth/resolve.ts": ["ModelsError", "resolveProviderAuth"],
    f"{BASE}/bun-oauth.ts": ["registerBunOAuthFlows"],
    f"{BASE}/images-models.ts": ["ImagesModelsImpl", "createImagesProvider"],
    f"{BASE}/model-catalog.ts": ["flattenModelCatalog"],
    f"{BASE}/models-store.ts": ["InMemoryModelsStore"],
    f"{BASE}/models.ts": ["ModelsImpl", "createProvider", "calculateCost", "clampThinkingLevel"],
    f"{BASE}/providers/all.ts": ["builtinProviders", "builtinModels"],
    f"{BASE}/providers/amazon-bedrock.ts": ["amazonBedrockProvider"],
    f"{BASE}/auth/oauth/pkce.ts": ["generatePKCE"],
    f"{BASE}/auth/oauth/device-code.ts": ["pollOAuthDeviceCodeFlow"],
    f"{BASE}/auth/oauth/oauth-page.ts": ["oauthSuccessHtml", "oauthErrorHtml"],
}

for fpath, names in exported_subs.items():
    for name in names:
        # Find the sub-node
        for sn in sub_nodes:
            if sn["filePath"] == fpath and sn["name"] == name:
                add_edge(f"file:{fpath}", sn["id"], "exports", 0.8)
                break

# --- depends_on edges (cross-file runtime dependencies beyond imports) ---
# cli.ts depends on models.ts (via index.ts re-exports) - already captured via imports
# images-models.ts depends on auth/resolve.ts - already captured via imports

# --- calls edges (confident cross-file function calls) ---
# auth/resolve.ts calls resolveProviderAuth from itself - internal
# models.ts calls createProvider - internal
# providers/all.ts calls builtinProviders, builtinModels - internal

print(f"Total edges before split: {len(edges)}")
print(f"Total nodes: {len(file_nodes) + len(sub_nodes)}")

# ============================================================
# SPLIT INTO PARTS
# ============================================================
all_nodes = file_nodes + sub_nodes

# Sort files alphabetically by path
sorted_paths = sorted([fn["filePath"] for fn in file_nodes])
total_files = len(sorted_paths)
parts = math.ceil(max(len(all_nodes) / 60, len(edges) / 120))
files_per_part = math.ceil(total_files / parts)

print(f"\nSplitting into {parts} parts, {files_per_part} files per part")
print(f"Total nodes: {len(all_nodes)}, Total edges: {len(edges)}")

# Partition files into parts
file_parts = []
for i in range(parts):
    start = i * files_per_part
    end = min(start + files_per_part, total_files)
    file_parts.append(set(sorted_paths[start:end]))

for i, fp in enumerate(file_parts):
    print(f"Part {i+1}: {len(fp)} files - {sorted(fp)[:3]}...")

# Partition nodes and edges
for part_idx, part_files in enumerate(file_parts):
    part_num = part_idx + 1
    part_nodes = [n for n in all_nodes if n.get("filePath") in part_files]
    part_node_ids = {n["id"] for n in part_nodes}
    
    # Edges whose source is in this part's nodes
    part_edges = [e for e in edges if e["source"] in part_node_ids]
    
    output = {"nodes": part_nodes, "edges": part_edges}
    
    out_path = os.path.join(OUT_DIR, f"batch-10-part-{part_num}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\nPart {part_num}: {len(part_nodes)} nodes, {len(part_edges)} edges -> {out_path}")

# ============================================================
# VALIDATION
# ============================================================
print("\n=== VALIDATION ===")

# Verify total import edges
import_edges = [e for e in edges if e["type"] == "imports"]
print(f"Import edges: {len(import_edges)} (expected 120)")
assert len(import_edges) == 120, f"Import edge count mismatch: {len(import_edges)} != 120"

# Verify total contains edges
contains_edges = [e for e in edges if e["type"] == "contains"]
print(f"Contains edges: {len(contains_edges)} (expected {len(sub_nodes)})")
assert len(contains_edges) == len(sub_nodes)

# Verify total exports edges
exports_edges = [e for e in edges if e["type"] == "exports"]
print(f"Exports edges: {len(exports_edges)}")

# Verify no self-referencing edges
self_refs = [e for e in edges if e["source"] == e["target"]]
print(f"Self-referencing edges: {len(self_refs)}")
assert len(self_refs) == 0

# Verify all node IDs are unique
all_ids = [n["id"] for n in all_nodes]
dups = [x for x in all_ids if all_ids.count(x) > 1]
print(f"Duplicate node IDs: {len(set(dups))}")
assert len(set(dups)) == 0

# Verify each part's JSON is valid
for part_idx in range(parts):
    part_num = part_idx + 1
    out_path = os.path.join(OUT_DIR, f"batch-10-part-{part_num}.json")
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Part {part_num}: valid JSON, {len(data['nodes'])} nodes, {len(data['edges'])} edges")

print("\n=== ALL VALIDATION PASSED ===")
