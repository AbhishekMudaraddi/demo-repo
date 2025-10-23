# 🚀 Learning Git & GitHub Actions

This repository documents my journey of learning **Git** and **GitHub Actions** — covering everything from setting up SSH keys to branching, merging, and undoing commits.

---

## 📘 Table of Contents

1. [Difference between HTTPS and SSH in GitHub](#difference-between-https-and-ssh-in-github)
2. [How to Clone a Repository](#how-to-clone-a-repository)
3. [Git Basics](#git-basics)
   - [git status](#git-status)
   - [git add](#git-add)
   - [git commit](#git-commit)
   - [git push](#git-push)
4. [Setting Up SSH Keys on macOS](#setting-up-ssh-keys-on-macos)
5. [Origin and Main](#origin-and-main)
6. [Initializing a Local Repository](#initializing-a-local-repository)
7. [Git Remote Commands](#git-remote-commands)
8. [Branching in Git](#branching-in-git)
9. [Git Checkout and Diff](#git-checkout-and-diff)
10. [Pulling and Merging](#pulling-and-merging)
11. [Undoing Changes](#undoing-changes)

---

## 🔐 Difference between HTTPS and SSH in GitHub

| Protocol | Description | Pros | Cons |
|-----------|--------------|------|------|
| **HTTPS** | Uses username/password or token for authentication. | Easy setup, works everywhere. | Requires typing credentials often. |
| **SSH** | Uses a secure key pair for authentication. | Faster, more secure, no need to re-enter credentials. | Requires setup of SSH keys. |

✅ **Best Option:** Use **SSH** if you work on GitHub regularly — it's faster and more secure.

---

## 💻 How to Clone a Repository

### Using HTTPS:
```bash
git clone https://github.com/username/repo-name.git
```

### Using SSH:
```bash
git clone git@github.com:username/repo-name.git
```

---

## 📊 Git Basics

### git status

The `git status` command shows the current state of your working directory and staging area:

```bash
git status
```

This command tells you:
- Which branch you're on
- Which files are tracked/untracked
- Which changes are staged for commit
- Which changes are not staged

### git add

The `git add` command adds changes to the staging area:

```bash
# Add a specific file
git add filename.txt

# Add all files
git add .

# Add all files of a specific type
git add *.js

# Add files interactively
git add -p
```

### git commit

The `git commit` command records changes to the repository:

```bash
# Standard commit with message
git commit -m "Your commit message"

# Commit with both title and description
git commit -m "Title" -m "Detailed description"

# Add all changes and commit in one command
git commit -am "Your commit message"

# Amend the previous commit
git commit --amend
```

**Best Practices for Commit Messages:**
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add detailed description after a blank line if needed

### git push

The `git push` command uploads local repository content to a remote repository:

```bash
# Push to default remote (origin) and branch
git push

# Push to specific remote and branch
git push origin main

# Push all branches
git push --all

# Force push (use with caution!)
git push -f
```

---

## 🔑 Setting Up SSH Keys on macOS

1. **Generate an SSH key pair:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Start the SSH agent:**
   ```bash
   eval "$(ssh-agent -s)"
   ```

3. **Add your SSH key to the agent:**
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

4. **Copy the public key to clipboard:**
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```

5. **Add the key to GitHub:**
   - Go to GitHub → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your key and give it a title
   - Click "Add SSH key"

6. **Test your connection:**
   ```bash
   ssh -T git@github.com
   ```

---

## 🔄 Origin and Main

- **origin**: The default name for the remote repository you cloned from
- **main**: The default name for the primary branch (previously called "master")

```bash
# View remote repositories
git remote -v

# Push to origin's main branch
git push origin main

# Pull from origin's main branch
git pull origin main
```

---

## 🏁 Initializing a Local Repository

```bash
# Create a new directory
mkdir my-project
cd my-project

# Initialize a new Git repository
git init

# Add a remote repository
git remote add origin git@github.com:username/repo-name.git

# Create and commit initial files
touch README.md
git add README.md
git commit -m "Initial commit"

# Push to remote repository
git push -u origin main
```

---

## 📡 Git Remote Commands

```bash
# List all remote repositories
git remote -v

# Add a new remote
git remote add origin git@github.com:username/repo-name.git

# Remove a remote
git remote remove origin

# Rename a remote
git remote rename old-name new-name

# Change remote URL
git remote set-url origin git@github.com:username/new-repo-name.git
```

---

## 🌿 Branching in Git

Branches allow you to develop features, fix bugs, or experiment with new ideas in isolation from your main codebase.

### Uses of Branching:
- Feature development
- Bug fixes
- Experimentation
- Release management
- Collaboration with multiple developers

### Branching Commands:

```bash
# List all branches
git branch

# Create a new branch
git branch feature-name

# Create and switch to a new branch
git checkout -b feature-name

# Switch to an existing branch
git checkout branch-name

# Delete a branch
git branch -d branch-name

# Force delete a branch
git branch -D branch-name

# Rename current branch
git branch -m new-name

# List remote branches
git branch -r

# List all branches (local and remote)
git branch -a
```

---

## 🔍 Git Checkout and Diff

### git checkout

The `git checkout` command is used to switch branches or restore working tree files:

```bash
# Switch to another branch
git checkout branch-name

# Create and switch to a new branch
git checkout -b new-branch

# Discard changes in a file
git checkout -- filename.txt

# Checkout a specific commit
git checkout commit-hash
```

### git diff

The `git diff` command shows changes between commits, commit and working tree, etc:

```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Compare two branches
git diff branch1..branch2

# Compare specific files
git diff branch1..branch2 -- filename.txt

# Show changes in a specific commit
git diff commit-hash^ commit-hash

# Show word-level differences
git diff --word-diff
```

---

## ⬇️ Pulling and Merging

### git pull

The `git pull` command fetches from and integrates with another repository or branch:

```bash
# Pull from default remote branch
git pull

# Pull from specific remote and branch
git pull origin main

# Pull with rebase instead of merge
git pull --rebase

# Pull without auto-merge
git pull --no-commit
```

### Merging

Merging combines changes from different branches:

```bash
# Merge a branch into current branch
git merge branch-name

# Merge without fast-forward
git merge --no-ff branch-name

# Abort a merge with conflicts
git merge --abort

# Continue merge after resolving conflicts
git merge --continue
```

---

## ↩️ Undoing Changes

### git reset

The `git reset` command resets current HEAD to the specified state:

```bash
# Unstage changes but keep them in working directory
git reset HEAD filename.txt

# Undo last commit but keep changes
git reset --soft HEAD~1

# Undo last commit and discard changes
git reset --hard HEAD~1

# Reset to a specific commit
git reset --hard commit-hash
```

### git log

The `git log` command shows commit logs:

```bash
# Show commit history
git log

# Show commit history with graph
git log --graph

# Show compact log
git log --oneline

# Show log with patches
git log -p

# Show log for specific file
git log -- filename.txt

# Show log with stats
git log --stat

# Show log with specific format
git log --pretty=format:"%h - %an, %ar : %s"
```

---

## 📚 Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Pro Git Book](https://git-scm.com/book/en/v2)

---

*Last updated: 2023*
