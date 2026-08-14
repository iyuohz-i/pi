import json, os, math

with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-14.json", "r") as f:
    extract_data = json.load(f)
with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-14.json", "r") as f:
    dispatch_data = json.load(f)

batch_import_data = dispatch_data["batchImportData"]
results = {r["path"]: r for r in extract_data["results"]}
all_files = sorted(results.keys())

file_meta = {
    "packages/coding-agent/src/core/extensions/types.ts": ("扩展系统核心类型定义模块，定义了扩展接口、工具定义、会话事件、斜杠命令等所有扩展相关的 TypeScript 类型契约，是整个扩展体系的类型基础。", ["type-definition", "extensions", "api-contract"], "complex", "大量 interface/type 定义，是扩展系统的类型契约中枢。"),
    "packages/coding-agent/src/core/extensions/wrapper.ts": ("扩展工具包装器，将已注册的扩展工具与 ExtensionRunner 关联起来，为工具调用提供扩展生命周期钩子。", ["extensions", "middleware", "tool-wrapper"], "simple", None),
    "packages/coding-agent/src/core/footer-data-provider.ts": ("底部状态栏数据提供者，管理 Git 分支监控、扩展状态跟踪和可用 provider 计数，通过文件系统监视实现实时分支变更通知。", ["ui-data", "git", "file-watcher", "status-bar"], "complex", None),
    "packages/coding-agent/src/core/http-dispatcher.ts": ("HTTP 请求分发器配置模块，管理 undici dispatcher 的空闲超时、代理设置和全局 HTTP 分发器实例。", ["http", "network", "configuration"], "moderate", None),
    "packages/coding-agent/src/core/model-config.ts": ("模型配置加载器，从 models.json 配置文件解析 provider 定义，支持 JSON 注释剥离和配置错误诊断。", ["config", "model", "provider"], "moderate", None),
    "packages/coding-agent/src/core/model-registry.ts": ("模型注册表，封装 ModelRuntime 提供 provider 查询、模型搜索、认证状态检查和 provider 动态注册/注销功能。", ["model", "registry", "provider", "auth"], "moderate", None),
    "packages/coding-agent/src/core/model-resolver.ts": ("模型解析器，处理 CLI 模型参数解析、模式匹配、模糊查找和会话模型恢复，支持 provider/model 格式和作用域解析。", ["model", "resolver", "cli", "pattern-matching"], "complex", None),
    "packages/coding-agent/src/core/model-runtime.ts": ("模型运行时核心，管理 provider 组合、模型可用性刷新、凭据同步、流式/完成请求，是 LLM 交互的中央运行时引擎。", ["model", "runtime", "llm", "provider", "core"], "complex", "45 个方法的超大类，是 LLM 交互的中枢，管理 provider 生命周期和凭据同步。"),
    "packages/coding-agent/src/core/models-store.ts": ("模型存储抽象层，提供内存和文件两种存储后端，用于持久化用户自定义模型配置。", ["model", "storage", "persistence"], "moderate", None),
    "packages/coding-agent/src/core/output-guard.ts": ("输出保护模块，接管 stdout 输出流以防止 TUI 模式下非 TUI 输出污染终端，提供原始输出和背压管理。", ["output", "stdout", "tui", "guard"], "moderate", None),
    "packages/coding-agent/src/core/package-manager.ts": ("包管理器核心实现，处理 npm/git 源的安装、更新、卸载，以及自动发现 skills/prompts/themes/extensions 等资源。", ["package-manager", "npm", "git", "resources", "core"], "complex", "近 2700 行的超大模块，DefaultPackageManager 类有 98 个方法，涵盖 npm/git 安装、资源收集和路径管理。"),
    "packages/coding-agent/src/core/pi-manifest.ts": ("Pi 清单读取器，从 package.json 解析 pi 扩展的 manifest 配置。", ["manifest", "config", "package"], "simple", None),
    "packages/coding-agent/src/core/project-trust.ts": ("项目信任管理模块，处理项目信任选项选择和信任状态解析，控制扩展在项目中的执行权限。", ["security", "trust", "project", "permissions"], "moderate", None),
    "packages/coding-agent/src/core/prompt-templates.ts": ("提示词模板加载器，从文件系统发现和加载自定义提示词模板，支持参数替换和 frontmatter 解析。", ["prompt", "template", "loader"], "moderate", None),
    "packages/coding-agent/src/core/provider-attribution.ts": ("Provider 归因头管理，为 LLM 请求添加 session 追踪和遥测归因 HTTP 头。", ["provider", "http-headers", "attribution", "telemetry"], "moderate", None),
    "packages/coding-agent/src/core/provider-composer.ts": ("Provider 组合器，将基础配置、模型 JSON、扩展覆盖和认证信息组合成完整的 provider 模型定义。", ["provider", "composer", "config", "auth"], "complex", None),
    "packages/coding-agent/src/core/radius.ts": ("Radius provider 的重新导出模块，从远程 catalog 加载 Radius 模型配置。", ["barrel", "radius", "re-export"], "simple", None),
    "packages/coding-agent/src/core/resolve-config-value.ts": ("配置值解析器，支持从环境变量、shell 命令和字面量解析配置值，带缓存和模板插值功能。", ["config", "resolver", "shell", "env-var"], "complex", None),
    "packages/coding-agent/src/core/resource-loader.ts": ("资源加载器核心，统一发现和加载扩展、skills、prompts、themes 和 context 文件，处理冲突检测和信任管理。", ["resource-loader", "extensions", "skills", "themes", "core"], "complex", "902 行的 DefaultResourceLoader 类管理所有运行时资源的发现、加载和冲突检测。"),
    "packages/coding-agent/src/core/runtime-credentials.ts": ("运行时凭据管理器，在 auth storage 之上提供 API key 运行时覆盖，支持临时凭据注入。", ["auth", "credentials", "runtime"], "simple", None),
    "packages/coding-agent/src/core/sdk.ts": ("SDK 入口模块，导出 createAgentSession 和所有公开工具创建函数，是外部集成的主要 API 表面。", ["sdk", "entry-point", "api", "barrel"], "complex", "大量 re-exports 组成 SDK 公开 API，createAgentSession 是核心工厂函数。"),
    "packages/coding-agent/src/core/session-cwd.ts": ("会话工作目录管理，检测和格式化会话 CWD 缺失错误，提供恢复提示。", ["session", "cwd", "error-handling"], "simple", None),
    "packages/coding-agent/src/core/session-manager.ts": ("会话管理器核心，处理会话的创建、持久化、分支、上下文构建和历史迁移，支持树形会话结构。", ["session", "persistence", "manager", "core"], "complex", "1714 行的会话管理核心，SessionManager 类有 45 个方法，支持树形分支和版本迁移。"),
    "packages/coding-agent/src/core/settings-manager.ts": ("设置管理器核心，处理全局和项目级设置的加载、持久化、迁移和版本控制，管理 100+ 配置项。", ["settings", "config", "persistence", "manager", "core"], "complex", "1290 行，SettingsManager 类有 137 个方法，覆盖所有配置项的 getter/setter。"),
    "packages/coding-agent/src/core/skills.ts": ("Skills 加载器，从文件系统发现和加载 skill 定义，支持 frontmatter 解析、名称验证和冲突检测。", ["skills", "loader", "discovery"], "complex", None),
    "packages/coding-agent/src/core/slash-commands.ts": ("斜杠命令加载器，从配置和扩展中收集自定义斜杠命令定义。", ["slash-commands", "loader", "config"], "simple", None),
    "packages/coding-agent/src/core/source-info.ts": ("资源来源信息工厂，创建标记资源来源（builtin/package/extension 等）的 SourceInfo 对象。", ["source-info", "factory", "metadata"], "simple", None),
    "packages/coding-agent/src/core/system-prompt.ts": ("系统提示词构建器，组装 agent 的系统提示词，包含 skills 列表和工具说明。", ["system-prompt", "builder", "agent"], "moderate", None),
    "packages/coding-agent/src/core/telemetry.ts": ("遥测模块，重新导出设置管理器的遥测配置访问。", ["telemetry", "barrel", "re-export"], "simple", None),
    "packages/coding-agent/src/core/timings.ts": ("性能计时工具，提供带命名空间的计时函数和分组打印功能。", ["performance", "timing", "utility"], "simple", None),
    "packages/coding-agent/src/core/tools/bash.ts": ("Bash 工具实现，创建 shell 命令执行工具定义，支持超时、输出截断和结果渲染。", ["tool", "bash", "shell", "command-execution"], "complex", None),
    "packages/coding-agent/src/core/tools/edit-diff.ts": ("编辑差异计算模块，提供 fuzzy 匹配、行尾规范化、统一 diff 生成和编辑应用功能。", ["tool", "diff", "fuzzy-match", "edit"], "complex", None),
    "packages/coding-agent/src/core/tools/edit.ts": ("编辑工具实现，创建文件编辑工具定义，支持多编辑操作、diff 预览渲染和文件变更队列。", ["tool", "edit", "file-mutation", "diff"], "complex", None),
}

