import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ============================================================
# URL Target
# ============================================================
LOGIN_URL = "https://the-internet.herokuapp.com/login"

# ============================================================
# GHERKIN SYNTAX
#
# Feature: User Authentication - The Internet Herokuapp
#
#   Scenario: Login dengan username dan password yang benar
#     Given user berada di halaman login
#     And user memiliki akun yang valid
#     When user memasukkan username "tomsmith" dan password "SuperSecretPassword!"
#     Then user diarahkan ke halaman secure
#     And pesan sukses ditampilkan
#
#   Scenario: Login dengan username benar dan password yang salah
#     Given user berada di halaman login
#     And user memiliki akun yang valid
#     When user memasukkan username "tomsmith" dan password yang salah "wrongpassword"
#     Then user tetap di halaman login
#     And pesan error ditampilkan
# ============================================================


@pytest.fixture
def driver():
    """Setup dan teardown WebDriver Chrome."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Uncomment baris di bawah kalau mau run tanpa buka browser (headless)
    # options.add_argument("--headless")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()


def take_screenshot(driver, filename):
    """Helper function untuk ambil screenshot dan simpan ke folder screenshots/."""
    os.makedirs("screenshots", exist_ok=True)
    filepath = os.path.join("screenshots", filename)
    driver.save_screenshot(filepath)
    print(f"\n📸 Screenshot disimpan: {filepath}")


# ============================================================
# TEST CASE 1: Login dengan Username dan Password BENAR
# ============================================================
def test_login_correct_credentials(driver):
    """
    Scenario: Login dengan username dan password yang benar
      Given user berada di halaman login
      And user memiliki akun yang valid
      When user memasukkan username "tomsmith" dan password "SuperSecretPassword!"
      Then user diarahkan ke halaman secure
      And pesan sukses ditampilkan
    """
    # Given - user berada di halaman login
    driver.get(LOGIN_URL)
    assert "login" in driver.current_url, "Gagal membuka halaman login"

    # When - user memasukkan credentials yang benar
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.clear()
    username_field.send_keys("tomsmith")

    password_field.clear()
    password_field.send_keys("SuperSecretPassword!")

    login_button.click()

    # Then - user diarahkan ke halaman secure dan pesan sukses muncul
    WebDriverWait(driver, 10).until(
        EC.url_contains("/secure")
    )

    success_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )

    assert "/secure" in driver.current_url, "User tidak diarahkan ke halaman secure"
    assert success_message.is_displayed(), "Pesan sukses tidak ditampilkan"
    assert "You logged into a secure area!" in success_message.text, \
        f"Teks pesan sukses tidak sesuai: {success_message.text}"

    print("\n✅ TEST PASSED: Login dengan credentials benar berhasil!")
    print(f"   URL sekarang: {driver.current_url}")
    print(f"   Pesan: {success_message.text.strip()}")

    take_screenshot(driver, "test_1_login_success.png")


# ============================================================
# TEST CASE 2: Login dengan Username Benar dan Password SALAH
# ============================================================
def test_login_wrong_password(driver):
    """
    Scenario: Login dengan username benar dan password yang salah
      Given user berada di halaman login
      And user memiliki akun yang valid
      When user memasukkan username "tomsmith" dan password yang salah "wrongpassword"
      Then user tetap di halaman login
      And pesan error ditampilkan
    """
    # Given - user berada di halaman login
    driver.get(LOGIN_URL)
    assert "login" in driver.current_url, "Gagal membuka halaman login"

    # When - user memasukkan password yang salah
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.clear()
    username_field.send_keys("tomsmith")

    password_field.clear()
    password_field.send_keys("wrongpassword")

    login_button.click()

    # Then - user tetap di halaman login dan pesan error muncul
    time.sleep(1)  # tunggu sebentar agar halaman merespon

    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.error"))
    )

    assert "/secure" not in driver.current_url, "User seharusnya TIDAK diarahkan ke halaman secure"
    assert error_message.is_displayed(), "Pesan error tidak ditampilkan"
    assert "Your password is invalid!" in error_message.text, \
        f"Teks pesan error tidak sesuai: {error_message.text}"

    print("\n✅ TEST PASSED: Login dengan password salah berhasil dideteksi!")
    print(f"   URL sekarang: {driver.current_url}")
    print(f"   Pesan error: {error_message.text.strip()}")

    take_screenshot(driver, "test_2_login_wrong_password.png")
