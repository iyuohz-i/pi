import json, os, math

fid = lambda p: f"file:{p}"
fnid = lambda p, n: f"function:{p}:{n}"
cid = lambda p, n: f"class:{p}:{n}"

with open('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-analyzer-input-1.json') as f:
    batchImportData = json.load(f)['batchImportData']

nodes = []
edges = []

def add_file(path, summary, tags, complexity, language_notes=None):
    name = path.split('/')[-1]
    node = {"id": fid(path), "type": "file", "name": name, "filePath": path, "summary": summary, "tags": tags, "complexity": complexity}
    if language_notes:
        node["languageNotes"] = language_notes
    nodes.append(node)

def add_fn(path, name, start, end, summary, tags, complexity, exported=False):
    nodes.append({"id": fnid(path, name), "type": "function", "name": name, "filePath": path, "lineRange": [start, end], "summary": summary, "tags": tags, "complexity": complexity})
    edges.append({"source": fid(path), "target": fnid(path, name), "type": "contains", "direction": "forward", "weight": 1.0})
    if exported:
        edges.append({"source": fid(path), "target": fnid(path, name), "type": "exports", "direction": "forward", "weight": 0.8})

def add_cls(path, name, start, end, summary, tags, complexity, exported=False):
    nodes.append({"id": cid(path, name), "type": "class", "name": name, "filePath": path, "lineRange": [start, end], "summary": summary, "tags": tags, "complexity": complexity})
    edges.append({"source": fid(path), "target": cid(path, name), "type": "contains", "direction": "forward", "weight": 1.0})
    if exported:
        edges.append({"source": fid(path), "target": cid(path, name), "type": "exports", "direction": "forward", "weight": 0.8})

def add_imports(path):
    for imp in batchImportData.get(path, []):
        if imp == path:
            continue
        edges.append({"source": fid(path), "target": fid(imp), "type": "imports", "direction": "forward", "weight": 0.7})

def add_edge(src, tgt, etype, weight):
    if src == tgt:
        return
    edges.append({"source": src, "target": tgt, "type": etype, "direction": "forward", "weight": weight})

# ============ FILE 1: generate-telemetry-docs.ts ============
p = "packages/agent/scripts/generate-telemetry-docs.ts"
add_file(p, "从遥测 schema 定义生成 Markdown 文档的脚本，渲染属性表格与父级描述。", ["script", "telemetry", "documentation", "utility"], "moderate")
add_fn(p, "renderSchema", 36, 82, "将遥测 schema 的属性定义渲染为 Markdown 表格，包含允许值、默认值和说明。", ["telemetry", "serialization", "markdown"], "moderate")
add_fn(p, "renderAgentTelemetrySchemaMarkdown", 84, 94, "渲染 agent 遥测 schema 的完整 Markdown 文档。", ["telemetry", "serialization", "markdown"], "simple", exported=True)
add_fn(p, "generateTelemetryDocs", 96, 110, "生成遥测文档并写入指定输出路径的主入口函数。", ["telemetry", "documentation", "entry-point"], "simple", exported=True)
add_imports(p)

# ============ FILE 2: agent-loop.ts ============
p = "packages/agent/src/agent-loop.ts"
add_file(p, "Agent 核心循环逻辑，管理 LLM 流式响应、工具调用执行（串行/并行）与终止条件判断。", ["agent", "core-loop", "tool-execution", "streaming"], "complex",
    "使用 async generator 实现流式 agent 循环，支持串行与并行工具调用批次。")
add_fn(p, "agentLoop", 31, 54, "创建 agent 循环的 async generator，处理用户消息并产出流式事件。", ["agent", "core-loop", "async-generator"], "moderate", exported=True)
add_fn(p, "agentLoopContinue", 64, 93, "从已有状态继续 agent 循环的 async generator 变体。", ["agent", "core-loop", "async-generator"], "moderate", exported=True)
add_fn(p, "runAgentLoop", 95, 118, "执行 agent 循环并收集所有流式事件的封装函数。", ["agent", "core-loop"], "moderate", exported=True)
add_fn(p, "runAgentLoopContinue", 120, 143, "从已有状态继续执行 agent 循环的封装函数。", ["agent", "core-loop"], "moderate", exported=True)
add_fn(p, "createAgentStream", 145, 150, "创建 agent 流式响应的工厂函数。", ["agent", "factory", "streaming"], "simple", exported=False)
add_fn(p, "runLoop", 155, 275, "Agent 循环的核心实现，迭代 LLM 响应与工具调用直到终止。", ["agent", "core-loop", "tool-execution"], "complex")
add_fn(p, "streamAssistantResponse", 281, 372, "流式处理 LLM 助手响应，解析流块并产出事件。", ["agent", "streaming", "llm"], "complex")
add_fn(p, "failToolCallsFromTruncatedMessage", 381, 406, "处理因消息截断导致的工具调用失败，生成错误结果。", ["agent", "tool-execution", "error-handling"], "moderate")
add_fn(p, "executeToolCalls", 411, 426, "执行工具调用批次，根据配置选择串行或并行模式。", ["agent", "tool-execution"], "simple")
add_fn(p, "executeToolCallsSequential", 433, 487, "串行执行工具调用，每个工具完成后才执行下一个。", ["agent", "tool-execution", "sequential"], "moderate")
add_fn(p, "executeToolCallsParallel", 489, 554, "并行执行工具调用，所有工具同时运行后收集结果。", ["agent", "tool-execution", "parallel"], "moderate")
add_fn(p, "prepareToolCallArguments", 586, 598, "准备工具调用的参数解析与验证。", ["agent", "tool-execution", "validation"], "simple")
add_fn(p, "prepareToolCall", 600, 668, "准备单个工具调用，包括参数解析、权限检查与执行环境设置。", ["agent", "tool-execution", "validation"], "moderate")
add_fn(p, "executePreparedToolCall", 670, 711, "执行已准备好的工具调用并处理结果。", ["agent", "tool-execution"], "moderate")
add_fn(p, "finalizeExecutedToolCall", 713, 758, "完成工具调用后处理，包括结果格式化与遥测记录。", ["agent", "tool-execution", "telemetry"], "moderate")
add_fn(p, "createToolResultMessage", 777, 791, "从工具执行结果创建消息对象。", ["agent", "tool-execution", "message"], "simple")
add_imports(p)

