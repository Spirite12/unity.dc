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
6. 创建 PR 前优先使用 `gh`；若 `gh` 不可用或未登录，输出明确的安装、登录和网页登录创建方案。

## 第一阶段：Core Skill 检查

1. 确认当前目标分支；若无法可靠判断，询问开发者。
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
7. 在阶段报告后追加询问：是否需要帮忙推送当前 Git 更改到远端。
   - 若 Core Skill 检查产生了文档或脚本改动，提示这些改动需要先提交并推送到远端，后续开发者使用 Skill 时才能获取最新内容。
   - 推送前必须先让开发者确认要提交/推送的文件范围、提交信息和目标远端分支。
   - 不把该询问等同于第一阶段审核通过；开发者可选择只确认报告、不推送，或确认报告并授权提交推送。

## 第二阶段：创建 GitHub PR

开发者确认第一阶段报告后，按以下顺序处理：

1. 优先判断当前环境是否可用 `gh`：
   - 先执行 `gh --version` 或 `Get-Command gh`；若 PATH 未刷新，可在常见安装目录或开发者提供路径中查找 `gh.exe`，并用完整路径重试。
   - 再执行 `gh auth status` 检查登录状态。
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
   - `gh auth status`
3. 确认每个仓库的当前分支、目标分支和远端仓库。
4. 基于分支整体改动列出 1-2 个 PR 标题候选，等待开发者给出最终标题。
5. 生成 PR 正文草稿，并等待开发者确认。正文至少包含：
   - 当前分支与目标分支；
   - 变更摘要；
   - Core Skill 自检结果；
6. 推送当前分支到 GitHub 远端。
7. 分别为主仓库和框架子仓库创建 PR。
8. PR 创建成功后，列出每个 GitHub PR 网页地址，确保开发者可以直接点开查看；若某个仓库不需要创建 PR，说明原因并给出已存在 PR 或 compare 页面地址。
