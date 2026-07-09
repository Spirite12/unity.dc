---
name: github-pr
description: 用于处理当前项目的 GitHub Pull Request 相关工作，适用于主仓库与 Assets/DCFrame 框架子仓库的分支检查、远端同步和 PR 创建。
---

# GitHub PR 流程

用于在当前 Unity 项目中准备并创建 GitHub Pull Request。当前项目固定包含两个仓库：

- 主仓库：仓库根目录
- 框架子仓库：`..\Assets\DCFrame`，以该目录下 `.git` 为准

## 第一阶段：Core Skill 检查

1. 确认当前目标分支；若无法可靠判断，询问开发者。
2. 读取当前分支相对目标分支的整体改动；发现无关脏改动时，只列出并避开。
3. 汇总命中的节点、目录与关键入口。
4. 只检查 Core Skill：
   - 使用 `.agents/registries/skill-self-check.json` 中注册的 `core` 配置。
   - 若改动影响 Core Skill 事实，补丁式更新 `.agents/skills/core/SKILL.md` 或对应 `references/*.md`。
   - 不检查 `github-pr` 自身，除非开发者另行要求。
5. 执行一次 Core Skill 检查，优先使用：
   - `python .agents/scripts/skill_self_check.py --base <目标分支> --head <当前分支>`
   - 存在无关脏改动时，用 `--path` 缩小到本次相关路径。
6. 输出阶段报告并停止等待开发者确认。报告必须包含：
   - 目标分支、当前分支、命中范围；
   - Core Skill 是否更新、更新摘要、检查命令与结果；
   - 需要开发者确认的事项。
7. 询问是否进入 Todo 检查阶段；若本阶段产生 Skill 文档或脚本改动，提示需先提交并推送后，后续使用者才能获取最新内容。

## 第二阶段：Todo 检查与清理

开发者确认第一阶段报告后，先检查 `Assets/Docs/ToDo.md`，再决定是否进入 PR 创建阶段：

1. 确认 Todo 文件是否存在，以及检查前是否已有本地变更；若存在无关变更，先询问开发者，未经确认不修改。
2. 对照当前分支相对目标分支的提交和整体改动，只删除能明确对应为已完成的 Todo；无法确认、仅部分完成或无关事项必须保留。
3. 删除后检查 Todo 文件差异；若无有效差异，报告“Todo 无需清理”或“清理后无有效差异”。
4. Todo 文件有变更时，列出删除项、diff 摘要与文件状态，并询问是否允许仅提交并推送该清理改动；提交信息需遵守 `Assets/Docs/Standard.md`。
5. 输出阶段报告并停止等待开发者确认。报告必须包含：
   - Todo 文件状态、已删除项、保留的疑似相关项；
   - Todo 清理是否已提交、提交哈希与推送结果，或未提交/未推送原因；
   - 需要开发者确认的事项。

## 第三阶段：创建 GitHub PR

开发者确认第二阶段报告后，按以下顺序处理：

1. 优先判断当前环境是否可用 `gh`：
   - 先执行 `gh --version` 或 `Get-Command gh`；若 PATH 未刷新，可在常见安装目录或开发者提供路径中查找 `gh.exe`，并用完整路径重试。
   - 再执行 `gh auth status` 检查登录状态；GitHub token、浏览器登录和权限授权由开发者处理。
   - 若 `gh` 未安装或不可用，停止自动创建 PR，并输出对应仓库的 GitHub 创建页面地址：
     - 主仓库：`https://github.com/<owner>/<main-repo>/compare/<target>...<branch>?expand=1`
     - 框架子仓库：`https://github.com/<owner>/<frame-repo>/compare/<target>...<branch>?expand=1`
   - 同时输出 GitHub CLI 安装与登录提示：
     - 安装地址：`https://github.com/cli/cli/releases`
     - 第一次使用前需要登录 GitHub：`gh auth login`
     - 一般选择：`GitHub.com`、`HTTPS`、`Login with a web browser`
     - 登录完成后验证：`gh auth status`
2. 分别检查主仓库与框架子仓库的状态：
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`
3. 确认每个仓库的当前分支、目标分支和远端仓库；发现无关脏改动时，只列出并避开。
4. 基于分支整体改动列出 1-2 个 PR 标题候选，等待开发者给出最终标题。
5. 基于同一份分支整体改动，分别生成 PR 正文草稿与 `Assets/Docs/Version.md` 更新草稿，并等待开发者确认。
   - PR 正文至少包含：当前分支与目标分支、变更摘要、Core Skill 自检结果。
   - Version 更新需遵守 `Assets/Docs/Standard.md` 与 `Assets/Docs/Version.md` 现有格式，记录功能、修复、完善、导入包或文档信息；版本号与是否写入由开发者最终确认。
   - 若 `Assets/Docs/Version.md` 不存在或已有无关本地变更，先说明状态并询问开发者，未经确认不修改该文件。
6. 开发者确认后，按草稿更新 `Assets/Docs/Version.md`；若该文件产生变更，提交信息需遵守 `Assets/Docs/Standard.md`，并随当前分支推送到远端；若本次无需版本记录，说明原因并跳过。
7. 推送当前分支到 GitHub 远端；不使用 `git reset --hard`、强推或破坏性命令，除非开发者明确要求。
8. 分别为主仓库和框架子仓库创建 PR。
9. PR 创建成功后，列出每个 GitHub PR 网页地址，确保开发者可以直接点开查看；若某个仓库不需要创建 PR，说明原因并给出已存在 PR 或 compare 页面地址。
