#!/usr/bin/env python3
"""根据仓库改动定位需要复核的 Skill 文档与检查项。"""

from __future__ import annotations

import argparse
from functools import lru_cache
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    """单条自检规则。"""

    rule_id: str
    summary: str
    triggers: tuple[str, ...]
    documents: tuple[str, ...]
    checks: tuple[str, ...]


@dataclass(frozen=True)
class SkillConfig:
    """单个 Skill 的自检配置。"""

    name: str
    description: str
    config_path: str
    rules: tuple[Rule, ...]


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(
        description="根据 git 改动定位需要进行 Skill 自检的文档与核对项。"
    )
    parser.add_argument(
        "--repo-root",
        default=str(default_repo_root()),
        help="仓库根目录，默认按脚本位置自动推导。",
    )
    parser.add_argument(
        "--registry",
        default=".agents/registries/skill-self-check.json",
        help="Skill 自检注册表路径，默认相对仓库根目录。",
    )
    parser.add_argument(
        "--base",
        help="对比起点；传入后将使用 git diff 模式收集改动。",
    )
    parser.add_argument(
        "--head",
        help="对比终点；未传时按 git diff 的默认行为处理。",
    )
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="手动指定要检查的相对路径，可重复传入。",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="若命中规则但对应文档一个都未出现在当前改动中，则返回非零退出码。",
    )
    return parser.parse_args()


def default_repo_root() -> Path:
    """根据脚本所在位置反推仓库根目录。"""
    return Path(__file__).resolve().parents[2]


def normalize_path(path_text: str) -> str:
    """统一路径分隔符，便于跨平台匹配。"""
    normalized = path_text.replace("\\", "/").strip()
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


@lru_cache(maxsize=None)
def compile_glob(pattern: str) -> re.Pattern[str]:
    """将仓库内使用的 glob 规则转换为正则表达式。"""
    parts: list[str] = ["^"]
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                while index + 1 < len(pattern) and pattern[index + 1] == "*":
                    index += 1
                parts.append(".*")
            else:
                parts.append("[^/]*")
        elif char == "?":
            parts.append("[^/]")
        else:
            parts.append(re.escape(char))
        index += 1
    parts.append("$")
    return re.compile("".join(parts))


def run_git(repo_root: Path, args: list[str]) -> str:
    """执行 git 命令并返回标准输出。"""
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=False,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git 命令执行失败。")
    return completed.stdout


def parse_porcelain_paths(output: str) -> list[str]:
    """从 git status --porcelain 输出中提取路径。"""
    paths: list[str] = []
    for raw_line in output.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue

        payload = line[3:] if len(line) >= 4 else ""
        if " -> " in payload:
            payload = payload.split(" -> ", maxsplit=1)[1]
        payload = payload.strip('"')
        normalized = normalize_path(payload)
        if normalized:
            paths.append(normalized)
    return sorted(set(paths))


def collect_changed_files(repo_root: Path, base: str | None, head: str | None, paths: list[str]) -> list[str]:
    """收集当前需要参与自检的改动路径。"""
    if paths:
        return sorted({normalize_path(item) for item in paths if normalize_path(item)})

    if base:
        diff_args = ["diff", "--name-only", "--diff-filter=ACDMRTUXB", base]
        if head:
            diff_args.append(head)
        output = run_git(repo_root, diff_args)
        return sorted({normalize_path(line) for line in output.splitlines() if normalize_path(line)})

    output = run_git(repo_root, ["status", "--porcelain=v1", "--untracked-files=all"])
    return parse_porcelain_paths(output)


def load_skill_configs(repo_root: Path, registry_path: str) -> list[SkillConfig]:
    """读取已注册的 Skill 自检配置。"""
    registry_file = (repo_root / registry_path).resolve()
    registry_data = json.loads(registry_file.read_text(encoding="utf-8"))

    configs: list[SkillConfig] = []
    for item in registry_data.get("skills", []):
        config_rel_path = normalize_path(item["config"])
        config_file = (repo_root / config_rel_path).resolve()
        raw_config = json.loads(config_file.read_text(encoding="utf-8"))
        rules = tuple(
            Rule(
                rule_id=rule["id"],
                summary=rule["summary"],
                triggers=tuple(normalize_path(pattern) for pattern in rule.get("triggers", [])),
                documents=tuple(normalize_path(doc) for doc in rule.get("documents", [])),
                checks=tuple(rule.get("checks", [])),
            )
            for rule in raw_config.get("rules", [])
        )
        configs.append(
            SkillConfig(
                name=raw_config["skill"],
                description=raw_config.get("description", ""),
                config_path=config_rel_path,
                rules=rules,
            )
        )
    return configs


