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

### 改进后（ste-language-improvement 重写）

```markdown
Gate C 的离线准备工作全部完成，没有调用 DeepSeek。

本轮交付了八项：

- 五位专家评审的提示词定稿，以及对外发送清单（egress manifest）。
- 主稿评审和正、反两个校准集的提示词定稿，各带一份发送清单。
- 评审材料的两阶段生成机制：先出草稿，再由裁判（adjudicator）定稿。
- 提示词包（prompt bundle）执行器。包一经生成，不再改动。
- 媒介传播领域的评审专家已加入金丝雀小组（canary panel）。
- 评分轴阈值的校准结果。
- 来源包（source packet）的使用台账。
- `reasoning_content` 字段在写入持久存储前递归删除；删除路径有记录，并配了回归测试。

验证结果如下：

- 内核测试全部通过。
- 录制回放（recorded-live）集成测试 5 项通过 5 项。
- 隐私与脱敏（privacy/redaction）测试通过。
- 新增和修改的脚本都通过了 `node --check`。
- 全程没有联网，没有正式导出，没有注册新种子。

现在只剩一道硬性门禁：由具名的人类签字。签字请求在 `SEED-CHARTER-SIGNOFF-REQUEST.json`。
```

### 指标

| 指标 | 改进前 | 改进后 | 变化 |
|---|---:|---:|---|
| 英文词密度（个/百字） | 27.7 | 7.7 | **-72%** |
| 列表条目为完整句（有谓语） | 2/13 | 13/13 | **+85 个百分点** |
| 事实保留（数字/条件/标识符） | — | 全部 | 100% |

平均句长从 11 字升到 16 字——这是修复的一部分：电报式碎片（"M3 五专家 exact prompt + egress manifest"）被拼回有主语、有谓语的完整句。改进前的问题不是句子太长，而是根本不成句。

术语没有被消灭，而是被驯化：`egress manifest` 变成「对外发送清单（egress manifest）」，首次出现给中文，代码标识符（`reasoning_content`、`node --check`、文件名）原样保留。

## 与 explain-to-me 的关系

[explain-to-me](https://github.com/JamieJustTang/explain-to-me) 把 Claude/Codex 会话导入 DeepSeek Harness；本技能让导入后的解释、以及 DeepSeek 自己的输出保持平实中文。推荐同时安装 [decision-walkthrough](https://github.com/JamieJustTang/decision-walkthrough)——它负责“逐项解释并敲定待决策项”的对话流程。

## 声明

完整 ASD-STE100 标准免费见 <https://asd-ste100.org>（受版权保护，本仓库不复制标准正文）。本技能非官方，与 ASD 无关。ASD-STE100 是欧盟注册商标（No. 017966390）。中文规则为社区补充，独立于官方标准。
