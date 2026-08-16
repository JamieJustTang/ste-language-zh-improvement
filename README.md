# ste-language-zh-improvement

把面向人的文字（文档、PR 描述、错误信息、智能体输出）写成平实、自然、没有「AI 味」的中文或英文。

英文侧遵循 ASD-STE100 Simplified Technical English（Issue 9）；中文侧是本地魔改的补充规则——把翻译腔、互联网黑话、欧化句式改回自然的中文。本技能通用，任何具备技能机制的 agent 都能用。推荐搭档：[explain-everything-to-me-dsh](https://github.com/JamieJustTang/explain-everything-to-me-dsh)——把 Claude/Codex 会话导入 DeepSeek 的插件，与本技能配合得到“导入 + 说人话”的完整体验。

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
  ~/.agents/skills/ste-language-zh-improvement
```

放入你所用 agent 的技能目录（如 `~/.agents/skills/`）即被自动发现。

## 效果实测

一组真实会话对照。左侧是 Claude 多智能体产出的决策审查与调研简报（原文摘录，……为省略）；
右侧是 DeepSeek 被问「它做了什么、提了哪些建议」时给出的解读（真实输出摘录）——
右侧的语言形态正是本技能规则所固化的目标：

![同一段工作的两种讲法:左侧 Claude 多智能体产出,右侧 DeepSeek 的解读](https://raw.githubusercontent.com/JamieJustTang/explain-everything-to-me-dsh/main/assets/demo.png)

*(交互版 HTML 与截图由 [explain-everything-to-me-dsh](https://github.com/JamieJustTang/explain-everything-to-me-dsh) 提供。)*

| Claude 多智能体产出（原文摘录，……为省略） | DeepSeek 的解读（真实会话输出摘录） |
|---|---|
| `docs/DECISIONS.md` 最近被改过——看是不是你把决策写进去了（对比 git）：<br>决策已入账（`2923900`）。现在按你的 P0 优先级派出三个并行调研 agent（Opus），覆盖所有「需要文献调研才能继续深谈」的决策点：<br># 决策审查意见<br>15 条决策已入账并提交（`2923900`）。总体判断：**这套决策内部自洽、优先级排布合理，且你把「哪些还不能拍」识别得很准**——D-v4-06 评分构念和 D-v4-08 基线可跑性都显式留给了调研，这正是该调研先行的两处。逐块意见：<br>**两处执行风险旗（不是反对，是排期上要正视）**：<br>1. **D-v4-02 六周直冲**：算力和 agent 并行能压缩的只有实现与跑批；**压不动的是三件人事**——人类专家盲评的招募与执行（D-v4-06）、自建任务集的专家验证（D-v4-03）、外部基线的适配调试（D-v4-08）。<br>……<br>\| A 评估方法学 \| D-v4-06 四步的前三步 \| 14 个竞争系统/基准的评估做法逐一解剖 → 以批评文献（Hidden Pitfalls、Correct Answer Wrong Mechanism 等）为锚批判 → 从 QD 多样性、科学计量新颖性、社科理论质量标准（Davis「That's Interesting!」、Whetten、Corley & Gioia）、HCI 协作测度、长程生产率五个文献带提出候选构念池 + 强人框架草案 \|<br>……<br>**① FP-4 的漏洞被精确定位到了代码行**：`claim-ladder.mjs` 的 `resolveEvidenceFacts()` 受理形状③——裸字符串 `evidence_level` 被直接采信，这就是「自报」通道；手术面极小（只换这一个形状为 provenance 推导）。给出三个设计模式：**A 前瞻模式声明**（RR 式，结果已知前签、事后改即 tampered）、**B 单向棘轮**（L1→L2 晋升必须独立 confirmatory 重推导，挂在 CRYSTALLIZE 上）、**C GRADE 式严苛度记分**（基线由步骤定 + 机检升降级）。推荐 **A+C 组合、B 做成消融开关**。最关键的治理洞见是 Vazire 悖论：只给 confirmatory 装牙齿，引擎会理性地全部声明 exploratory——所以防套利的重点是「让探索产物结构性到不了高阶梯」，不是惩罚探索。<br>……<br>**① 评分框架的骨架已经被文献逼出来了（D-v4-06 第四步的雏形）**。三条铁证——novelty mirage（LLM judge 一贯高估机器产物新颖性、专家结论相反）、Agents4Science 的 AI-人相关仅 r=0.12–0.26、而人-人一致性上界本身只有 r=0.14——共同决定了唯一站得住的结构：**机器可算仪表盘（高频）→ 受约束的 LLM judge（中频，novelty 不得单独裁定）→ 人类专家锚点（低频）**三层，外加两个强制元层：判官偏倚在自家 rubric 上实测、LLM-人/人-人/LLM-LLM 三重一致性同报。 | ## 一、Claude 这一次做了什么（动作清单，已核实）<br>这一次**没有动系统代码**，全是「调研 + 记账」：<br>1. **把决策写进账本并提交**：`docs/DECISIONS.md` 新增 §I（D-v4-01 到 D-v4-15，共 45 行），commit `2923900`，工作树 clean。<br>2. **按 P0 优先级，派了 3 个并行调研 agent**（Opus）：A 评估方法学、B 基线可跑性、C 设计输入。<br>3. **三份报告存档**；最后给你一份「决策审查意见」+ 一份「跨报告综合简报」，甩给你一张「待拍板清单」。<br>值得注意的是：他做的**不是**「又跑一遍实验」，而是**把下一步的决策风险提前用文献和实测摸了一遍**。<br>……<br>### 调研 B——发现了一个会推翻前提的问题<br>你之前定的「两个外部基线跑同一批题」**不成立**：ASS 只吃「社会情境」，Agent Laboratory 吃自由文本题目，两者输入单元根本不同类。解法：自建任务集里刻意设计 8–10 题「情境可表达」任务，让两个基线在这个子集上同台。**连带后果**：自建集升格为主力评测集，变成单点故障，标注人力必须最早锁定。<br>……<br>### 调研 A——把评分框架的骨架逼出来了<br>普查了 16 个系统/基准的评估做法，最硬的三条铁证：<br>1. **novelty 幻象**：LLM judge 一贯高估机器产物的新颖性，专家结论相反 → novelty 维度绝不能由 LLM judge 单独裁定。<br>2. AI-人相关只有 r=0.12–0.26；人-人一致性上界本身只有 r≈0.14 → 报「LLM 和人一致」时必须同报人-人一致性当上界，否则是自欺。<br>由此推出的骨架 = 机器可算仪表盘（高频）→ 受约束的 LLM judge（中频）→ 人类专家盲评锚点（低频）。<br>……<br>**你现在面临的核心选择其实只有一个**：下一步怎么处理这 10 个待决项——在对话里逐个讨论，还是生成一张决策地图让你点选。选完，实验设计文档和工程就同时开工。 |

差异是结构性的，数字为辅：平均句长 32 → 27 字；超过 40 字的长句占比 25% → 12%；分节标题 1 → 3。真正的差别在解耦——左侧把 15 条决策、3 份调研、审查意见纠缠在同一段流里，每次阅读都要自己拆；右侧先回答「做了什么」（4 个动作），再按报告逐份讲「发现了什么」，最后收拢成「你现在只需做一个选择」。

### 同义改写基准（分层指标）

上面这组是「解读」而非逐句改写，不适用事实保留率；分层可理解性指标在下面两组
「同义改写」样本上计算（经 deepseek-v4-pro 逐条重写，2026-08-16，temperature 0，
样本见 [metrics/samples/](metrics/samples/)）：

| 层 | 指标 | 案例 1 前→后 | 案例 2 前→后 |
|---|---|---|---|
| A 术语可及性 | 未解释行话密度（个/百字） | 11.5 → **1.7**（-85%） | 10.5 → **1.9**（-82%） |
| A 术语可及性 | 行话首现释义率 | 12% → **76%** | 0% → **75%** |
| B 句法完整性 | 列表条目成句率（句末标点判定） | 0/13 → **13/13** | 8/8 → 10/10 |
| C 信息完整性 | 事实原子保留率（逐项核对） | — | **100% / 100%** |
| D 残留缩写 | 项目内代号未展开数 | 3 → 3 | 5 → 5 |

**为什么平均句长变长是改进**：改进前的问题不是句子长，而是不成句——
`M3 五专家 exact prompt + egress manifest` 没有主语和谓语，读者必须自己脑补整句话。

**D 层是诚实的天花板**：M3、V5、S16–S18 这类项目内部代号在改写前后都未展开——它们的
意义不在语言层，在项目上下文层。这正是
[explain-everything-to-me-dsh](https://github.com/JamieJustTang/explain-everything-to-me-dsh)
的价值：把整个会话导入，用上下文补齐这一层。

**事实可得性测验（[metrics/comprehension.py](metrics/comprehension.py)）**：8 道事实题，
deepseek-v4-pro 仅凭文本作答——改写前后均 **8/8**。这个「无差异」本身就是发现：模型读者
自动翻越术语墙，可理解性成本是人类读者专属的，所以 A/B/D 结构层才是人类侧的正确度量，
而 8/8 保证改写没有为可读性牺牲机器可提取性。

全部指标由 [metrics/measure.py](metrics/measure.py) 确定性计算，可复现。

## 推荐搭档

推荐搭档：[explain-everything-to-me-dsh](https://github.com/JamieJustTang/explain-everything-to-me-dsh) 把 Claude/Codex 会话导入 DeepSeek，本技能让导入后的解释、以及模型自己的输出保持平实中文。另一个推荐搭档：[decision-one-by-one](https://github.com/JamieJustTang/decision-one-by-one)——它负责“逐项解释并敲定待决策项”的对话流程。

## 声明

完整 ASD-STE100 标准免费见 <https://asd-ste100.org>（受版权保护，本仓库不复制标准正文）。本技能非官方，与 ASD 无关。ASD-STE100 是欧盟注册商标（No. 017966390）。中文规则为社区补充，独立于官方标准。
