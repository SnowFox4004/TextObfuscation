import jieba
import time


def load_jieba_freq():
    # 加载jieba的词典文件路径（通常位于安装目录下的dict.txt）
    dict_path = jieba.get_dict_file().name
    word_freq = {}
    with open(dict_path, "r", encoding="utf-8") as f:
        for line in f:
            word, freq, _ = line.strip().split(" ")
            word_freq[word] = int(freq)
    return word_freq


def query_frequency(word: str) -> int:
    return word_freq.get(word, 0)


__start = time.perf_counter()
# 加载词频字典
word_freq = load_jieba_freq()
print(f"加载耗时 : {time.perf_counter() - __start}")

if __name__ == "__main__":

    # 查询词语的常见程度
    while 1:
        word = input("请输入词语：")
        if word == "":
            break
        print(f"{word} 的常见程度：{query_frequency(word)}")