# ============ FILE 3: agent.ts ============
p = "packages/agent/src/agent.ts"
add_file(p, "Agent 类的核心实现，管理 agent 状态、消息队列、工具注册与对话循环入口。", ["agent", "core", "state-management"], "complex",
    "Agent 类持有 PendingMessageQueue 和可变状态，协调 LLM 调用与工具执行。")
add_fn(p, "createMutableAgentState", 68, 95, "创建 agent 的可变内部状态对象。", ["agent", "state-management", "factory"], "moderate")
add_cls(p, "PendingMessageQueue", 125, 159, "待处理消息队列，管理排队模式与消息优先级。", ["agent", "queue", "state-management"], "moderate")
add_cls(p, "Agent", 173, 592, "Agent 核心类，管理对话循环、工具调用、状态转换与消息处理。", ["agent", "core", "state-management", "tool-execution"], "complex", exported=True)
add_imports(p)

# ============ FILE 4: agent-harness.ts ============
p = "packages/agent/src/harness/agent-harness.ts"
add_file(p, "AgentHarness 类及其错误类型定义，作为 agent 运行时的协调层管理 session、compaction 与工具注册。", ["harness", "orchestration", "error-handling"], "complex",
    "AgentHarness 使用 Result 类型模式管理错误，包含多种领域特定错误类。")
add_cls(p, "HarnessFault", 57, 65, "Harness 运行时的严重错误，表示不可恢复的故障。", ["error-handling", "harness"], "simple")
add_cls(p, "HarnessClosed", 67, 72, "Harness 已关闭时抛出的错误。", ["error-handling", "harness"], "simple")
add_cls(p, "HarnessNotImplemented", 74, 82, "Harness 功能未实现时抛出的错误。", ["error-handling", "harness"], "simple")
add_cls(p, "UnavailableRegistry", 219, 235, "注册表不可用时抛出的错误，包含缺失组件信息。", ["error-handling", "registry"], "simple")
add_cls(p, "AgentHarness", 305, 508, "Agent 运行时 Harness 类，协调 session 管理、compaction、工具注册与执行生命周期。", ["harness", "orchestration", "session-management", "tool-execution"], "complex", exported=True)
add_imports(p)

# ============ FILE 5: branch-summarization.ts ============
p = "packages/agent/src/harness/compaction/branch-summarization.ts"
add_file(p, "分支摘要生成模块，收集对话分支条目并通过 LLM 生成摘要消息。", ["compaction", "branch-summary", "llm"], "complex")
add_fn(p, "collectEntriesForBranchSummary", 82, 111, "收集用于生成分支摘要的对话条目。", ["compaction", "branch-summary"], "moderate", exported=True)
add_fn(p, "getMessageFromEntry", 112, 129, "从会话条目中提取消息内容。", ["compaction", "message"], "simple", exported=False)
add_fn(p, "prepareBranchEntries", 132, 171, "准备分支摘要所需的条目列表，包括文件操作提取与格式化。", ["compaction", "branch-summary", "preparation"], "moderate", exported=True)
add_fn(p, "generateBranchSummary", 208, 280, "通过 LLM 生成分支摘要消息，包含重试逻辑与错误处理。", ["compaction", "branch-summary", "llm"], "complex", exported=True)
add_imports(p)

# ============ FILE 6: compaction.ts ============
p = "packages/agent/src/harness/compaction/compaction.ts"
add_file(p, "对话压缩核心模块，包含 token 估算、上下文窗口管理、摘要生成与压缩执行逻辑。", ["compaction", "token-estimation", "context-management", "llm"], "complex",
    "实现多策略 token 估算与对话切割点检测，支持 LLM 摘要压缩。")
