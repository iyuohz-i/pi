
import json, os, math

with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-14.json", "r") as f:
    extract_data = json.load(f)
with open("/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-14.json", "r") as f:
    dispatch_data = json.load(f)

batch_import_data = dispatch_data["batchImportData"]
results = {r["path"]: r for r in extract_data["results"]}
all_files = sorted(results.keys())

file_meta = {
"packages/coding-agent/src/core/extensions/types.ts": ("扩展系统核心类型定义模块，定义了扩展接口、工具定义、会话事件、斜杠命令等所有扩展相关的 TypeScript 类型契约，是整个扩展体系的类型基础。", ["type-definition","extensions","api-contract"], "complex", "大量 interface/type 定义，是扩展系统的类型契约中枢。"),
"packages/coding-agent/src/core/extensions/wrapper.ts": ("扩展工具包装器，将已注册的扩展工具与 ExtensionRunner 关联起来，为工具调用提供扩展生命周期钩子。", ["extensions","middleware","tool-wrapper"], "simple", None),
"packages/coding-agent/src/core/footer-data-provider.ts": ("底部状态栏数据提供者，管理 Git 分支监控、扩展状态跟踪和可用 provider 计数，通过文件系统监视实现实时分支变更通知。", ["ui-data","git","file-watcher","status-bar"], "complex", None),
"packages/coding-agent/src/core/http-dispatcher.ts": ("HTTP 请求分发器配置模块，管理 undici dispatcher 的空闲超时、代理设置和全局 HTTP 分发器实例。", ["http","network","configuration"], "moderate", None),
"packages/coding-agent/src/core/model-config.ts": ("模型配置加载器，从 models.json 配置文件解析 provider 定义，支持 JSON 注释剥离和配置错误诊断。", ["config","model","provider"], "moderate", None),
"packages/coding-agent/src/core/model-registry.ts": ("模型注册表，封装 ModelRuntime 提供 provider 查询、模型搜索、认证状态检查和 provider 动态注册/注销功能。", ["model","registry","provider","auth"], "moderate", None),
"packages/coding-agent/src/core/model-resolver.ts": ("模型解析器，处理 CLI 模型参数解析、模式匹配、模糊查找和会话模型恢复，支持 provider/model 格式和作用域解析。", ["model","resolver","cli","pattern-matching"], "complex", None),
"packages/coding-agent/src/core/model-runtime.ts": ("模型运行时核心，管理 provider 组合、模型可用性刷新、凭据同步、流式/完成请求，是 LLM 交互的中央运行时引擎。", ["model","runtime","llm","provider","core"], "complex", "45 个方法的超大类，是 LLM 交互的中枢，管理 provider 生命周期和凭据同步。"),
"packages/coding-agent/src/core/models-store.ts": ("模型存储抽象层，提供内存和文件两种存储后端，用于持久化用户自定义模型配置。", ["model","storage","persistence"], "moderate", None),
"packages/coding-agent/src/core/output-guard.ts": ("输出保护模块，接管 stdout 输出流以防止 TUI 模式下非 TUI 输出污染终端，提供原始输出和背压管理。", ["output","stdout","tui","guard"], "moderate", None),
"packages/coding-agent/src/core/package-manager.ts": ("包管理器核心实现，处理 npm/git 源的安装、更新、卸载，以及自动发现 skills/prompts/themes/extensions 等资源。", ["package-manager","npm","git","resources","core"], "complex", "近 2700 行的超大模块，DefaultPackageManager 类有 98 个方法，涵盖 npm/git 安装、资源收集和路径管理。"),
"packages/coding-agent/src/core/pi-manifest.ts": ("Pi 清单读取器，从 package.json 解析 pi 扩展的 manifest 配置。", ["manifest","config","package"], "simple", None),
"packages/coding-agent/src/core/project-trust.ts": ("项目信任管理模块，处理项目信任选项选择和信任状态解析，控制扩展在项目中的执行权限。", ["security","trust","project","permissions"], "moderate", None),
"packages/coding-agent/src/core/prompt-templates.ts": ("提示词模板加载器，从文件系统发现和加载自定义提示词模板，支持参数替换和 frontmatter 解析。", ["prompt","template","loader"], "moderate", None),
"packages/coding-agent/src/core/provider-attribution.ts": ("Provider 归因头管理，为 LLM 请求添加 session 追踪和遥测归因 HTTP 头。", ["provider","http-headers","attribution","telemetry"], "moderate", None),
"packages/coding-agent/src/core/provider-composer.ts": ("Provider 组合器，将基础配置、模型 JSON、扩展覆盖和认证信息组合成完整的 provider 模型定义。", ["provider","composer","config","auth"], "complex", None),
"packages/coding-agent/src/core/radius.ts": ("Radius provider 的重新导出模块，从远程 catalog 加载 Radius 模型配置。", ["barrel","radius","re-export"], "simple", None),
"packages/coding-agent/src/core/resolve-config-value.ts": ("配置值解析器，支持从环境变量、shell 命令和字面量解析配置值，带缓存和模板插值功能。", ["config","resolver","shell","env-var"], "complex", None),
"packages/coding-agent/src/core/resource-loader.ts": ("资源加载器核心，统一发现和加载扩展、skills、prompts、themes 和 context 文件，处理冲突检测和信任管理。", ["resource-loader","extensions","skills","themes","core"], "complex", "902 行的 DefaultResourceLoader 类管理所有运行时资源的发现、加载和冲突检测。"),
"packages/coding-agent/src/core/runtime-credentials.ts": ("运行时凭据管理器，在 auth storage 之上提供 API key 运行时覆盖，支持临时凭据注入。", ["auth","credentials","runtime"], "simple", None),
"packages/coding-agent/src/core/sdk.ts": ("SDK 入口模块，导出 createAgentSession 和所有公开工具创建函数，是外部集成的主要 API 表面。", ["sdk","entry-point","api","barrel"], "complex", "大量 re-exports 组成 SDK 公开 API，createAgentSession 是核心工厂函数。"),
"packages/coding-agent/src/core/session-cwd.ts": ("会话工作目录管理，检测和格式化会话 CWD 缺失错误，提供恢复提示。", ["session","cwd","error-handling"], "simple", None),
"packages/coding-agent/src/core/session-manager.ts": ("会话管理器核心，处理会话的创建、持久化、分支、上下文构建和历史迁移，支持树形会话结构。", ["session","persistence","manager","core"], "complex", "1714 行的会话管理核心，SessionManager 类有 45 个方法，支持树形分支和版本迁移。"),
"packages/coding-agent/src/core/settings-manager.ts": ("设置管理器核心，处理全局和项目级设置的加载、持久化、迁移和版本控制，管理 100+ 配置项。", ["settings","config","persistence","manager","core"], "complex", "1290 行，SettingsManager 类有 137 个方法，覆盖所有配置项的 getter/setter。"),
"packages/coding-agent/src/core/skills.ts": ("Skills 加载器，从文件系统发现和加载 skill 定义，支持 frontmatter 解析、名称验证和冲突检测。", ["skills","loader","discovery"], "complex", None),
"packages/coding-agent/src/core/slash-commands.ts": ("斜杠命令加载器，从配置和扩展中收集自定义斜杠命令定义。", ["slash-commands","loader","config"], "simple", None),
"packages/coding-agent/src/core/source-info.ts": ("资源来源信息工厂，创建标记资源来源（builtin/package/extension 等）的 SourceInfo 对象。", ["source-info","factory","metadata"], "simple", None),
"packages/coding-agent/src/core/system-prompt.ts": ("系统提示词构建器，组装 agent 的系统提示词，包含 skills 列表和工具说明。", ["system-prompt","builder","agent"], "moderate", None),
"packages/coding-agent/src/core/telemetry.ts": ("遥测模块，重新导出设置管理器的遥测配置访问。", ["telemetry","barrel","re-export"], "simple", None),
"packages/coding-agent/src/core/timings.ts": ("性能计时工具，提供带命名空间的计时函数和分组打印功能。", ["performance","timing","utility"], "simple", None),
"packages/coding-agent/src/core/tools/bash.ts": ("Bash 工具实现，创建 shell 命令执行工具定义，支持超时、输出截断和结果渲染。", ["tool","bash","shell","command-execution"], "complex", None),
"packages/coding-agent/src/core/tools/edit-diff.ts": ("编辑差异计算模块，提供 fuzzy 匹配、行尾规范化、统一 diff 生成和编辑应用功能。", ["tool","diff","fuzzy-match","edit"], "complex", None),
"packages/coding-agent/src/core/tools/edit.ts": ("编辑工具实现，创建文件编辑工具定义，支持多编辑操作、diff 预览渲染和文件变更队列。", ["tool","edit","file-mutation","diff"], "complex", None),
}
print("File metadata loaded:", len(file_meta))
