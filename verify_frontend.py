import os
import time
from playwright.sync_api import sync_playwright

def verify_frontend():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Valid-looking JWT payload {"user_id": 1}
        dummy_token = "header.eyJ1c2VyX2lkIjogMX0=.signature"

        # Mock API responses
        page.route("**/api/auth/login", lambda route: route.fulfill(
            status=200,
            body=f'{{"token": "{dummy_token}"}}',
            headers={"Content-Type": "application/json"}
        ))

        page.route("**/api/task/list", lambda route: route.fulfill(
            status=200,
            body='[{"task_id": 1, "task_name": "Test Task 1", "task_type": "backup_task", "task_status": "FINISHED", "create_time": "2023-10-27T10:00:00Z"}, {"task_id": 2, "task_name": "Test Task 2", "task_type": "backup_task", "task_status": "RUNNING", "create_time": "2023-10-27T11:00:00Z"}]',
            headers={"Content-Type": "application/json"}
        ))

        print("Navigating to login...")
        # Go to Login
        try:
            page.goto("http://localhost:5173/login", timeout=10000)
        except Exception as e:
            print(f"Failed to load page: {e}")
            # Check if frontend is running
            import subprocess
            res = subprocess.run(["curl", "-I", "http://localhost:5173"], capture_output=True)
            print(f"Curl check: {res.stdout.decode()} {res.stderr.decode()}")
            raise e

        # Check login page
        print("Checking login page...")
        if not page.is_visible("text=Sign in to your account"):
            page.screenshot(path="verification/error_login.png")
            raise Exception("Login page not visible")

        # Fill form
        print("Filling login form...")
        page.fill("input[name='username']", "admin")
        page.fill("input[name='password']", "password")
        page.click("button[type='submit']")

        # Wait for navigation to Dashboard
        print("Waiting for dashboard...")
        page.wait_for_url("http://localhost:5173/")

        # Check dashboard content
        print("Checking dashboard content...")
        page.wait_for_selector("text=Your Tasks")
        if not page.is_visible("text=Test Task 1"):
             page.screenshot(path="verification/error_dashboard.png")
             raise Exception("Task list not visible")

        # Take screenshot
        os.makedirs("verification", exist_ok=True)
        page.screenshot(path="verification/dashboard.png")

        browser.close()
        print("Verification successful!")

if __name__ == "__main__":
    # Wait for frontend to start
    print("Waiting for frontend server...")
    time.sleep(5)
    verify_frontend()