func_meta = {
    ("packages/coding-agent/src/core/extensions/wrapper.ts", "wrapRegisteredTool"): ("将已注册的扩展工具包装为带 ExtensionRunner 钩子的工具定义。", ["extensions", "tool-wrapper", "middleware"]),
    ("packages/coding-agent/src/core/footer-data-provider.ts", "findGitPaths"): ("查找给定工作目录下的 .git 路径，支持 worktree 和子模块。", ["git", "path-finding", "utility"]),
    ("packages/coding-agent/src/core/footer-data-provider.ts", "resolveBranchWithGitAsync"): ("异步解析 Git 仓库的当前分支名称。", ["git", "branch", "async"]),
    ("packages/coding-agent/src/core/http-dispatcher.ts", "parseHttpIdleTimeoutMs"): ("解析 HTTP 空闲超时设置字符串为毫秒值。", ["http", "parser", "timeout"]),
    ("packages/coding-agent/src/core/http-dispatcher.ts", "createUndiciOriginDispatcher"): ("为指定 origin 创建 undici dispatcher 实例。", ["http", "dispatcher", "undici"]),
    ("packages/coding-agent/src/core/http-dispatcher.ts", "configureHttpDispatcher"): ("配置全局 HTTP dispatcher 的空闲超时和代理设置。", ["http", "configuration", "dispatcher"]),
    ("packages/coding-agent/src/core/model-config.ts", "formatValidationPath"): ("格式化配置验证错误中的路径信息。", ["config", "validation", "formatter"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "findExactModelReferenceMatch"): ("在可用模型列表中查找与模型引用精确匹配的模型。", ["model", "matcher", "exact-match"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "tryMatchModel"): ("尝试用模式匹配可用模型列表，返回最佳匹配。", ["model", "matcher", "pattern"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "buildFallbackModel"): ("当无法找到匹配模型时构建回退模型定义。", ["model", "fallback", "builder"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "parseModelPattern"): ("解析 provider/model 模式字符串，支持通配符和作用域。", ["model", "parser", "pattern"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "resolveModelScopeFromModels"): ("从模型列表解析模式集合，返回匹配的模型作用域。", ["model", "resolver", "scope"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "resolveModelScope"): ("解析模型作用域，委托给 ModelRuntime 获取可用模型。", ["model", "resolver", "scope"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "resolveCliModel"): ("从 CLI 参数解析用户选择的模型，支持多种输入格式和回退逻辑。", ["model", "resolver", "cli"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "findInitialModel"): ("查找会话的初始模型，考虑默认 provider 和上次使用模型。", ["model", "resolver", "initialization"]),
    ("packages/coding-agent/src/core/model-resolver.ts", "restoreModelFromSession"): ("从已保存的会话状态恢复 provider 和模型选择。", ["model", "resolver", "session-restore"]),
    ("packages/coding-agent/src/core/model-runtime.ts", "mergeHeaders"): ("合并两组 HTTP 头，覆盖值优先。", ["http", "merge", "utility"]),
    ("packages/coding-agent/src/core/output-guard.ts", "writeRawStdoutChunk"): ("绕过 TUI 输出保护直接写入 stdout 原始文本块。", ["output", "stdout", "raw"]),
    ("packages/coding-agent/src/core/output-guard.ts", "takeOverStdout"): ("接管 stdout 输出流，安装 TUI 输出保护机制。", ["output", "stdout", "guard"]),
    ("packages/coding-agent/src/core/package-manager.ts", "getEnv"): ("获取包管理操作的默认环境变量。", ["package-manager", "env", "utility"]),
    ("packages/coding-agent/src/core/package-manager.ts", "prefixIgnorePattern"): ("为 ignore 模式添加前缀以匹配文件路径。", ["package-manager", "ignore", "pattern"]),
    ("packages/coding-agent/src/core/package-manager.ts", "addIgnoreRules"): ("向 ignore 实例添加目录的忽略规则。", ["package-manager", "ignore", "rules"]),
    ("packages/coding-agent/src/core/package-manager.ts", "splitPatterns"): ("将模式字符串拆分为模式数组。", ["package-manager", "pattern", "splitter"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectFiles"): ("递归收集目录中匹配指定模式的文件。", ["package-manager", "files", "collector"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectSkillEntries"): ("从目录收集 skill 条目，支持根文件和子目录模式。", ["package-manager", "skills", "collector"]),
    ("packages/coding-agent/src/core/package-manager.ts", "findGitRepoRoot"): ("从指定目录向上查找 Git 仓库根目录。", ["package-manager", "git", "path-finding"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectAncestorAgentsSkillDirs"): ("收集祖先目录中的 .pi/agents/skills 路径。", ["package-manager", "skills", "discovery"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectAutoPromptEntries"): ("自动发现目录中的提示词模板条目。", ["package-manager", "prompts", "discovery"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectAutoThemeEntries"): ("自动发现目录中的主题文件条目。", ["package-manager", "themes", "discovery"]),
    ("packages/coding-agent/src/core/package-manager.ts", "resolveExtensionEntries"): ("解析目录中的扩展条目。", ["package-manager", "extensions", "resolver"]),
    ("packages/coding-agent/src/core/package-manager.ts", "collectAutoExtensionEntries"): ("自动发现目录中的扩展文件。", ["package-manager", "extensions", "discovery"]),
    ("packages/coding-agent/src/core/package-manager.ts", "matchesAnyPattern"): ("检查文件路径是否匹配任意 glob 模式。", ["package-manager", "pattern", "matcher"]),
    ("packages/coding-agent/src/core/package-manager.ts", "matchesAnyExactPattern"): ("检查文件路径是否精确匹配任意模式。", ["package-manager", "pattern", "matcher"]),
    ("packages/coding-agent/src/core/package-manager.ts", "isEnabledByOverrides"): ("根据覆盖模式判断文件是否启用。", ["package-manager", "pattern", "override"]),
    ("packages/coding-agent/src/core/package-manager.ts", "applyPatterns"): ("将包含/排除模式应用到路径列表，返回过滤后的结果。", ["package-manager", "pattern", "filter"]),
    ("packages/coding-agent/src/core/package-manager.ts", "applyAutoloadDisabledPatterns"): ("应用自动加载禁用模式过滤路径。", ["package-manager", "pattern", "autoload"]),
    ("packages/coding-agent/src/core/pi-manifest.ts", "readPiManifest"): ("从 package.json 读取 pi 扩展 manifest 配置。", ["manifest", "reader", "config"]),
    ("packages/coding-agent/src/core/project-trust.ts", "selectProjectTrustOption"): ("交互式选择项目信任选项。", ["security", "trust", "selector"]),
    ("packages/coding-agent/src/core/project-trust.ts", "resolveProjectTrusted"): ("解析项目是否被信任，处理信任提示和存储。", ["security", "trust", "resolver"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "parseCommandArgs"): ("解析提示词模板命令的参数字符串。", ["prompt", "parser", "args"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "substituteArgs"): ("将参数值替换到模板内容中的占位符。", ["prompt", "substitution", "args"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "loadTemplateFromFile"): ("从单个文件加载提示词模板，解析 frontmatter。", ["prompt", "loader", "file"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "loadTemplatesFromDir"): ("从目录批量加载提示词模板。", ["prompt", "loader", "directory"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "loadPromptTemplates"): ("加载所有提示词模板源，包括配置路径和自动发现。", ["prompt", "loader", "discovery"]),
    ("packages/coding-agent/src/core/prompt-templates.ts", "expandPromptTemplate"): ("展开模板文本中的参数引用。", ["prompt", "expansion", "template"]),
    ("packages/coding-agent/src/core/provider-attribution.ts", "getDefaultAttributionHeaders"): ("获取 provider 的默认归因 HTTP 头。", ["provider", "attribution", "http-headers"]),
    ("packages/coding-agent/src/core/provider-attribution.ts", "getSessionHeaders"): ("获取会话追踪 HTTP 头。", ["provider", "attribution", "session"]),
    ("packages/coding-agent/src/core/provider-attribution.ts", "mergeProviderAttributionHeaders"): ("合并多个来源的 provider 归因 HTTP 头。", ["provider", "attribution", "merge"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "mergeCompat"): ("合并两组兼容性配置，覆盖值优先。", ["provider", "compat", "merge"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "applyModelOverride"): ("将模型覆盖配置应用到基础模型定义。", ["provider", "model", "override"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "modelFromJson"): ("从 JSON 定义创建模型对象。", ["provider", "model", "factory"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "applyModelsJson"): ("将 models.json 配置应用到基础模型列表。", ["provider", "model", "config"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "applyExtension"): ("将扩展覆盖应用到 provider 模型列表。", ["provider", "model", "extension"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "adaptOAuth"): ("适配 OAuth 认证配置为标准格式。", ["provider", "oauth", "adapter"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "withConfiguredAuth"): ("为请求配置认证头和 API key。", ["provider", "auth", "configuration"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "configContextEnv"): ("提取配置上下文中的环境变量值。", ["provider", "config", "env"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "composeApiKeyAuth"): ("组合 API key 认证配置，处理环境变量和 shell 命令。", ["provider", "auth", "api-key"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "composeOAuthAuth"): ("组合 OAuth 认证配置。", ["provider", "auth", "oauth"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "rawModelHeaders"): ("提取模型的原始 HTTP 头配置。", ["provider", "model", "http-headers"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "validateExtensionProvider"): ("验证扩展 provider 配置的合法性。", ["provider", "validation", "extension"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "composeModelProvider"): ("组合完整的 provider 模型定义，包括模型列表、认证和头。", ["provider", "composer", "core"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "resolveConfiguredModelHeaders"): ("解析模型配置的 HTTP 头，处理环境变量引用。", ["provider", "model", "http-headers"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "resolveCompatibilityRequestConfig"): ("解析兼容性请求配置。", ["provider", "compat", "resolver"]),
    ("packages/coding-agent/src/core/provider-composer.ts", "configuredRequestAuthStatus"): ("检查配置的请求认证状态。", ["provider", "auth", "status"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "parseConfigValueTemplate"): ("解析配置值模板，识别 env 和 shell 命令引用。", ["config", "parser", "template"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "resolveTemplate"): ("用环境变量值解析模板部分。", ["config", "resolver", "template"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "executeWithConfiguredShell"): ("使用配置的 shell 执行命令并返回输出。", ["config", "shell", "executor"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "executeWithDefaultShell"): ("使用默认 shell 执行命令。", ["config", "shell", "executor"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "resolveConfigValueOrThrow"): ("解析配置值，失败时抛出描述性错误。", ["config", "resolver", "error"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "resolveHeaders"): ("解析 HTTP 头配置中的环境变量和命令引用。", ["config", "resolver", "http-headers"]),
    ("packages/coding-agent/src/core/resolve-config-value.ts", "resolveHeadersOrThrow"): ("解析 HTTP 头配置，失败时抛出错误。", ["config", "resolver", "http-headers"]),
    ("packages/coding-agent/src/core/resource-loader.ts", "resolvePromptInput"): ("解析提示词输入，处理文件路径和内联文本。", ["resource-loader", "prompt", "resolver"]),
    ("packages/coding-agent/src/core/resource-loader.ts", "loadContextFileFromDir"): ("从目录加载 context 文件。", ["resource-loader", "context", "loader"]),
    ("packages/coding-agent/src/core/resource-loader.ts", "findShadowedContextFile"): ("查找被项目级配置覆盖的 context 文件。", ["resource-loader", "context", "shadowing"]),
    ("packages/coding-agent/src/core/resource-loader.ts", "loadProjectContextFiles"): ("加载项目上下文文件，合并全局和项目级配置。", ["resource-loader", "context", "loader"]),
    ("packages/coding-agent/src/core/sdk.ts", "createAgentSession"): ("创建完整的 agent 会话实例，组装所有运行时组件包括模型、工具、扩展和资源。", ["sdk", "factory", "agent-session", "core"]),
    ("packages/coding-agent/src/core/session-cwd.ts", "getMissingSessionCwdIssue"): ("检测会话工作目录是否缺失并返回诊断信息。", ["session", "cwd", "diagnostics"]),
    ("packages/coding-agent/src/core/session-manager.ts", "migrateV1ToV2"): ("将会话条目从 V1 格式迁移到 V2。", ["session", "migration", "version"]),
    ("packages/coding-agent/src/core/session-manager.ts", "migrateV2ToV3"): ("将会话条目从 V2 格式迁移到 V3。", ["session", "migration", "version"]),
    ("packages/coding-agent/src/core/session-manager.ts", "migrateToCurrentVersion"): ("将会话条目迁移到当前版本。", ["session", "migration", "version"]),
    ("packages/coding-agent/src/core/session-manager.ts", "parseSessionEntries"): ("解析会话文件内容为条目数组。", ["session", "parser", "entries"]),
    ("packages/coding-agent/src/core/session-manager.ts", "buildSessionPath"): ("从会话条目构建到指定叶节点的路径。", ["session", "tree", "path"]),
    ("packages/coding-agent/src/core/session-manager.ts", "getSessionContextSettings"): ("从会话路径提取上下文设置。", ["session", "context", "settings"]),
    ("packages/coding-agent/src/core/session-manager.ts", "sessionEntryToContextMessages"): ("将会话条目转换为 LLM 上下文消息。", ["session", "context", "converter"]),
    ("packages/coding-agent/src/core/session-manager.ts", "buildContextEntries"): ("构建到指定叶节点的上下文条目链。", ["session", "context", "builder"]),
    ("packages/coding-agent/src/core/session-manager.ts", "buildSessionContext"): ("从条目构建完整的会话上下文。", ["session", "context", "builder"]),
    ("packages/coding-agent/src/core/session-manager.ts", "loadEntriesFromFile"): ("从会话文件加载并解析条目，处理迁移。", ["session", "loader", "file"]),
    ("packages/coding-agent/src/core/session-manager.ts", "readSessionHeader"): ("读取会话文件头部信息。", ["session", "reader", "header"]),
    ("packages/coding-agent/src/core/session-manager.ts", "findMostRecentSession"): ("在目录中查找最近的会话文件。", ["session", "finder", "recent"]),
    ("packages/coding-agent/src/core/session-manager.ts", "extractTextContent"): ("从消息中提取纯文本内容。", ["session", "extractor", "text"]),
    ("packages/coding-agent/src/core/session-manager.ts", "getMessageActivityTime"): ("获取会话条目的活动时间戳。", ["session", "time", "extractor"]),
    ("packages/coding-agent/src/core/session-manager.ts", "buildSessionInfo"): ("从会话文件构建会话信息摘要。", ["session", "builder", "info"]),
    ("packages/coding-agent/src/core/session-manager.ts", "buildSessionInfosWithConcurrency"): ("并发构建多个会话信息。", ["session", "builder", "concurrency"]),
    ("packages/coding-agent/src/core/session-manager.ts", "listSessionsFromDir"): ("列出目录中的所有会话。", ["session", "lister", "directory"]),
    ("packages/coding-agent/src/core/settings-manager.ts", "deepMergeObjects"): ("深度合并两个设置对象。", ["settings", "merge", "utility"]),
    ("packages/coding-agent/src/core/settings-manager.ts", "parseTimeoutSetting"): ("解析超时设置值。", ["settings", "parser", "timeout"]),
    ("packages/coding-agent/src/core/skills.ts", "prefixIgnorePattern"): ("为 skill 忽略模式添加前缀。", ["skills", "ignore", "pattern"]),
    ("packages/coding-agent/src/core/skills.ts", "addIgnoreRules"): ("向 ignore 实例添加 skill 目录规则。", ["skills", "ignore", "rules"]),
    ("packages/coding-agent/src/core/skills.ts", "validateName"): ("验证 skill 名称的合法性。", ["skills", "validation", "name"]),
    ("packages/coding-agent/src/core/skills.ts", "validateDescription"): ("验证 skill 描述的合法性。", ["skills", "validation", "description"]),
    ("packages/coding-agent/src/core/skills.ts", "createSkillSourceInfo"): ("创建 skill 的来源信息对象。", ["skills", "source-info", "factory"]),
    ("packages/coding-agent/src/core/skills.ts", "loadSkillsFromDirInternal"): ("从目录内部加载 skill 定义，解析 frontmatter。", ["skills", "loader", "directory"]),
    ("packages/coding-agent/src/core/skills.ts", "loadSkillFromFile"): ("从单个文件加载 skill 定义。", ["skills", "loader", "file"]),
    ("packages/coding-agent/src/core/skills.ts", "formatSkillsForPrompt"): ("将 skills 列表格式化为系统提示词文本。", ["skills", "formatter", "prompt"]),
    ("packages/coding-agent/src/core/skills.ts", "loadSkills"): ("从所有配置源加载 skills，包括自动发现和扩展。", ["skills", "loader", "discovery"]),
    ("packages/coding-agent/src/core/source-info.ts", "createSyntheticSourceInfo"): ("创建合成的来源信息对象，用于非文件来源。", ["source-info", "factory", "synthetic"]),
    ("packages/coding-agent/src/core/system-prompt.ts", "buildSystemPrompt"): ("构建 agent 系统提示词，组装基础指令、skills 和上下文。", ["system-prompt", "builder", "agent"]),
    ("packages/coding-agent/src/core/timings.ts", "time"): ("计时函数，记录带命名空间的时间段。", ["timing", "performance", "measure"]),
    ("packages/coding-agent/src/core/timings.ts", "printTimingGroup"): ("打印一组计时结果。", ["timing", "performance", "print"]),
    ("packages/coding-agent/src/core/tools/bash.ts", "resolveTimeoutMs"): ("解析 bash 命令超时毫秒值。", ["bash", "timeout", "resolver"]),
    ("packages/coding-agent/src/core/tools/bash.ts", "createLocalBashOperations"): ("创建本地 bash 操作集，封装进程生成和输出处理。", ["bash", "operations", "factory"]),
    ("packages/coding-agent/src/core/tools/bash.ts", "resolveSpawnContext"): ("解析 bash 命令的生成上下文，处理环境变量和 shell 配置。", ["bash", "spawn", "context"]),
    ("packages/coding-agent/src/core/tools/bash.ts", "rebuildBashResultRenderComponent"): ("重建 bash 结果的渲染组件，包含输出和状态。", ["bash", "render", "result"]),
    ("packages/coding-agent/src/core/tools/bash.ts", "createBashToolDefinition"): ("创建完整的 bash 工具定义，包括执行、渲染和截断逻辑。", ["bash", "tool-definition", "factory"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "normalizeForFuzzyMatch"): ("规范化文本用于模糊匹配，去除空白和大小写差异。", ["diff", "normalize", "fuzzy-match"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "getReplacementLineRange"): ("获取替换操作的行范围。", ["diff", "replacement", "line-range"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "applyReplacements"): ("将替换操作应用到内容上。", ["diff", "replacement", "apply"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "applyReplacementsPreservingUnchangedLines"): ("应用替换同时保留未更改的行。", ["diff", "replacement", "preserve"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "fuzzyFindText"): ("在内容中模糊查找文本，支持容错匹配。", ["diff", "fuzzy-match", "finder"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "getNotFoundError"): ("生成未找到文本的错误消息。", ["diff", "error", "not-found"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "getDuplicateError"): ("生成重复匹配的错误消息。", ["diff", "error", "duplicate"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "applyEditsToNormalizedContent"): ("将编辑操作应用到规范化后的内容上。", ["diff", "edit", "apply"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "generateDiffString"): ("生成旧内容和新内容之间的 diff 字符串。", ["diff", "generator", "unified"]),
    ("packages/coding-agent/src/core/tools/edit-diff.ts", "computeEditsDiff"): ("计算编辑操作的 diff 结果。", ["diff", "compute", "edit"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "prepareEditArguments"): ("准备和验证编辑工具的输入参数。", ["edit", "args", "preparation"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "getEditCallRenderComponent"): ("获取编辑调用的渲染组件。", ["edit", "render", "component"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "getRenderablePreviewInput"): ("获取可渲染的编辑预览输入。", ["edit", "render", "preview"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "formatEditResult"): ("格式化编辑操作的结果文本。", ["edit", "formatter", "result"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "getEditHeaderBg"): ("获取编辑预览的头部背景色。", ["edit", "render", "theme"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "buildEditCallComponent"): ("构建编辑调用的完整渲染组件。", ["edit", "render", "builder"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "setEditPreview"): ("设置编辑预览内容和参数键。", ["edit", "preview", "setter"]),
    ("packages/coding-agent/src/core/tools/edit.ts", "createEditToolDefinition"): ("创建完整的编辑工具定义，包括执行、diff 预览和渲染。", ["edit", "tool-definition", "factory"]),
}

class_meta = {
    ("packages/coding-agent/src/core/footer-data-provider.ts", "FooterDataProvider"): ("底部状态栏数据提供者类，管理 Git 分支监视、扩展状态和 provider 计数，通过回调通知变更。", ["status-bar", "git", "file-watcher", "provider"]),
    ("packages/coding-agent/src/core/model-config.ts", "ModelConfig"): ("模型配置类，加载和解析 models.json，提供 provider 查询和错误诊断。", ["model", "config", "provider"]),
    ("packages/coding-agent/src/core/model-registry.ts", "ModelRegistry"): ("模型注册表类，封装 ModelRuntime 提供 provider 查询、模型搜索、认证检查和动态注册。", ["model", "registry", "provider", "auth"]),
    ("packages/coding-agent/src/core/model-runtime.ts", "ModelRuntime"): ("模型运行时核心类，管理 provider 组合、可用性刷新、凭据同步和 LLM 请求，是 LLM 交互的中央引擎。", ["model", "runtime", "llm", "core"]),
    ("packages/coding-agent/src/core/models-store.ts", "InMemoryCodingAgentModelsStore"): ("内存模型存储实现，用于测试和临时配置。", ["model", "storage", "in-memory"]),
    ("packages/coding-agent/src/core/models-store.ts", "FileModelsStore"): ("文件模型存储实现，持久化用户自定义模型配置到 JSON 文件。", ["model", "storage", "file"]),
    ("packages/coding-agent/src/core/package-manager.ts", "DefaultPackageManager"): ("默认包管理器实现，处理 npm/git 源安装、更新、卸载和资源自动发现，98 个方法覆盖完整生命周期。", ["package-manager", "npm", "git", "core"]),
    ("packages/coding-agent/src/core/resource-loader.ts", "DefaultResourceLoader"): ("默认资源加载器实现，统一发现和加载扩展、skills、prompts、themes 和 context 文件。", ["resource-loader", "extensions", "skills", "core"]),
    ("packages/coding-agent/src/core/runtime-credentials.ts", "RuntimeCredentials"): ("运行时凭据管理类，在 auth storage 之上提供 API key 临时覆盖。", ["auth", "credentials", "runtime"]),
    ("packages/coding-agent/src/core/session-manager.ts", "SessionManager"): ("会话管理器类，处理会话创建、持久化、分支、上下文构建和版本迁移，支持树形会话结构。", ["session", "manager", "persistence", "core"]),
    ("packages/coding-agent/src/core/settings-manager.ts", "FileSettingsStorage"): ("文件设置存储后端，处理全局和项目级设置的文件 I/O 和锁。", ["settings", "storage", "file"]),
    ("packages/coding-agent/src/core/settings-manager.ts", "SettingsManager"): ("设置管理器核心类，管理 100+ 配置项的加载、持久化、迁移和版本控制。", ["settings", "manager", "config", "core"]),
}

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
