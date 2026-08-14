import json

nodes = []
edges = []

# ============================================================
# SOURCE UTILITY FILES
# ============================================================

# --- paths.ts ---
nodes.append({
    "id": "file:packages/coding-agent/src/utils/paths.ts",
    "type": "file",
    "name": "paths.ts",
    "filePath": "packages/coding-agent/src/utils/paths.ts",
    "summary": "提供路径规范化、解析、相对路径转换及云同步标记等路径处理工具函数，被整个 coding-agent 项目广泛复用。",
    "tags": ["utility", "path", "filesystem", "normalization"],
    "complexity": "moderate",
    "languageNotes": "使用 realpathSync 实现 symlink 解析并容错降级，支持 Unicode 空格归一化和 Windows 路径转换。"
})

path_fns = [
    ("isLocalPath", 50, 64, "判断字符串是否为本地文件路径，支持 ~ 开头和相对路径前缀检测。", ["utility", "path", "validation"]),
    ("normalizePath", 75, 100, "对输入路径进行 trim、tilde 展开、Unicode 空格归一化及 Windows 路径格式转换。", ["utility", "path", "normalization"]),
    ("getCwdRelativePath", 108, 117, "将文件路径转换为相对于当前工作目录的相对路径表示。", ["utility", "path", "relative"]),
    ("markPathIgnoredByCloudSync", 124, 139, "通过设置扩展属性标记文件使其被 iCloud Drive 等云同步服务忽略。", ["utility", "cloud-sync", "filesystem"]),
]
for name, s, e, summary, tags in path_fns:
    nodes.append({
        "id": f"function:packages/coding-agent/src/utils/paths.ts:{name}",
        "type": "function",
        "name": name,
        "filePath": "packages/coding-agent/src/utils/paths.ts",
        "lineRange": [s, e],
        "summary": summary,
        "tags": tags,
        "complexity": "simple"
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/paths.ts",
        "target": f"function:packages/coding-agent/src/utils/paths.ts:{name}",
        "type": "contains",
        "direction": "forward",
        "weight": 1.0
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/paths.ts",
        "target": f"function:packages/coding-agent/src/utils/paths.ts:{name}",
        "type": "exports",
        "direction": "forward",
        "weight": 0.8
    })

# --- shell.ts ---
nodes.append({
    "id": "file:packages/coding-agent/src/utils/shell.ts",
    "type": "file",
    "name": "shell.ts",
    "filePath": "packages/coding-agent/src/utils/shell.ts",
    "summary": "提供 shell 环境配置、bash 路径查找、二进制输出清理及进程树终止等 shell 相关工具函数。",
    "tags": ["utility", "shell", "process-management", "environment"],
    "complexity": "moderate",
    "languageNotes": "跨平台支持 WSL bash 路径检测和 PATH 上的 bash 查找，使用 detached child PID 追踪机制管理进程。"
})

shell_fns = [
    ("findBashOnPath", 24, 58, "在 PATH 中查找可用的 bash 可执行文件路径，支持 Windows WSL 和原生 bash 检测。", ["utility", "shell", "bash", "detection"]),
    ("getShellConfig", 67, 120, "根据自定义 shell 路径或系统环境返回 shell 配置对象，包含 shell 路径和参数。", ["utility", "shell", "config"]),
    ("sanitizeBinaryOutput", 144, 174, "清理 shell 命令输出中的二进制字符和无效 UTF-8 序列，确保输出可安全渲染。", ["utility", "shell", "sanitization"]),
    ("killProcessTree", 200, 225, "递归终止指定 PID 及其所有子进程，支持跨平台进程树清理。", ["utility", "process-management", "kill"]),
]
for name, s, e, summary, tags in shell_fns:
    nodes.append({
        "id": f"function:packages/coding-agent/src/utils/shell.ts:{name}",
        "type": "function",
        "name": name,
        "filePath": "packages/coding-agent/src/utils/shell.ts",
        "lineRange": [s, e],
        "summary": summary,
        "tags": tags,
        "complexity": "moderate" if name in ("getShellConfig", "sanitizeBinaryOutput") else "simple"
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/shell.ts",
        "target": f"function:packages/coding-agent/src/utils/shell.ts:{name}",
        "type": "contains",
        "direction": "forward",
        "weight": 1.0
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/shell.ts",
        "target": f"function:packages/coding-agent/src/utils/shell.ts:{name}",
        "type": "exports",
        "direction": "forward",
        "weight": 0.8
    })

