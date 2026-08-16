#!/usr/bin/env python3
"""explain-to-me / ste-language-improvement 可理解性度量套件。

对"改进前 / 改进后"两段文本计算四层指标,全部确定性、可复现:

A 术语可及性 —— 区分「必须保留的代码标识符」与「未解释的行话」:
    A1 未解释行话密度(个/百字):行话出现且当句无中文释义(括号附注或反引号)的次数
    A2 行话首现释义率:不同行话中,首次出现即带释义的比例
B 句法完整性 —— 客观判定"成句",不用动词词表:
    B1 列表条目成句率:以句末标点(。!?!)结尾的条目占比
    B2 描述句长:以汉字计的平均句长(上下文参考,不设好坏阈值)
C 信息完整性 —— 事实原子保留率:从原文枚举数字/标识符/文件/条件等
   事实原子,逐一核对在改写文本中出现(保留率,可人工复查清单)
D 残留缩写负担 —— 项目内缩写(如 M3、V5)在两版中的未展开计数。
   语言层修不掉的部分,显式呈现,交给 explain-to-me 的会话导入层解决。

用法:python3 measure.py before.txt after.txt
"""

import re
import sys
from dataclasses import dataclass, field

SENTENCE_END = '。!?!'
GLOSS_PATTERN_CACHE = None


def load_text(path: str) -> str:
    return open(path, encoding='utf-8').read().strip()


def split_sentences(text: str) -> list[str]:
    parts: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.endswith(':') or line.endswith('：'):
            continue
        line = line.lstrip('- ').strip()
        parts.extend(p.strip() for p in re.split(r'[。;；]', line) if p.strip())
    return parts


def bullets(text: str) -> list[str]:
    return [l.strip().lstrip('- ').strip() for l in text.splitlines() if l.strip().startswith('- ')]


def zh_chars(text: str) -> int:
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def inside_backticks(sentence: str) -> set[str]:
    return set(re.findall(r'`([^`]+)`', sentence))


@dataclass
class TermStats:
    total_occurrences = 0
    unexplained_occurrences = 0
    terms: dict[str, bool] = field(default_factory=dict)  # term -> first occurrence glossed?

    def density_per_100(self, zh: int) -> float:
        return self.unexplained_occurrences / max(1, zh) * 100

    @property
    def first_gloss_rate(self) -> float:
        if not self.terms:
            return 1.0
        return sum(self.terms.values()) / len(self.terms)


def is_code_identifier(token: str) -> bool:
    """代码标识符/路径/命令/文件名:包含 _ . / 数字后缀、-- 选项、已知扩展名,或全大写常量。"""
    if any(ch in token for ch in '_'):
        return True
    if '--' in token:
        return True
    if re.search(r'\.[a-z]{1,5}$', token):  # .json .md .mjs ...
        return True
    if token.isupper() and len(token) <= 6 and token.isalpha():
        return True
    return False


def prose_jargon_terms(sentence: str) -> list[str]:
    """行话:连续 1–3 个英文小写词,排除代码标识符、反引号内容、链接目标。"""
    code = inside_backticks(sentence)
    sentence = re.sub(r'`[^`]+`', ' ', sentence)
    sentence = re.sub(r'\]\([^)]*\)', '] ', sentence)  # markdown 链接目标
    terms = []
    for match in re.finditer(r'[A-Za-z][A-Za-z/-]*(?:\s+[a-z][a-z/-]*){0,2}', sentence):
        raw = match.group(0).strip()
        words = raw.split()
        # 逐词归组:尾部词若像标识符则截断
        kept: list[str] = []
        for w in words:
            if is_code_identifier(w) or w in code:
                break
            kept.append(w)
        if kept and not is_code_identifier(kept[0]):
            terms.append(' '.join(kept))
    return [t for t in terms if len(t) > 2]


def glossed(term: str, sentence: str) -> bool:
    """当句内释义:术语出现在中文全/半角括号里,或本身在反引号里。"""
    if term in inside_backticks(sentence):
        return True
    escaped = re.escape(term)
    return re.search(r'[（(][^（）()]*' + escaped + r'[^（）()]*[)）]', sentence) is not None


def term_stats(text: str) -> TermStats:
    stats = TermStats()
    for sentence in split_sentences(text):
        for term in prose_jargon_terms(sentence):
            ok = glossed(term, sentence)
            stats.total_occurrences += 1
            if not ok:
                stats.unexplained_occurrences += 1
            if term not in stats.terms:
                stats.terms[term] = ok
    return stats


def fact_atoms(text: str) -> list[str]:
    """从原文枚举可核对的事实原子:反引号标识符、数字、链接文件名、字母-数字代号。"""
    atoms: list[str] = []
    atoms += re.findall(r'`([^`]+)`', text)
    atoms += re.findall(r'\]\(([^)]+)\)', text)
    atoms += re.findall(r'\b\d+(?:/\d+)?\b', text)
    atoms += re.findall(r'\b[A-Z]{1,3}\d+[A-Za-z0-9-]*\b', text)
    return list(dict.fromkeys(a.strip() for a in atoms if a.strip()))


def fact_recall(before: str, after: str) -> tuple[float, list[str]]:
    missing = [a for a in fact_atoms(before) if a not in after]
    total = len(fact_atoms(before))
    return (total - len(missing)) / max(1, total), missing


def sentence_completeness(text: str) -> tuple[int, int]:
    bs = bullets(text)
    complete = sum(1 for b in bs if b and b[-1] in SENTENCE_END)
    return complete, len(bs)


def avg_sentence_len(text: str) -> float:
    lens = [len(re.findall(r'[\u4e00-\u9fff]', s)) for s in split_sentences(text)]
    return sum(lens) / max(1, len(lens))


def acronyms(text: str) -> list[str]:
    return sorted(set(re.findall(r'\b[A-Z]{1,3}\d+[A-Za-z0-9-]*\b', text)))


def report(name: str, text: str) -> dict:
    zh = zh_chars(text)
    ts = term_stats(text)
    complete, total_bullets = sentence_completeness(text)
    return {
        'name': name,
        'zh': zh,
        'A1_unexplained_per_100': ts.density_per_100(zh),
        'A2_first_gloss_rate': ts.first_gloss_rate,
        'A2_terms': dict(ts.terms),
        'B1_complete_bullets': (complete, total_bullets),
        'B2_avg_len': avg_sentence_len(text),
        'D_acronyms': acronyms(text),
    }


def main() -> None:
    before_path, after_path = sys.argv[1], sys.argv[2]
    before, after = load_text(before_path), load_text(after_path)
    rb, ra = report('改进前', before), report('改进后', after)
    recall, missing = fact_recall(before, after)

    for r in (rb, ra):
        c, t = r['B1_complete_bullets']
        print(f"{r['name']}: A1 未解释行话 {r['A1_unexplained_per_100']:.1f} 个/百字"
              f" | A2 首现释义率 {r['A2_first_gloss_rate']:.0%}({len(r['A2_terms'])} 个术语)"
              f" | B1 成句条目 {c}/{t}"
              f" | B2 平均句长 {r['B2_avg_len']:.0f} 字"
              f" | D 残留缩写 {','.join(r['D_acronyms']) or '无'}")
    print(f"C 事实原子保留率: {recall:.0%}(缺失: {missing or '无'})")
    print('A2 明细(改进后):', ', '.join(f"{t}={'释' if g else '未'}" for t, g in ra['A2_terms'].items()) or '无行话')


if __name__ == '__main__':
    main()
