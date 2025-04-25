# 将本地vscode编写的代码发布到github



使用 GitHub 记录编程学习进度是一个非常好的习惯，这不仅能帮助你追踪进步，还能让你熟悉版本控制，这是程序员必备的技能之一。

我们将分步进行，确保每一步都清晰明了。



## **核心概念速览：**

*   **Git:** 一种版本控制系统，用来追踪文件和代码的变化。想象成一个超级聪明的历史记录器，随时可以回溯到以前的版本。
*   **GitHub:** 一个基于 Git 的代码托管平台。你可以把本地用 Git 管理的项目放到 GitHub 上，方便备份、分享和协作（虽然你现在可能主要用于个人记录）。
*   **Repository (仓库):** 在 Git 和 GitHub 上，你的项目就被称为一个仓库。它包含了你的所有文件以及它们的历史记录。
*   **Clone (克隆):** 把 GitHub 上的仓库完整地复制到你的本地电脑上。
*   **Commit (提交):** 记录你对文件做的一次或一组修改。每次提交都有一个独特 ID 和一条描述信息（提交信息）。
*   **Push (推送):** 把你在本地仓库做的提交上传到 GitHub 上的远程仓库。
*   **Pull (拉取):** 把远程仓库（GitHub）上的最新变化下载到你的本地仓库。



## **步骤一：注册 GitHub 账号**

