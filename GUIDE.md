# 📘 日常操作指南

> 面向 Git 零基础用户，用最短时间学会用 GitHub 记录学习过程。

---

## 一、先理解三个"区"

用快递类比帮你建立直觉：

| 概念 | 类比 | 含义 |
|------|------|------|
| **工作区** | 你的书桌 | 你正在编辑的文件，改了什么 Git 都知道 |
| **暂存区** | 打包箱 | 告诉 Git "这些改动我要提交" |
| **本地仓库** | 已打包的快递 | 改动正式记录进历史，随时可追溯 |
| **远程仓库** | 快递寄到 GitHub | 别人能看到的最新版本 |

每次上传学三样操作：

```
工作区  ──git add──▶  暂存区  ──git commit──▶  本地仓库  ──git push──▶  GitHub
```

---

## 二、每日标准流程

每天学完新内容后，在终端中按顺序执行以下 4 步。**一条一条敲，等上一条跑完再敲下一条。**

### 第 1 步：进入仓库目录

```bash
cd ~/Desktop/python
```

### 第 2 步：把今天的新文件加入暂存区

```bash
# ✅ 推荐：只加 notebooks 目录（安全，不会误传其他文件）
git add notebooks/

# 或者更精确：只加某一个文件
git add notebooks/03_pandas_basics.ipynb

# ❌ 不推荐：会把你桌面上的 .docx、.xlsx 等无关文件也一并上传
# git add .
```

> ⚠️ `git add .` 会收录当前目录下**所有**未被 `.gitignore` 排除的文件。如果你的仓库根目录下有 Word、Excel 或其他学习资料，它们也会被一起推到 GitHub。

### 第 3 步：提交（记录一条"今天做了什么"）

```bash
git commit -m "简短地描述今天学了什么"
```

`-m` 后面的引号里写一句话注释，例如：

```bash
git commit -m "03: Pandas Series 与 DataFrame 入门"
git commit -m "更新 README 学习进度"
git commit -m "修复金叉策略的日期索引问题"
```

**规范：** 用中文写，简短但具体，让一个月后的自己能看懂。

### 第 4 步：推送到 GitHub

```bash
git push
```

推送成功后打开 `github.com/Echo-Tian1/0-100-quant`，刷新就能看到更新。

---

## 三、完整示例：今天学完 Pandas 后

```
$ cd ~/Desktop/python

$ git status                        # （可选）看看有哪些改动
On branch main
Untracked files:
  notebooks/03_pandas_basics.ipynb

$ git add notebooks/

$ git commit -m "03: Pandas Series 与 DataFrame 入门"

$ git push
Enter passphrase for key: ********   # 输入 SSH 密钥密码
枚举对象中: 5, 完成.
...
To github.com:Echo-Tian1/0-100-quant.git
   fbb1233..a1b2c3d  main -> main    # ← 看到这行说明成功
```

---

## 四、常用命令速查

| 你想做什么 | 命令 |
|-----------|------|
| 看看改了哪些文件 | `git status` |
| 看看具体改了什么内容 | `git diff` |
| 查看提交历史 | `git log --oneline` |
| 撤销还没 add 的改动 | `git checkout -- 文件名` |
| 撤销已经 add 但还没 commit 的 | `git reset HEAD 文件名` |
| 修改上一次的 commit 信息 | `git commit --amend -m "新信息"` |
| 拉取远程最新内容 | `git pull` |
| 强制覆盖远程（危险⚠️） | `git push --force` |

---

## 五、文件放哪里？——仓库目录规范

```
~/Desktop/python/              ← 你的本地仓库根目录
├── notebooks/                  ← 所有 Jupyter Notebook 放这里
│   ├── 02_numpy_operations.ipynb
│   ├── 03_pandas_basics.ipynb
│   └── ...（按编号 + 主题命名）
├── strategies/                 ← 策略代码放这里
│   └── golden_cross_strategy.py
├── data/                       ← 数据文件（CSV 等），太大就不传
├── README.md                   ← 仓库首页展示
├── GUIDE.md                    ← 你正在看的这个文件
└── .gitignore                  ← 不用管它
```

**命名建议：**
- Notebook：`编号_主题.ipynb`，例如 `03_pandas_basics.ipynb`
- 策略文件：`策略名.py`，例如 `rsi_strategy.py`
- 学完一个主题后记得回来更新 `README.md` 里的学习进度表

---

## 六、什么时候 commit？多久 push 一次？

| 频率 | 建议 |
|------|------|
| 每天学完 | commit 一次，push 一次 |
| 一个主题分几天 | 每天 commit，主题结束时 push |
| 代码调试中 | 先不 commit，调通了再 commit |

一个 commit 对应一个完整的小成果，不要堆太多东西在一 commit 里。

---

## 七、三个常见踩坑

### 坑 1：push 时提示"fetch first"

```
! [rejected]  main -> main (fetch first)
```

**原因：** GitHub 上有你本地没有的更新（比如你在网页上改了 README）。

**解决：**

```bash
git pull --rebase origin main
git push
```

如果提示冲突，按 `git checkout --ours 文件名` 选择保留本地版本。

### 坑 2：忘了自己在哪个目录

每次打开终端先敲 `cd ~/Desktop/python`。养成肌肉记忆。

### 坑 3：git add . 加错了文件

```bash
git reset HEAD 那个文件    # 从暂存区移除
```

然后在 `.gitignore` 里加上这个文件，以后再也不会误加。

---

## 八、进阶：直接在 GitHub 网页上编辑

如果你只是改 README.md 里的一两行文字，不需要用终端：

1. 打开 [github.com/Echo-Tian1/0-100-quant](https://github.com/Echo-Tian1/0-100-quant)
2. 点文件 → 点右上角 ✏️（编辑按钮）
3. 改完 → 点绿色 "Commit changes" 按钮
4. 搞定

但注意：网页上改了之后，下次在终端 push 前要先 `git pull`。

---

## 九、一句话总结

> **写完代码 → `git add notebooks/` → `git commit -m "..."` → `git push`**
>
> 就这三件事，每天重复，一个月后你会感谢现在的自己。
