import argparse
import json
import os
import time
import unicodedata as ud
from pathlib import Path

import tqdm
from loguru import logger

import test_replace as rplc


def convert_fiction(
    input_dir: str, output_dir: str, confusion_lvl: int = 500, force: bool = False
):
    # logger.info("Converting {}".format(input_dir))
    output_dir = Path(output_dir)
    input_dir = Path(input_dir)

    fiction_files = list(
        filter(lambda filename: filename.endswith("txt"), os.listdir(input_dir))
    )

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for file in tqdm.tqdm(fiction_files):
        if os.path.exists(output_dir / file) and not force:
            logger.warning(f"skipping exist file {file}")
            continue

        replaced_content = rplc.replace_file(input_dir / file, confusion_lvl)
        open(output_dir / file, "w+", encoding="utf-8").write(replaced_content)
    logger.success(f"converted {input_dir.relative_to(os.getcwd())} successfully!")


def create_aplaca_from_dir(
    input_dir: str,
    origin_dir: str,
    output_dir: str,
    force: bool = False,
    slice_len: int = 1000,
):
    """
    将混淆后的 `fiction` 目录下所有文件 转换为`aplaca`格式
    """

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    origin_dir = Path(origin_dir)
    alpaca_filename = f"{input_dir.name}_aplaca.json"

    # logger.info(f"Converting {input_dir}/ to aplaca format")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_dir / alpaca_filename) and not force:
        logger.warning("aplaca.json already exists, skipping...")
        return

    fiction_files = list(
        filter(lambda filename: filename.endswith("txt"), os.listdir(input_dir))
    )

    dataset = []
    for file in tqdm.tqdm(fiction_files):
        with open(input_dir / file, "r", encoding="utf-8") as f:
            mixed_content = f.read()
        with open(origin_dir / file, "r", encoding="utf-8") as f:
            origin_content = f.read()
            origin_content = ud.normalize("NFKC", origin_content)

        for i in range(0, len(mixed_content), slice_len):
            current_mix = mixed_content[i : i + slice_len]
            current_ori = origin_content[i : i + slice_len]
            dataset.append(
                {
                    "instruction": "以下是一段混淆的文本，请将其还原为正常的文本。",
                    "input": current_mix,
                    "output": current_ori,
                }
            )

    json.dump(
        dataset,
        open(output_dir / alpaca_filename, "w+", encoding="utf-8"),
        indent=4,
        ensure_ascii=False,
    )
    logger.success(
        f"成功生成 {output_dir.relative_to(os.getcwd())}/aplaca.json 数据集文件"
    )
    logger.success(f"共生成 {len(dataset)} 条数据")


def main():
    parser = argparse.ArgumentParser(
        description="文本混淆及Alpaca格式数据集生成工具",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-i", "--input-dir", required=True, help="原始文本目录路径")
    parser.add_argument(
        "-m",
        "--mixed-dir",
        help="混淆后文件输出目录（默认自动生成到 ./data_converted/输入目录名）",
    )
    parser.add_argument(
        "-d", "--dataset-dir", default="./datasets", help="Alpaca格式数据集输出目录"
    )
    parser.add_argument(
        "-l",
        "--confusion-lvl",
        type=int,
        default=500,
        help="混淆程度等级 (数值越大替换越多)",
    )
    parser.add_argument(
        "-f",
        "--force",
        # type=bool,
        default=False,
        help="是否强制覆盖已存在的文件",
        action="store_true",
    )
    args = parser.parse_args()

    # 输入目录处理
    input_path = Path(args.input_dir)
    if not input_path.exists():
        raise FileNotFoundError(f"输入目录不存在: {input_path}")
    if not input_path.is_dir():
        raise NotADirectoryError(f"输入路径不是目录: {input_path}")

    # 自动生成混合目录
    if not args.mixed_dir:
        args.mixed_dir = Path(f"./data_converted/{input_path.name}")
    else:
        args.mixed_dir = Path(args.mixed_dir)

    # 日志输出路径信息
    logger.info(f"输入目录: {input_path}")
    logger.info(f"混淆输出目录: {args.mixed_dir}")
    logger.info(f"数据集输出目录: {Path(args.dataset_dir)}")

    input_path = input_path.resolve()
    args.mixed_dir = args.mixed_dir.resolve()
    args.dataset_dir = Path(args.dataset_dir).resolve()

    # 执行处理流程
    start_time = time.time()
    convert_fiction(
        input_dir=str(input_path),
        output_dir=str(args.mixed_dir),
        confusion_lvl=args.confusion_lvl,
        force=args.force,
    )
    create_aplaca_from_dir(
        input_dir=str(args.mixed_dir),
        origin_dir=str(input_path),
        output_dir=args.dataset_dir,
        force=args.force,
    )
    logger.success(f"全流程完成! 总耗时: {time.time() - start_time:.2f}s")


if __name__ == "__main__":
    # os._exit(0)
    # convert_fiction(
    #     input_dir="./fictions/test",
    #     output_dir="./data_converted/test",
    #     confusion_lvl=500,
    # )
    # create_aplaca_from_dir(
    #     input_dir="./data_converted/test",
    #     origin_dir="./fictions/test",
    #     output_dir="./datasets/test",
    # )
    pass
    main()
