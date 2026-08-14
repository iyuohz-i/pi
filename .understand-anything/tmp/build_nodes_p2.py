import json, os

out = '/Users/zhouyi/AiHub/pi/.understand-anything/intermediate/batch-8.json'
with open(out, 'r') as f:
    data = json.load(f)

nodes = data['nodes']

# 13. armin.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/armin.ts",
  "type": "file", "name": "armin.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/armin.ts",
  "summary": "ASCII 艺术动画组件 Armin，支持打字机、扫描线、雨滴、淡入、CRT、故障和溶解等多种视觉效果。",
  "tags": ["interactive","component","animation","ascii-art"], "complexity": "complex",
  "languageNotes": "使用字符网格和帧动画实现多种终端视觉效果。"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/armin.ts:ArminComponent",
  "type": "class", "name": "ArminComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/armin.ts",
  "lineRange": [60,382],
  "summary": "Armin 动画组件类，管理字符网格、帧动画循环和多种视觉效果的状态机。",
  "tags": ["interactive","component","animation"], "complexity": "complex"
})

# 14. assistant-message.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/assistant-message.ts",
  "type": "file", "name": "assistant-message.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/assistant-message.ts",
  "summary": "渲染助手消息的交互式组件，支持 Markdown 转换、思考块折叠和流式更新。",
  "tags": ["interactive","component","message-rendering","markdown"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/assistant-message.ts:AssistantMessageComponent",
  "type": "class", "name": "AssistantMessageComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/assistant-message.ts",
  "lineRange": [14,197],
  "summary": "助手消息渲染组件，处理 Markdown 显示、思考块隐藏和流式内容更新。",
  "tags": ["interactive","component","message-rendering"], "complexity": "moderate"
})

# 15. bash-execution.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/bash-execution.ts",
  "type": "file", "name": "bash-execution.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/bash-execution.ts",
  "summary": "渲染 Bash 命令执行结果的交互式组件，支持输出截断、展开/折叠和状态显示。",
  "tags": ["interactive","component","bash","output-rendering"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/bash-execution.ts:BashExecutionComponent",
  "type": "class", "name": "BashExecutionComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/bash-execution.ts",
  "lineRange": [21,220],
  "summary": "Bash 执行结果渲染组件，管理命令输出、截断显示和展开折叠状态。",
  "tags": ["interactive","component","bash"], "complexity": "moderate"
})

# 16. bordered-loader.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/bordered-loader.ts",
  "type": "file", "name": "bordered-loader.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/bordered-loader.ts",
  "summary": "带边框的加载动画组件，支持取消操作和信号控制。",
  "tags": ["interactive","component","loader","ui"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/bordered-loader.ts:BorderedLoader",
  "type": "class", "name": "BorderedLoader",
  "filePath": "packages/coding-agent/src/modes/interactive/components/bordered-loader.ts",
  "lineRange": [7,68],
  "summary": "带边框的加载器组件，封装可取消的加载动画和键盘输入处理。",
  "tags": ["interactive","component","loader"], "complexity": "simple"
})

# 17. branch-summary-message.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/branch-summary-message.ts",
  "type": "file", "name": "branch-summary-message.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/branch-summary-message.ts",
  "summary": "渲染分支摘要消息的交互式组件，支持展开/折叠显示摘要内容。",
  "tags": ["interactive","component","message-rendering","branch-summary"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/branch-summary-message.ts:BranchSummaryMessageComponent",
  "type": "class", "name": "BranchSummaryMessageComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/branch-summary-message.ts",
  "lineRange": [10,58],
  "summary": "分支摘要消息渲染组件，支持展开折叠和 Markdown 显示。",
  "tags": ["interactive","component","branch-summary"], "complexity": "simple"
})

# 18. compaction-summary-message.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/compaction-summary-message.ts",
  "type": "file", "name": "compaction-summary-message.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/compaction-summary-message.ts",
  "summary": "渲染压缩摘要消息的交互式组件，支持展开/折叠显示压缩前后的上下文信息。",
  "tags": ["interactive","component","message-rendering","compaction"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/compaction-summary-message.ts:CompactionSummaryMessageComponent",
  "type": "class", "name": "CompactionSummaryMessageComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/compaction-summary-message.ts",
  "lineRange": [10,59],
  "summary": "压缩摘要消息渲染组件，支持展开折叠和 Markdown 显示。",
  "tags": ["interactive","component","compaction"], "complexity": "simple"
})

