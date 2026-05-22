# 🤖 Tugas Tutorial SE - Automation Test
**Target:** https://the-internet.herokuapp.com/login

## Test Cases
1. ✅ Login dengan username & password BENAR → redirect ke /secure
2. ❌ Login dengan username benar & password SALAH → muncul pesan error

---

## 📦 Setup & Instalasi

### 1. Clone / Download project ini
```bash
git clone <url-repo-kamu>
cd tugas-automation-se
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

> Pastikan Google Chrome sudah terinstall di komputer kamu.  
> `webdriver-manager` akan otomatis download ChromeDriver yang sesuai.

---

## ▶️ Cara Menjalankan Test

### Run semua test:
```bash
pytest test_login.py -v
```

### Run dengan output lebih detail (termasuk print):
```bash
pytest test_login.py -v -s
```

### Contoh output yang diharapkan:
```
test_login.py::test_login_correct_credentials PASSED
test_login.py::test_login_wrong_password PASSED

2 passed in X.XXs
```

---

## 📸 Screenshot
Screenshot otomatis tersimpan di folder `screenshots/`:
- `test_1_login_success.png` → halaman setelah login berhasil
- `test_2_login_wrong_password.png` → halaman setelah login gagal

---

## 🗂️ Struktur Project
```
tugas-automation-se/
├── test_login.py        ← script utama (berisi Gherkin syntax)
├── requirements.txt     ← daftar library
├── screenshots/         ← screenshot hasil test (auto-generated)
└── README.md
```

---

## 🧪 Gherkin Syntax (ada di dalam test_login.py)

```gherkin
Feature: User Authentication - The Internet Herokuapp

  Scenario: Login dengan username dan password yang benar
    Given user berada di halaman login
    And user memiliki akun yang valid
    When user memasukkan username "tomsmith" dan password "SuperSecretPassword!"
    Then user diarahkan ke halaman secure
    And pesan sukses ditampilkan

  Scenario: Login dengan username benar dan password yang salah
    Given user berada di halaman login
    And user memiliki akun yang valid
    When user memasukkan username "tomsmith" dan password yang salah "wrongpassword"
    Then user tetap di halaman login
    And pesan error ditampilkan
```

---

## 📤 Push ke GitHub

```bash
git init
git add .
git commit -m "Add automation test for login scenarios"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git push -u origin main
```
