import fs from 'fs';

// Read the extraction results and dispatch data
const extractData = JSON.parse(fs.readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-8.json','utf8'));
const dispatchData = JSON.parse(fs.readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-8.json','utf8'));

const batchImportData = dispatchData.batchImportData;
const results = extractData.results;

const nodes = [];
const edges = [];

function addNode(n) { nodes.push(n); }
function addEdge(s, t, type, weight) {
  if (s === t) return;
  edges.push({ source: s, target: t, type, direction: "forward", weight });
}

// Significance filter for functions: 10+ lines OR exported
function isSignificantFunction(fn, exports) {
  const lineCount = fn.endLine - fn.startLine + 1;
  const isExported = exports.some(e => e.name === fn.name);
  return lineCount >= 10 || isExported;
}

// Significance filter for classes: 2+ methods OR 20+ lines OR exported
function isSignificantClass(cls, exports) {
  const lineCount = cls.endLine - cls.startLine + 1;
  const methodCount = (cls.methods || []).length;
  const isExported = exports.some(e => e.name === cls.name);
  return methodCount >= 2 || lineCount >= 20 || isExported;
}

// Process each file
for (const r of results) {
  const fp = r.path;
  const exports = r.exports || [];
  const functions = r.functions || [];
  const classes = r.classes || [];
  const metrics = r.metrics || {};
  const totalLines = r.totalLines || 0;
  const nonEmptyLines = r.nonEmptyLines || 0;

  // Determine complexity
  let complexity = "simple";
  if (nonEmptyLines > 200) complexity = "complex";
  else if (nonEmptyLines > 50) complexity = "moderate";

  // Create file node
  const fileNode = {
    id: `file:${fp}`,
    type: "file",
    name: fp.split('/').pop(),
    filePath: fp,
    summary: "", // will be set from existing or generated
    tags: [],
    complexity
  };

  // We'll use pre-built summaries from the existing broken file
  // For now, use a generic placeholder that we'll fix
  nodes.push(fileNode);

  // Create function nodes
  for (const fn of functions) {
    if (!isSignificantFunction(fn, exports)) continue;
    const fnLines = fn.endLine - fn.startLine + 1;
    let fnComplexity = "simple";
    if (fnLines > 50) fnComplexity = "complex";
    else if (fnLines > 20) fnComplexity = "moderate";

    nodes.push({
      id: `function:${fp}:${fn.name}`,
      type: "function",
      name: fn.name,
      filePath: fp,
      lineRange: [fn.startLine, fn.endLine],
      summary: "",
      tags: [],
      complexity: fnComplexity
    });

    // contains edge: file -> function
    addEdge(`file:${fp}`, `function:${fp}:${fn.name}`, "contains", 1.0);

    // exports edge: file -> exported function
    if (exports.some(e => e.name === fn.name)) {
      addEdge(`file:${fp}`, `function:${fp}:${fn.name}`, "exports", 0.8);
    }
  }

  // Create class nodes
  for (const cls of classes) {
    if (!isSignificantClass(cls, exports)) continue;
    const clsLines = cls.endLine - cls.startLine + 1;
    let clsComplexity = "simple";
    if (clsLines > 50) clsComplexity = "complex";
    else if (clsLines > 20) clsComplexity = "moderate";

    nodes.push({
      id: `class:${fp}:${cls.name}`,
      type: "class",
      name: cls.name,
      filePath: fp,
      lineRange: [cls.startLine, cls.endLine],
      summary: "",
      tags: [],
      complexity: clsComplexity
    });

    // contains edge: file -> class
    addEdge(`file:${fp}`, `class:${fp}:${cls.name}`, "contains", 1.0);

    // exports edge: file -> exported class
    if (exports.some(e => e.name === cls.name)) {
      addEdge(`file:${fp}`, `class:${fp}:${cls.name}`, "exports", 0.8);
    }
  }
}

// Create import edges
for (const [filePath, importPaths] of Object.entries(batchImportData)) {
  for (const targetPath of importPaths) {
    addEdge(`file:${filePath}`, `file:${targetPath}`, "imports", 0.7);
  }
}

// Try to read the existing file to extract summaries/tags we already wrote
const existingNodes = {};
try {
  const existingRaw = fs.readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-8.json','utf8');
  // Parse line by line - each line that starts with {"id" is a node
  const lines = existingRaw.split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('{"id":')) {
      try {
        const obj = JSON.parse(trimmed);
        existingNodes[obj.id] = obj;
      } catch(e) {
        // skip malformed
      }
    }
  }
} catch(e) {
  // File doesn't exist yet, that's fine
}