add_fn(p, "extractFileOperations", 44, 67, "从对话消息中提取文件操作记录。", ["compaction", "file-operations"], "moderate")
add_fn(p, "completeSimpleWithRetries", 102, 122, "带重试的简单 LLM 补全请求封装。", ["compaction", "llm", "retry"], "moderate", exported=True)
add_fn(p, "combineUsage", 124, 145, "合并多次 LLM 调用的 token 使用量。", ["compaction", "usage-tracking"], "moderate")
add_fn(p, "getAssistantUsage", 168, 181, "获取 assistant 消息的 token 使用量信息。", ["compaction", "usage-tracking"], "simple", exported=True)
add_fn(p, "getLastAssistantUsage", 184, 193, "获取对话中最后一条 assistant 消息的 token 使用量。", ["compaction", "usage-tracking"], "simple", exported=True)
add_fn(p, "estimateContextTokens", 216, 244, "估算当前对话上下文的 token 数量。", ["compaction", "token-estimation"], "moderate", exported=True)
add_fn(p, "estimateTokens", 271, 311, "估算文本与图片内容的 token 数量，支持多种估算策略。", ["compaction", "token-estimation"], "moderate", exported=True)
add_fn(p, "findValidCutPoints", 312, 344, "查找对话中有效的压缩切割点。", ["compaction", "context-management"], "moderate")
add_fn(p, "findTurnStartIndex", 347, 361, "查找对话轮次的起始索引。", ["compaction", "context-management"], "simple", exported=True)
add_fn(p, "findCutPoint", 374, 422, "根据 token 限制查找最佳压缩切割点。", ["compaction", "context-management"], "moderate", exported=True)
add_fn(p, "generateSummary", 501, 526, "通过 LLM 生成对话摘要。", ["compaction", "llm", "summarization"], "moderate", exported=True)
add_fn(p, "generateSummaryWithUsage", 529, 593, "生成对话摘要并返回 token 使用量信息。", ["compaction", "llm", "summarization", "usage-tracking"], "complex", exported=True)
add_fn(p, "prepareCompaction", 616, 687, "准备压缩操作，确定切割点与待摘要内容。", ["compaction", "preparation"], "complex", exported=True)
add_fn(p, "compact", 707, 794, "执行对话压缩，生成摘要并重组消息列表。", ["compaction", "core", "summarization"], "complex", exported=True)
add_fn(p, "generateTurnPrefixSummary", 795, 848, "生成对话轮次前缀摘要。", ["compaction", "summarization"], "moderate")
add_imports(p)

# ============ FILE 7: compaction/utils.ts ============
p = "packages/agent/src/harness/compaction/utils.ts"
add_file(p, "压缩模块的工具函数，包括文件操作提取、格式化与对话序列化。", ["compaction", "utility", "serialization"], "moderate")
add_fn(p, "extractFileOpsFromMessage", 24, 51, "从单条消息中提取文件操作记录。", ["compaction", "file-operations"], "moderate", exported=True)
add_fn(p, "computeFileLists", 54, 59, "计算文件操作中的文件列表。", ["compaction", "file-operations"], "simple", exported=True)
add_fn(p, "formatFileOperations", 62, 72, "格式化文件操作列表为可读字符串。", ["compaction", "formatting"], "simple", exported=True)
add_fn(p, "serializeConversation", 91, 132, "将对话条目序列化为文本格式。", ["compaction", "serialization"], "moderate", exported=True)
add_imports(p)

# ============ FILE 8: nodejs.ts ============
p = "packages/agent/src/harness/env/nodejs.ts"
add_file(p, "Node.js 执行环境实现，提供进程管理、shell 配置、文件操作与命令执行能力。", ["execution-environment", "nodejs", "process-management", "shell"], "complex",
    "NodeExecutionEnv 类封装了 child_process 管理、WSL 兼容性与 bash 路径查找。")
add_fn(p, "resolveTimeoutMs", 38, 49, "解析超时配置，支持环境变量覆盖。", ["execution-environment", "configuration"], "simple")
add_fn(p, "resolvePath", 51, 65, "解析文件路径，处理相对路径与工作目录。", ["execution-environment", "path"], "simple")
add_fn(p, "toFileError", 97, 121, "将 Node.js 错误转换为 FileError 类型。", ["execution-environment", "error-handling"], "moderate")
add_fn(p, "runCommand", 136, 169, "在 shell 中执行命令并返回结果。", ["execution-environment", "shell", "command-execution"], "moderate")
add_fn(p, "findBashOnPath", 171, 179, "在系统 PATH 中查找 bash 可执行文件。", ["execution-environment", "shell"], "simple")
add_fn(p, "getShellConfig", 196, 238, "获取 shell 配置，处理 WSL 与不同平台的兼容性。", ["execution-environment", "shell", "configuration"], "complex")
add_fn(p, "getShellEnv", 240, 251, "获取 shell 环境变量配置。", ["execution-environment", "shell", "configuration"], "simple")
add_fn(p, "killProcessTree", 253, 276, "终止进程树，包括所有子进程。", ["execution-environment", "process-management"], "moderate")
add_fn(p, "waitForChildProcess", 278, 345, "等待子进程完成，支持超时与取消。", ["execution-environment", "process-management"], "complex")
add_cls(p, "NodeExecutionEnv", 347, 695, "Node.js 执行环境类，实现文件读写、命令执行与进程管理接口。", ["execution-environment", "nodejs", "process-management"], "complex", exported=True)
add_imports(p)

