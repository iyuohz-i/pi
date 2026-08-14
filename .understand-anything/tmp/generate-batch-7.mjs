import { readFileSync, writeFileSync } from 'fs';

const extract = JSON.parse(readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/ua-file-extract-results-7.json', 'utf8'));
const dispatch = JSON.parse(readFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/tmp/dispatch-batch-7.json', 'utf8'));

const batchImportData = dispatch.batchImportData;

// Sort files alphabetically
const sortedFiles = [...extract.results].sort((a, b) => a.path.localeCompare(b.path));

// Split into 2 parts
const mid = Math.ceil(sortedFiles.length / 2);
const part1Files = sortedFiles.slice(0, mid);
const part2Files = sortedFiles.slice(mid);

// Helper: get summary for a test file based on its name and imports
function getFileSummary(filePath, imports) {
  const base = filePath.split('/').pop().replace('.test.ts', '');
  const srcImports = imports.filter(p => p.includes('/src/'));

  if (base === 'stream') return '核心流式和完成 API 的综合测试套件，覆盖文本生成、工具调用、流式传输、思考链、图像处理和多轮对话等场景。';
  if (base === 'tokens') return '测试 LLM 流式请求在中途终止时的 token 计数和费用统计正确性。';
  if (base === 'total-tokens') return '验证多供应商 LLM 响应中 totalTokens 字段与各 token 分量之和的一致性，包括缓存读写场景。';
  if (base === 'unicode-surrogate') return '测试包含 emoji、LinkedIn 真实数据和未配对高代理项的 Unicode 代理对在工具结果和消息中的正确处理。';
  if (base === 'tool-call-id-normalization') return '验证不同供应商 API 对 tool call ID 的标准化处理，确保跨供应商的 ID 格式一致性。';
  if (base === 'tool-call-without-result') return '测试当工具调用缺少结果时，多轮对话中 agent 的容错处理能力。';
  if (base === 'provider-error-body-regression') return '回归测试，验证 Bedrock、OpenAI Completions 和 OpenAI Responses 三个 API 在错误响应体透传方面的一致性。';
  if (base === 'openai-responses-terminal-event') return '测试 OpenAI Responses API 流的终端事件处理，验证流结束时的正确终止行为。';
  if (base === 'openai-responses-namespace') return '测试 OpenAI Responses API 的命名空间隔离和消息转换逻辑。';
  if (base === 'openai-responses-reasoning-replay-e2e') return '端到端测试 OpenAI Responses API 的推理（reasoning）重放功能。';
  if (base === 'openai-responses-partial-json-cleanup') return '测试 OpenAI Responses API 流中部分 JSON 片段的清理和修复逻辑。';
  if (base === 'openai-responses-tool-result-images') return '验证 OpenAI Responses API 在工具调用结果中保留图像数据的功能。';
  if (base === 'openai-responses-foreign-toolcall-id') return '测试 OpenAI Responses API 对外来（非原生）tool call ID 的处理和哈希标准化。';
  if (base === 'openai-responses-message-id') return '测试 OpenAI Responses API 消息 ID 的生成和传递正确性。';
  if (base === 'overflow') return '测试上下文溢出检测和长度恢复逻辑，验证错误消息的识别和处理。';
  if (base === 'pi-messages') return '测试 Pi 自定义消息 API 的流式和完成端点，使用本地 mock 服务器验证请求/响应格式。';
  if (base === 'provider-error-body-passthrough') return '测试供应商 API 错误响应体的透传行为，确保错误信息正确传递给调用方。';
  if (base === 'provider-retry') return '测试供应商请求重试逻辑，验证可重试错误的识别和重试计数。';
  if (base === 'qwen-token-plan-models') return '测试 Qwen 通义千问 token 计划模型的注册和可用性。';
  if (base === 'responseid') return '验证各供应商 LLM 响应中 responseId 字段的存在性和类型正确性。';
  if (base === 'retry') return '测试 assistant 调用的重试机制，使用 faux provider 模拟可重试错误。';
  if (base === 'sampling-options') return '测试采样参数（temperature、topP 等）在不同供应商 API 中的正确传递。';
  if (base === 'supports-xhigh') return '测试模型是否正确报告对 xhigh 推理级别的支持。';
  if (base === 'telemetry-options') return '测试遥测选项配置，验证模型参数构建和图像 API 注册逻辑。';
  if (base === 'together-models') return '测试 Together AI 模型的注册和 API 密钥环境变量解析。';
  if (base === 'transform-messages-copilot-openai-to-anthropic') return '测试从 Copilot OpenAI 消息格式到 Anthropic 消息格式的转换逻辑。';
  if (base === 'uuid') return '测试 uuidv7 生成器的时间戳可解析性和唯一性。';
  if (base === 'validation') return '测试工具调用验证逻辑，包括 schema 验证和参数校验。';
  if (base === 'xhigh') return '测试 xhigh 推理级别的配置和模型行为。';
  if (base === 'xiaomi-models') return '测试小米模型在供应商列表中的注册。';
  if (base === 'xiaomi-token-plan-ams-anthropic-empty-signature-smoke') return '冒烟测试小米 token 计划 AMS Anthropic 端点在空签名场景下的行为。';
  if (base === 'zen') return '测试 Zen 模型的基本流式生成功能。';
  if (base === 'openrouter-cache-control-models') return '测试 OpenRouter 缓存控制模型的注册。';
  if (base === 'openrouter-cache-write-repro') return 'OpenRouter 缓存写入行为的复现测试，验证长系统提示的缓存写入。';
  if (base === 'openrouter-images') return '测试 OpenRouter 图像生成 API 的调用和响应处理。';

  return `测试 ${base} 功能的测试文件。`;
}

function getTags(filePath) {
  const base = filePath.split('/').pop().replace('.test.ts', '');
  const tags = ['test'];

  if (['stream', 'tokens', 'total-tokens', 'unicode-surrogate', 'tool-call-without-result', 'multiTurn'].some(k => base.includes(k))) {
    tags.push('integration');
  }
  if (['retry', 'provider-retry', 'provider-error-body-passthrough', 'provider-error-body-regression', 'overflow'].some(k => base.includes(k))) {
    tags.push('error-handling');
  }
  if (base.includes('openai-responses') || base.includes('openrouter')) {
    tags.push('openai');
  }
  if (base.includes('stream') || base.includes('tokens') || base.includes('total-tokens')) {
    tags.push('streaming');
  }
  if (base.includes('tool-call')) {
    tags.push('tool-call');
  }
  if (base.includes('model') || base === 'supports-xhigh' || base === 'xhigh' || base === 'zen') {
    tags.push('model-registry');
  }
  if (['validation', 'uuid', 'responseid', 'sampling-options'].includes(base)) {
    tags.push('validation');
  }
  if (['transform-messages-copilot-openai-to-anthropic', 'pi-messages'].some(k => base.includes(k))) {
    tags.push('message-transform');
  }
  if (base.includes('image')) {
    tags.push('image');
  }
  if (base.includes('telemetry')) {
    tags.push('telemetry');
  }
  if (tags.length < 3) tags.push('unit');

  return tags.slice(0, 5);
}

function getComplexity(nonEmptyLines) {
  if (nonEmptyLines < 50) return 'simple';
  if (nonEmptyLines < 200) return 'moderate';
  return 'complex';
}

// Significance filter for functions
function isSignificantFunction(fn) {
  return (fn.endLine - fn.startLine + 1) >= 10;
}

function isSignificantClass(cls) {
  return (cls.methods && cls.methods.length >= 2) || (cls.endLine - cls.startLine + 1) >= 20;
}

// Function summary generator
function getFunctionSummary(fnName, filePath) {
  const summaries = {
    'createOutput': '创建测试用的 OpenAI Responses API 输出对象，包含模型和时间戳。',
    'createModel': '创建测试用的模型配置对象，用于流式或完成 API 调用。',
    'verifyToolResultImagesStayInFunctionCallOutput': '验证工具调用结果中的图像数据在多轮对话中被正确保留在 function_call_output 中。',
    'createErrorMessage': '构造上下文溢出或长度超限的模拟错误消息，用于测试溢出检测逻辑。',
    'startServer': '启动本地 HTTP mock 服务器，用于拦截和验证 Pi 消息 API 的请求/响应。',
    'expectResponseId': '执行 LLM 完成调用并验证响应中 responseId 字段的存在性和类型。',
    'makeCompletionsModel': '创建使用 OpenAI Completions API 格式的测试模型配置。',
    'makeAnthropicModel': '创建使用 Anthropic API 格式的测试模型配置。',
    'capturePayload': '执行流式调用并捕获发送给供应商的请求 payload，用于验证采样参数。',
    'basicTextGeneration': '测试基本文本生成，验证响应角色、内容、usage 统计和多轮对话。',
    'handleToolCall': '测试流式工具调用，验证工具调用事件的开始、增量和结束事件序列。',
    'handleStreaming': '测试流式文本生成，验证文本块的开始、增量和完成事件。',
    'handleThinking': '测试流式思考链（thinking）生成，验证思考块的事件序列。',
    'handleImage': '测试图像输入处理，验证模型能正确识别和描述图像内容。',
    'multiTurn': '测试多轮对话场景，包含工具调用、思考链和文本生成的完整流程。',
    'completedStream': '创建预完成的流式响应，用于测试遥测选项和模型参数构建。',
    'testTokensOnAbort': '测试流式请求在中途终止时的 token 计数和费用统计正确性。',
    'testToolCallWithoutResult': '测试当工具调用缺少结果时，后续对话轮次的容错处理。',
    'testTotalTokensWithCache': '验证带缓存的 LLM 响应中 totalTokens 与各 token 分量之和的一致性。',
    'makeCopilotClaudeModel': '创建模拟 Copilot Claude 模型配置，用于消息格式转换测试。',
    'makeAssistantMessage': '构造包含工具调用的 assistant 消息，用于消息转换测试。',
    'testEmojiInToolResults': '测试包含 emoji 的工具结果在多轮对话中的正确处理。',
    'testRealWorldLinkedInData': '测试包含真实 LinkedIn 数据（含特殊 Unicode 字符）的工具结果处理。',
    'testUnpairedHighSurrogate': '测试未配对高代理项 Unicode 字符在 LLM 请求中的处理。',
    'createToolCallWithPlainSchema': '创建带 plain schema 的工具调用对象，用于验证工具调用参数校验。',
    'makeContext': '创建测试用的对话上下文，包含随机消息以避免缓存命中。',
    'makeInitialContext': '创建初始对话上下文，用于冒烟测试 thinking 重放。',
    'captureReplayPayload': '执行流式调用并捕获重放 payload，用于验证 thinking 块的签名处理。',
  };
  return summaries[fnName] || `测试辅助函数 ${fnName}。`;
}

// Build nodes and edges for a set of files
function buildPart(files) {
  const nodes = [];
  const edges = [];

  for (const file of files) {
    const filePath = file.path;
    const imports = batchImportData[filePath] || [];

    // File node
    nodes.push({
      id: `file:${filePath}`,
      type: 'file',
      name: filePath.split('/').pop(),
      filePath,
      summary: getFileSummary(filePath, imports),
      tags: getTags(filePath),
      complexity: getComplexity(file.nonEmptyLines),
    });

    // Function nodes
    if (file.functions) {
      for (const fn of file.functions) {
        if (!isSignificantFunction(fn)) continue;
        const fnId = `function:${filePath}:${fn.name}`;
        nodes.push({
          id: fnId,
          type: 'function',
          name: fn.name,
          filePath,
          lineRange: [fn.startLine, fn.endLine],
          summary: getFunctionSummary(fn.name, filePath),
          tags: ['test', 'test-helper'],
          complexity: getComplexity(fn.endLine - fn.startLine + 1),
        });
        // contains edge
        edges.push({
          source: `file:${filePath}`,
          target: fnId,
          type: 'contains',
          direction: 'forward',
          weight: 1.0,
        });
      }
    }

    // Class nodes
    if (file.classes) {
      for (const cls of file.classes) {
        if (!isSignificantClass(cls)) continue;
        const clsId = `class:${filePath}:${cls.name}`;
        nodes.push({
          id: clsId,
          type: 'class',
          name: cls.name,
          filePath,
          lineRange: [cls.startLine, cls.endLine],
          summary: `测试辅助类 ${cls.name}，用于模拟 API 错误或捕获 payload。`,
          tags: ['test', 'test-helper'],
          complexity: getComplexity(cls.endLine - cls.startLine + 1),
        });
        edges.push({
          source: `file:${filePath}`,
          target: clsId,
          type: 'contains',
          direction: 'forward',
          weight: 1.0,
        });
      }
    }

    // Import edges (1:1)
    for (const imp of imports) {
      edges.push({
        source: `file:${filePath}`,
        target: `file:${imp}`,
        type: 'imports',
        direction: 'forward',
        weight: 0.7,
      });
    }

    // tested_by edges (from src files to this test file)
    for (const imp of imports) {
      if (imp.includes('/src/')) {
        edges.push({
          source: `file:${imp}`,
          target: `file:${filePath}`,
          type: 'tested_by',
          direction: 'forward',
          weight: 0.5,
        });
      }
    }
  }

  return { nodes, edges };
}

const part1 = buildPart(part1Files);
const part2 = buildPart(part2Files);

writeFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-7-part-1.json', JSON.stringify(part1, null, 2));
writeFileSync('/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-7-part-2.json', JSON.stringify(part2, null, 2));

console.log(`Part 1: ${part1.nodes.length} nodes, ${part1.edges.length} edges (${part1Files.length} files)`);
console.log(`Part 2: ${part2.nodes.length} nodes, ${part2.edges.length} edges (${part2Files.length} files)`);
console.log(`Total: ${part1.nodes.length + part2.nodes.length} nodes, ${part1.edges.length + part2.edges.length} edges`);

// Verify import edge count
let totalImports = 0;
for (const f of sortedFiles) {
  totalImports += (batchImportData[f.path] || []).length;
}
console.log(`Expected imports edges: ${totalImports}`);
let actualImports = 0;
for (const e of [...part1.edges, ...part2.edges]) {
  if (e.type === 'imports') actualImports++;
}
console.log(`Actual imports edges: ${actualImports}`);