// Merge existing summaries/tags into new nodes
for (const node of nodes) {
  if (existingNodes[node.id]) {
    const ex = existingNodes[node.id];
    if (ex.summary) node.summary = ex.summary;
    if (ex.tags && ex.tags.length > 0) node.tags = ex.tags;
    if (ex.languageNotes) node.languageNotes = ex.languageNotes;
  }
}

// Fill in missing summaries and tags for nodes that don't have them
// File-level summaries
const fileSummaries = {
  "packages/coding-agent/src/core/compaction/branch-summarization.ts": {s:"处理对话分支的摘要生成，收集分支条目并通过 LLM 生成结构化的分支总结。",t:["compaction","summarization","branch","llm"]},
  "packages/coding-agent/src/core/compaction/compaction.ts": {s:"核心上下文压缩模块，负责 token 估算、对话截断点选择、摘要生成与会话压缩的完整流程。",t:["compaction","context-management","token-estimation","llm"]},
  "packages/coding-agent/src/core/compaction/utils.ts": {s:"提供压缩模块的实用工具函数，包括文件操作提取、对话序列化和摘要系统提示。",t:["compaction","utility","serialization"]},
  "packages/coding-agent/src/core/export-html/ansi-to-html.ts": {s:"将 ANSI 终端颜色转义码转换为带内联 CSS 样式的 HTML，支持 256 色和 SGR 参数解析。",t:["export-html","ansi","html","conversion"]},
  "packages/coding-agent/src/core/export-html/tool-renderer.ts": {s:"为 HTML 导出功能渲染工具调用结果，将各种工具输出格式化为可展示的 HTML。",t:["export-html","tool-renderer","html"]},
  "packages/coding-agent/src/core/keybindings.ts": {s:"管理键绑定配置，包括默认键映射、配置迁移、加载和 KeybindingsManager 类。",t:["keybindings","config","input-handling"]},
  "packages/coding-agent/src/core/messages.ts": {s:"定义消息类型和构造函数，包括分支摘要、压缩摘要、自定义消息的创建以及 LLM 格式转换。",t:["messages","data-model","serialization"]},
  "packages/coding-agent/src/extensions/llama/client.ts": {s:"Llama 本地推理服务器的 HTTP 客户端，负责模型加载/卸载、下载和推理请求。",t:["llama","client","http","inference"]},
  "packages/coding-agent/src/extensions/llama/huggingface.ts": {s:"HuggingFace Hub API 客户端，用于搜索模型和获取模型详情，支持 token 认证和速率限制处理。",t:["huggingface","client","model-search"]},
  "packages/coding-agent/src/extensions/llama/index.ts": {s:"Llama 扩展入口模块，注册本地 Llama 推理 provider 和管理命令。",t:["llama","extension","entry-point","provider"]},
  "packages/coding-agent/src/extensions/llama/provider.ts": {s:"创建 Llama 模型 provider，将本地 Llama 服务器模型注册到 Pi 的模型运行时。",t:["llama","provider","model-runtime"]},
  "packages/coding-agent/src/extensions/llama/ui.ts": {s:"Llama 扩展的终端 UI 组件，提供 HuggingFace 模型搜索界面和 Llama 管理视图。",t:["llama","ui","tui","model-search"]},
  "packages/coding-agent/src/modes/interactive/components/armin.ts": {s:"ASCII 艺术动画组件 Armin，支持打字机、扫描线、雨滴、淡入、CRT、故障和溶解等多种视觉效果。",t:["interactive","component","animation","ascii-art"]},
  "packages/coding-agent/src/modes/interactive/components/assistant-message.ts": {s:"渲染助手消息的交互式组件，支持 Markdown 转换、思考块折叠和流式更新。",t:["interactive","component","message-rendering","markdown"]},
  "packages/coding-agent/src/modes/interactive/components/bash-execution.ts": {s:"渲染 Bash 命令执行结果的交互式组件，支持输出截断、展开/折叠和状态显示。",t:["interactive","component","bash","output-rendering"]},
  "packages/coding-agent/src/modes/interactive/components/bordered-loader.ts": {s:"带边框的加载动画组件，支持取消操作和信号控制。",t:["interactive","component","loader","ui"]},
  "packages/coding-agent/src/modes/interactive/components/branch-summary-message.ts": {s:"渲染分支摘要消息的交互式组件，支持展开/折叠显示摘要内容。",t:["interactive","component","message-rendering","branch-summary"]},
  "packages/coding-agent/src/modes/interactive/components/compaction-summary-message.ts": {s:"渲染压缩摘要消息的交互式组件，支持展开/折叠显示压缩前后的上下文信息。",t:["interactive","component","message-rendering","compaction"]},
  "packages/coding-agent/src/modes/interactive/components/countdown-timer.ts": {s:"倒计时定时器组件，在终端 UI 中显示剩余秒数并在到期时回调。",t:["interactive","component","timer","utility"]},
  "packages/coding-agent/src/modes/interactive/components/custom-editor.ts": {s:"自定义编辑器组件，处理键盘快捷键、粘贴图片和扩展快捷键等编辑器操作。",t:["interactive","component","editor","input-handling"]},
  "packages/coding-agent/src/modes/interactive/components/custom-message.ts": {s:"渲染自定义类型消息的交互式组件，支持自定义渲染器和展开/折叠。",t:["interactive","component","message-rendering","custom"]},
  "packages/coding-agent/src/modes/interactive/components/daxnuts.ts": {s:"ASCII 艺术动画组件 Daxnuts，渲染图像并逐帧播放动画效果。",t:["interactive","component","animation","ascii-art"]},
  "packages/coding-agent/src/modes/interactive/components/diff.ts": {s:"在终端中渲染 diff 输出的组件，支持行内差异高亮和颜色标记。",t:["interactive","component","diff","rendering"]},
  "packages/coding-agent/src/modes/interactive/components/dynamic-border.ts": {s:"动态边框组件，根据主题颜色渲染可变颜色的边框。",t:["interactive","component","border","ui"]},
  "packages/coding-agent/src/modes/interactive/components/earendil-announcement.ts": {s:"Earendil 公告组件，在终端中渲染 Base64 图片公告动画。",t:["interactive","component","announcement","animation"]},
  "packages/coding-agent/src/modes/interactive/components/extension-editor.ts": {s:"扩展编辑器组件，提供多行文本编辑和外部编辑器调用功能。",t:["interactive","component","editor","extension"]},
  "packages/coding-agent/src/modes/interactive/components/extension-input.ts": {s:"扩展输入组件，提供带倒计时的单行文本输入界面。",t:["interactive","component","input","extension"]},
  "packages/coding-agent/src/modes/interactive/components/extension-selector.ts": {s:"扩展选择器组件，提供带倒计时的列表选择界面。",t:["interactive","component","selector","extension"]},
  "packages/coding-agent/src/modes/interactive/components/first-time-setup.ts": {s:"首次启动设置向导组件，引导用户选择主题和分析偏好。",t:["interactive","component","setup","onboarding"]},
  "packages/coding-agent/src/modes/interactive/components/keybinding-hints.ts": {s:"格式化键绑定提示文本的工具函数集，支持按键文本和提示行渲染。",t:["interactive","utility","keybindings","formatting"]},
  "packages/coding-agent/src/modes/interactive/components/login-dialog.ts": {s:"登录对话框组件，处理 OAuth 认证流程、设备码显示和手动输入等登录方式。",t:["interactive","component","login","oauth"]},
  "packages/coding-agent/src/modes/interactive/components/markdown-transform.ts": {s:"Markdown 转换工具，创建和应用自定义 Markdown 变换器处理消息内容。",t:["interactive","utility","markdown","transform"]},
  "packages/coding-agent/src/modes/interactive/components/model-selector.ts": {s:"模型选择器组件，提供模型搜索、筛选、排序和 scoped model 管理功能。",t:["interactive","component","model-selector","search"]},
  "packages/coding-agent/src/modes/interactive/components/oauth-selector.ts": {s:"OAuth 认证选择器组件，列出可用认证提供商并支持搜索过滤。",t:["interactive","component","oauth","selector"]},
  "packages/coding-agent/src/modes/interactive/components/scoped-models-selector.ts": {s:"Scoped 模型选择器组件，管理启用的模型列表，支持排序、刷新和搜索过滤。",t:["interactive","component","model-selector","scoped-models"]}
};

