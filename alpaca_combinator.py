import os
import json
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Alpaca格式数据集合并工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input-dir", required=True, help="Alpaca格式数据集目录路径"
    )
    parser.add_argument(
        "-o", "--output-file", default="./merged.json", help="合并后文件输出路径"
    )
    parser.add_argument(
        "-f",
        "--force",
        default=False,
        help="是否强制覆盖已存在的文件",
        action="store_true",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    output_file = Path(args.output_file)
    if not input_dir.exists():
        raise FileNotFoundError(f"输入目录不存在: {input_dir}")

    merged_dataset = []
    for file in input_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            dataset = json.load(f)
            merged_dataset.extend(dataset)

    if not os.path.exists(output_file.parent):
        os.makedirs(output_file.parent, exist_ok=True)

    if output_file.exists() and not args.force:
        raise FileExistsError(f"输出文件已存在: {output_file}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_dataset, f, ensure_ascii=False, indent=4)

    print(f"合并完成，共合并 {len(merged_dataset)} 条数据，输出文件为: {output_file}")


if __name__ == "__main__":
    main()