# 19. countdown-timer.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/countdown-timer.ts",
  "type": "file", "name": "countdown-timer.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/countdown-timer.ts",
  "summary": "倒计时定时器组件，在终端 UI 中显示剩余秒数并在到期时回调。",
  "tags": ["interactive","component","timer","utility"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/countdown-timer.ts:CountdownTimer",
  "type": "class", "name": "CountdownTimer",
  "filePath": "packages/coding-agent/src/modes/interactive/components/countdown-timer.ts",
  "lineRange": [7,39],
  "summary": "倒计时定时器类，管理间隔定时器和到期回调。",
  "tags": ["interactive","component","timer"], "complexity": "simple"
})

# 20. custom-editor.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/custom-editor.ts",
  "type": "file", "name": "custom-editor.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/custom-editor.ts",
  "summary": "自定义编辑器组件，处理键盘快捷键、粘贴图片和扩展快捷键等编辑器操作。",
  "tags": ["interactive","component","editor","input-handling"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/custom-editor.ts:CustomEditor",
  "type": "class", "name": "CustomEditor",
  "filePath": "packages/coding-agent/src/modes/interactive/components/custom-editor.ts",
  "lineRange": [7,90],
  "summary": "自定义编辑器类，代理键盘输入并分发动作处理器给上层组件。",
  "tags": ["interactive","component","editor"], "complexity": "simple"
})

# 21. custom-message.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/custom-message.ts",
  "type": "file", "name": "custom-message.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/custom-message.ts",
  "summary": "渲染自定义类型消息的交互式组件，支持自定义渲染器和展开/折叠。",
  "tags": ["interactive","component","message-rendering","custom"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/custom-message.ts:CustomMessageComponent",
  "type": "class", "name": "CustomMessageComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/custom-message.ts",
  "lineRange": [12,113],
  "summary": "自定义消息渲染组件，支持自定义渲染器、Markdown 主题和展开折叠。",
  "tags": ["interactive","component","custom-message"], "complexity": "moderate"
})

# 22. daxnuts.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/daxnuts.ts",
  "type": "file", "name": "daxnuts.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/daxnuts.ts",
  "summary": "ASCII 艺术动画组件 Daxnuts，渲染图像并逐帧播放动画效果。",
  "tags": ["interactive","component","animation","ascii-art"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/daxnuts.ts:DaxnutsComponent",
  "type": "class", "name": "DaxnutsComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/daxnuts.ts",
  "lineRange": [57,164],
  "summary": "Daxnuts 动画组件类，管理图像解析、帧动画循环和渲染缓存。",
  "tags": ["interactive","component","animation"], "complexity": "moderate"
})

# 23. diff.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/diff.ts",
  "type": "file", "name": "diff.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/diff.ts",
  "summary": "在终端中渲染 diff 输出的组件，支持行内差异高亮和颜色标记。",
  "tags": ["interactive","component","diff","rendering"], "complexity": "moderate"
})
nodes.append({
  "id": "function:packages/coding-agent/src/modes/interactive/components/diff.ts:renderDiff",
  "type": "function", "name": "renderDiff",
  "filePath": "packages/coding-agent/src/modes/interactive/components/diff.ts",
  "lineRange": [79,147],
  "summary": "渲染 diff 文本为带颜色的终端输出，支持行内差异高亮显示。",
  "tags": ["interactive","diff","rendering"], "complexity": "complex"
})
nodes.append({
  "id": "function:packages/coding-agent/src/modes/interactive/components/diff.ts:renderIntraLineDiff",
  "type": "function", "name": "renderIntraLineDiff",
  "filePath": "packages/coding-agent/src/modes/interactive/components/diff.ts",
  "lineRange": [26,66],
  "summary": "计算两个文本行的行内差异并生成高亮标记。",
  "tags": ["interactive","diff","algorithm"], "complexity": "moderate"
})

