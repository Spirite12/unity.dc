@AGENTS.md

## Claude Code 兼容说明

- 本文件仅作为 Claude Code 的项目入口，仓库级协作约束以 `AGENTS.md` 为主源。
- 本仓库的项目 Skill 主源位于 `.agents/skills/`。
- 当任务需要使用项目 Skill 时，请优先读取 `.agents/skills/<skill-name>/SKILL.md`，并按其中的 `references`、`scripts` 与边界说明继续执行。
- 不在 `.claude/skills/` 维护重复 Skill；避免新增或修改 Skill 时产生多处同步成本。