def matches_pattern(path_text: str, pattern: str) -> bool:
    """判断路径是否命中 glob 规则。"""
    normalized_path = normalize_path(path_text)
    normalized_pattern = normalize_path(pattern)
    if not normalized_pattern:
        return False
    if normalized_path == normalized_pattern:
        return True
    return bool(compile_glob(normalized_pattern).match(normalized_path))


def rule_matches(rule: Rule, changed_files: list[str]) -> bool:
    """判断一条规则是否被当前改动触发。"""
    for path_text in changed_files:
        if any(matches_pattern(path_text, pattern) for pattern in rule.triggers):
            return True
    return False


def format_report(
    changed_files: list[str],
    matched_configs: list[tuple[SkillConfig, list[Rule]]],
) -> tuple[str, bool]:
    """生成文本报告，并返回是否存在“命中规则但未修改任何对应文档”的情况。"""
    lines: list[str] = []
    lines.append("[skill-self-check] 已收集改动路径：")
    if changed_files:
        for path_text in changed_files:
            lines.append(f"- {path_text}")
    else:
        lines.append("- 当前没有检测到未提交改动。")

    missing_docs_found = False
    if not matched_configs:
        lines.append("")
        lines.append("[skill-self-check] 未命中任何已注册 Skill 的自检规则。")
        return "\n".join(lines), missing_docs_found

    lines.append("")
    lines.append(f"[skill-self-check] 命中 {len(matched_configs)} 个 Skill：")
    changed_set = set(changed_files)
    for config, matched_rules in matched_configs:
        documents: list[str] = []
        checks: list[str] = []
        for rule in matched_rules:
            for document in rule.documents:
                if document not in documents:
                    documents.append(document)
            for check in rule.checks:
                if check not in checks:
                    checks.append(check)

        touched_documents = [document for document in documents if document in changed_set]
        pending_documents = [document for document in documents if document not in changed_set]
        if documents and not touched_documents:
            missing_docs_found = True

        lines.append(f"- Skill：{config.name}")
        if config.description:
            lines.append(f"  说明：{config.description}")
        lines.append("  命中规则：")
        for rule in matched_rules:
            lines.append(f"  - {rule.rule_id}：{rule.summary}")
        if documents:
            lines.append("  建议复核文档：")
            for document in documents:
                lines.append(f"  - {document}")
        if touched_documents:
            lines.append("  本次已改动的相关文档：")
            for document in touched_documents:
                lines.append(f"  - {document}")
        if pending_documents:
            lines.append("  当前尚未改动、但建议重点检查的文档：")
            for document in pending_documents:
                lines.append(f"  - {document}")
        if checks:
            lines.append("  核对点：")
            for check in checks:
                lines.append(f"  - {check}")

    return "\n".join(lines), missing_docs_found


def main() -> int:
    """脚本主入口。"""
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.is_dir():
        print(f"仓库目录不存在：{repo_root}", file=sys.stderr)
        return 2

    try:
        changed_files = collect_changed_files(
            repo_root=repo_root,
            base=args.base,
            head=args.head,
            paths=args.path,
        )
        configs = load_skill_configs(repo_root=repo_root, registry_path=args.registry)
    except Exception as exc:  # noqa: BLE001
        print(f"[skill-self-check] {exc}", file=sys.stderr)
        return 2

    matched_configs: list[tuple[SkillConfig, list[Rule]]] = []
    for config in configs:
        matched_rules = [rule for rule in config.rules if rule_matches(rule, changed_files)]
        if matched_rules:
            matched_configs.append((config, matched_rules))

    report, missing_docs_found = format_report(changed_files, matched_configs)
    print(report)

    if args.strict and missing_docs_found:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