# --- sleep.ts ---
nodes.append({
    "id": "file:packages/coding-agent/src/utils/sleep.ts",
    "type": "file",
    "name": "sleep.ts",
    "filePath": "packages/coding-agent/src/utils/sleep.ts",
    "summary": "提供可中断的 Promise 延时工具函数，支持 AbortSignal 取消。",
    "tags": ["utility", "sleep", "async", "abort-signal"],
    "complexity": "simple"
})

# --- tools-manager.ts ---
nodes.append({
    "id": "file:packages/coding-agent/src/utils/tools-manager.ts",
    "type": "file",
    "name": "tools-manager.ts",
    "filePath": "packages/coding-agent/src/utils/tools-manager.ts",
    "summary": "管理外部工具的二进制下载、版本检查、解压安装及路径解析，支持 GitHub release 资产自动获取。",
    "tags": ["utility", "tools", "download", "binary-management"],
    "complexity": "complex",
    "languageNotes": "支持 tar.gz 和 zip 格式解压，离线模式检测，以及通过 GitHub API 获取最新版本号。"
})

tm_fns = [
    ("getToolPath", 86, 105, "获取指定工具的本地安装路径，按平台选择正确的二进制文件名。", ["utility", "tools", "path"]),
    ("getLatestVersion", 108, 123, "通过 GitHub API 获取指定仓库的最新 release 版本号。", ["utility", "tools", "version", "github-api"]),
    ("findBinaryRecursively", 141, 161, "递归搜索目录树查找指定二进制文件，使用迭代栈避免递归溢出。", ["utility", "tools", "search"]),
    ("extractZipArchive", 204, 240, "解压 zip 格式归档文件到指定目录，处理平台差异和错误情况。", ["utility", "tools", "zip", "extraction"]),
    ("downloadTool", 243, 318, "下载指定工具的二进制文件，包括版本检查、资产选择、下载和解压的完整流程。", ["utility", "tools", "download", "installation"]),
    ("ensureTool", 328, 371, "确保指定工具已安装并可用，若不存在则自动下载安装。", ["utility", "tools", "ensure", "installation"]),
]
for name, s, e, summary, tags in tm_fns:
    nodes.append({
        "id": f"function:packages/coding-agent/src/utils/tools-manager.ts:{name}",
        "type": "function",
        "name": name,
        "filePath": "packages/coding-agent/src/utils/tools-manager.ts",
        "lineRange": [s, e],
        "summary": summary,
        "tags": tags,
        "complexity": "complex" if name in ("downloadTool", "ensureTool") else "moderate"
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/tools-manager.ts",
        "target": f"function:packages/coding-agent/src/utils/tools-manager.ts:{name}",
        "type": "contains",
        "direction": "forward",
        "weight": 1.0
    })
    if name in ("getToolPath", "ensureTool"):
        edges.append({
            "source": "file:packages/coding-agent/src/utils/tools-manager.ts",
            "target": f"function:packages/coding-agent/src/utils/tools-manager.ts:{name}",
            "type": "exports",
            "direction": "forward",
            "weight": 0.8
        })

# --- windows-self-update.ts ---
nodes.append({
    "id": "file:packages/coding-agent/src/utils/windows-self-update.ts",
    "type": "file",
    "name": "windows-self-update.ts",
    "filePath": "packages/coding-agent/src/utils/windows-self-update.ts",
    "summary": "处理 Windows 平台自更新时的原生依赖隔离与清理，通过隔离机制避免文件锁定问题。",
    "tags": ["utility", "windows", "self-update", "quarantine"],
    "complexity": "moderate",
    "languageNotes": "利用 process.report.getReport 获取已加载共享对象列表，实现 native 依赖的隔离与清理。"
})

