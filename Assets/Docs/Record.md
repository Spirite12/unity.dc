# 笔记说明

- 本文列出开发过程中知识笔记；

# 笔记

- **ADF 导致的打包失败：**ADF资源的同层级以及子目录不允许有 Editor 文件夹，会导致打包失败；要想放 Editor 文件夹的话，则额外给这个 Editor 文件夹添加 ADF 资源，并设置平台为 Editor ；[参考链接](https://zhuanlan.zhihu.com/p/34285007)

- **Git 仓库设置提交信息：**全局提交信息在 Fork -> File -> Preferences -> Git，查看个人提交信息；

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
