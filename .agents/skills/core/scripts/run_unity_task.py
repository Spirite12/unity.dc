#!/usr/bin/env python3
"""通过 Unity 命令行执行项目内的 Editor 静态入口。"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable


TASK_METHODS = {
    "table": "TableEditor.PackageConfig",
    "localize": "LocalizeEditor.CreateLocalizeAsset",
}


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="调用 Unity Editor 的 -executeMethod 执行导表或本地化相关入口。"
    )
    parser.add_argument(
        "task",
        choices=("table", "localize", "all", "init-localize"),
        help="要执行的任务：table=一键导表，localize=本地化资源生成，all=依次执行导表与本地化资源生成，init-localize=按 LocalizeRules 的两个按钮顺序执行初始化。",
    )
    parser.add_argument(
        "--project-path",
        default=str(default_project_path()),
        help="Unity 项目根目录，默认自动定位到当前仓库根目录。",
    )
    parser.add_argument(
        "--unity-path",
        help="Unity.exe 的完整路径；未传时会尝试按项目版本自动查找。",
    )
    parser.add_argument(
        "--log-file",
        default="-",
        help="Unity 的日志输出位置，默认使用 '-' 输出到当前终端。",
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="额外透传给 Unity 的单个参数，可重复传入多次。",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印最终命令，不实际启动 Unity。",
    )
    return parser.parse_args()


def default_project_path() -> Path:
    """从 skill 脚本目录反推仓库根目录。"""
    return Path(__file__).resolve().parents[4]


def read_project_version(project_path: Path) -> str:
    """读取 Unity 项目版本。"""
    version_file = project_path / "ProjectSettings" / "ProjectVersion.txt"
    if not version_file.is_file():
        raise FileNotFoundError(f"未找到 Unity 版本文件：{version_file}")

    match = re.search(r"m_EditorVersion:\s*(.+)", version_file.read_text(encoding="utf-8"))
    if not match:
        raise RuntimeError(f"无法从 {version_file} 解析 Unity 版本号。")
    return match.group(1).strip()


def iter_common_unity_paths(version: str) -> Iterable[Path]:
    """按常见安装目录生成 Unity 候选路径。"""
    roots: list[Path] = []
    for env_name in ("UNITY_EXE",):
        value = os.environ.get(env_name)
        if value:
            yield Path(value).expanduser()

    for env_name in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
        value = os.environ.get(env_name)
        if value:
            roots.append(Path(value))

    seen: set[str] = set()
    for root in roots:
        candidates = [
            root / "Unity" / "Hub" / "Editor" / version / "Editor" / "Unity.exe",
            root / "Unity" / "Editor" / "Unity.exe",
        ]
        for candidate in candidates:
            key = str(candidate).lower()
            if key in seen:
                continue
            seen.add(key)
            yield candidate


def resolve_unity_path(project_path: Path, provided_path: str | None) -> Path:
    """解析 Unity 可执行文件路径。"""
    if provided_path:
        path = Path(provided_path).expanduser()
        if path.is_file():
            return path
        raise FileNotFoundError(f"--unity-path 指定的文件不存在：{path}")

    version = read_project_version(project_path)
    for candidate in iter_common_unity_paths(version):
        if candidate.is_file():
            return candidate

    raise FileNotFoundError(
        "未能自动找到 Unity.exe。请显式传入 --unity-path，"
        f"或设置 UNITY_EXE 环境变量。项目版本：{version}"
    )


def build_command(
    unity_path: Path,
    project_path: Path,
    method_name: str,
    log_file: str,
    extra_args: list[str],
) -> list[str]:
    """组装 Unity 执行命令。"""
    command = [
        str(unity_path),
        "-batchmode",
        "-quit",
        "-projectPath",
        str(project_path),
        "-executeMethod",
        method_name,
        "-logFile",
        log_file,
    ]
    command.extend(extra_args)
    return command


def validate_localize_root(project_path: Path) -> None:
    """在执行本地化资源生成前做目录检查。"""
    localize_root = project_path / "Assets" / "Game" / "Localize"
    if not localize_root.exists():
        raise FileNotFoundError(
            f"本地化资源目录不存在：{localize_root}。"
            "请先创建目录结构，再执行 localize 任务。"
        )


def run_task(
    task_name: str,
    unity_path: Path,
    project_path: Path,
    log_file: str,
    extra_args: list[str],
    dry_run: bool,
) -> int:
    """执行单个 Unity 自动化任务。"""
    if task_name == "localize":
        validate_localize_root(project_path)

    method_name = TASK_METHODS[task_name]
    command = build_command(unity_path, project_path, method_name, log_file, extra_args)
    print(f"[run_unity_task] 执行任务: {task_name}")
    print("[run_unity_task] 命令: " + " ".join(f'"{item}"' if " " in item else item for item in command))

    if dry_run:
        return 0

    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> int:
    """脚本主入口。"""
    args = parse_args()
    project_path = Path(args.project_path).expanduser().resolve()
    if not project_path.is_dir():
        print(f"项目目录不存在：{project_path}", file=sys.stderr)
        return 2

    try:
        unity_path = resolve_unity_path(project_path, args.unity_path)
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 2

    if args.task in ("all", "init-localize"):
        tasks = ("table", "localize")
    else:
        tasks = (args.task,)
    for task_name in tasks:
        try:
            exit_code = run_task(
                task_name=task_name,
                unity_path=unity_path,
                project_path=project_path,
                log_file=args.log_file,
                extra_args=args.extra_arg,
                dry_run=args.dry_run,
            )
        except Exception as exc:  # noqa: BLE001
            print(str(exc), file=sys.stderr)
            return 2

        if exit_code != 0:
            print(f"[run_unity_task] 任务失败: {task_name}，退出码：{exit_code}", file=sys.stderr)
            return exit_code

    print("[run_unity_task] 全部任务执行完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
