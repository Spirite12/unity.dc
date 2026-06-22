---
name: github-pr
description: 用于提交当前项目到 GitHub 并创建 Pull Request。适用于用户要求提交当前分支、推送远端、创建 PR、请求合并主仓库与 Assets/DCFrame 框架子仓库时；流程包含 PR 前 Core Skill 检查、开发者确认、分仓库推送与 PR 创建。
---

# GitHub PR 流程

用于在当前 Unity 项目中准备并创建 GitHub Pull Request。当前项目固定包含两个仓库：

- 主仓库：仓库根目录
- 框架子仓库：`..\Assets\DCFrame`，以该目录下 `.git` 为准

## 总体约束

1. 先执行 PR 前 Core Skill 检查，经开发者审核确认后，再进入 PR 创建阶段。
2. 不自动处理与本次 PR 无关的脏改动；若发现无关改动，明确列出并避开。
3. 不使用 `git reset --hard`、强推或破坏性命令，除非开发者明确要求。
4. GitHub token、浏览器登录和权限授权由开发者处理；Agent 只检查 `gh auth status` 并说明阻塞点。
5. PR 标题必须由开发者最终确认。Agent 先基于分支整体改动列出 1-2 个标题候选，再等待开发者给出最终标题。

## 第一阶段：PR 前 Core Skill 检查

1. 确认目标分支。优先读取远端默认分支；若无法可靠判断，询问开发者。
2. 读取当前分支相对目标分支的全部改动，而不是逐提交自检。
3. 汇总分支整体改动命中的节点、目录与关键入口。
4. 只检查 Core Skill：
   - 使用 `.agents/registries/skill-self-check.json` 中注册的 `core` 配置。
   - 若改动影响 Core Skill 事实，补丁式更新 `.agents/skills/core/SKILL.md` 或对应 `references/*.md`。
   - 不检查 `github-pr` 自身，不做全量 Skill 自检，除非开发者另行要求。
5. 修改完成后执行一次 Core Skill 检查，优先使用：
   - `python .agents/scripts/skill_self_check.py --base <目标分支> --head <当前分支>`
   - 若存在无关脏改动，使用 `--path` 缩小到本次相关路径。
6. 输出阶段报告并停止等待开发者确认。报告必须包含：
   - 对比的目标分支与当前分支；
   - 命中的节点、目录或模块；
   - Core Skill 是否需要更新；
   - 已更新的文件与具体内容摘要；
   - Core Skill 检查命令与结果；
   - 需要开发者审核确认的事项。

## 第二阶段：创建 GitHub PR

开发者确认第一阶段报告后，按以下顺序处理：

1. 分别检查主仓库与框架子仓库的状态：
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`
   - `gh auth status`
2. 确认每个仓库的当前分支、目标分支和远端仓库。
3. 基于分支整体改动列出 1-2 个 PR 标题候选，等待开发者给出最终标题。
4. 生成 PR 正文草稿，并等待开发者确认。正文至少包含：
   - 仓库类型：主仓库或框架子仓库；
   - 当前分支与目标分支；
   - 变更摘要；
   - Core Skill 自检结果；
   - 人工审核或 Unity 编辑器内确认项。
5. 推送当前分支到 GitHub 远端。
6. 分别为主仓库和框架子仓库创建 PR。
7. 输出两个 PR 链接；若某个仓库不需要创建 PR，说明原因。

## 常用命令提示

- 查看默认远端分支：`git remote show origin`
- 查看分支改动文件：`git diff --name-only <base>...HEAD`
- 查看当前脏改动：`git status --short`
- 检查 GitHub CLI 登录：`gh auth status`
- 创建 PR：`gh pr create --base <target> --head <branch> --title "<title>" --body "<body>"`
