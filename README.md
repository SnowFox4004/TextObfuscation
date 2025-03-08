# 文本混淆器

## 使用

生成混淆文本

```python
python dataset_creator.py -i <input_dir:str> -l <lvl_of_obfuscation:int> -o [output_dir:str]
```

合并混淆数据集

```python
python alpaca_combinator.py -i <input_dir:str> -o [output_filename:str, default: merged.json]
```

参数说明:

```python
python dataset_creator.py -h
```

## 鸣谢

[词义对照开源项目 https://github.com/guotong1988/chinese_dictionary.git](https://github.com/guotong1988/chinese_dictionary.git)

## 免责声明

使用者应对输出内容进行独立判断并承担所有风险，开发者不对任何直接/间接损失或后果承担责任。使用者须确保其应用场景符合所在司法管辖区法律法规.
禁止用于以下用途（包括但不限于）：

1. 生成违法、侵权、欺诈、歧视、暴力或违反公序良俗的内容
2. 制造虚假信息、实施网络攻击或破坏网络安全
3. 任何可能危及人身安全或国家安全的行为