wsu_fns = [
    ("getLoadedSharedObjectsInPackageDir", 26, 48, "获取当前进程中加载的、属于指定包目录的共享对象文件列表。", ["utility", "windows", "shared-objects"]),
    ("quarantineWindowsNativeDependencies", 62, 84, "将 Windows 原生依赖文件隔离到临时目录，为自更新操作做准备。", ["utility", "windows", "quarantine", "self-update"]),
]
for name, s, e, summary, tags in wsu_fns:
    nodes.append({
        "id": f"function:packages/coding-agent/src/utils/windows-self-update.ts:{name}",
        "type": "function",
        "name": name,
        "filePath": "packages/coding-agent/src/utils/windows-self-update.ts",
        "lineRange": [s, e],
        "summary": summary,
        "tags": tags,
        "complexity": "moderate"
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/windows-self-update.ts",
        "target": f"function:packages/coding-agent/src/utils/windows-self-update.ts:{name}",
        "type": "contains",
        "direction": "forward",
        "weight": 1.0
    })
    edges.append({
        "source": "file:packages/coding-agent/src/utils/windows-self-update.ts",
        "target": f"function:packages/coding-agent/src/utils/windows-self-update.ts:{name}",
        "type": "exports",
        "direction": "forward",
        "weight": 0.8
    })

# ============================================================
# TEST FILES
# ============================================================

test_files = [
    ("packages/coding-agent/test/agent-session-auto-compaction-queue.test.ts", 449, 398,
     "测试 agent session 的自动压缩队列行为，验证上下文窗口满时的触发逻辑和排队机制。",
     ["test", "agent-session", "compaction", "queue"]),
    ("packages/coding-agent/test/agent-session-branching.test.ts", 156, 132,
     "测试 agent session 的分支功能，验证对话分支创建和管理逻辑。",
     ["test", "agent-session", "branching"]),
    ("packages/coding-agent/test/agent-session-compaction.test.ts", 209, 167,
     "测试 agent session 的上下文压缩功能，验证压缩触发条件和消息截断行为。",
     ["test", "agent-session", "compaction"]),
    ("packages/coding-agent/test/agent-session-concurrent.test.ts", 629, 566,
     "测试 agent session 的并发行为，验证多请求同时处理时的正确性和资源竞争处理。",
     ["test", "agent-session", "concurrent"]),
    ("packages/coding-agent/test/agent-session-dynamic-provider.test.ts", 179, 153,
     "测试 agent session 的动态 provider 切换功能，验证运行时更换 LLM provider 的行为。",
     ["test", "agent-session", "dynamic-provider"]),
    ("packages/coding-agent/test/agent-session-dynamic-tools.test.ts", 256, 230,
     "测试 agent session 的动态工具加载功能，验证运行时添加和移除工具的行为。",
     ["test", "agent-session", "dynamic-tools"]),
    ("packages/coding-agent/test/agent-session-retry.test.ts", 322, 288,
     "测试 agent session 的重试机制，验证 API 失败后的自动重试和退避策略。",
     ["test", "agent-session", "retry"]),
    ("packages/coding-agent/test/agent-session-runtime-events.test.ts", 257, 229,
     "测试 agent session 运行时事件系统，验证事件触发顺序和事件处理器注册机制。",
     ["test", "agent-session", "runtime-events"]),
    ("packages/coding-agent/test/agent-session-stats.test.ts", 283, 252,
     "测试 agent session 的统计信息收集功能，验证 token 用量和会话指标计算。",
     ["test", "agent-session", "stats"]),
    ("packages/coding-agent/test/agent-session-tree-navigation.test.ts", 323, 246,
     "测试 agent session 的对话树导航功能，验证分支树遍历和历史回溯逻辑。",
     ["test", "agent-session", "tree-navigation"]),
    ("packages/coding-agent/test/args.test.ts", 480, 402,
     "测试 CLI 参数解析逻辑，验证各种命令行参数组合的解析和验证行为。",
     ["test", "cli", "args", "parsing"]),
    ("packages/coding-agent/test/auth-check.test.ts", 171, 148,
     "测试认证检查功能，验证 API key 验证和认证状态检测逻辑。",
     ["test", "auth", "authentication"]),
    ("packages/coding-agent/test/auth-storage.test.ts", 535, 482,
     "测试认证存储模块，验证凭证的持久化、读取和多种存储后端的行为。",
     ["test", "auth", "storage"]),
    ("packages/coding-agent/test/bash-close-hang-windows.test.ts", 126, 110,
     "测试 Windows 平台 bash 进程关闭挂起问题，验证进程清理和超时处理。",
     ["test", "bash", "windows", "process-cleanup"]),
    ("packages/coding-agent/test/block-images.test.ts", 148, 119,
     "测试图片阻止功能，验证文件处理器对内嵌图片的过滤和阻止行为。",
     ["test", "images", "file-processor", "filtering"]),
    ("packages/coding-agent/test/cache-stats.test.ts", 143, 128,
     "测试缓存统计功能，验证缓存命中率和使用量统计的准确性。",
     ["test", "cache", "stats"]),
    ("packages/coding-agent/test/compaction-extensions-example.test.ts", 152, 136,
     "测试扩展系统的压缩示例，验证扩展在上下文压缩时的行为。",
     ["test", "compaction", "extensions"]),
    ("packages/coding-agent/test/compaction-extensions.test.ts", 416, 348,
     "测试扩展系统的压缩功能，验证扩展与上下文压缩机制的交互行为。",
     ["test", "compaction", "extensions"]),
    ("packages/coding-agent/test/config-value-migration.test.ts", 178, 162,
     "测试配置值迁移逻辑，验证旧配置格式到新格式的自动迁移行为。",
     ["test", "config", "migration"]),
    ("packages/coding-agent/test/config.test.ts", 437, 386,
     "测试配置模块，验证安装方式检测、路径解析和包管理器识别逻辑。",
     ["test", "config", "installation"]),
    ("packages/coding-agent/test/credential-print.test.ts", 130, 120,
     "测试凭证打印功能，验证 CLI 中凭证显示和格式化逻辑。",
     ["test", "credential", "cli"]),
    ("packages/coding-agent/test/default-tools-setting.test.ts", 150, 135,
     "测试默认工具设置功能，验证工具配置加载和默认工具集合的初始化。",
     ["test", "tools", "default-settings"]),
    ("packages/coding-agent/test/edit-tool-legacy-input.test.ts", 116, 103,
     "测试编辑工具的旧版输入格式兼容性，验证遗留输入格式的解析和处理。",
     ["test", "edit-tool", "legacy", "compatibility"]),
    ("packages/coding-agent/test/edit-tool-no-full-redraw.test.ts", 235, 210,
     "测试编辑工具的增量渲染功能，验证大文件编辑时避免全量重绘的优化行为。",
     ["test", "edit-tool", "rendering", "optimization"]),
    ("packages/coding-agent/test/experimental-tool-strict-mode.test.ts", 38, 33,
     "测试实验性工具的严格模式，验证严格模式下工具行为的约束。",
     ["test", "experimental", "tools", "strict-mode"]),
    ("packages/coding-agent/test/experimental.test.ts", 44, 32,
     "测试实验性功能开关模块，验证功能标志的读取和启用逻辑。",
     ["test", "experimental", "feature-flags"]),
    ("packages/coding-agent/test/extensions-discovery.test.ts", 532, 432,
     "测试扩展发现机制，验证扩展加载器的目录扫描、缓存和错误处理行为。",
     ["test", "extensions", "discovery", "loader"]),
    ("packages/coding-agent/test/extensions-input-event.test.ts", 125, 111,
     "测试扩展输入事件处理，验证扩展运行时对用户输入事件的响应机制。",
     ["test", "extensions", "input-event", "runner"]),
]

