# 笔记说明

- 本文列出开发过程中知识笔记；

# 笔记

1. **ADF 导致的打包失败**

   - ADF资源的同层级以及子目录不允许有 Editor 文件夹，会导致打包失败；要想放 Editor 文件夹的话，则额外给这个 Editor 文件夹添加 ADF 资源，并设置平台为 Editor ；[参考链接](https://zhuanlan.zhihu.com/p/34285007)

2. **Git 仓库设置提交信息**

  - 全局提交信息在 Fork -> File -> Preferences -> Git，查看个人提交信息；

  - 如想为指定仓库使用不同的用户名和邮箱，则打开当前仓库根路径 -> .git -> config，并添加如下代码：

    - ```bash
      [user]
          name = XXX
          email = YYY
      ```

  - 验证方式：打开当前仓库的控制台（Console） 窗口，输入如下指令：

    - ```bash
      git config --get user.name
      git config --get user.email
      ```

3. **Git 全局忽略文件**

  - Git 处理 `.gitignore` 的顺序如下：

    - 全局 `.gitignore`  文件（gitignore_global.txt）
    - 仓库级 `.gitignore` 文件（在 `工程目录/.gitignore`）
    - Git 本地配置（`core.excludesFile` 可能定义额外忽略规则）

  - 使用 git 指令查询：全局忽略文件路径如下：

    - ```
      git config --global core.excludesFile
      ```

  - 使用 git 指令查询：某个文件在哪个忽略文件产生效果如下：

    - ```
      git check-ignore -v xxx（xxx为查询文件）
      ```