# ============ FILE 9: messages.ts ============
p = "packages/agent/src/harness/messages.ts"
add_file(p, "消息构造工具模块，提供 bash 执行、分支摘要、压缩摘要等消息的创建与 LLM 格式转换。", ["message", "utility", "serialization"], "moderate")
add_fn(p, "bashExecutionToText", 63, 79, "将 bash 执行记录转换为可读文本。", ["message", "formatting", "bash"], "simple", exported=True)
add_fn(p, "createBranchSummaryMessage", 81, 92, "创建分支摘要消息。", ["message", "branch-summary"], "simple", exported=True)
add_fn(p, "createCompactionSummaryMessage", 94, 105, "创建压缩摘要消息。", ["message", "compaction"], "simple", exported=True)
add_fn(p, "createCustomMessage", 107, 122, "创建自定义类型的系统消息。", ["message", "factory"], "moderate", exported=True)
add_fn(p, "convertToLlm", 124, 168, "将内部消息格式转换为 LLM API 格式。", ["message", "serialization", "llm"], "moderate", exported=True)
add_imports(p)

# ============ FILE 10: prompt-templates.ts ============
p = "packages/agent/src/harness/prompt-templates.ts"
add_file(p, "Prompt 模板加载模块，从文件系统读取 frontmatter 格式的模板并解析参数。", ["prompt-template", "loader", "frontmatter"], "complex")
add_fn(p, "loadPromptTemplates", 30, 62, "从指定目录加载所有 prompt 模板。", ["prompt-template", "loader"], "moderate", exported=True)
add_fn(p, "loadSourcedPromptTemplates", 70, 93, "从指定源路径加载 prompt 模板。", ["prompt-template", "loader"], "moderate", exported=True)
add_fn(p, "loadTemplatesFromDir", 95, 121, "遍历目录加载模板文件。", ["prompt-template", "loader"], "moderate")
add_fn(p, "loadTemplateFromFile", 123, 166, "从单个文件加载并解析模板，包括 frontmatter 与命令参数。", ["prompt-template", "loader", "frontmatter"], "complex")
add_fn(p, "resolveKind", 168, 199, "解析模板类型，区分 prompt 与 command。", ["prompt-template", "validation"], "moderate")
add_fn(p, "parseCommandArgs", 218, 241, "解析命令模板的参数定义。", ["prompt-template", "parsing"], "moderate", exported=True)
add_fn(p, "substituteArgs", 244, 257, "替换模板中的参数占位符。", ["prompt-template", "substitution"], "simple", exported=True)
add_imports(p)

# ============ FILE 11: reducer.ts ============
p = "packages/agent/src/harness/reducer.ts"
add_file(p, "Lane 状态 reducer 模块，验证 record log 条目并派生有效的 lane 状态。", ["reducer", "state-management", "validation", "record-log"], "complex",
    "实现 record log 验证、attempt 序列校验与工具批次状态派生。")
add_cls(p, "RecordLogCorruption", 36, 44, "Record log 损坏错误，表示日志验证失败。", ["error-handling", "record-log"], "simple", exported=True)
add_fn(p, "validateRecordLog", 312, 390, "验证 record log 的完整性与一致性，检测损坏与序列错误。", ["reducer", "validation", "record-log"], "complex", exported=True)
add_fn(p, "deriveEffectiveConfiguration", 400, 427, "从 record log 派生生效的配置。", ["reducer", "configuration"], "moderate")
add_fn(p, "deriveNewestOwn", 429, 443, "派生最新的所有权信息。", ["reducer", "state-derivation"], "simple")
add_fn(p, "deriveToolBatch", 445, 503, "从 record log 条目派生工具批次状态。", ["reducer", "tool-execution", "state-derivation"], "moderate")
add_fn(p, "reduceLaneState", 506, 667, "核心 reducer 函数，从 record log 派生完整的 lane 状态。", ["reducer", "core", "state-management"], "complex", exported=True)
add_imports(p)

# ============ FILE 12: result.ts ============
p = "packages/agent/src/harness/result.ts"
add_file(p, "Result 类型实现，提供 ok/err 构造与错误匹配的函数式错误处理模式。", ["result", "error-handling", "functional"], "simple",
    "使用 TaggedError 实现类型安全的错误分类。")
add_fn(p, "TaggedError", 28, 51, "创建带标签的错误对象，支持错误分类与模式匹配。", ["error-handling", "tagged-error"], "moderate", exported=True)
add_fn(p, "matchError", 57, 63, "根据错误标签进行模式匹配。", ["error-handling", "pattern-matching"], "simple", exported=True)
add_imports(p)