1.  打开浏览器，访问 [https://github.com/](https://github.com/)
2.  点击 "Sign up"（注册）按钮。
3.  按照提示填写信息（用户名、邮箱、密码）。
4.  完成邮箱验证。



## **步骤二：在 GitHub 上创建你的第一个仓库**

1.  登录 GitHub。
2.  在页面右上角找到你的头像，点击下拉菜单，选择 "Your repositories"（你的仓库）。
3.  点击绿色的 "New"（新建）按钮。
4.  **Repository name (仓库名称):** 给你的项目起个名字。建议用一个清晰的名字，比如 `my-learning-progress` 或者 `programming-journey-2023`。
5.  **Description (描述):** (可选) 简单描述一下这个仓库是用来干什么的，比如 "记录我的编程学习历程和代码练习"。
6.  **Public (公开) or Private (私有):**
    *   **Public (公开):** 任何人都能看到你的代码和进度。好处是以后可以分享给朋友，或者作为你的作品集。
    *   **Private (私有):** 只有你自己和邀请的人才能看到。如果你的学习笔记或代码涉及隐私，或者你只是想完全自己看，就选私有。
    *   **建议:** 作为学习记录，选择 **Private** 更自在，不用担心代码写得不好看被人看到。等你有信心了，可以再创建公开仓库展示作品。
7.  **Initialize this repository with:** (初始化仓库)
    *   ✅ **Add a README file:** **强烈建议勾选！** README 文件是项目的说明书，别人（或未来的你）一看就知道这是什么项目。GitHub 会自动创建一个 README.md 文件（使用 Markdown 格式编写）。
    *   Add .gitignore: (可选) 可以选择一个适合你学习语言的模板（比如 Python, Node），它会自动忽略一些不需要上传的文件（比如编译生成的文件、日志文件）。初期可以先不选，后面再加也行。
    *   Choose a license: (可选) 许可证决定了别人如何使用你的代码。对于个人学习记录，可以不选。
8.  点击绿色的 "Create repository"（创建仓库）按钮。

好了，你的第一个 GitHub 仓库就创建成功了！



## **步骤三：在你的电脑上安装 Git**

你需要安装 Git 软件才能在本地使用版本控制功能。

1.  **Windows:**
    *   访问 [https://git-scm.com/download/win](https://git-scm.com/download/win)
    *   下载安装包并运行。安装过程中选项很多，对于初学者，大部分保持默认设置即可。注意：在选择默认编辑器时，如果你熟悉 VS Code，可以选择 VS Code 作为默认编辑器（Git Bash comes with... -> Use Visual Studio Code as Git's default editor）。
2.  **macOS:**
    *   安装 Homebrew（如果没装过）：打开终端，运行 `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    *   使用 Homebrew 安装 Git：打开终端，运行 `brew install git`
    *   或者，安装 Xcode Command Line Tools 也会包含 Git：在终端运行 `xcode-select --install`
3.  **Linux:**
    *   Debian/Ubuntu: 打开终端，运行 `sudo apt-get update` 后运行 `sudo apt-get install git`
    *   Fedora: 打开终端，运行 `sudo dnf install git`
    *   CentOS/RHEL: 打开终端，运行 `sudo yum install git`

**验证安装：** 打开终端或命令提示符（Windows 搜索 cmd 或 PowerShell），输入 `git --version`，如果显示了 Git 的版本号，说明安装成功。



## **步骤四：配置 Git (重要！)**

在你开始使用 Git 之前，需要告诉 Git 你是谁，这样它才能正确地记录是谁做了哪些修改。

打开终端或命令提示符，输入以下两条命令（将 Your Name 替换成你的名字或昵称，将 your.email@example.com 替换成你注册 GitHub 用的邮箱）：

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

`--global` 参数表示这些设置会应用到你电脑上所有的 Git 仓库。



## **步骤五：将 GitHub 仓库克隆到本地电脑**

现在，我们要把你在 GitHub 上创建的仓库复制到本地。

1.  回到 GitHub 网站，找到你刚才创建的仓库页面。
2.  点击绿色的 `<> Code`（代码）按钮。
3.  你会看到一个弹窗，里面有几种克隆方式：HTTPS 和 SSH。
    *   **对于初学者，建议使用 HTTPS。** 它通常更简单，特别是结合 Git Credential Manager（凭据管理器）时。点击 HTTPS 选项卡，然后点击右边的复制按钮（一个剪贴板图标），复制仓库的 URL。URL 看起来像这样：`https://github.com/你的用户名/你的仓库名.git`
    *   SSH 更安全，不需要每次输入密码，但需要额外设置 SSH 密钥对。我们先从 HTTPS 开始。
4.  在你的电脑上，打开终端或命令提示符。
5.  导航到你想要存放项目文件的目录（比如 `Documents` 或 `Desktop`）。你可以使用 `cd` 命令来改变目录。例如：
    ```bash
    cd Documents
    # 如果是Windows，可能需要进入特定的盘符 E: 回车
    ```
6.  运行 `git clone` 命令，后面粘贴你刚才复制的 HTTPS URL：
    ```bash
    git clone https://github.com/你的用户名/你的仓库名.git
    ```
7.  Git 会开始下载仓库文件。过程中可能会提示你输入 GitHub 的用户名和密码。**注意：** 由于安全原因，GitHub 推荐使用 Personal Access Token (PAT) 代替密码进行 HTTPS 认证。但对于新手来说，现在更方便的方式是使用 **Git Credential Manager**。如果你安装 Git 时选择了默认选项，Git Credential Manager 通常会帮你处理认证问题，第一次操作时会弹出一个 GitHub 登录窗口，你登录后，它会记住你的凭据。
8.  克隆完成后，你会看到在你当前目录下多了一个文件夹，名字就是你的仓库名。进入这个文件夹：
    ```bash
    cd 你的仓库名
    ```

现在，你已经成功将 GitHub 仓库克隆到本地了！



## **步骤六：在 VS Code 中打开你的项目文件夹**

1.  打开 VS Code。
2.  点击菜单栏的 "File"（文件）-> "Open Folder..."（打开文件夹...）。
3.  导航到你刚才克隆下来的仓库文件夹（比如 `Documents/你的仓库名`），选中它，然后点击 "Select Folder"（选择文件夹）。

VS Code 会打开这个文件夹。在左侧的文件浏览器中，你应该能看到 README.md 文件。



## **步骤七：开始记录你的学习进度！ (修改和新增文件)**

现在你可以在这个文件夹里创建文件和编写内容了。这就是你记录学习进度的地方。

1.  **编辑 README.md:**
    *   点击左侧文件浏览器中的 `README.md` 文件。
    *   你可以在这里写下项目介绍、你的学习目标等等。Markdown 是一种很方便的格式（比如 `# 标题`, `- 列表`, `**加粗**`），GitHub 也能很好地渲染 Markdown 文件。
2.  **创建新的文件:**
    *   你可以在文件浏览器空白处右键点击，选择 "New File..."（新建文件...）。
    *   比如，你可以创建一个 `daily_progress.md` 文件来记录每日进度。
    *   或者，创建一个 `day1_intro.py` 文件，把你第一天学习 Python 写的代码放进去。
    *   你可以根据日期创建文件夹和文件，比如 `/Day01/learning_log.md`, `/Day01/first_script.py` 等等。

尽情地写下你的学习心得、遇到的问题、解决的方法、练习的代码吧！



## **步骤八：在 VS Code 中使用 Git (提交修改)**

当你对文件做了修改（比如编辑了 README 或新增了文件）后，VS Code 会检测到这些变化。

1.  在 VS Code 的侧边栏，点击第三个图标（三个圆点连起来的，叫做 **Source Control** 或 **源代码管理**）。
2.  你会看到一个列表，显示了所有被修改或新增的文件。这些文件目前处于 "Changes"（更改）区域。
3.  **暂存 (Stage Changes):** Git 有一个叫做“暂存区”的概念。你需要把你想包含在下一次提交中的变化添加到暂存区。
    *   对于每个你想提交的文件，点击文件名旁边的 `+` 号。
    *   或者，如果你想暂存所有变化，鼠标悬停在 "Changes" 标题上，点击出现的 `+` 图标 "Stage All Changes"。
    *   文件会从 "Changes" 区域移动到 "Staged Changes"（已暂存的更改）区域。
4.  **提交 (Commit):** 暂存好文件后，就可以提交了。
    *   在 "Message"（消息）文本框中，输入一条简短清晰的**提交信息**。这条信息是这条提交的“标题”，说明你这次做了什么修改。比如 "Add initial README content", "Record Day 1 progress and code", "Fix typo in learning log"。写好提交信息是一个好习惯！
    *   点击消息框上方的勾号按钮（Commit）。
    *   或者，使用快捷键 `Ctrl+Enter` (Windows) / `Cmd+Enter` (macOS)。

你现在已经完成了在本地仓库的第一次提交！这个提交包含了你暂存的所有修改，并且有你写的提交信息。



## **步骤九：将本地提交推送到 GitHub (同步到远程仓库)**

你的提交目前只存在于你的本地电脑上。为了让 GitHub 也能看到你的进度（并作为备份），你需要将本地提交推送到远程仓库。

1.  在 VS Code 的 Source Control 侧边栏顶部，会有一个蓝色的同步按钮（一个旋转的箭头图标），或者在右侧的 `...` 菜单中找到 "Push"（推送）选项。
2.  点击这个 **Sync Changes**（同步更改）按钮。
3.  VS Code 会询问你是否确定要推送并拉取（Pull, 把远程的新变化拉下来；Push, 把本地新变化推上去）。点击 **OK**。
4.  Git 会尝试连接到 GitHub 并上传你的提交。

*   **安全与认证:** 第一次推送时，如果之前没有设置好 Git Credential Manager 或 SSH key，Git 会弹出认证提示。
    *   **HTTPS + Git Credential Manager (推荐):** 如果你的系统有 Git Credential Manager，它会弹出一个 GitHub 登录窗口，你输入 GitHub 的账号和密码（或者使用浏览器授权）即可。一旦认证成功，后续它会记住你的凭据，通常不需要再次输入。这是对于初学者来说最方便的“安全有效联动”方式，因为它帮你处理了复杂的认证过程。
    *   **HTTPS + PAT:** 如果没有 Credential Manager 或者遇到问题，GitHub 可能会提示你输入用户名和密码。**此时不要输入你的 GitHub 账号密码！** GitHub 不再支持使用账号密码进行 Git 操作。你需要去 GitHub 网站生成一个 Personal Access Token (PAT)，并在密码提示时输入你的用户名，然后在密码位置输入这个 PAT。PAT 的生成步骤可以在 GitHub 设置里找到（Settings -> Developer settings -> Personal access tokens）。这个方法更安全，但稍微复杂一点。
    *   **SSH:** 克隆时如果使用的是 SSH URL (以 `git@github.com:` 开头)，推送时会使用 SSH 密钥对进行认证，这种方式也非常安全且无需输入密码。但你需要先生成 SSH 密钥并将公钥添加到你的 GitHub 账号设置中（Settings -> SSH and GPG keys）。这是一个非常推荐的长期方案，但初期设置比 HTTPS+Credential Manager 略复杂一些。

选择 HTTPS 并确保 Git Credential Manager 工作正常，是初学者最平滑的体验。

5.  推送成功后，VS Code 底部状态栏可能会显示 "Sync completed" 或类似信息。



## **步骤十：在 GitHub 上验证你的进度**

打开浏览器，访问你的 GitHub 仓库页面。刷新页面，你应该能看到你刚才提交的文件和修改已经显示在仓库里了。README 文件也会被漂亮地渲染出来。

**后续日常操作流程 (持续记录进度)**

每天或每当你完成一段学习后：

1.  在 VS Code 中打开你的仓库文件夹。
2.  修改或创建新的文件来记录你的学习内容和代码。
3.  在 VS Code 的 Source Control 侧边栏，暂存 (Stage) 你的变化。
4.  提交 (Commit) 你的变化，写下清晰的提交信息。
5.  推送 (Push) 你的提交到 GitHub。

**关于安全与有效联动：**

*   **安全 (安全):**
    *   **认证:** 通过 HTTPS + Git Credential Manager 或 SSH Key 方式连接 GitHub，而不是直接输入账号密码，保障了你 GitHub 账号的安全。你的学习记录是私有的（如果你选择了私有仓库），不会被未经授权的人看到。
    *   **版本控制:** Git 本身就提供了强大的版本控制和历史记录功能，每次提交都是一个快照，即使不小心删除了文件或写出了 Bug，也可以轻松回溯到以前的版本，防止丢失数据。
*   **有效 (有效):**
    *   **进度记录:** 每次提交都有信息和时间戳，清晰地记录了你在何时做了什么。
    *   **代码管理:** 你的代码和学习笔记都在一个地方集中管理，结构清晰。
    *   **备份:** 你的所有进度都备份在 GitHub 云端，本地电脑坏了也不怕。
    *   **VS Code 集成:** VS Code 对 Git 的支持非常友好，你可以直接在编辑器界面完成暂存、提交、查看历史等操作，无需频繁切换到命令行，大大提高了效率。
    
    

## **总结**

恭喜你迈出了第一步！虽然一开始步骤看起来有点多，但熟悉后，每天的记录流程就是简单的：**修改 -> 暂存 -> 提交 -> 推送**。

别害怕犯错，Git 和 GitHub 就是用来帮助你管理错误的。多练习几次，你会发现这个流程非常顺畅和实用。祝你编程学习顺利，记录下每一个精彩瞬间！