// Function/class summaries
const fnSummaries = {
  "collectEntriesForBranchSummary": {s:"从会话中收集需要生成分支摘要的条目，定位旧叶子节点到目标节点之间的对话片段。",t:["compaction","session","branch"]},
  "prepareBranchEntries": {s:"在 token 预算内准备分支条目，截断过长的序列化对话内容。",t:["compaction","token-budget","preparation"]},
  "generateBranchSummary": {s:"调用 LLM 为分支条目生成分支摘要，支持自定义指令和流式回调。",t:["compaction","llm","summarization","streaming"]},
  "estimateTokens": {s:"估算消息的 token 数量，考虑文本和图片内容的字符数。",t:["token-estimation","utility"]},
  "findCutPoint": {s:"在对话条目中查找最佳压缩截断点，保留最近的 token 数量并寻找有效的回合起始点。",t:["compaction","cut-point","algorithm"]},
  "generateSummary": {s:"调用 LLM 为当前对话上下文生成摘要，支持自定义指令、思考级别和流式回调。",t:["compaction","llm","summarization"]},
  "prepareCompaction": {s:"准备压缩操作，计算上下文 token、查找截断点并提取文件操作记录。",t:["compaction","preparation","context-management"]},
  "compact": {s:"执行完整的压缩流程：生成摘要、构建压缩消息并更新会话条目。",t:["compaction","core","session"]},
  "generateSummaryWithUsage": {s:"生成摘要并返回 token 用量信息，支持重试和流式回调。",t:["compaction","llm","usage-tracking"]},
  "estimateContextTokens": {s:"估算当前对话上下文的总 token 数量。",t:["token-estimation","context"]},
  "shouldCompact": {s:"判断当前上下文是否需要执行压缩。",t:["compaction","decision"]},
  "findTurnStartIndex": {s:"查找对话回合的起始索引位置。",t:["compaction","turn-detection"]},
  "completeSummarization": {s:"完成摘要操作，构建压缩消息和更新会话状态。",t:["compaction","summarization"]},
  "extractFileOpsFromMessage": {s:"从消息中提取文件读写操作记录，累积到文件操作对象中。",t:["compaction","file-operations","extraction"]},
  "serializeConversation": {s:"将消息数组序列化为文本格式，保留角色信息和文件操作上下文供 LLM 摘要使用。",t:["compaction","serialization","conversation"]},
  "ansiToHtml": {s:"将包含 ANSI 转义码的文本转换为带内联 CSS 样式的 HTML 字符串。",t:["export-html","ansi","html"]},
  "applySgrCode": {s:"解析并应用 SGR (Select Graphic Rendition) 参数，设置文本颜色、背景色和样式。",t:["ansi","sgr","style-parsing"]},
  "createToolHtmlRenderer": {s:"创建工具 HTML 渲染器工厂函数，根据工具类型生成对应的 HTML 输出。",t:["export-html","tool-renderer","factory"]},
  "migrateKeybindingsConfig": {s:"将旧版键绑定配置迁移到新格式，处理已弃用的键名。",t:["keybindings","migration","config"]},
  "convertToLlm": {s:"将内部消息格式转换为 LLM API 所需的消息格式，处理工具调用和内容提取。",t:["messages","llm","conversion"]},
  "createCompactionSummaryMessage": {s:"创建压缩摘要消息，包含摘要文本和压缩前的 token 数量。",t:["messages","compaction","factory"]},
  "llamaExtension": {s:"Llama 扩展主函数，注册 provider、管理命令和 UI 交互，处理模型加载和连接错误。",t:["llama","extension","provider-registration"]},
  "createLlamaProvider": {s:"创建 Llama provider 实例，定义模型列表获取和推理请求转发的逻辑。",t:["llama","provider","factory"]},
  "runWithProgress": {s:"在 Llama UI 中以进度条形式执行异步操作，显示加载或下载进度。",t:["llama","ui","progress"]},
  "renderDiff": {s:"渲染 diff 文本为带颜色的终端输出，支持行内差异高亮显示。",t:["interactive","diff","rendering"]},
  "renderIntraLineDiff": {s:"计算两个文本行的行内差异并生成高亮标记。",t:["interactive","diff","algorithm"]},
  "formatKeyText": {s:"将键绑定标识格式化为可显示的按键文本。",t:["keybindings","formatting","utility"]},
  "applyMarkdownTransformers": {s:"按顺序应用 Markdown 变换器链处理输入文本。",t:["markdown","transform","utility"]},
  "formatAuthSelectorProviderType": {s:"格式化认证提供商类型为显示文本。",t:["oauth","formatting","utility"]}
};