# ============ FILE 13: session/context.ts ============
p = "packages/agent/src/harness/session/context.ts"
add_file(p, "会话上下文构建模块，将会话条目转换为 LLM 可用的上下文消息。", ["session", "context", "message"], "moderate")
add_fn(p, "deriveSessionContextState", 25, 43, "从会话状态派生上下文状态。", ["session", "context", "state-derivation"], "simple")
add_fn(p, "defaultContextEntryTransform", 45, 57, "默认的上下文条目转换函数。", ["session", "context", "transform"], "simple", exported=True)
add_fn(p, "buildContextEntries", 59, 63, "构建上下文条目列表。", ["session", "context"], "simple", exported=True)
add_fn(p, "sessionEntryToContextMessages", 65, 88, "将会话条目转换为上下文消息列表。", ["session", "context", "message"], "moderate", exported=True)
add_fn(p, "buildSessionContext", 90, 100, "构建完整的会话上下文。", ["session", "context"], "simple", exported=True)
add_imports(p)

# ============ FILE 14: session/index.ts ============
p = "packages/agent/src/harness/session/index.ts"
add_file(p, "Session 模块的 barrel 导出文件，重新导出 JSONL session 相关的类型与接口。", ["barrel", "session", "entry-point"], "simple")
add_imports(p)

# ============ FILE 15: session/jsonl/codec.ts ============
p = "packages/agent/src/harness/session/jsonl/codec.ts"
add_file(p, "JSONL session 编解码器，处理 header 与 mutation 的序列化/反序列化。", ["jsonl", "codec", "serialization", "session"], "complex",
    "实现 JSONL 格式的 header 编解码与多种 mutation 类型的解析。")
add_fn(p, "decodeHeader", 70, 100, "解码 JSONL 文件的 header 信息。", ["jsonl", "codec", "deserialization"], "moderate")
add_fn(p, "metadataFromHeader", 115, 129, "从 header 提取会话元数据。", ["jsonl", "codec", "metadata"], "moderate", exported=True)
add_fn(p, "parseEntryMutation", 131, 144, "解析条目 mutation 操作。", ["jsonl", "codec", "mutation"], "simple")
add_fn(p, "parseRecordMutation", 146, 170, "解析 record mutation 操作。", ["jsonl", "codec", "mutation"], "moderate")
add_fn(p, "parseLaneMutation", 172, 179, "解析 lane mutation 操作。", ["jsonl", "codec", "mutation"], "simple")
add_fn(p, "parseFactMutation", 181, 201, "解析 fact mutation 操作。", ["jsonl", "codec", "mutation"], "moderate")
add_fn(p, "decodeMutation", 203, 218, "解码 JSONL 条目的 mutation。", ["jsonl", "codec", "deserialization"], "moderate")
add_fn(p, "encodeMutation", 229, 240, "编码 mutation 为 JSONL 格式。", ["jsonl", "codec", "serialization"], "simple", exported=True)
add_imports(p)

# ============ FILE 16: session/jsonl/errors.ts ============
p = "packages/agent/src/harness/session/jsonl/errors.ts"
add_file(p, "JSONL session 的错误类型与结果辅助函数。", ["jsonl", "error-handling", "session"], "simple")
add_cls(p, "JsonlDecodeError", 4, 12, "JSONL 解码错误类，携带行号与原始内容信息。", ["error-handling", "jsonl"], "simple", exported=True)
add_fn(p, "fileResult", 14, 23, "将文件操作错误转换为 Result 类型。", ["error-handling", "result"], "simple", exported=True)
add_imports(p)

# ============ FILE 17: session/jsonl/repo.ts ============
p = "packages/agent/src/harness/session/jsonl/repo.ts"
add_file(p, "JSONL session 仓库管理模块，提供 session 目录查找、元数据列表与存储加载。", ["jsonl", "repository", "session-management"], "complex")
add_fn(p, "listJsonlSessionMetadata", 65, 87, "列出所有 JSONL session 的元数据。", ["jsonl", "repository", "metadata"], "moderate", exported=True)
add_fn(p, "loadJsonlSessionStorage", 89, 102, "加载指定 session 的 JSONL 存储实例。", ["jsonl", "repository", "storage"], "moderate", exported=True)
add_cls(p, "JsonlSessionRepo", 109, 247, "JSONL session 仓库类，管理 session 的创建、列表、加载与删除。", ["jsonl", "repository", "session-management"], "complex", exported=True)
add_imports(p)

# ============ FILE 18: session/jsonl/storage.ts ============
p = "packages/agent/src/harness/session/jsonl/storage.ts"
add_file(p, "JSONL session 存储实现，提供原子写入、mutation 追加与记录读取功能。", ["jsonl", "storage", "session", "persistence"], "complex",
    "使用原子文件写入确保 session 持久化的数据一致性。")
add_fn(p, "publishFileAtomically", 33, 46, "原子性地写入文件，先写临时文件再重命名。", ["jsonl", "storage", "atomic-write"], "simple")
add_cls(p, "JsonlSessionStorage", 48, 277, "JSONL session 存储类，管理 header、mutation 与记录的持久化读写。", ["jsonl", "storage", "session", "persistence"], "complex", exported=True)
add_imports(p)

