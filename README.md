# 🔵 CNAMER

**Simple & Beautiful CNAME Record Checker**

A lightweight command-line tool written in Python that checks whether domains have CNAME records and separates them into two clean lists.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![DNS](https://img.shields.io/badge/DNS-CNAME-blue)

---

## ✨ Features

- Check a single domain or a list of domains
- Clean separation of domains **with CNAME** and **without CNAME**
- Colored terminal output + optional file export
- Beautiful blue ASCII banner
- Fast and lightweight (uses `dnspython`)
- Simple and intuitive CLI

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cnamer.git
cd cnamer

# Install dependency
pip install -r requirements.txt
```

Or just:

```bash
pip install dnspython
```

---

## 🚀 Usage

### Check a single domain
```bash
python cnamer.py -u example.com
python cnamer.py -u www.github.com
```

### Check a list of domains
```bash
python cnamer.py -list domains.txt
python cnamer.py -list subdomains.txt
```

### Save results to a file
```bash
python cnamer.py -u example.com -o result.txt
python cnamer.py -list domains.txt -o cname_results.txt
```

### Hide the banner
```bash
python cnamer.py -u example.com -q
```

---

## 📋 Example Output

```
   ██████╗███╗   ██╗ █████╗ ███╗   ███╗███████╗██████╗ 
  ██╔════╝████╗  ██║██╔══██╗████╗ ████║██╔════╝██╔══██╗
  ██║     ██╔██╗ ██║███████║██╔████╔██║█████╗  ██████╔╝
  ██║     ██║╚██╗██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗
  ╚██████╗██║ ╚████║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
   ╚═════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝

          ★ CNAME Record Checker ★

Scanning 3 domain(s)...

======================
  CNAME:
======================
www.github.com (CNAME: github.com)

======================
  no CNAME:
======================
example.com
google.com

✓ Found 1 with CNAME | 2 without
```

---

## 📄 Input File Format

One domain per line:

```text
example.com
www.github.com
blog.example.org
# comments are ignored
sub.domain.net
```

---

## 🛠️ Options

| Option | Description |
|--------|-------------|
| `-u`, `--url` | Check a single domain |
| `-list`, `--list` | Path to a file containing domains |
| `-o`, `--output` | Save results to a file |
| `-q`, `--quiet` | Suppress the banner |
| `-h`, `--help` | Show help message |

---

## 📌 Requirements

- Python 3.7+
- `dnspython`

---

## 📜 License

MIT License — feel free to use and modify.

---

Made with ❤️ for recon & DNS analysis