// Class summaries
const clsSummaries = {
  "KeybindingsManager": {s:"管理键绑定配置的加载、创建和重载，提供有效配置查询接口。",t:["keybindings","manager","config"]},
  "LlamaClient": {s:"封装 Llama 服务器的 HTTP API，提供模型列表、加载、卸载、下载和推理功能。",t:["llama","client","http","api"]},
  "HuggingFaceClient": {s:"封装 HuggingFace Hub API，提供模型搜索和详情查询功能，自动处理速率限制。",t:["huggingface","client","api"]},
  "HuggingFaceSearch": {s:"HuggingFace 模型搜索 TUI 组件，提供输入过滤、防抖搜索和结果选择功能。",t:["llama","ui","search","tui"]},
  "LlamaView": {s:"Llama 管理视图 TUI 组件，展示模型列表、加载状态和进度信息。",t:["llama","ui","tui","model-management"]},
  "ArminComponent": {s:"Armin 动画组件类，管理字符网格、帧动画循环和多种视觉效果的状态机。",t:["interactive","component","animation"]},
  "AssistantMessageComponent": {s:"助手消息渲染组件，处理 Markdown 显示、思考块隐藏和流式内容更新。",t:["interactive","component","message-rendering"]},
  "BashExecutionComponent": {s:"Bash 执行结果渲染组件，管理命令输出、截断显示和展开折叠状态。",t:["interactive","component","bash"]},
  "BorderedLoader": {s:"带边框的加载器组件，封装可取消的加载动画和键盘输入处理。",t:["interactive","component","loader"]},
  "BranchSummaryMessageComponent": {s:"分支摘要消息渲染组件，支持展开折叠和 Markdown 显示。",t:["interactive","component","branch-summary"]},
  "CompactionSummaryMessageComponent": {s:"压缩摘要消息渲染组件，支持展开折叠和 Markdown 显示。",t:["interactive","component","compaction"]},
  "CountdownTimer": {s:"倒计时定时器类，管理间隔定时器和到期回调。",t:["interactive","component","timer"]},
  "CustomEditor": {s:"自定义编辑器类，代理键盘输入并分发动作处理器给上层组件。",t:["interactive","component","editor"]},
  "CustomMessageComponent": {s:"自定义消息渲染组件，支持自定义渲染器、Markdown 主题和展开折叠。",t:["interactive","component","custom-message"]},
  "DaxnutsComponent": {s:"Daxnuts 动画组件类，管理图像解析、帧动画循环和渲染缓存。",t:["interactive","component","animation"]},
  "DynamicBorder": {s:"动态边框类，根据主题颜色渲染可变颜色的边框。",t:["interactive","component","border"]},
  "EarendilAnnouncementComponent": {s:"Earendil 公告组件类，加载并渲染 Base64 图片到终端。",t:["interactive","component","announcement"]},
  "ExtensionEditorComponent": {s:"扩展编辑器组件类，处理键盘输入、外部编辑器调用和提交/取消回调。",t:["interactive","component","editor"]},
  "ExtensionInputComponent": {s:"扩展输入组件类，管理文本输入、倒计时和提交/取消回调。",t:["interactive","component","input"]},
  "ExtensionSelectorComponent": {s:"扩展选择器组件类，管理选项列表、选择索引和倒计时。",t:["interactive","component","selector"]},
  "FirstTimeSetupComponent": {s:"首次设置向导组件类，管理步骤导航、主题选择和选项列表。",t:["interactive","component","setup"]},
  "LoginDialogComponent": {s:"登录对话框组件类，管理多种认证状态和用户交互。",t:["interactive","component","login","oauth"]},
  "ModelSelectorComponent": {s:"模型选择器组件类，管理模型列表、搜索过滤、scoped model 和模型刷新。",t:["interactive","component","model-selector"]},
  "OAuthSelectorComponent": {s:"OAuth 选择器组件类，管理认证提供商列表、搜索过滤和选择回调。",t:["interactive","component","oauth"]},
  "ScopedModelsSelectorComponent": {s:"Scoped 模型选择器组件类，管理启用模型 ID、排序顺序和刷新状态。",t:["interactive","component","scoped-models"]}
};