# ============ FILE 19: session/jsonl/types.ts ============
p = "packages/agent/src/harness/session/jsonl/types.ts"
add_file(p, "JSONL session 的类型定义文件，定义 header、mutation 与存储接口的结构。", ["jsonl", "type-definition", "session"], "simple")
add_imports(p)

# ============ FILE 20: session/memory.ts ============
p = "packages/agent/src/harness/session/memory.ts"
add_file(p, "内存中的 session 存储与仓库实现，用于测试与临时会话。", ["session", "in-memory", "storage", "testing"], "moderate")
add_cls(p, "InMemorySessionStorage", 25, 146, "内存 session 存储类，模拟 JSONL 存储接口的行为。", ["session", "in-memory", "storage"], "complex", exported=True)
add_cls(p, "InMemorySessionRepo", 148, 192, "内存 session 仓库类，管理内存中的 session 集合。", ["session", "in-memory", "repository"], "moderate", exported=True)
add_imports(p)

# ============ FILE 21: session/session.ts ============
p = "packages/agent/src/harness/session/session.ts"
add_file(p, "Session 类实现，管理会话状态、mutation 追加、记录查询与条目迭代。", ["session", "state-management", "mutation"], "complex",
    "Session 类提供基于 record log 的会话状态管理与查询接口。")
add_fn(p, "assertJsonSerializable", 42, 100, "验证值是否可 JSON 序列化。", ["session", "validation", "json"], "moderate", exported=True)
add_cls(p, "Session", 102, 299, "Session 核心类，管理会话 mutation、状态派生与条目查询。", ["session", "core", "state-management"], "complex", exported=True)
add_imports(p)

# ============ FILE 22: session/state.ts ============
p = "packages/agent/src/harness/session/state.ts"
add_file(p, "SessionState 类实现，维护会话的 record log、lane 状态与有效配置。", ["session", "state-management", "record-log"], "complex")
add_cls(p, "SessionState", 50, 344, "Session 状态类，管理 record log 追加、lane 状态派生与配置管理。", ["session", "state-management", "record-log"], "complex", exported=True)
add_imports(p)

# ============ FILE 23: session/testing/conformance.ts ============
p = "packages/agent/src/harness/session/testing/conformance.ts"
add_file(p, "Session 后端一致性测试套件，验证不同 session 存储实现的接口合规性。", ["test", "conformance", "session", "testing"], "complex",
    "生成大量测试用例验证 session 存储后端的接口契约一致性。")
add_fn(p, "createUserMessage", 14, 20, "创建测试用用户消息。", ["test", "fixture", "message"], "simple")
add_fn(p, "createAssistantMessage", 22, 40, "创建测试用 assistant 消息。", ["test", "fixture", "message"], "simple")
add_fn(p, "createCase", 75, 89, "创建一致性测试用例的工厂函数。", ["test", "fixture", "factory"], "simple")
add_fn(p, "createSessionBackendConformance", 92, 1016, "创建 session 后端一致性测试套件，包含 mutation、查询、状态管理等全面验证。", ["test", "conformance", "session", "factory"], "complex", exported=True)
add_imports(p)

# ============ FILE 24: session/testing/index.ts ============
p = "packages/agent/src/harness/session/testing/index.ts"
add_file(p, "Session 测试模块的 barrel 导出文件。", ["barrel", "test", "entry-point"], "simple")
add_imports(p)

# ============ FILE 25: session/testing/types.ts ============
p = "packages/agent/src/harness/session/testing/types.ts"
add_file(p, "Session 测试模块的类型定义，定义一致性测试用例与 fixture 接口。", ["type-definition", "test", "session"], "simple")
add_imports(p)

# ============ FILE 26: session/types.ts ============
p = "packages/agent/src/harness/session/types.ts"
add_file(p, "Session 模块的核心类型定义，包含 mutation、entry、lane 与配置接口。", ["type-definition", "session", "mutation"], "complex",
    "定义 session 的 mutation 类型系统，包括 entry、record、lane 与 fact mutation。")
add_cls(p, "SessionError", 385, 393, "Session 操作错误类。", ["error-handling", "session"], "simple", exported=True)
add_imports(p)

# ============ FILE 27: skills.ts ============
p = "packages/agent/src/harness/skills.ts"
add_file(p, "Skills 加载模块，从文件系统读取 skill 定义并解析 frontmatter 元数据。", ["skills", "loader", "frontmatter"], "complex",
    "支持从目录递归加载 skill 文件，解析 frontmatter 并应用 ignore 规则。")
