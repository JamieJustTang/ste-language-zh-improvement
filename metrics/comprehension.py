#!/usr/bin/env python3
"""事实可得性测验:对 before/after 两版文本,让模型仅凭文本作答同一组事实题。

题目与标准答案从原文事实原子人工拟定(见 QUESTIONS),评分按关键词自动判定。
读者模型默认 deepseek-v4-pro;两版使用同一读者与同一题目,只对比文本本身。

实测两版均满分——该指标度量「改写没有丢失机器可提取的事实」,不度量人类
可读性:模型读者会自动翻越术语墙,这正是 A/B/D 结构层指标存在的原因。

用法:DEEPSEEK_API_KEY=... python3 comprehension.py before.txt after.txt
"""

import json
import os
import re
import sys
import urllib.request

API_URL = 'https://api.deepseek.com/chat/completions'
MODEL = 'deepseek-v4-pro'

QUESTIONS: list[tuple[str, list[str]]] = [
    ('recorded-live 集成测试通过了多少项?', ['5']),
    ('哪个字段在写入持久存储之前会被删除?', ['reasoning_content']),
    ('目前还差什么条件才算完成 Gate C?', ['签署', '签字', '签核']),
    ('本轮准备工作有没有调用 DeepSeek?', ['没有', '未调用', '无']),
    ('M3 有几位专家参与评审?', ['五', '5']),
    ('本轮注册了新种子吗?', ['没有', '未']),
    ('脚本用什么命令做语法检查?', ['node --check']),
    ('签字请求放在哪个文件?', ['SEED-CHARTER-SIGNOFF-REQUEST']),
]

PROMPT_HEAD = (
    '仅依据下面的文本回答问题。每题一行,格式为「Qn: 答案」。'
    '答案必须来自文本;文本给不出答案就写「Qn: 未知」。不要输出其他内容。\n\n<文本>\n'
)


def ask_model(text: str) -> str:
    body = json.dumps({
        'model': MODEL,
        'messages': [
            {'role': 'user', 'content': PROMPT_HEAD + text + '\n</文本>\n\n'
             + '\n'.join(f'Q{i + 1}: {q}' for i, (q, _) in enumerate(QUESTIONS))},
        ],
        'temperature': 0,
        'max_tokens': 3000,
    }).encode()
    request = urllib.request.Request(
        API_URL, data=body,
        headers={'Content-Type': 'application/json',
                 'Authorization': f"Bearer {os.environ['DEEPSEEK_API_KEY']}"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        data = json.load(response)
    return data['choices'][0]['message']['content']


def grade(reply: str) -> tuple[int, list[str]]:
    correct = 0
    details: list[str] = []
    for i, (_, keywords) in enumerate(QUESTIONS):
        line = next((l for l in reply.splitlines() if l.strip().startswith(f'Q{i + 1}')), '')
        ok = any(k in line for k in keywords)
        correct += ok
        details.append(f"Q{i + 1} {'✓' if ok else '✗'} {line.strip() or '(无作答)'}")
    return correct, details


def main() -> None:
    for path in sys.argv[1:3]:
        text = open(path, encoding='utf-8').read().strip()
        reply = ask_model(text)
        correct, details = grade(reply)
        print(f'== {path}: {correct}/{len(QUESTIONS)}')
        for d in details:
            print('  ' + d)


if __name__ == '__main__':
    main()