# 24. dynamic-border.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/dynamic-border.ts",
  "type": "file", "name": "dynamic-border.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/dynamic-border.ts",
  "summary": "动态边框组件，根据主题颜色渲染可变颜色的边框。",
  "tags": ["interactive","component","border","ui"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/dynamic-border.ts:DynamicBorder",
  "type": "class", "name": "DynamicBorder",
  "filePath": "packages/coding-agent/src/modes/interactive/components/dynamic-border.ts",
  "lineRange": [11,25],
  "summary": "动态边框类，根据主题颜色渲染可变颜色的边框。",
  "tags": ["interactive","component","border"], "complexity": "simple"
})

# 25. earendil-announcement.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/earendil-announcement.ts",
  "type": "file", "name": "earendil-announcement.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/earendil-announcement.ts",
  "summary": "Earendil 公告组件，在终端中渲染 Base64 图片公告动画。",
  "tags": ["interactive","component","announcement","animation"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/earendil-announcement.ts:EarendilAnnouncementComponent",
  "type": "class", "name": "EarendilAnnouncementComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/earendil-announcement.ts",
  "lineRange": [27,53],
  "summary": "Earendil 公告组件类，加载并渲染 Base64 图片到终端。",
  "tags": ["interactive","component","announcement"], "complexity": "simple"
})

# 26. extension-editor.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/extension-editor.ts",
  "type": "file", "name": "extension-editor.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-editor.ts",
  "summary": "扩展编辑器组件，提供多行文本编辑和外部编辑器调用功能。",
  "tags": ["interactive","component","editor","extension"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/extension-editor.ts:ExtensionEditorComponent",
  "type": "class", "name": "ExtensionEditorComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-editor.ts",
  "lineRange": [22,132],
  "summary": "扩展编辑器组件类，处理键盘输入、外部编辑器调用和提交/取消回调。",
  "tags": ["interactive","component","editor"], "complexity": "moderate"
})

# 27. extension-input.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/extension-input.ts",
  "type": "file", "name": "extension-input.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-input.ts",
  "summary": "扩展输入组件，提供带倒计时的单行文本输入界面。",
  "tags": ["interactive","component","input","extension"], "complexity": "simple"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/extension-input.ts:ExtensionInputComponent",
  "type": "class", "name": "ExtensionInputComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-input.ts",
  "lineRange": [16,87],
  "summary": "扩展输入组件类，管理文本输入、倒计时和提交/取消回调。",
  "tags": ["interactive","component","input"], "complexity": "simple"
})

# 28. extension-selector.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/extension-selector.ts",
  "type": "file", "name": "extension-selector.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-selector.ts",
  "summary": "扩展选择器组件，提供带倒计时的列表选择界面。",
  "tags": ["interactive","component","selector","extension"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/extension-selector.ts:ExtensionSelectorComponent",
  "type": "class", "name": "ExtensionSelectorComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/extension-selector.ts",
  "lineRange": [18,112],
  "summary": "扩展选择器组件类，管理选项列表、选择索引和倒计时。",
  "tags": ["interactive","component","selector"], "complexity": "moderate"
})

# 29. first-time-setup.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/first-time-setup.ts",
  "type": "file", "name": "first-time-setup.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/first-time-setup.ts",
  "summary": "首次启动设置向导组件，引导用户选择主题和分析偏好。",
  "tags": ["interactive","component","setup","onboarding"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/first-time-setup.ts:FirstTimeSetupComponent",
  "type": "class", "name": "FirstTimeSetupComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/first-time-setup.ts",
  "lineRange": [32,145],
  "summary": "首次设置向导组件类，管理步骤导航、主题选择和选项列表。",
  "tags": ["interactive","component","setup"], "complexity": "moderate"
})

# 30. keybinding-hints.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/keybinding-hints.ts",
  "type": "file", "name": "keybinding-hints.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/keybinding-hints.ts",
  "summary": "格式化键绑定提示文本的工具函数集，支持按键文本和提示行渲染。",
  "tags": ["interactive","utility","keybindings","formatting"], "complexity": "simple"
})
nodes.append({
  "id": "function:packages/coding-agent/src/modes/interactive/components/keybinding-hints.ts:formatKeyText",
  "type": "function", "name": "formatKeyText",
  "filePath": "packages/coding-agent/src/modes/interactive/components/keybinding-hints.ts",
  "lineRange": [17,27],
  "summary": "将键绑定标识格式化为可显示的按键文本。",
  "tags": ["keybindings","formatting","utility"], "complexity": "simple"
})