// Language notes
const langNotes = {
  "packages/coding-agent/src/core/compaction/branch-summarization.ts": "使用 token 预算策略控制分支条目的序列化长度。",
  "packages/coding-agent/src/core/compaction/compaction.ts": "包含多阶段压缩策略：截断点查找、摘要生成与用量计算。",
  "packages/coding-agent/src/core/export-html/ansi-to-html.ts": "实现了完整的 SGR (Select Graphic Rendition) 参数解析。",
  "packages/coding-agent/src/core/keybindings.ts": "支持从旧版键绑定格式迁移到新格式。",
  "packages/coding-agent/src/extensions/llama/client.ts": "支持 AbortSignal 取消和加载/下载进度解析。",
  "packages/coding-agent/src/modes/interactive/components/armin.ts": "使用字符网格和帧动画实现多种终端视觉效果。"
};

// Fill in missing summaries and tags
for (const node of nodes) {
  if (node.type === "file") {
    const fp = node.filePath;
    if (!node.summary && fileSummaries[fp]) {
      node.summary = fileSummaries[fp].s;
      node.tags = fileSummaries[fp].t;
    }
    if (!node.languageNotes && langNotes[fp]) {
      node.languageNotes = langNotes[fp];
    }
  } else if (node.type === "function") {
    const name = node.name;
    if (!node.summary && fnSummaries[name]) {
      node.summary = fnSummaries[name].s;
      node.tags = fnSummaries[name].t;
    }
  } else if (node.type === "class") {
    const name = node.name;
    if (!node.summary && clsSummaries[name]) {
      node.summary = clsSummaries[name].s;
      node.tags = clsSummaries[name].t;
    }
  }

  // Fallback for any still-missing summary
  if (!node.summary) {
    node.summary = node.type === "file" ? `${node.name} 源文件。` : `${node.name} ${node.type}。`;
  }
  if (!node.tags || node.tags.length === 0) {
    node.tags = ["code"];
  }
}

// Write output
const output = { nodes, edges };
const outPath = '/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-8.json';
fs.writeFileSync(outPath, JSON.stringify(output, null, 2));

console.log(`Nodes: ${nodes.length}`);
console.log(`Edges: ${edges.length}`);
console.log(`Import edges expected: 88`);

// Count edge types
const edgeTypes = {};
for (const e of edges) {
  edgeTypes[e.type] = (edgeTypes[e.type] || 0) + 1;
}
console.log('Edge types:', JSON.stringify(edgeTypes));
