import rule_api as rquery
import unicodedata as ud


def replace_file(file_name: str, confusion_lvl: int = 500, encoding="utf-8"):
    rules = rquery.get_rule(confusion_lvl)

    with open(file_name, "r", encoding=encoding) as f:
        content = f.read()
    content = ud.normalize("NFKC", content)

    for rule in rules:
        content = content.replace(rule[0], rule[1])
    return content


def replace_txt(text: str, confusion_lvl: int = 500):
    rules = rquery.get_rule(confusion_lvl)
    text = ud.normalize("NFKC", text)
    for rule in rules:
        text = text.replace(rule[0], rule[1])
    return text


if __name__ == "__main__":
    test_file = "fictions/test/temp1.txt"
    content = replace_file(test_file, 1000)

    print(content)
