# ste-language-improvement

把面向人的文字（文档、PR 描述、错误信息、智能体输出）写成平实、自然、没有「AI 味」的中文或英文。

英文侧遵循 ASD-STE100 Simplified Technical English（Issue 9）；中文侧是本地魔改的补充规则——把翻译腔、互联网黑话、欧化句式改回自然的中文。这是 [explain-to-me](https://github.com/JamieJustTang/explain-to-me) 的推荐搭档：它负责把 Claude/Codex 的会话搬进 DeepSeek，本技能负责让 DeepSeek 说人话。

## 它解决什么

现在的 coding agent 有两副面孔：对机器协作和工具调用越来越强，对人类越来越“不说人话”——术语堆叠、电报式罗列、名词化、中英混杂。人类开发者读这样的输出，慢，且容易在没看懂的情况下点头。

规则的核心（完整规则见 [SKILL.md](SKILL.md)）：

- 一个概念只用一个词；术语首次出现给中文并附原文，此后统一。
- 拆掉「对……进行……」「被……」等欧化结构；短句、主动语态。
- 删掉黑话（赋能/抓手/闭环/对齐/颗粒度）和填充词（值得注意的是/综上所述）。
- 每个事实都保留：数字、条件、范围限定词、代码标识符原样。
- 三种模式：**write**（新写）、**rewrite**（改写）、**review**（只出违规对照表）。

## 安装

```sh
git clone https://github.com/JamieJustTang/ste-language-improvement.git \
  ~/.agents/skills/ste-language-improvement
```

放入 agent 的技能目录（如 `~/.agents/skills/`）即被具备技能机制的 agent（DeepSeek Harness、ZCode 等）自动发现。

## 效果实测

原文取自一段真实的 Codex 会话汇报（项目标识已匿名化），用本技能的中文规则改写。

### 改进前（Codex 原文）

```markdown
已完成 Gate C 的全部非 live 准备，且没有调用 DeepSeek。

交付包括：

- M3 五专家 exact prompt + egress manifest
- M6 主稿及正反校准的 exact prompt + manifest
- 两阶段 M3 adjudicator materialization 机制
- immutable prompt bundle 执行器
- V5 媒介传播专家进入 canary panel
- 轴阈值校准结果
- source-packet usage ledger
- `reasoning_content` 持久化前递归删除、redaction 路径记录及回归测试

验证结果：

- Kernel 完整测试：全绿
- recorded-live 集成测试：5/5
- provider privacy/redaction 测试：通过
- 新增及修改脚本 `node --check`：通过
- 无网络、无正式导出、无新种子注册

当前唯一硬门禁是具名人类签署。相关请求位于：
[SEED-CHARTER-SIGNOFF-REQUEST.json](…)
```

### 改进后（deepseek-v4-pro 实际输出）

```markdown
Gate C 的全部非实况（non-live）准备工作已完成，全程没有调用 DeepSeek。

交付包括：

- 已交付 M3 五名专家的精确提示词（exact prompt）与出站清单（egress manifest）。
- 已交付 M6 主稿及正反校准用的精确提示词与清单（manifest）。
- 已建立 M3 裁决器（adjudicator）的两阶段物化（materialization）机制。
- 已交付不可变提示词包（immutable prompt bundle）执行器。
- V5 的媒介传播专家已进入金丝雀评审组（canary panel）。
- 已交付轴阈值校准结果。
- 已交付源数据包用量台账（source-packet usage ledger）。
- 在持久化前递归删除 `reasoning_content`，记录脱敏（redaction）路径，并补齐回归测试。

验证结果：

- Kernel 完整测试全部通过。
- recorded-live 集成测试结果为 5/5。
- 提供方（provider）的隐私与脱敏测试通过。
- 新增及修改脚本的 `node --check` 检查通过。
- 全程无网络访问、无正式导出、无新种子注册。

当前唯一的硬门禁是具名人类签署。相关请求位于 [SEED-CHARTER-SIGNOFF-REQUEST.json](docs/gates/gate-c/SEED-CHARTER-SIGNOFF-REQUEST.json)。
```

### 指标（分层可理解性度量）

全部指标由 [metrics/measure.py](metrics/measure.py) 确定性计算，样本随仓库提供
（[改进前](metrics/samples/codex-gate-c.before.md) / [改进后](metrics/samples/codex-gate-c.after.md)），可复现：

| 层 | 指标 | 改进前 | 改进后 | 变化 |
|---|---|---:|---:|---|
| A 术语可及性 | 未解释行话密度（个/百字） | 11.5 | 1.7 | **-85%** |
| A 术语可及性 | 行话首现释义率 | 12% | 76% | +64 个百分点 |
| B 句法完整性 | 列表条目成句率（句末标点判定） | 0/13 | 13/13 | **+100 个百分点** |
| B 句法完整性 | 平均句长（汉字） | 7 | 14 | 碎片拼回完整句（见下） |
| C 信息完整性 | 事实原子保留率（数字/标识符/文件/条件逐项核对） | — | **100%** | 原子清单可人工复查 |
| D 残留缩写 | 项目内缩写未展开数 | 3（M3/M6/V5） | 3（同） | 语言层天花板，见下 |

**为什么平均句长变长是改进**：改进前的问题不是句子长，而是不成句——
`M3 五专家 exact prompt + egress manifest` 没有主语和谓语，读者必须自己脑补整句话。
成句率从 0/13 到 13/13 度量的正是这个。

**D 层是诚实的天花板**：M3、V5 这类项目内部代号在两版中都未展开——它们的意义不在
语言层，在项目上下文层。这正是 [explain-to-me](https://github.com/JamieJustTang/explain-to-me)
的价值：把整个会话导入 DeepSeek，用上下文（而不是措辞）补齐这一层。

**事实可得性测验（[metrics/comprehension.py](metrics/comprehension.py)）**：8 道事实题
（5/5 通过多少项、哪个字段被删除、还差什么签署……），deepseek-v4-pro 仅凭文本作答——
两版均 **8/8**。这个“无差异”本身就是发现：模型读者自动翻越术语墙，事实提取从来不是
它的瓶颈；可理解性成本是人类读者专属的，所以上表 A/B/D 结构层才是人类侧的正确度量，
而 8/8 保证改写没有为可读性牺牲机器可提取性。

生成方式：改进后文本由 **deepseek-v4-pro** 于 2026-08-16 经 DeepSeek Harness headless
运行产出（`pnpm dsh --profile headless`，技能经 `~/.agents/skills` 加载），非人工改写。

## 与 explain-to-me 的关系

[explain-to-me](https://github.com/JamieJustTang/explain-to-me) 把 Claude/Codex 会话导入 DeepSeek Harness；本技能让导入后的解释、以及 DeepSeek 自己的输出保持平实中文。推荐同时安装 [decision-walkthrough](https://github.com/JamieJustTang/decision-walkthrough)——它负责“逐项解释并敲定待决策项”的对话流程。

## 声明

完整 ASD-STE100 标准免费见 <https://asd-ste100.org>（受版权保护，本仓库不复制标准正文）。本技能非官方，与 ASD 无关。ASD-STE100 是欧盟注册商标（No. 017966390）。中文规则为社区补充，独立于官方标准。
