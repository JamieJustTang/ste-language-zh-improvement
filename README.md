# ste-language-improvement

把面向人的文字（文档、PR 描述、错误信息、智能体输出）写成平实、自然、没有「AI 味」的中文或英文。

英文侧遵循 ASD-STE100 Simplified Technical English（Issue 9）；中文侧是本地魔改的补充规则——把翻译腔、互联网黑话、欧化句式改回自然的中文。这是 [explain-to-me](https://github.com/JamieJustTang/explain-everything-to-me-dsh) 的推荐搭档：它负责把 Claude/Codex 的会话搬进 DeepSeek，本技能负责让 DeepSeek 说人话。

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
git clone https://github.com/JamieJustTang/ste-language-zh-improvement.git \
  ~/.agents/skills/ste-language-improvement
```

放入 agent 的技能目录（如 `~/.agents/skills/`）即被具备技能机制的 agent（DeepSeek Harness、ZCode 等）自动发现。

## 效果实测

原文均取自真实 Codex 会话（项目标识已匿名化），用本技能的中文规则改写。

### 案例 1：交付汇报（长文）

| 改进前（Codex 原文） | 改进后（deepseek-v4-pro 实际输出） |
|---|---|
| 已完成 Gate C 的全部非 live 准备,且没有调用 DeepSeek。<br>交付包括:<br>• M3 五专家 exact prompt + egress manifest<br>• M6 主稿及正反校准的 exact prompt + manifest<br>• 两阶段 M3 adjudicator materialization 机制<br>• immutable prompt bundle 执行器<br>• V5 媒介传播专家进入 canary panel<br>• 轴阈值校准结果<br>• source-packet usage ledger<br>• `reasoning_content` 持久化前递归删除、redaction 路径记录及回归测试<br>验证结果:<br>• Kernel 完整测试:全绿<br>• recorded-live 集成测试:5/5<br>• provider privacy/redaction 测试:通过<br>• 新增及修改脚本 `node --check`:通过<br>• 无网络、无正式导出、无新种子注册<br>当前唯一硬门禁是具名人类签署。相关请求位于:<br>[SEED-CHARTER-SIGNOFF-REQUEST.json](docs/gates/gate-c/SEED-CHARTER-SIGNOFF-REQUEST.json) | Gate C 的全部非实况（non-live）准备工作已完成，全程没有调用 DeepSeek。<br>交付包括：<br>• 已交付 M3 五名专家的精确提示词（exact prompt）与出站清单（egress manifest）。<br>• 已交付 M6 主稿及正反校准用的精确提示词与清单（manifest）。<br>• 已建立 M3 裁决器（adjudicator）的两阶段物化（materialization）机制。<br>• 已交付不可变提示词包（immutable prompt bundle）执行器。<br>• V5 的媒介传播专家已进入金丝雀评审组（canary panel）。<br>• 已交付轴阈值校准结果。<br>• 已交付源数据包用量台账（source-packet usage ledger）。<br>• 在持久化前递归删除 `reasoning_content`，记录脱敏（redaction）路径，并补齐回归测试。<br>验证结果：<br>• Kernel 完整测试全部通过。<br>• recorded-live 集成测试结果为 5/5。<br>• 提供方（provider）的隐私与脱敏测试通过。<br>• 新增及修改脚本的 `node --check` 检查通过。<br>• 全程无网络访问、无正式导出、无新种子注册。<br>当前唯一的硬门禁是具名人类签署。相关请求位于 [SEED-CHARTER-SIGNOFF-REQUEST.json](docs/gates/gate-c/SEED-CHARTER-SIGNOFF-REQUEST.json)。 |

### 案例 2：状态简报（短文）

| 改进前（Codex 原文） | 改进后（deepseek-v4-pro 实际输出） |
|---|---|
| 已完成分配的 R2 语料与 Lane B V5 非 live 准备工作,并向主任务汇报。<br>验证结果:<br>• S16–S18 charter、canonical digest、CFP card:全部通过正式契约断言。<br>• V5 gardener profile:通过 `assertProfile`。<br>• 媒介研究包:14/14 来源可解析,四组 rival concepts 4/4 覆盖。<br>• stale-packet checker:4/4 smoke 通过;第三次使用产生 `stale-packet` 和退出码 3。<br>• S16–S18:仅 proposal,未写入 portfolio ledger。<br>• B2-S5:仍为 `parked`。<br>• 未调用 DeepSeek 或网络,未上传任何原始 PDF。<br>• 四位候选来源明确保留为待核验,未冒充已核验来源。 | 我完成了分配的 R2 语料与 Lane B V5 的非线上（live）准备工作，并向主任务汇报。<br>验证结果：<br>• S16–S18 的章程（charter）、规范摘要（canonical digest）与 CFP 卡（CFP card）全部通过正式契约断言。<br>• V5 园丁画像（gardener profile）通过 `assertProfile`。<br>• 媒介研究包的 14/14 个来源可解析。<br>• 媒介研究包的四组竞争概念（rival concepts）覆盖 4/4。<br>• stale-packet 检查器（checker）的冒烟测试（smoke test）4/4 通过。<br>• 该检查器第三次使用时产生 `stale-packet` 与退出码 3。<br>• S16–S18 仅有提案（proposal），未写入组合账本（portfolio ledger）。<br>• B2-S5 仍为搁置（`parked`）。<br>• 未调用 DeepSeek 或网络，也未上传任何原始 PDF。<br>• 四位候选来源明确保留为待核验，未冒充已核验来源。 |

### 指标（分层可理解性度量）

由 [metrics/measure.py](metrics/measure.py) 确定性计算，样本随仓库提供（[metrics/samples/](metrics/samples/)），可复现：

| 层 | 指标 | 案例 1 前→后 | 案例 2 前→后 |
|---|---|---|---|
| A 术语可及性 | 未解释行话密度（个/百字） | 11.5 → **1.7**（-85%） | 10.5 → **1.9**（-82%） |
| A 术语可及性 | 行话首现释义率 | 12% → **76%** | 0% → **75%** |
| B 句法完整性 | 列表条目成句率（句末标点判定） | 0/13 → **13/13** | 8/8 → 10/10 |
| C 信息完整性 | 事实原子保留率（数字/标识符/文件/条件逐项核对） | — | **100% / 100%** |
| D 残留缩写 | 项目内代号未展开数 | 3 → 3（语言层天花板，见下） | 5 → 5（同） |

**为什么平均句长变长是改进**：改进前的问题不是句子长，而是不成句——
`M3 五专家 exact prompt + egress manifest` 没有主语和谓语，读者必须自己脑补整句话。
成句率（句末标点客观判定）度量的正是这个。

**D 层是诚实的天花板**：M3、V5、S16–S18 这类项目内部代号在两版中都未展开——它们的
意义不在语言层，在项目上下文层。这正是
[explain-everything-to-me-dsh](https://github.com/JamieJustTang/explain-everything-to-me-dsh)
的价值：把整个会话导入 DeepSeek，用上下文（而不是措辞）补齐这一层。

**事实可得性测验（[metrics/comprehension.py](metrics/comprehension.py)）**：8 道事实题
（5/5 通过多少项、哪个字段被删除、还差什么签署……），deepseek-v4-pro 仅凭文本作答——
两版均 **8/8**。这个“无差异”本身就是发现：模型读者自动翻越术语墙，事实提取从来不是
它的瓶颈；可理解性成本是人类读者专属的，所以上表 A/B/D 结构层才是人类侧的正确度量，
而 8/8 保证改写没有为可读性牺牲机器可提取性。

生成方式：两组“改进后”文本均由 **deepseek-v4-pro** 于 2026-08-16 经 DeepSeek Harness
headless 运行产出（`pnpm dsh --profile headless`，技能经 `~/.agents/skills` 加载），
非人工改写。

## 与 explain-everything-to-me-dsh 的关系

[explain-to-me](https://github.com/JamieJustTang/explain-everything-to-me-dsh) 把 Claude/Codex 会话导入 DeepSeek Harness；本技能让导入后的解释、以及 DeepSeek 自己的输出保持平实中文。推荐同时安装 [decision-one-by-one](https://github.com/JamieJustTang/decision-one-by-one)——它负责“逐项解释并敲定待决策项”的对话流程。

## 声明

完整 ASD-STE100 标准免费见 <https://asd-ste100.org>（受版权保护，本仓库不复制标准正文）。本技能非官方，与 ASD 无关。ASD-STE100 是欧盟注册商标（No. 017966390）。中文规则为社区补充，独立于官方标准。
