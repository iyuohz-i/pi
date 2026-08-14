import { readFileSync, writeFileSync } from 'fs';

const extract = JSON.parse(readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-24.json', 'utf8'));
const dispatch = JSON.parse(readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-24.json', 'utf8'));

const nodes = [];
const edges = [];

// File-level metadata: summary, tags, complexity
const fileMeta = {
  "packages/tui/src/kill-ring.ts": {
    summary: "实现 Emacs 风格的 kill/yank 环形缓冲区，支持连续删除文本的累积合并与轮换粘贴操作。",
    tags: ["utility", "text-editing", "kill-ring"],
    complexity: "simple"
  },
  "packages/tui/src/latex.ts": {
    summary: "LaTeX 数学公式渲染器，将 LaTeX 源文本解析为 Unicode 布局节点并以终端字符画形式渲染，支持分数、上下标、矩阵等常见数学结构。",
    tags: ["rendering", "latex", "parser", "terminal-art"],
    complexity: "complex",
    languageNotes: "使用递归下降解析器处理 LaTeX 命令和环境，输出为二维布局节点树。"
  },
  "packages/tui/src/layout-node.ts": {
    summary: "定义布局节点类型接口（StackLayoutNode、ScrollLayoutNode），为 TUI 组件提供布局计算的抽象契约。",
    tags: ["type-definition", "layout", "component"],
    complexity: "simple"
  },
  "packages/tui/src/layout.ts": {
    summary: "TUI 布局引擎，负责组件的测量、定位、裁剪和绘制，包括滚动条渲染和 Kitty 图像裁剪。",
    tags: ["layout", "rendering", "component", "terminal-art"],
    complexity: "complex"
  },
  "packages/tui/src/native-modifiers.ts": {
    summary: "通过原生 native addon 检测键盘修饰键（shift/command/control/option）的按下状态，提供跨平台修饰键查询能力。",
    tags: ["utility", "keyboard", "native-addon"],
    complexity: "moderate"
  },
  "packages/tui/src/stdin-buffer.ts": {
    summary: "标准输入缓冲器，将分片到达的 stdin 数据累积为完整的终端转义序列后再发射，防止半序列被误解为普通按键。",
    tags: ["terminal", "buffer", "event-handler", "streaming"],
    complexity: "complex",
    languageNotes: "基于 OpenTUI 的序列完整性检测逻辑，支持 CSI、OSC、DCS、APC 等多种转义序列类型。"
  },
  "packages/tui/src/terminal-colors.ts": {
    summary: "解析终端颜色方案报告，包括 OSC 11 背景色响应和终端深色/浅色模式检测。",
    tags: ["terminal", "color", "utility"],
    complexity: "moderate"
  },
  "packages/tui/src/terminal-image.ts": {
    summary: "终端图像协议实现，支持 Kitty 图形协议和 iTerm2 内联图像的编码、渲染、尺寸计算及能力检测。",
    tags: ["terminal", "image", "protocol", "rendering"],
    complexity: "complex",
    languageNotes: "实现 Kitty 和 iTerm2 两种图像协议的编码，并解析 PNG/JPEG/GIF/WebP 二进制头部获取尺寸。"
  },
  "packages/tui/src/terminal.ts": {
    summary: "终端控制层，管理 stdin 原始模式、Kitty 键盘协议协商、鼠标事件、光标控制、进度条及终端尺寸查询。",
    tags: ["terminal", "keyboard-protocol", "event-handler", "entry-point"],
    complexity: "complex"
  },
  "packages/tui/src/tui-alt-screen.ts": {
    summary: "备用屏幕 TUI 实现，提供完整的交替屏幕渲染、文本选择、搜索高亮、鼠标滚动、滚动条拖拽、Kitty 图像管理和 URL 点击等功能。",
    tags: ["tui", "rendering", "terminal", "component", "event-handler"],
    complexity: "complex",
    languageNotes: "实现了完整的鼠标交互系统（选择、滚动条、右键粘贴）和搜索导航，是 TUI 的核心展示层。"
  },
  "packages/tui/src/tui-main-screen.ts": {
    summary: "主屏幕 TUI 实现，采用差量渲染策略在普通终端屏幕上绘制内容，管理 Kitty 图像的上传和清理。",
    tags: ["tui", "rendering", "terminal", "differential-render"],
    complexity: "complex"
  },
  "packages/tui/src/tui.ts": {
    summary: "TUI 框架核心基类，提供差分渲染、overlay 合成、终端色彩检测、硬件光标定位及组件容器管理。",
    tags: ["tui", "framework", "rendering", "component", "entry-point"],
    complexity: "complex"
  },
  "packages/tui/src/undo-stack.ts": {
    summary: "通用撤销栈，使用 structuredClone 实现深拷贝快照语义，支持 push/pop/clear 操作。",
    tags: ["utility", "undo", "data-structure"],
    complexity: "simple"
  },
  "packages/tui/src/utils.ts": {
    summary: "TUI 核心工具库，提供 Unicode 字素宽度计算、ANSI 转义序列处理、文本截断与换行、OSC 8 超链接解析及 ANSI 状态追踪。",
    tags: ["utility", "unicode", "terminal", "text-processing", "ansi"],
    complexity: "complex",
    languageNotes: "大量使用 Intl.Segmenter 进行 Unicode 字素和词边界分割，处理 CJK 全角字符和组合 emoji。"
  },
  "packages/tui/src/word-navigation.ts": {
    summary: "文本编辑器中的词级导航功能，基于 Intl.Segmenter 实现按词前后移动光标。",
    tags: ["utility", "text-editing", "navigation"],
    complexity: "moderate"
  },
  "packages/tui/test/autocomplete.test.ts": {
    summary: "自动补全功能的集成测试，验证文件系统路径补全在不同目录结构和输入下的行为。",
    tags: ["test", "autocomplete", "integration"],
    complexity: "complex"
  },
  "packages/tui/test/chat-simple.ts": {
    summary: "简单聊天 TUI 演示脚本，展示编辑器、Markdown 渲染、Loader 和自动补全等组件的基本集成。",
    tags: ["test", "demo", "component"],
    complexity: "moderate"
  },
  "packages/tui/test/editor-history-keybindings.test.ts": {
    summary: "编辑器历史记录与快捷键绑定的集成测试，验证快捷键触发的编辑器行为。",
    tags: ["test", "editor", "keybindings"],
    complexity: "simple"
  },
  "packages/tui/test/editor.test.ts": {
    summary: "编辑器组件的全面测试套件，覆盖文本输入、删除、选择、自动补全、换行、Emacs 快捷键等交互场景。",
    tags: ["test", "editor", "component", "integration"],
    complexity: "complex"
  },
  "packages/tui/test/fuzzy.test.ts": {
    summary: "模糊匹配算法的单元测试，验证 fuzzyMatch 和 fuzzyFilter 的匹配精度和评分。",
    tags: ["test", "fuzzy", "unit"],
    complexity: "moderate"
  },
  "packages/tui/test/image-test.ts": {
    summary: "终端图像渲染的可视化测试脚本，验证 Kitty/iTerm2 图像协议在 TUI 中的显示效果。",
    tags: ["test", "image", "demo"],
    complexity: "simple"
  },
  "packages/tui/test/input.test.ts": {
    summary: "Input 组件的测试套件，验证文本输入、光标移动、选择及剪贴板操作等行为。",
    tags: ["test", "input", "component"],
    complexity: "complex"
  },
  "packages/tui/test/key-tester.ts": {
    summary: "键盘事件测试工具，拦截并记录所有终端按键输入及其协议类型，用于调试键盘映射。",
    tags: ["test", "keyboard", "debug-tool"],
    complexity: "moderate"
  },
  "packages/tui/test/keybindings.test.ts": {
    summary: "快捷键绑定系统的测试，验证 KeybindingsManager 的绑定、冲突检测和查找功能。",
    tags: ["test", "keybindings", "unit"],
    complexity: "moderate"
  },
  "packages/tui/test/keys.test.ts": {
    summary: "键盘协议解析的测试套件，覆盖 Kitty 键盘协议、修饰键、按键释放/重复事件等解析场景。",
    tags: ["test", "keyboard", "protocol"],
    complexity: "complex"
  },
  "packages/tui/test/latex.test.ts": {
    summary: "LaTeX 渲染器的测试套件，覆盖希腊字母、分数、上下标、矩阵、运算符等多种数学公式的渲染正确性。",
    tags: ["test", "latex", "rendering"],
    complexity: "complex"
  },
  "packages/tui/test/layout.test.ts": {
    summary: "布局引擎的测试套件，验证 HStack/VStack 布局、ScrollView 滚动及组件尺寸计算的正确性。",
    tags: ["test", "layout", "component"],
    complexity: "complex"
  }
};

// Determine significance for function/class nodes
function isSignificantFunction(fn) {
  return (fn.endLine - fn.startLine + 1) >= 10;
}
function isSignificantClass(cls) {
  const lines = cls.endLine - cls.startLine + 1;
  return cls.methods.length >= 2 || lines >= 20;
}

// Function summaries
const fnSummaries = {
  // latex.ts
  "replaceCharacters": "对字符串执行多字符替换映射。",
  "formatScript": "格式化上标或下标文本。",
  "normalizeOutput": "规范化 LaTeX 渲染输出，清理多余空格。",
  "joinLayouts": "将多个布局节点垂直拼接为单一布局。",
  "renderLayout": "将解析后的 LaTeX 节点树渲染为二维布局字符画。",
  "renderLatex": "将 LaTeX 源字符串渲染为终端多行文本输出。",
  // layout.ts
  "renderCached": "缓存组件的渲染结果以避免重复计算。",
  "layoutComponent": "核心布局函数，递归计算组件的位置、尺寸和裁剪区域。",
  "styleScrollbarCell": "为滚动条单元格应用样式。",
  "getScrollbarGeometry": "计算滚动条的几何位置和尺寸。",
  "paintScrollbar": "绘制滚动条到屏幕缓冲区。",
  "paintBox": "将布局盒子的渲染行绘制到屏幕缓冲区。",
  "renderLayoutFrame": "渲染布局帧，将组件树转换为可绘制的屏幕行。",
  "getScrollViewBox": "获取 ScrollView 组件对应的布局盒子。",
  "getScrollViewsAt": "查找指定坐标处的所有 ScrollView 组件。",
  // native-modifiers.ts
  "loadNativeModifiersHelper": "动态加载 native 修饰键检测 addon。",
  // stdin-buffer.ts
  "isCompleteSequence": "检测缓冲区数据是否构成完整的转义序列。",
  "isCompleteCsiSequence": "检测 CSI 转义序列是否完整。",
  "isCompleteOscSequence": "检测 OSC 转义序列是否完整。",
  "isCompleteDcsSequence": "检测 DCS 转义序列是否完整。",
  "isCompleteApcSequence": "检测 APC 转义序列是否完整。",
  "extractCompleteSequences": "从缓冲区中提取所有完整的转义序列。",
  // terminal-colors.ts
  "parseOscHexChannel": "解析 OSC 响应中的十六进制颜色通道值。",
  "parseOsc11BackgroundColor": "解析 OSC 11 响应获取终端背景色。",
  // terminal-image.ts
  "probeTmuxHyperlinks": "检测 tmux 是否支持超链接。",
  "detectCapabilities": "检测终端图像协议能力（Kitty/iTerm2）。",
  "encodeKitty": "将 base64 图像数据编码为 Kitty 图形协议转义序列。",
  "encodeITerm2": "将 base64 图像数据编码为 iTerm2 内联图像转义序列。",
  "getKittyImagePlacement": "解析 Kitty 图像放置信息。",
  "cropKittyImageLine": "裁剪 Kitty 图像行以适配可见区域。",
  "calculateImageCellSize": "计算图像在终端中占用的单元格尺寸。",
  "getPngDimensions": "从 PNG base64 数据中解析图像尺寸。",
  "getJpegDimensions": "从 JPEG base64 数据中解析图像尺寸。",
  "getGifDimensions": "从 GIF base64 数据中解析图像尺寸。",
  "getWebpDimensions": "从 WebP base64 数据中解析图像尺寸。",
  "getImageDimensions": "根据 MIME 类型解析图像尺寸。",
  "renderImage": "渲染图像到终端，自动选择 Kitty 或 iTerm2 协议。",
  "imageFallback": "当图像协议不可用时生成文本占位符。",
  // terminal.ts
  "parseKeyboardProtocolNegotiationSequence": "解析键盘协议协商转义序列。",
  "resolveEscapeTimeoutMs": "解析转义序列超时配置。",
  // tui-main-screen.ts
  "parseKittyImageHeader": "解析终端行中的 Kitty 图像头部信息。",
  // tui.ts
  "parseSizeValue": "解析尺寸值（百分比或绝对值）为像素数。",
  "compositeTuiLine": "将 overlay 行合成到基础行上。",
  // utils.ts
  "couldBeEmoji": "检测字符串片段是否可能是 emoji。",
  "truncateFragmentToWidth": "将文本片段截断到指定显示宽度。",
  "finalizeTruncatedResult": "完成截断结果，添加省略号和对齐。",
  "graphemeWidth": "计算单个字素单元的显示宽度。",
  "visibleWidth": "计算含 ANSI 转义序列的字符串的可见显示宽度。",
  "stripTerminalSequences": "移除字符串中的所有终端转义序列。",
  "getGraphemeCellRange": "获取指定列位置处字素的单元格范围。",
  "getOsc8LinkAtColumn": "获取指定列位置处的 OSC 8 超链接。",
  "normalizeTerminalOutput": "规范化终端输出文本。",
  "extractAnsiCode": "从字符串中提取 ANSI 转义代码。",
  "parseOsc8Hyperlink": "解析 OSC 8 超链接转义序列。",
  "getActiveOsc8Close": "获取当前活跃的 OSC 8 关闭序列。",
  "updateTrackerFromText": "更新 ANSI 代码追踪器的文本状态。",
  "splitIntoTokensWithAnsi": "将含 ANSI 代码的文本拆分为标记序列。",
  "wrapTextWithAnsi": "对含 ANSI 转义序列的文本进行换行处理。",
  "wrapSingleLine": "对单行文本进行宽度换行处理。",
  "breakLongWord": "将超长单词在指定宽度处断开。",
  "applyBackgroundToLine": "为整行应用背景色。",
  "truncateToWidth": "将文本截断到指定显示宽度，支持省略号。",
  "sliceWithWidth": "按列切片并计算宽度的文本截取。",
  "extractSegments": "从文本行中提取 Unicode 字素段。",
  // word-navigation.ts
  "findWordBackward": "向前（左）搜索词边界位置。",
  "findWordForward": "向后（右）搜索词边界位置。",
  // test files
  "resolveFdPath": "解析文件描述符路径用于测试。",
  "setupFolder": "设置临时测试文件夹结构。",
  "applyCompletion": "应用自动补全建议到编辑器。",
  "withEnv": "设置测试环境变量。",
  "withEnvVars": "设置多个测试环境变量。"
};

// Class summaries
const classSummaries = {
  "KillRing": "Emacs 风格 kill ring 环形缓冲区，支持 push/peek/rotate 操作和连续删除累积。",
  "LatexParser": "LaTeX 数学公式递归下降解析器，支持命令、环境、分数、矩阵、上下标等语法结构。",
  "StdinBuffer": "标准输入序列缓冲器，累积分片数据直到检测到完整转义序列后发射。",
  "ProcessTerminal": "终端进程控制类，管理 raw 模式、Kitty 键盘协议、鼠标事件、光标和进度条。",
  "TuiAltScreen": "备用屏幕 TUI 类，实现完整交替屏幕渲染、选择、搜索、滚动和图像管理。",
  "TuiMainScreen": "主屏幕 TUI 类，实现差量渲染和 Kitty 图像行管理。",
  "Container": "TUI 组件容器基类，管理子组件的添加、移除和渲染失效。",
  "UndoStack": "泛型撤销栈，使用深拷贝存储状态快照。",
  "AnsiCodeTracker": "ANSI 转义代码状态追踪器，跟踪当前活跃的文本样式和颜色。",
  "KeyLogger": "测试用键盘事件记录器，捕获并显示所有按键及其协议类型。"
};

// Function tags
const fnTags = {
  "replaceCharacters": ["utility", "string", "text-processing"],
  "formatScript": ["utility", "formatting", "latex"],
  "normalizeOutput": ["utility", "formatting", "latex"],
  "joinLayouts": ["layout", "utility", "latex"],
  "renderLayout": ["rendering", "latex", "layout"],
  "renderLatex": ["rendering", "latex", "entry-point"],
  "renderCached": ["rendering", "cache", "layout"],
  "layoutComponent": ["layout", "rendering", "core"],
  "styleScrollbarCell": ["rendering", "scrollbar", "layout"],
  "getScrollbarGeometry": ["layout", "scrollbar", "geometry"],
  "paintScrollbar": ["rendering", "scrollbar", "layout"],
  "paintBox": ["rendering", "layout", "terminal-art"],
  "renderLayoutFrame": ["rendering", "layout", "entry-point"],
  "getScrollViewBox": ["layout", "scroll-view", "query"],
  "getScrollViewsAt": ["layout", "scroll-view", "hit-test"],
  "loadNativeModifiersHelper": ["native-addon", "keyboard", "loader"],
  "isCompleteSequence": ["parsing", "terminal", "validation"],
  "isCompleteCsiSequence": ["parsing", "terminal", "validation"],
  "isCompleteOscSequence": ["parsing", "terminal", "validation"],
  "isCompleteDcsSequence": ["parsing", "terminal", "validation"],
  "isCompleteApcSequence": ["parsing", "terminal", "validation"],
  "extractCompleteSequences": ["parsing", "terminal", "buffer"],
  "parseOscHexChannel": ["parsing", "color", "utility"],
  "parseOsc11BackgroundColor": ["parsing", "color", "terminal"],
  "probeTmuxHyperlinks": ["terminal", "detection", "image"],
  "detectCapabilities": ["terminal", "detection", "image"],
  "encodeKitty": ["encoding", "image", "kitty-protocol"],
  "encodeITerm2": ["encoding", "image", "iterm2-protocol"],
  "getKittyImagePlacement": ["parsing", "image", "kitty-protocol"],
  "cropKittyImageLine": ["image", "cropping", "kitty-protocol"],
  "calculateImageCellSize": ["image", "geometry", "layout"],
  "getPngDimensions": ["image", "parsing", "png"],
  "getJpegDimensions": ["image", "parsing", "jpeg"],
  "getGifDimensions": ["image", "parsing", "gif"],
  "getWebpDimensions": ["image", "parsing", "webp"],
  "getImageDimensions": ["image", "parsing", "utility"],
  "renderImage": ["rendering", "image", "entry-point"],
  "imageFallback": ["image", "fallback", "utility"],
  "parseKeyboardProtocolNegotiationSequence": ["parsing", "keyboard-protocol", "terminal"],
  "resolveEscapeTimeoutMs": ["configuration", "terminal", "utility"],
  "parseKittyImageHeader": ["parsing", "image", "kitty-protocol"],
  "parseSizeValue": ["utility", "layout", "geometry"],
  "compositeTuiLine": ["rendering", "overlay", "compositing"],
  "couldBeEmoji": ["utility", "unicode", "detection"],
  "truncateFragmentToWidth": ["text-processing", "truncation", "unicode"],
  "finalizeTruncatedResult": ["text-processing", "truncation", "formatting"],
  "graphemeWidth": ["utility", "unicode", "width"],
  "visibleWidth": ["utility", "unicode", "ansi", "width"],
  "stripTerminalSequences": ["utility", "ansi", "text-processing"],
  "getGraphemeCellRange": ["utility", "unicode", "layout"],
  "getOsc8LinkAtColumn": ["utility", "hyperlink", "osc8"],
  "normalizeTerminalOutput": ["utility", "terminal", "normalization"],
  "extractAnsiCode": ["parsing", "ansi", "utility"],
  "parseOsc8Hyperlink": ["parsing", "hyperlink", "osc8"],
  "getActiveOsc8Close": ["utility", "hyperlink", "osc8"],
  "updateTrackerFromText": ["ansi", "tracking", "state"],
  "splitIntoTokensWithAnsi": ["parsing", "ansi", "text-processing"],
  "wrapTextWithAnsi": ["text-processing", "wrapping", "ansi"],
  "wrapSingleLine": ["text-processing", "wrapping", "utility"],
  "breakLongWord": ["text-processing", "wrapping", "utility"],
  "applyBackgroundToLine": ["rendering", "terminal", "color"],
  "truncateToWidth": ["text-processing", "truncation", "unicode"],
  "sliceWithWidth": ["text-processing", "slicing", "unicode"],
  "extractSegments": ["utility", "unicode", "parsing"],
  "findWordBackward": ["navigation", "text-editing", "utility"],
  "findWordForward": ["navigation", "text-editing", "utility"],
  "resolveFdPath": ["test", "utility", "filesystem"],
  "setupFolder": ["test", "utility", "filesystem"],
  "applyCompletion": ["test", "autocomplete", "editor"],
  "withEnv": ["test", "utility", "environment"],
  "withEnvVars": ["test", "utility", "environment"]
};

const classTags = {
  "KillRing": ["data-structure", "text-editing", "kill-ring"],
  "LatexParser": ["parser", "latex", "rendering"],
  "StdinBuffer": ["buffer", "terminal", "event-handler"],
  "ProcessTerminal": ["terminal", "keyboard-protocol", "event-handler"],
  "TuiAltScreen": ["tui", "rendering", "terminal", "component"],
  "TuiMainScreen": ["tui", "rendering", "differential-render"],
  "Container": ["component", "tui", "container"],
  "UndoStack": ["data-structure", "undo", "utility"],
  "AnsiCodeTracker": ["ansi", "state-tracking", "terminal"],
  "KeyLogger": ["test", "keyboard", "debug-tool"]
};

function getFnComplexity(fn) {
  const lines = fn.endLine - fn.startLine + 1;
  if (lines >= 60) return "complex";
  if (lines >= 25) return "moderate";
  return "simple";
}

function getClassComplexity(cls) {
  const lines = cls.endLine - cls.startLine + 1;
  if (lines >= 400) return "complex";
  if (lines >= 100) return "complex";
  if (lines >= 50) return "moderate";
  return "simple";
}

// Process each file
const resultMap = {};
for (const r of extract.results) {
  resultMap[r.path] = r;
}

for (const r of extract.results) {
  const meta = fileMeta[r.path];
  if (!meta) {
    console.error("No meta for:", r.path);
    continue;
  }

  // File node
  const nodeType = r.path.includes('/test/') ? 'file' : 'file';
  nodes.push({
    id: `file:${r.path}`,
    type: nodeType,
    name: r.path.split('/').pop(),
    filePath: r.path,
    summary: meta.summary,
    tags: meta.tags,
    complexity: meta.complexity,
    ...(meta.languageNotes ? { languageNotes: meta.languageNotes } : {})
  });

  // Class nodes
  if (r.classes) {
    for (const cls of r.classes) {
      if (!isSignificantClass(cls)) continue;
      const summary = classSummaries[cls.name] || `${cls.name} 类。`;
      const tags = classTags[cls.name] || ["class", "component"];
      nodes.push({
        id: `class:${r.path}:${cls.name}`,
        type: "class",
        name: cls.name,
        filePath: r.path,
        lineRange: [cls.startLine, cls.endLine],
        summary,
        tags,
        complexity: getClassComplexity(cls)
      });
      // contains edge
      edges.push({
        source: `file:${r.path}`,
        target: `class:${r.path}:${cls.name}`,
        type: "contains",
        direction: "forward",
        weight: 1.0
      });
      // exports edge if exported
      const isExported = r.exports?.some(e => e.name === cls.name);
      if (isExported) {
        edges.push({
          source: `file:${r.path}`,
          target: `class:${r.path}:${cls.name}`,
          type: "exports",
          direction: "forward",
          weight: 0.8
        });
      }
    }
  }

  // Function nodes
  if (r.functions) {
    for (const fn of r.functions) {
      if (!isSignificantFunction(fn)) continue;
      const summary = fnSummaries[fn.name] || `${fn.name} 函数。`;
      const tags = fnTags[fn.name] || ["function", "utility"];
      nodes.push({
        id: `function:${r.path}:${fn.name}`,
        type: "function",
        name: fn.name,
        filePath: r.path,
        lineRange: [fn.startLine, fn.endLine],
        summary,
        tags,
        complexity: getFnComplexity(fn)
      });
      // contains edge
      edges.push({
        source: `file:${r.path}`,
        target: `function:${r.path}:${fn.name}`,
        type: "contains",
        direction: "forward",
        weight: 1.0
      });
      // exports edge if exported
      const isExported = r.exports?.some(e => e.name === fn.name);
      if (isExported) {
        edges.push({
          source: `file:${r.path}`,
          target: `function:${r.path}:${fn.name}`,
          type: "exports",
          direction: "forward",
          weight: 0.8
        });
      }
    }
  }
}

// Import edges from batchImportData
let importEdgeCount = 0;
for (const [filePath, imports] of Object.entries(dispatch.batchImportData)) {
  for (const target of imports) {
    edges.push({
      source: `file:${filePath}`,
      target: `file:${target}`,
      type: "imports",
      direction: "forward",
      weight: 0.7
    });
    importEdgeCount++;
  }
}

// tested_by edges: test files -> production files
const testedByMap = {
  "packages/tui/test/autocomplete.test.ts": ["packages/tui/src/autocomplete.ts"],
  "packages/tui/test/editor-history-keybindings.test.ts": ["packages/tui/src/components/editor.ts", "packages/tui/src/keybindings.ts"],
  "packages/tui/test/editor.test.ts": ["packages/tui/src/components/editor.ts", "packages/tui/src/utils.ts"],
  "packages/tui/test/fuzzy.test.ts": ["packages/tui/src/fuzzy.ts"],
  "packages/tui/test/input.test.ts": ["packages/tui/src/components/input.ts", "packages/tui/src/utils.ts"],
  "packages/tui/test/keybindings.test.ts": ["packages/tui/src/keybindings.ts"],
  "packages/tui/test/keys.test.ts": ["packages/tui/src/keys.ts"],
  "packages/tui/test/latex.test.ts": ["packages/tui/src/latex.ts"],
  "packages/tui/test/layout.test.ts": ["packages/tui/src/layout.ts", "packages/tui/src/utils.ts"]
};

for (const [testFile, prodFiles] of Object.entries(testedByMap)) {
  for (const prodFile of prodFiles) {
    edges.push({
      source: `file:${prodFile}`,
      target: `file:${testFile}`,
      type: "tested_by",
      direction: "forward",
      weight: 0.5
    });
  }
}

console.error(`Total nodes: ${nodes.length}`);
console.error(`Total edges: ${edges.length}`);
console.error(`Import edges: ${importEdgeCount}`);

// Split into parts
const allFiles = extract.results.map(r => r.path).sort();
const nodeCount = nodes.length;
const edgeCount = edges.length;

let parts = 1;
if (nodeCount > 60 || edgeCount > 120) {
  parts = Math.ceil(Math.max(nodeCount / 60, edgeCount / 120));
}

const filesPerPart = Math.ceil(allFiles.length / parts);
const fileChunks = [];
for (let i = 0; i < allFiles.length; i += filesPerPart) {
  fileChunks.push(new Set(allFiles.slice(i, i + filesPerPart)));
}

for (let k = 0; k < fileChunks.length; k++) {
  const chunk = fileChunks[k];
  const partNodes = nodes.filter(n => {
    if (n.filePath) return chunk.has(n.filePath);
    return false;
  });
  const partNodeIds = new Set(partNodes.map(n => n.id));
  const partEdges = edges.filter(e => partNodeIds.has(e.source));

  const output = { nodes: partNodes, edges: partEdges };
  const partName = parts === 1
    ? `batch-24.json`
    : `batch-24-part-${k + 1}.json`;
  writeFileSync(`/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/${partName}`, JSON.stringify(output, null, 2));
  console.error(`Wrote ${partName}: ${partNodes.length} nodes, ${partEdges.length} edges`);
}