# 31. login-dialog.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/login-dialog.ts",
  "type": "file", "name": "login-dialog.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/login-dialog.ts",
  "summary": "登录对话框组件，处理 OAuth 认证流程、设备码显示和手动输入等登录方式。",
  "tags": ["interactive","component","login","oauth"], "complexity": "complex"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/login-dialog.ts:LoginDialogComponent",
  "type": "class", "name": "LoginDialogComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/login-dialog.ts",
  "lineRange": [11,233],
  "summary": "登录对话框组件类，管理多种认证状态（授权、设备码、手动输入、等待）和用户交互。",
  "tags": ["interactive","component","login","oauth"], "complexity": "complex"
})

# 32. markdown-transform.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/markdown-transform.ts",
  "type": "file", "name": "markdown-transform.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/markdown-transform.ts",
  "summary": "Markdown 转换工具，创建和应用自定义 Markdown 变换器处理消息内容。",
  "tags": ["interactive","utility","markdown","transform"], "complexity": "simple"
})
nodes.append({
  "id": "function:packages/coding-agent/src/modes/interactive/components/markdown-transform.ts:applyMarkdownTransformers",
  "type": "function", "name": "applyMarkdownTransformers",
  "filePath": "packages/coding-agent/src/modes/interactive/components/markdown-transform.ts",
  "lineRange": [12,29],
  "summary": "按顺序应用 Markdown 变换器链处理输入文本。",
  "tags": ["markdown","transform","utility"], "complexity": "simple"
})

# 33. model-selector.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/model-selector.ts",
  "type": "file", "name": "model-selector.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/model-selector.ts",
  "summary": "模型选择器组件，提供模型搜索、筛选、排序和 scoped model 管理功能。",
  "tags": ["interactive","component","model-selector","search"], "complexity": "complex"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/model-selector.ts:ModelSelectorComponent",
  "type": "class", "name": "ModelSelectorComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/model-selector.ts",
  "lineRange": [35,373],
  "summary": "模型选择器组件类，管理模型列表、搜索过滤、scoped model 和模型刷新。",
  "tags": ["interactive","component","model-selector"], "complexity": "complex"
})

# 34. oauth-selector.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/oauth-selector.ts",
  "type": "file", "name": "oauth-selector.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/oauth-selector.ts",
  "summary": "OAuth 认证选择器组件，列出可用认证提供商并支持搜索过滤。",
  "tags": ["interactive","component","oauth","selector"], "complexity": "moderate"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/oauth-selector.ts:OAuthSelectorComponent",
  "type": "class", "name": "OAuthSelectorComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/oauth-selector.ts",
  "lineRange": [29,214],
  "summary": "OAuth 选择器组件类，管理认证提供商列表、搜索过滤和选择回调。",
  "tags": ["interactive","component","oauth"], "complexity": "moderate"
})

# 35. scoped-models-selector.ts
nodes.append({
  "id": "file:packages/coding-agent/src/modes/interactive/components/scoped-models-selector.ts",
  "type": "file", "name": "scoped-models-selector.ts",
  "filePath": "packages/coding-agent/src/modes/interactive/components/scoped-models-selector.ts",
  "summary": "Scoped 模型选择器组件，管理启用的模型列表，支持排序、刷新和搜索过滤。",
  "tags": ["interactive","component","model-selector","scoped-models"], "complexity": "complex"
})
nodes.append({
  "id": "class:packages/coding-agent/src/modes/interactive/components/scoped-models-selector.ts:ScopedModelsSelectorComponent",
  "type": "class", "name": "ScopedModelsSelectorComponent",
  "filePath": "packages/coding-agent/src/modes/interactive/components/scoped-models-selector.ts",
  "lineRange": [92,403],
  "summary": "Scoped 模型选择器组件类，管理启用模型 ID、排序顺序和刷新状态。",
  "tags": ["interactive","component","scoped-models"], "complexity": "complex"
})

data['nodes'] = nodes
with open(out, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Total nodes: {len(nodes)}")