add_fn(p, "loadSkills", 49, 75, "从指定目录加载所有 skill 定义。", ["skills", "loader"], "moderate", exported=True)
add_fn(p, "loadSourcedSkills", 83, 101, "从指定源路径加载 skill。", ["skills", "loader"], "moderate", exported=True)
add_fn(p, "loadSkillsFromDirInternal", 103, 175, "递归遍历目录加载 skill 文件，应用 ignore 规则过滤。", ["skills", "loader", "directory-traversal"], "complex")
add_fn(p, "addIgnoreRules", 177, 223, "解析并添加 skill 目录的 ignore 规则。", ["skills", "ignore-rules"], "moderate")
add_fn(p, "loadSkillFromFile", 243, 288, "从单个文件加载 skill 定义，解析 frontmatter 与内容。", ["skills", "loader", "frontmatter"], "moderate")
add_fn(p, "resolveKind", 328, 359, "解析 skill 类型，区分 prompt 与 command。", ["skills", "validation"], "moderate")
add_fn(p, "parseFrontmatter", 312, 326, "解析 skill 文件的 YAML frontmatter。", ["skills", "frontmatter", "parsing"], "simple")
add_imports(p)

# ============ FILE 28: system-prompt.ts ============
p = "packages/agent/src/harness/system-prompt.ts"
add_file(p, "系统 prompt 格式化模块，将 skill 定义注入 system prompt 的 XML 格式中。", ["system-prompt", "formatting", "skills"], "simple")
add_fn(p, "formatSkillsForSystemPrompt", 3, 25, "将 skill 列表格式化为 system prompt 中的 XML 标签。", ["system-prompt", "formatting", "skills"], "moderate", exported=True)
add_imports(p)

# ============ FILE 29: telemetry.ts ============
p = "packages/agent/src/harness/telemetry.ts"
add_file(p, "遥测 schema 定义与 span 管理模块，定义 agent 与 harness 的遥测属性 schema。", ["telemetry", "schema-definition", "tracing"], "complex",
    "使用类型化 schema 定义遥测属性，支持 AI span 与 harness span 的 OpenTelemetry 集成。")
add_fn(p, "startAiSpan", 138, 145, "启动 AI 相关的遥测 span。", ["telemetry", "tracing", "span"], "simple", exported=True)
add_fn(p, "startHarnessSpan", 602, 615, "启动 harness 相关的遥测 span。", ["telemetry", "tracing", "span"], "simple", exported=True)
add_imports(p)

# ============ FILE 30: tools/bash.ts ============
p = "packages/agent/src/harness/tools/bash.ts"
add_file(p, "Bash 工具实现，提供 shell 命令执行能力与超时控制。", ["tool", "bash", "shell", "command-execution"], "moderate")
add_fn(p, "createBashTool", 51, 161, "创建 bash 工具实例，封装命令执行、超时处理与输出截断逻辑。", ["tool", "bash", "factory", "command-execution"], "complex", exported=True)
add_imports(p)

# ============ FILE 31: tools/edit-diff.ts ============
p = "packages/agent/src/harness/tools/edit-diff.ts"
add_file(p, "文件编辑 diff 模块，提供文本规范化、模糊匹配、行级替换与 unified diff 生成。", ["tool", "edit", "diff", "fuzzy-matching"], "complex",
    "实现 BOM 处理、行尾规范化、模糊文本查找与保持未修改行的精确替换。")
add_fn(p, "normalizeForFuzzyMatch", 30, 51, "规范化文本用于模糊匹配，处理空白与大小写。", ["edit", "normalization", "fuzzy-matching"], "moderate", exported=True)
add_fn(p, "getReplacementLineRange", 80, 105, "计算替换操作的行范围。", ["edit", "line-range"], "moderate")
add_fn(p, "applyReplacementsPreservingUnchangedLines", 128, 169, "应用替换同时保留未修改的行。", ["edit", "replacement", "preservation"], "moderate", exported=True)
add_fn(p, "fuzzyFindText", 203, 241, "在文本中模糊查找指定内容，支持容错匹配。", ["edit", "fuzzy-matching", "search"], "moderate", exported=True)
add_fn(p, "applyEditsToNormalizedContent", 301, 363, "在规范化后的内容上应用编辑操作。", ["edit", "replacement", "normalization"], "complex", exported=True)
add_fn(p, "generateUnifiedPatch", 366, 371, "生成 unified diff patch。", ["edit", "diff", "patch"], "simple", exported=True)
add_fn(p, "generateDiffString", 377, 500, "生成 diff 字符串，支持多种格式与上下文行。", ["edit", "diff", "formatting"], "complex", exported=True)
add_imports(p)

# ============ FILE 32: tools/edit.ts ============
p = "packages/agent/src/harness/tools/edit.ts"
add_file(p, "Edit 工具实现，提供文件编辑能力，集成 diff 生成与文件变更队列。", ["tool", "edit", "file-mutation"], "moderate")
add_fn(p, "prepareEditArguments", 48, 64, "准备 edit 工具的参数，解析路径与编辑内容。", ["tool", "edit", "validation"], "simple")
add_fn(p, "createEditTool", 77, 127, "创建 edit 工具实例，封装文件编辑、diff 生成与变更队列管理。", ["tool", "edit", "factory"], "moderate", exported=True)
add_imports(p)