for path, lines, nonempty, summary, tags in test_files:
    fname = path.split("/")[-1]
    complexity = "simple" if nonempty < 50 else ("moderate" if nonempty < 200 else "complex")
    nodes.append({
        "id": f"file:{path}",
        "type": "file",
        "name": fname,
        "filePath": path,
        "summary": summary,
        "tags": tags,
        "complexity": complexity
    })

# ============================================================
# IMPORT EDGES (1:1 for every batchImportData entry)
# ============================================================

import_data = {
    "packages/coding-agent/src/utils/paths.ts": ["packages/coding-agent/src/utils/child-process.ts"],
    "packages/coding-agent/src/utils/shell.ts": ["packages/coding-agent/src/config.ts"],
    "packages/coding-agent/src/utils/sleep.ts": [],
    "packages/coding-agent/src/utils/tools-manager.ts": ["packages/coding-agent/src/config.ts", "packages/coding-agent/src/utils/management-http.ts"],
    "packages/coding-agent/src/utils/windows-self-update.ts": ["packages/coding-agent/src/utils/paths.ts"],
    "packages/coding-agent/test/agent-session-auto-compaction-queue.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-branching.test.ts": ["packages/coding-agent/src/core/agent-session-runtime.ts", "packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-compaction.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/index.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-concurrent.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/core/system-prompt.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-dynamic-provider.test.ts": ["packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/model-runtime.ts", "packages/coding-agent/src/core/resource-loader.ts", "packages/coding-agent/src/core/sdk.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts"],
    "packages/coding-agent/test/agent-session-dynamic-tools.test.ts": ["packages/coding-agent/src/core/resource-loader.ts", "packages/coding-agent/src/core/sdk.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/core/tools/bash.ts"],
    "packages/coding-agent/test/agent-session-retry.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-runtime-events.test.ts": ["packages/coding-agent/src/core/agent-session-runtime.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/model-runtime.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/index.ts"],
    "packages/coding-agent/test/agent-session-stats.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/core/usage-totals.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/agent-session-tree-navigation.test.ts": ["packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/args.test.ts": ["packages/coding-agent/src/cli/args.ts"],
    "packages/coding-agent/test/auth-check.test.ts": ["packages/coding-agent/src/cli/args.ts", "packages/coding-agent/src/cli/auth-check.ts", "packages/coding-agent/src/cli/auth-command.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/model-runtime.ts"],
    "packages/coding-agent/test/auth-storage.test.ts": ["packages/coding-agent/src/core/auth-storage.ts"],
    "packages/coding-agent/test/bash-close-hang-windows.test.ts": ["packages/coding-agent/src/core/bash-executor.ts", "packages/coding-agent/src/core/tools/bash.ts"],
    "packages/coding-agent/test/block-images.test.ts": ["packages/coding-agent/src/cli/file-processor.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/core/tools/read.ts"],
    "packages/coding-agent/test/cache-stats.test.ts": ["packages/coding-agent/src/core/cache-stats.ts", "packages/coding-agent/src/core/session-manager.ts"],
    "packages/coding-agent/test/compaction-extensions-example.test.ts": ["packages/coding-agent/src/core/extensions/index.ts"],
    "packages/coding-agent/test/compaction-extensions.test.ts": ["packages/coding-agent/src/core/agent-session.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/extensions/index.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts", "packages/coding-agent/src/core/source-info.ts", "packages/coding-agent/src/index.ts", "packages/coding-agent/test/model-runtime-test-utils.ts", "packages/coding-agent/test/utilities.ts"],
    "packages/coding-agent/test/config-value-migration.test.ts": ["packages/coding-agent/src/config.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/migrations.ts", "packages/coding-agent/test/model-runtime-test-utils.ts"],
    "packages/coding-agent/test/config.test.ts": ["packages/coding-agent/src/config.ts"],
    "packages/coding-agent/test/credential-print.test.ts": ["packages/coding-agent/src/cli/args.ts", "packages/coding-agent/src/cli/auth-command.ts", "packages/coding-agent/src/cli/credential-print.ts", "packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/model-runtime.ts", "packages/coding-agent/src/main.ts"],
    "packages/coding-agent/test/default-tools-setting.test.ts": ["packages/coding-agent/src/core/agent-session-services.ts", "packages/coding-agent/src/core/resource-loader.ts", "packages/coding-agent/src/core/sdk.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/src/core/settings-manager.ts"],
    "packages/coding-agent/test/edit-tool-legacy-input.test.ts": ["packages/coding-agent/src/core/extensions/types.ts", "packages/coding-agent/src/core/tools/edit.ts"],
    "packages/coding-agent/test/edit-tool-no-full-redraw.test.ts": ["packages/coding-agent/src/core/tools/edit-diff.ts", "packages/coding-agent/src/core/tools/edit.ts", "packages/coding-agent/src/modes/interactive/components/tool-execution.ts", "packages/coding-agent/src/modes/interactive/theme/theme.ts"],
    "packages/coding-agent/test/experimental-tool-strict-mode.test.ts": ["packages/coding-agent/src/core/tools/index.ts"],
    "packages/coding-agent/test/experimental.test.ts": ["packages/coding-agent/src/core/experimental.ts"],
    "packages/coding-agent/test/extensions-discovery.test.ts": ["packages/coding-agent/src/core/extensions/loader.ts"],
    "packages/coding-agent/test/extensions-input-event.test.ts": ["packages/coding-agent/src/core/auth-storage.ts", "packages/coding-agent/src/core/extensions/loader.ts", "packages/coding-agent/src/core/extensions/runner.ts", "packages/coding-agent/src/core/session-manager.ts", "packages/coding-agent/test/model-runtime-test-utils.ts"],
}

for src, targets in import_data.items():
    for tgt in targets:
        edges.append({
            "source": f"file:{src}",
            "target": f"file:{tgt}",
            "type": "imports",
            "direction": "forward",
            "weight": 0.7
        })

# ============================================================
# TESTED_BY EDGES (test -> production file it tests)
# ============================================================

tested_by_map = {
    "packages/coding-agent/test/agent-session-auto-compaction-queue.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-branching.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-compaction.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-concurrent.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-dynamic-provider.test.ts": "packages/coding-agent/src/core/model-runtime.ts",
    "packages/coding-agent/test/agent-session-dynamic-tools.test.ts": "packages/coding-agent/src/core/sdk.ts",
    "packages/coding-agent/test/agent-session-retry.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-runtime-events.test.ts": "packages/coding-agent/src/core/agent-session-runtime.ts",
    "packages/coding-agent/test/agent-session-stats.test.ts": "packages/coding-agent/src/core/agent-session.ts",
    "packages/coding-agent/test/agent-session-tree-navigation.test.ts": "packages/coding-agent/test/utilities.ts",
    "packages/coding-agent/test/args.test.ts": "packages/coding-agent/src/cli/args.ts",
    "packages/coding-agent/test/auth-check.test.ts": "packages/coding-agent/src/cli/auth-check.ts",
    "packages/coding-agent/test/auth-storage.test.ts": "packages/coding-agent/src/core/auth-storage.ts",
    "packages/coding-agent/test/bash-close-hang-windows.test.ts": "packages/coding-agent/src/core/tools/bash.ts",
    "packages/coding-agent/test/block-images.test.ts": "packages/coding-agent/src/cli/file-processor.ts",
    "packages/coding-agent/test/cache-stats.test.ts": "packages/coding-agent/src/core/cache-stats.ts",
    "packages/coding-agent/test/compaction-extensions-example.test.ts": "packages/coding-agent/src/core/extensions/index.ts",
    "packages/coding-agent/test/compaction-extensions.test.ts": "packages/coding-agent/src/core/extensions/index.ts",
    "packages/coding-agent/test/config-value-migration.test.ts": "packages/coding-agent/src/migrations.ts",
    "packages/coding-agent/test/config.test.ts": "packages/coding-agent/src/config.ts",
    "packages/coding-agent/test/credential-print.test.ts": "packages/coding-agent/src/cli/credential-print.ts",
    "packages/coding-agent/test/default-tools-setting.test.ts": "packages/coding-agent/src/core/sdk.ts",
    "packages/coding-agent/test/edit-tool-legacy-input.test.ts": "packages/coding-agent/src/core/tools/edit.ts",
    "packages/coding-agent/test/edit-tool-no-full-redraw.test.ts": "packages/coding-agent/src/core/tools/edit.ts",
    "packages/coding-agent/test/experimental-tool-strict-mode.test.ts": "packages/coding-agent/src/core/tools/index.ts",
    "packages/coding-agent/test/experimental.test.ts": "packages/coding-agent/src/core/experimental.ts",
    "packages/coding-agent/test/extensions-discovery.test.ts": "packages/coding-agent/src/core/extensions/loader.ts",
    "packages/coding-agent/test/extensions-input-event.test.ts": "packages/coding-agent/src/core/extensions/runner.ts",
}

for test_file, prod_file in tested_by_map.items():
    edges.append({
        "source": f"file:{prod_file}",
        "target": f"file:{test_file}",
        "type": "tested_by",
        "direction": "forward",
        "weight": 0.5
    })

# ============================================================
# DEPENDS_ON: windows-self-update -> paths (uses getCwdRelativePath)
# ============================================================
edges.append({
    "source": "file:packages/coding-agent/src/utils/windows-self-update.ts",
    "target": "file:packages/coding-agent/src/utils/paths.ts",
    "type": "depends_on",
    "direction": "forward",
    "weight": 0.6
})

output = {"nodes": nodes, "edges": edges}

with open("/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-16.json", "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Nodes: {len(nodes)}")
print(f"Edges: {len(edges)}")
print(f"Import edges: {sum(len(v) for v in import_data.values())}")

# Verify import edge count
import_edge_count = sum(1 for e in edges if e["type"] == "imports")
print(f"Actual import edges: {import_edge_count}")
