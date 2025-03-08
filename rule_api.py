import os
import random as rnd
import time
import test_jieba as jbquery
import math

__start = time.perf_counter()
rule_file_name = "chinese_dictionary\dict_antonym.txt"
with open(rule_file_name, "r", encoding="utf-8") as f:
    lines = f.readlines()
    # lines.sort(key=lambda x: len(x))
    for i in range(len(lines)):
        lines[i] = (
            lines[i]
            .strip()
            .replace("——", "--")  # 神人分隔符
            .replace("──", "--")
            .replace("—", "--")
            .replace("―", "--")
            .split("--")
        )
    rules = lines


print("读取反义词规则成功 共有", len(rules))
# print(f"preview: \n{chr(10).join(str(i) for i in rules[:10])}")

for _ in enumerate(filter(lambda x: len(x) < 2, rules)):
    print(_)


rules_weight = [
    math.log10(jbquery.query_frequency(rule[0]) + 0.001)
    + math.log10(jbquery.query_frequency(rule[1]) + 0.001)
    for rule in rules
]
print(f"读取反义词权重成功 耗时: {time.perf_counter() - __start}s")
# print(f"weight preview: {set(rules_weight)}")


def get_rule(num: int = 10):
    return set(tuple(i) for i in rnd.choices(rules, rules_weight, k=num))


if __name__ == "__main__":
    print(len(get_rule(5000)))