# ============ FILE 33: tools/file-mutation-queue.ts ============
p = "packages/agent/src/harness/tools/file-mutation-queue.ts"
add_file(p, "文件变更队列模块，确保对同一文件的并发编辑操作串行执行。", ["tool", "mutation-queue", "concurrency"], "simple",
    "使用基于文件路径的锁机制避免并发文件编辑冲突。")
add_fn(p, "withFileMutationQueue", 29, 56, "在文件变更队列中执行操作，确保同文件的编辑串行化。", ["tool", "mutation-queue", "concurrency"], "moderate", exported=True)
add_imports(p)

# ============ FILE 34: tools/image.ts ============
p = "packages/agent/src/harness/tools/image.ts"
add_file(p, "图片处理工具模块，提供 MIME 类型检测、base64 编码与图片格式验证。", ["tool", "image", "validation", "encoding"], "moderate",
    "通过 magic bytes 检测 PNG/BMP 格式，包括动画 PNG 识别。")
add_fn(p, "detectSupportedImageMimeType", 3, 10, "通过 magic bytes 检测图片的 MIME 类型。", ["image", "mime-detection", "validation"], "simple", exported=True)
add_fn(p, "encodeBase64", 12, 25, "将二进制数据编码为 base64 字符串。", ["image", "encoding", "base64"], "simple", exported=True)
add_imports(p)

# ============ FILE 35: tools/path-utils.ts ============
p = "packages/agent/src/harness/tools/path-utils.ts"
add_file(p, "工具路径处理模块，提供路径规范化、解析与读取路径验证。", ["tool", "path", "validation"], "simple")
add_fn(p, "resolveReadToolPath", 16, 30, "解析并验证工具的读取路径，确保安全访问。", ["tool", "path", "validation", "security"], "simple", exported=True)
add_imports(p)

# Add cross-file calls edges (high confidence only)
# agent.ts -> agent-loop.ts
add_edge(fid("packages/agent/src/agent.ts"), fid("packages/agent/src/agent-loop.ts"), "depends_on", 0.6)
# agent-harness.ts -> compaction/compaction.ts (already imported, add calls to specific functions)
add_edge(fnid("packages/agent/src/harness/agent-harness.ts","AgentHarness") if False else fid("packages/agent/src/harness/agent-harness.ts"), fnid("packages/agent/src/harness/compaction/compaction.ts","compact"), "calls", 0.8)
# branch-summarization.ts -> compaction.ts
add_edge(fid("packages/agent/src/harness/compaction/branch-summarization.ts"), fnid("packages/agent/src/harness/compaction/compaction.ts","generateSummary"), "calls", 0.8)
# session/repo.ts -> session/storage.ts
add_edge(fid("packages/agent/src/harness/session/jsonl/repo.ts"), fid("packages/agent/src/harness/session/jsonl/storage.ts"), "depends_on", 0.6)
# session/memory.ts -> session/session.ts
add_edge(fid("packages/agent/src/harness/session/memory.ts"), fid("packages/agent/src/harness/session/session.ts"), "depends_on", 0.6)
# session/context.ts -> messages.ts
add_edge(fid("packages/agent/src/harness/session/context.ts"), fid("packages/agent/src/harness/messages.ts"), "depends_on", 0.6)
# tools/edit.ts -> tools/edit-diff.ts
add_edge(fid("packages/agent/src/harness/tools/edit.ts"), fid("packages/agent/src/harness/tools/edit-diff.ts"), "depends_on", 0.6)
# tools/bash.ts -> utils/shell-output.ts (cross-batch, from neighborMap)
add_edge(fid("packages/agent/src/harness/tools/bash.ts"), fid("packages/agent/src/harness/utils/shell-output.ts"), "depends_on", 0.6)
# generate-telemetry-docs.ts -> telemetry.ts
add_edge(fnid("packages/agent/scripts/generate-telemetry-docs.ts","generateTelemetryDocs"), fid("packages/agent/src/harness/telemetry.ts"), "calls", 0.8)

# Split into parts
file_order = sorted(set(n.get("filePath","") for n in nodes if n["type"] == "file"))
parts_count = max(1, math.ceil(max(len(nodes) / 60, len(edges) / 120)))
chunk_size = math.ceil(len(file_order) / parts_count)

for part_idx in range(parts_count):
    part_files = set(file_order[part_idx * chunk_size : (part_idx + 1) * chunk_size])
    part_nodes = [n for n in nodes if n.get("filePath","") in part_files]
    part_node_ids = set(n["id"] for n in part_nodes)
    # Edges where source is in this part's nodes
    part_edges = []
    for e in edges:
        if e["source"] in part_node_ids:
            part_edges.append(e)
    
    out = {"nodes": part_nodes, "edges": part_edges}
    outpath = f"/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-1-part-{part_idx+1}.json"
    with open(outpath, 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Part {part_idx+1}: {len(part_nodes)} nodes, {len(part_edges)} edges -> {outpath}")

print(f"Total: {len(nodes)} nodes, {len(edges)} edges across {parts_count} parts")
