const fs = require('fs');
const dispatch = JSON.parse(fs.readFileSync('.understand-anything/tmp/dispatch-batch-13.json','utf8'));
const extract = JSON.parse(fs.readFileSync('.understand-anything/tmp/ua-file-extract-results-13.json','utf8'));
const batchImportData = dispatch.batchImportData;

const nodes = [];
const edges = [];

// === FILE NODES ===
const fileDefs = [
  {path:'packages/coding-agent/examples/extensions/git-merge-and-resolve.ts',name:'git-merge-and-resolve.ts',summary:'示例扩展，演示如何通过扩展 API 实现 Git 合并冲突检测与格式化输出。',tags:['extension','git','example','merge-conflict'],complexity:'moderate'},
  {path:'packages/coding-agent/examples/extensions/input-transform-streaming.ts',name:'input-transform-streaming.ts',summary:'示例扩展，演示流式输入转换功能，通过扩展 API 对用户输入进行实时变换。',tags:['extension','input-transform','streaming','example'],complexity:'simple'},
  {path:'packages/coding-agent/examples/extensions/trigger-compact.ts',name:'trigger-compact.ts',summary:'示例扩展，演示如何通过扩展 API 触发会话压缩（compact）操作。',tags:['extension','compact','example','session'],complexity:'simple'},
  {path:'packages/coding-agent/src/bun/cli.ts',name:'cli.ts',summary:'Bun 运行时的 CLI 入口，恢复沙箱环境变量后启动主程序。',tags:['entry-point','bun','cli','sandbox'],complexity:'simple'},
  {path:'packages/coding-agent/src/bun/restore-sandbox-env.ts',name:'restore-sandbox-env.ts',summary:'恢复 Bun 沙箱环境中被清除的环境变量，确保子进程能继承正确的 PATH 等配置。',tags:['bun','sandbox','environment','utility'],complexity:'simple'},
  {path:'packages/coding-agent/src/cli.ts',name:'cli.ts',summary:'CLI 主入口点，初始化配置并调用 main 函数启动编码 agent。',tags:['entry-point','cli','bootstrap'],complexity:'simple'},
  {path:'packages/coding-agent/src/cli/args.ts',name:'args.ts',summary:'解析命令行参数，处理 thinking level、模型选择、会话管理等所有 CLI 选项，并提供帮助信息输出。',tags:['cli','argument-parsing','configuration','validation'],complexity:'complex',languageNotes:'使用手动参数解析，支持大量 flag 和子命令。'},
  {path:'packages/coding-agent/src/cli/auth-check.ts',name:'auth-check.ts',summary:'检查各 LLM 供应商的认证状态，验证 API key 是否有效并返回凭据信息。',tags:['cli','auth','authentication','validation'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/auth-command.ts',name:'auth-command.ts',summary:'处理 auth 子命令的解析与验证逻辑，支持 login/logout 等认证命令的参数处理。',tags:['cli','auth','command-parsing','validation'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/config-selector.ts',name:'config-selector.ts',summary:'提供配置选择器的交互式 UI，允许用户从可用配置列表中选择配置项。',tags:['cli','config','interactive-ui','selector'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/credential-print.ts',name:'credential-print.ts',summary:'解析并打印指定供应商的认证凭据信息，支持 token 过期检查和刷新。',tags:['cli','credential','auth','printing'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/initial-message.ts',name:'initial-message.ts',summary:'根据解析的参数、文件内容和标准输入构建 agent 的初始消息。',tags:['cli','message-builder','initialization'],complexity:'simple'},
  {path:'packages/coding-agent/src/cli/list-models.ts',name:'list-models.ts',summary:'列出所有可用的 LLM 模型，支持按搜索模式过滤，并显示 token 上下文窗口等信息。',tags:['cli','model-listing','llm','search'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/project-trust.ts',name:'project-trust.ts',summary:'创建项目信任上下文，检查项目是否被标记为受信任，管理项目信任设置。',tags:['cli','project-trust','security','configuration'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/session-picker.ts',name:'session-picker.ts',summary:'提供交互式会话选择器，允许用户从当前或所有会话列表中选择要恢复的会话。',tags:['cli','session','interactive-ui','selector'],complexity:'moderate'},
  {path:'packages/coding-agent/src/cli/startup-ui.ts',name:'startup-ui.ts',summary:'管理启动时的终端 UI 初始化，包括主题加载、首次设置向导和交互式输入组件。',tags:['cli','startup','interactive-ui','theme','initialization'],complexity:'complex'},
  {path:'packages/coding-agent/src/config.ts',name:'config.ts',summary:'全局配置模块，提供包目录、路径解析、自更新命令检测、安装方法识别等核心配置功能。',tags:['config','paths','self-update','installation','core'],complexity:'complex',languageNotes:'包含大量路径解析函数和自更新逻辑，支持 npm/bun 等多种安装方式检测。'},
  {path:'packages/coding-agent/src/core/agent-session-runtime.ts',name:'agent-session-runtime.ts',summary:'Agent 会话运行时管理器，负责会话的创建、切换、分支、导入和销毁，协调服务层与底层 AgentSession。',tags:['runtime','session-management','core','agent'],complexity:'complex'},
  {path:'packages/coding-agent/src/core/agent-session-services.ts',name:'agent-session-services.ts',summary:'创建和管理 AgentSession 所需的服务层，包括模型运行时、资源加载器、会话管理器和扩展运行时的初始化。',tags:['service','session','factory','core','agent'],complexity:'complex'},
  {path:'packages/coding-agent/src/core/agent-session.ts',name:'agent-session.ts',summary:'Agent 会话核心实现，管理完整的 agent 交互生命周期，包括消息发送、工具调用、模型切换、压缩、分支、重试、bash 执行和扩展绑定等功能。',tags:['core','agent','session','lifecycle','tool-execution'],complexity:'complex',languageNotes:'超大型类（3000+ 行），包含 100+ 方法，是整个编码 agent 的核心枢纽。'},
  {path:'packages/coding-agent/src/core/auth-guidance.ts',name:'auth-guidance.ts',summary:'提供认证相关的用户引导信息，包括登录帮助和缺失 API key/模型时的错误消息格式化。',tags:['auth','guidance','error-message','core'],complexity:'simple'},
  {path:'packages/coding-agent/src/core/auth-storage.ts',name:'auth-storage.ts',summary:'认证凭据存储模块，提供文件级和内存级存储后端，支持文件锁、并发安全读写和多种存储后端切换。',tags:['auth','storage','file-lock','credential','core'],complexity:'complex',languageNotes:'使用文件锁实现并发安全，支持同步和异步两种锁模式。'},
  {path:'packages/coding-agent/src/core/bash-executor.ts',name:'bash-executor.ts',summary:'Bash 命令执行器，封装 bash 工具操作的执行逻辑，包括命令执行、输出截断和 ANSI 处理。',tags:['bash','executor','command-execution','core'],complexity:'moderate'},
  {path:'packages/coding-agent/src/core/cache-stats.ts',name:'cache-stats.ts',summary:'缓存统计模块，检测 LLM 请求中的缓存命中/未命中情况，计算缓存浪费并收集缓存未命中事件。',tags:['cache','statistics','llm','analytics','core'],complexity:'moderate'},
  {path:'packages/coding-agent/src/core/defaults.ts',name:'defaults.ts',summary:'定义默认 thinking level 等核心默认配置常量。',tags:['defaults','constants','core'],complexity:'simple'},
  {path:'packages/coding-agent/src/core/diagnostics.ts',name:'diagnostics.ts',summary:'诊断工具模块，提供运行时诊断信息的收集与输出功能。',tags:['diagnostics','debugging','core'],complexity:'simple'},
  {path:'packages/coding-agent/src/core/event-bus.ts',name:'event-bus.ts',summary:'轻量级事件总线，提供发布/订阅模式的事件通信机制，供扩展和核心组件使用。',tags:['event-bus','pubsub','events','core'],complexity:'simple'},
  {path:'packages/coding-agent/src/core/exec.ts',name:'exec.ts',summary:'命令执行封装模块，提供带超时和信号控制的子进程执行功能。',tags:['exec','command-execution','subprocess','core'],complexity:'moderate'},
  {path:'packages/coding-agent/src/core/experimental.ts',name:'experimental.ts',summary:'实验性功能开关模块，控制实验特性的启用状态和工具采样配置。',tags:['experimental','feature-flag','core'],complexity:'simple'},
  {path:'packages/coding-agent/src/core/export-html/index.ts',name:'index.ts',summary:'会话 HTML 导出模块，将会话记录渲染为带主题样式的 HTML 页面，支持自定义颜色派生和工具渲染。',tags:['export','html','session','theme','core'],complexity:'complex'},
  {path:'packages/coding-agent/src/core/extensions/index.ts',name:'index.ts',summary:'扩展模块的 barrel 文件，统一导出扩展系统的所有类型、接口和工厂函数。',tags:['barrel','extension','exports','core'],complexity:'moderate',languageNotes:'154 个 re-export，作为扩展系统的公共 API 入口。'},
  {path:'packages/coding-agent/src/core/extensions/loader.ts',name:'loader.ts',summary:'扩展加载器，负责发现、加载和缓存扩展模块，创建扩展 API 和运行时环境，支持目录扫描和工厂函数加载。',tags:['extension','loader','discovery','caching','core'],complexity:'complex',languageNotes:'支持扩展缓存机制，通过 cacheToken 实现缓存失效控制。'},
  {path:'packages/coding-agent/src/core/extensions/runner.ts',name:'runner.ts',summary:'扩展运行时管理器，绑定扩展核心功能、处理事件分发、管理工具注册和命令解析，是扩展系统的中枢组件。',tags:['extension','runner','event-dispatch','tool-registry','core'],complexity:'complex',languageNotes:'大型类（1000+ 行），包含 40+ 方法，管理扩展生命周期的各个方面。'},
];

for (const fd of fileDefs) {
  const node = {
    id: 'file:' + fd.path,
    type: 'file',
    name: fd.name,
    filePath: fd.path,
    summary: fd.summary,
    tags: fd.tags,
    complexity: fd.complexity
  };
  if (fd.languageNotes) node.languageNotes = fd.languageNotes;
  nodes.push(node);
}

// === FUNCTION/CLASS NODES ===
// Only significant ones per the filter

// git-merge-and-resolve.ts: findConflicts [27-54], formatConflicts [62-71]
nodes.push({id:'function:packages/coding-agent/examples/extensions/git-merge-and-resolve.ts:findConflicts',type:'function',name:'findConflicts',filePath:'packages/coding-agent/examples/extensions/git-merge-and-resolve.ts',lineRange:[27,54],summary:'在指定目录中查找 Git 合并冲突标记，返回冲突块列表。',tags:['git','merge-conflict','detection','utility'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/examples/extensions/git-merge-and-resolve.ts:formatConflicts',type:'function',name:'formatConflicts',filePath:'packages/coding-agent/examples/extensions/git-merge-and-resolve.ts',lineRange:[62,71],summary:'将检测到的冲突块格式化为可读的文本输出。',tags:['git','formatting','merge-conflict'],complexity:'simple'});

// restore-sandbox-env.ts: restoreSandboxEnv [19-36]
nodes.push({id:'function:packages/coding-agent/src/bun/restore-sandbox-env.ts:restoreSandboxEnv',type:'function',name:'restoreSandboxEnv',filePath:'packages/coding-agent/src/bun/restore-sandbox-env.ts',lineRange:[19,36],summary:'恢复 Bun 沙箱环境中被清除的环境变量，确保子进程能继承正确的 PATH 等配置。',tags:['bun','sandbox','environment','utility'],complexity:'simple'});

// args.ts: parseArgs [66-235], printHelp [237-428]
nodes.push({id:'function:packages/coding-agent/src/cli/args.ts:parseArgs',type:'function',name:'parseArgs',filePath:'packages/coding-agent/src/cli/args.ts',lineRange:[66,235],summary:'解析命令行参数数组，返回包含所有选项的解析结果对象，处理模型、会话、工具等配置。',tags:['cli','argument-parsing','configuration'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/cli/args.ts:printHelp',type:'function',name:'printHelp',filePath:'packages/coding-agent/src/cli/args.ts',lineRange:[237,428],summary:'输出 CLI 帮助信息，展示所有可用选项、标志和子命令的用法说明。',tags:['cli','help','documentation'],complexity:'moderate'});

// auth-check.ts: checkProviderAuth [22-53]
nodes.push({id:'function:packages/coding-agent/src/cli/auth-check.ts:checkProviderAuth',type:'function',name:'checkProviderAuth',filePath:'packages/coding-agent/src/cli/auth-check.ts',lineRange:[22,53],summary:'检查指定供应商的认证状态，验证 API key 有效性并返回认证结果。',tags:['cli','auth','validation','provider'],complexity:'moderate'});

// auth-command.ts: parseAuthCommand [47-95], validateAuthCommandArgs [97-117]
nodes.push({id:'function:packages/coding-agent/src/cli/auth-command.ts:parseAuthCommand',type:'function',name:'parseAuthCommand',filePath:'packages/coding-agent/src/cli/auth-command.ts',lineRange:[47,95],summary:'解析 auth 子命令参数，识别 login/logout 操作并提取相关选项。',tags:['cli','auth','command-parsing'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/cli/auth-command.ts:validateAuthCommandArgs',type:'function',name:'validateAuthCommandArgs',filePath:'packages/coding-agent/src/cli/auth-command.ts',lineRange:[97,117],summary:'验证 auth 子命令参数的合法性和完整性。',tags:['cli','auth','validation'],complexity:'simple'});
nodes.push({id:'class:packages/coding-agent/src/cli/auth-command.ts:AuthCommandError',type:'class',name:'AuthCommandError',filePath:'packages/coding-agent/src/cli/auth-command.ts',lineRange:[15,15],summary:'auth 命令解析过程中抛出的错误类。',tags:['error','auth','cli'],complexity:'simple'});

// config-selector.ts: selectConfig [20-56]
nodes.push({id:'function:packages/coding-agent/src/cli/config-selector.ts:selectConfig',type:'function',name:'selectConfig',filePath:'packages/coding-agent/src/cli/config-selector.ts',lineRange:[20,56],summary:'显示交互式配置选择器，返回用户选择的配置项。',tags:['cli','config','interactive-ui'],complexity:'moderate'});

// credential-print.ts: resolveCredentialForPrint [17-87]
nodes.push({id:'function:packages/coding-agent/src/cli/credential-print.ts:resolveCredentialForPrint',type:'function',name:'resolveCredentialForPrint',filePath:'packages/coding-agent/src/cli/credential-print.ts',lineRange:[17,87],summary:'解析指定供应商的凭据用于打印，支持 token 过期检查和自动刷新。',tags:['cli','credential','auth','resolution'],complexity:'moderate'});

// initial-message.ts: buildInitialMessage [20-43]
nodes.push({id:'function:packages/coding-agent/src/cli/initial-message.ts:buildInitialMessage',type:'function',name:'buildInitialMessage',filePath:'packages/coding-agent/src/cli/initial-message.ts',lineRange:[20,43],summary:'根据解析参数、文件内容和标准输入构建 agent 初始消息。',tags:['cli','message-builder','initialization'],complexity:'moderate'});

// list-models.ts: listModels [29-115]
nodes.push({id:'function:packages/coding-agent/src/cli/list-models.ts:listModels',type:'function',name:'listModels',filePath:'packages/coding-agent/src/cli/list-models.ts',lineRange:[29,115],summary:'列出所有可用 LLM 模型，支持搜索过滤和 token 上下文窗口显示。',tags:['cli','model-listing','llm','search'],complexity:'moderate'});

// project-trust.ts: createProjectTrustContext [7-62]
nodes.push({id:'function:packages/coding-agent/src/cli/project-trust.ts:createProjectTrustContext',type:'function',name:'createProjectTrustContext',filePath:'packages/coding-agent/src/cli/project-trust.ts',lineRange:[7,62],summary:'创建项目信任上下文，检查项目信任状态并构建信任管理选项。',tags:['cli','project-trust','security','context'],complexity:'moderate'});

// session-picker.ts: selectSession [15-55]
nodes.push({id:'function:packages/coding-agent/src/cli/session-picker.ts:selectSession',type:'function',name:'selectSession',filePath:'packages/coding-agent/src/cli/session-picker.ts',lineRange:[15,55],summary:'显示交互式会话选择器，允许用户选择当前或历史会话。',tags:['cli','session','interactive-ui','selector'],complexity:'moderate'});

// startup-ui.ts: significant functions
nodes.push({id:'function:packages/coding-agent/src/cli/startup-ui.ts:shouldRunFirstTimeSetup',type:'function',name:'shouldRunFirstTimeSetup',filePath:'packages/coding-agent/src/cli/startup-ui.ts',lineRange:[115,132],summary:'检查是否需要运行首次设置向导，基于设置文件是否存在判断。',tags:['cli','startup','first-time-setup'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/cli/startup-ui.ts:showStartupSelector',type:'function',name:'showStartupSelector',filePath:'packages/coding-agent/src/cli/startup-ui.ts',lineRange:[134,163],summary:'显示启动时的交互式选择器组件，返回用户选择结果。',tags:['cli','startup','interactive-ui','selector'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/cli/startup-ui.ts:showFirstTimeSetup',type:'function',name:'showFirstTimeSetup',filePath:'packages/coding-agent/src/cli/startup-ui.ts',lineRange:[166,205],summary:'显示首次设置向导，引导用户完成初始配置。',tags:['cli','startup','first-time-setup','interactive-ui'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/cli/startup-ui.ts:showStartupInput',type:'function',name:'showStartupInput',filePath:'packages/coding-agent/src/cli/startup-ui.ts',lineRange:[207,239],summary:'显示启动时的交互式输入组件，支持占位符文本。',tags:['cli','startup','interactive-ui','input'],complexity:'moderate'});

// config.ts: significant functions
nodes.push({id:'function:packages/coding-agent/src/config.ts:detectInstallMethod',type:'function',name:'detectInstallMethod',filePath:'packages/coding-agent/src/config.ts',lineRange:[73,94],summary:'检测当前安装方式（npm global、bun 等），返回安装方法枚举。',tags:['config','installation','detection'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/config.ts:getSelfUpdateCommandForMethod',type:'function',name:'getSelfUpdateCommandForMethod',filePath:'packages/coding-agent/src/config.ts',lineRange:[115,187],summary:'根据安装方式返回相应的自更新命令和参数。',tags:['config','self-update','installation'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/config.ts:getGlobalPackageRoots',type:'function',name:'getGlobalPackageRoots',filePath:'packages/coding-agent/src/config.ts',lineRange:[206,249],summary:'获取全局包安装根目录列表，用于路径比较和安装方式检测。',tags:['config','paths','global-installation'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/config.ts:getSelfUpdateCommand',type:'function',name:'getSelfUpdateCommand',filePath:'packages/coding-agent/src/config.ts',lineRange:[315,326],summary:'获取当前安装的自更新命令，整合安装方法检测和命令生成逻辑。',tags:['config','self-update','command'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/config.ts:getPackageDir',type:'function',name:'getPackageDir',filePath:'packages/coding-agent/src/config.ts',lineRange:[367,388],summary:'获取当前包的根目录路径。',tags:['config','paths','package'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/config.ts:getAgentDir',type:'function',name:'getAgentDir',filePath:'packages/coding-agent/src/config.ts',lineRange:[515,521],summary:'获取 agent 配置目录路径。',tags:['config','paths','agent-dir'],complexity:'simple'});

// agent-session-runtime.ts
nodes.push({id:'class:packages/coding-agent/src/core/agent-session-runtime.ts:AgentSessionRuntime',type:'class',name:'AgentSessionRuntime',filePath:'packages/coding-agent/src/core/agent-session-runtime.ts',lineRange:[74,406],summary:'Agent 会话运行时管理器，负责会话的创建、切换、分支、导入和销毁，协调服务层与底层 AgentSession。',tags:['runtime','session-management','core','agent'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/agent-session-runtime.ts:createAgentSessionRuntime',type:'function',name:'createAgentSessionRuntime',filePath:'packages/coding-agent/src/core/agent-session-runtime.ts',lineRange:[414,432],summary:'创建 AgentSessionRuntime 实例的工厂函数。',tags:['factory','runtime','session'],complexity:'simple'});
nodes.push({id:'class:packages/coding-agent/src/core/agent-session-runtime.ts:SessionImportFileNotFoundError',type:'class',name:'SessionImportFileNotFoundError',filePath:'packages/coding-agent/src/core/agent-session-runtime.ts',lineRange:[46,54],summary:'会话导入文件未找到时抛出的错误类。',tags:['error','session','import'],complexity:'simple'});

// agent-session-services.ts
nodes.push({id:'function:packages/coding-agent/src/core/agent-session-services.ts:applyExtensionFlagValues',type:'function',name:'applyExtensionFlagValues',filePath:'packages/coding-agent/src/core/agent-session-services.ts',lineRange:[82,128],summary:'将扩展 flag 值应用到资源加载器，处理扩展配置覆盖。',tags:['extension','config','service'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/agent-session-services.ts:createAgentSessionServices',type:'function',name:'createAgentSessionServices',filePath:'packages/coding-agent/src/core/agent-session-services.ts',lineRange:[135,193],summary:'创建 AgentSession 所需的全部服务，包括模型运行时、资源加载器、会话管理器和扩展运行时。',tags:['factory','service','session','core'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/agent-session-services.ts:createAgentSessionFromServices',type:'function',name:'createAgentSessionFromServices',filePath:'packages/coding-agent/src/core/agent-session-services.ts',lineRange:[202,221],summary:'基于已创建的服务实例化 AgentSession。',tags:['factory','session','service'],complexity:'moderate'});

// agent-session.ts
nodes.push({id:'class:packages/coding-agent/src/core/agent-session.ts:AgentSession',type:'class',name:'AgentSession',filePath:'packages/coding-agent/src/core/agent-session.ts',lineRange:[305,3344],summary:'Agent 会话核心实现类，管理完整的 agent 交互生命周期，包括消息发送、工具调用、模型切换、压缩、分支、重试和扩展绑定。',tags:['core','agent','session','lifecycle'],complexity:'complex',languageNotes:'超大型类（3000+ 行），100+ 方法，是编码 agent 的核心枢纽。'});
nodes.push({id:'function:packages/coding-agent/src/core/agent-session.ts:parseSkillBlock',type:'function',name:'parseSkillBlock',filePath:'packages/coding-agent/src/core/agent-session.ts',lineRange:[129,138],summary:'从文本中解析 skill 块，提取 skill 调用信息。',tags:['parsing','skill','utility'],complexity:'simple'});

// auth-guidance.ts: all small but exported
nodes.push({id:'function:packages/coding-agent/src/core/auth-guidance.ts:getProviderLoginHelp',type:'function',name:'getProviderLoginHelp',filePath:'packages/coding-agent/src/core/auth-guidance.ts',lineRange:[6,12],summary:'返回供应商登录帮助文本。',tags:['auth','guidance','provider'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/core/auth-guidance.ts:formatNoApiKeyFoundMessage',type:'function',name:'formatNoApiKeyFoundMessage',filePath:'packages/coding-agent/src/core/auth-guidance.ts',lineRange:[22,25],summary:'格式化未找到 API key 的错误消息。',tags:['auth','error-message','formatting'],complexity:'simple'});

// auth-storage.ts
nodes.push({id:'class:packages/coding-agent/src/core/auth-storage.ts:FileAuthStorageBackend',type:'class',name:'FileAuthStorageBackend',filePath:'packages/coding-agent/src/core/auth-storage.ts',lineRange:[47,202],summary:'文件级认证存储后端，使用文件锁实现并发安全的读写操作。',tags:['auth','storage','file-lock','backend'],complexity:'complex'});
nodes.push({id:'class:packages/coding-agent/src/core/auth-storage.ts:ReadOnlyAuthStorage',type:'class',name:'ReadOnlyAuthStorage',filePath:'packages/coding-agent/src/core/auth-storage.ts',lineRange:[204,291],summary:'只读认证存储，支持加载、读取和列举凭据但不允许修改。',tags:['auth','storage','readonly'],complexity:'moderate'});
nodes.push({id:'class:packages/coding-agent/src/core/auth-storage.ts:InMemoryAuthStorageBackend',type:'class',name:'InMemoryAuthStorageBackend',filePath:'packages/coding-agent/src/core/auth-storage.ts',lineRange:[293,323],summary:'内存级认证存储后端，用于测试和临时存储场景。',tags:['auth','storage','in-memory','backend'],complexity:'simple'});
nodes.push({id:'class:packages/coding-agent/src/core/auth-storage.ts:AuthStorage',type:'class',name:'AuthStorage',filePath:'packages/coding-agent/src/core/auth-storage.ts',lineRange:[328,491],summary:'认证存储统一接口，封装不同存储后端，提供凭据的 CRUD 操作。',tags:['auth','storage','interface','core'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/auth-storage.ts:readStoredCredential',type:'function',name:'readStoredCredential',filePath:'packages/coding-agent/src/core/auth-storage.ts',lineRange:[497,507],summary:'从存储中读取指定供应商的凭据。',tags:['auth','credential','storage','utility'],complexity:'simple'});

// bash-executor.ts
nodes.push({id:'function:packages/coding-agent/src/core/bash-executor.ts:executeBashWithOperations',type:'function',name:'executeBashWithOperations',filePath:'packages/coding-agent/src/core/bash-executor.ts',lineRange:[50,156],summary:'使用 bash 操作接口执行命令，处理输出截断、ANSI 清理和信号控制。',tags:['bash','executor','command-execution'],complexity:'complex'});

// cache-stats.ts
nodes.push({id:'function:packages/coding-agent/src/core/cache-stats.ts:detectMiss',type:'function',name:'detectMiss',filePath:'packages/coding-agent/src/core/cache-stats.ts',lineRange:[56,90],summary:'检测单条消息相对于前一次请求的缓存未命中情况。',tags:['cache','detection','analytics'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/cache-stats.ts:scan',type:'function',name:'scan',filePath:'packages/coding-agent/src/core/cache-stats.ts',lineRange:[104,132],summary:'扫描会话条目列表，检测所有缓存未命中事件。',tags:['cache','scanning','analytics'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/cache-stats.ts:computeCacheWaste',type:'function',name:'computeCacheWaste',filePath:'packages/coding-agent/src/core/cache-stats.ts',lineRange:[138,140],summary:'计算缓存浪费总量。',tags:['cache','statistics','analytics'],complexity:'simple'});

// event-bus.ts
nodes.push({id:'function:packages/coding-agent/src/core/event-bus.ts:createEventBus',type:'function',name:'createEventBus',filePath:'packages/coding-agent/src/core/event-bus.ts',lineRange:[12,33],summary:'创建轻量级事件总线实例，提供发布/订阅模式的事件通信。',tags:['event-bus','pubsub','factory'],complexity:'simple'});

// exec.ts
nodes.push({id:'function:packages/coding-agent/src/core/exec.ts:execCommand',type:'function',name:'execCommand',filePath:'packages/coding-agent/src/core/exec.ts',lineRange:[34,107],summary:'执行外部命令，提供超时控制和信号中止支持。',tags:['exec','command-execution','subprocess'],complexity:'moderate'});

// experimental.ts
nodes.push({id:'function:packages/coding-agent/src/core/experimental.ts:areExperimentalFeaturesEnabled',type:'function',name:'areExperimentalFeaturesEnabled',filePath:'packages/coding-agent/src/core/experimental.ts',lineRange:[3,5],summary:'检查实验性功能是否已启用。',tags:['experimental','feature-flag'],complexity:'simple'});

// export-html/index.ts
nodes.push({id:'function:packages/coding-agent/src/core/export-html/index.ts:deriveExportColors',type:'function',name:'deriveExportColors',filePath:'packages/coding-agent/src/core/export-html/index.ts',lineRange:[81,106],summary:'从基础颜色派生导出 HTML 所需的完整配色方案。',tags:['export','html','color','theme'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/export-html/index.ts:generateHtml',type:'function',name:'generateHtml',filePath:'packages/coding-agent/src/core/export-html/index.ts',lineRange:[143,175],summary:'根据会话数据和主题生成完整的 HTML 页面。',tags:['export','html','generation'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/export-html/index.ts:preRenderCustomTools',type:'function',name:'preRenderCustomTools',filePath:'packages/coding-agent/src/core/export-html/index.ts',lineRange:[183,230],summary:'预渲染自定义工具的调用结果为 HTML 片段。',tags:['export','html','tool-renderer'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/export-html/index.ts:exportSessionToHtml',type:'function',name:'exportSessionToHtml',filePath:'packages/coding-agent/src/core/export-html/index.ts',lineRange:[236,282],summary:'将会话记录导出为带主题样式的 HTML 文件。',tags:['export','html','session'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/export-html/index.ts:exportFromFile',type:'function',name:'exportFromFile',filePath:'packages/coding-agent/src/core/export-html/index.ts',lineRange:[288,316],summary:'从 JSONL 会话文件读取并导出为 HTML。',tags:['export','html','file-io'],complexity:'moderate'});

// extensions/loader.ts
nodes.push({id:'function:packages/coding-agent/src/core/extensions/loader.ts:createExtensionAPI',type:'function',name:'createExtensionAPI',filePath:'packages/coding-agent/src/core/extensions/loader.ts',lineRange:[249,426],summary:'为扩展创建 API 接口，提供工具注册、命令注册、事件监听等扩展能力。',tags:['extension','api','factory'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/loader.ts:createExtensionRuntime',type:'function',name:'createExtensionRuntime',filePath:'packages/coding-agent/src/core/extensions/loader.ts',lineRange:[174,242],summary:'创建扩展运行时环境，管理扩展注册表和生命周期。',tags:['extension','runtime','factory'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/loader.ts:loadExtension',type:'function',name:'loadExtension',filePath:'packages/coding-agent/src/core/extensions/loader.ts',lineRange:[490,516],summary:'加载单个扩展模块，处理模块导入和工厂函数调用。',tags:['extension','loader','module-loading'],complexity:'moderate'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/loader.ts:loadExtensions',type:'function',name:'loadExtensions',filePath:'packages/coding-agent/src/core/extensions/loader.ts',lineRange:[579,586],summary:'加载指定路径列表中的所有扩展。',tags:['extension','loader','batch-loading'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/loader.ts:discoverAndLoadExtensions',type:'function',name:'discoverAndLoadExtensions',filePath:'packages/coding-agent/src/core/extensions/loader.ts',lineRange:[689,737],summary:'发现并加载所有已配置的扩展，支持目录扫描和路径解析。',tags:['extension','discovery','loader'],complexity:'complex'});

// extensions/runner.ts
nodes.push({id:'class:packages/coding-agent/src/core/extensions/runner.ts:ExtensionRunner',type:'class',name:'ExtensionRunner',filePath:'packages/coding-agent/src/core/extensions/runner.ts',lineRange:[268,1236],summary:'扩展运行时管理器，绑定扩展核心功能、处理事件分发、管理工具注册和命令解析。',tags:['extension','runner','event-dispatch','tool-registry'],complexity:'complex'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/runner.ts:emitSessionShutdownEvent',type:'function',name:'emitSessionShutdownEvent',filePath:'packages/coding-agent/src/core/extensions/runner.ts',lineRange:[192,201],summary:'向所有扩展发出会话关闭事件。',tags:['extension','event','shutdown'],complexity:'simple'});
nodes.push({id:'function:packages/coding-agent/src/core/extensions/runner.ts:emitProjectTrustEvent',type:'function',name:'emitProjectTrustEvent',filePath:'packages/coding-agent/src/core/extensions/runner.ts',lineRange:[203,233],summary:'向扩展发出项目信任事件，处理信任决策回调。',tags:['extension','event','project-trust'],complexity:'moderate'});

// === EDGES ===

// contains edges for all function/class nodes
for (const node of nodes) {
  if (node.type === 'function' || node.type === 'class') {
    const filePath = node.filePath;
    edges.push({
      source: 'file:' + filePath,
      target: node.id,
      type: 'contains',
      direction: 'forward',
      weight: 1.0
    });
  }
}

// exports edges for exported function/class nodes
const exportMap = {};
for (const r of extract.results) {
  for (const e of (r.exports || [])) {
    const key = r.path + ':' + e.name;
    exportMap[key] = true;
  }
}
for (const node of nodes) {
  if (node.type === 'function' || node.type === 'class') {
    const key = node.filePath + ':' + node.name;
    if (exportMap[key]) {
      edges.push({
        source: 'file:' + node.filePath,
        target: node.id,
        type: 'exports',
        direction: 'forward',
        weight: 0.8
      });
    }
  }
}

// imports edges - 1:1 from batchImportData
for (const [filePath, importPaths] of Object.entries(batchImportData)) {
  for (const importPath of importPaths) {
    if (filePath !== importPath) {
      edges.push({
        source: 'file:' + filePath,
        target: 'file:' + importPath,
        type: 'imports',
        direction: 'forward',
        weight: 0.7
      });
    }
  }
}

// tested_by edges from neighborMap (test files in other batches)
const neighborMap = dispatch.neighborMap;
const testFileMap = {};
for (const [sourcePath, neighbors] of Object.entries(neighborMap)) {
  for (const n of neighbors) {
    if (n.path.includes('/test/') || n.path.endsWith('.test.ts')) {
      testFileMap[sourcePath] = testFileMap[sourcePath] || [];
      testFileMap[sourcePath].push(n.path);
    }
  }
}
for (const [prodPath, testPaths] of Object.entries(testFileMap)) {
  for (const testPath of testPaths) {
    edges.push({
      source: 'file:' + prodPath,
      target: 'file:' + testPath,
      type: 'tested_by',
      direction: 'forward',
      weight: 0.5
    });
  }
}

// Split into parts (93 nodes / 60 = 2, 353 edges / 120 = 3 => 3 parts)
// Sort files alphabetically, chunk into 3 groups of 11
const allFilePaths = fileDefs.map(f => f.path).sort();
const partsCount = 3;
const chunkSize = Math.ceil(allFilePaths.length / partsCount);
const parts = [];
for (let p = 0; p < partsCount; p++) {
  const partFiles = allFilePaths.slice(p * chunkSize, (p + 1) * chunkSize);
  const partFileSet = new Set(partFiles);
  // Also include function/class nodes whose filePath is in this part
  const partNodes = nodes.filter(n => {
    if (n.type === 'file') return partFileSet.has(n.filePath);
    if (n.filePath) return partFileSet.has(n.filePath);
    return false;
  });
  // Edges whose source is in this part's nodes
  const partNodeIds = new Set(partNodes.map(n => n.id));
  const partEdges = edges.filter(e => partNodeIds.has(e.source));
  parts.push({ nodes: partNodes, edges: partEdges });
  console.log('Part ' + (p+1) + ': ' + partNodes.length + ' nodes, ' + partEdges.length + ' edges. Files: ' + partFiles.length);
}

for (let p = 0; p < partsCount; p++) {
  const filename = '.understand-anything/intermediate/batch-13-part-' + (p + 1) + '.json';
  fs.writeFileSync(filename, JSON.stringify(parts[p], null, 2));
  console.log('Written: ' + filename);
}
