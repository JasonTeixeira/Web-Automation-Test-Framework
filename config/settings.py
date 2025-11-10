"""
Configuration settings for the test framework using Pydantic.
Loads environment variables and provides type-safe configuration access.
"""
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application Under Test
    base_url: str = Field(default="https://www.saucedemo.com", description="Base URL of the application")
    api_base_url: str = Field(default="https://www.saucedemo.com/api", description="API base URL")
    
    # Test Users
    standard_user: str = Field(default="standard_user", description="Standard test user")
    locked_user: str = Field(default="locked_out_user", description="Locked out user")
    problem_user: str = Field(default="problem_user", description="Problem user with buggy behavior")
    performance_user: str = Field(default="performance_glitch_user", description="Performance glitch user")
    error_user: str = Field(default="error_user", description="Error user")
    visual_user: str = Field(default="visual_user", description="Visual regression user")
    default_password: str = Field(default="secret_sauce", description="Default password for all users")
    
    # Browser Configuration
    browser: Literal["chromium", "firefox", "webkit"] = Field(default="chromium", description="Browser to use")
    headless: bool = Field(default=False, description="Run browser in headless mode")
    slow_mo: int = Field(default=0, description="Slow down operations by specified milliseconds")
    timeout: int = Field(default=30000, description="Default timeout in milliseconds")
    viewport_width: int = Field(default=1920, description="Browser viewport width")
    viewport_height: int = Field(default=1080, description="Browser viewport height")
    
    # Test Execution
    parallel_workers: int = Field(default=4, description="Number of parallel workers")
    retries: int = Field(default=1, description="Number of test retries on failure")
    screenshot_on_failure: bool = Field(default=True, description="Take screenshot on test failure")
    video_on_failure: bool = Field(default=True, description="Record video on test failure")
    trace_on_failure: bool = Field(default=True, description="Record trace on test failure")
    
    # Reporting
    allure_results_dir: str = Field(default="reports/allure-results", description="Allure results directory")
    html_report_dir: str = Field(default="reports", description="HTML report directory")
    screenshot_dir: str = Field(default="screenshots", description="Screenshots directory")
    log_dir: str = Field(default="logs", description="Logs directory")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO", description="Logging level"
    )
    
    # CI/CD Flags
    ci: bool = Field(default=False, description="Running in CI environment")
    run_visual_tests: bool = Field(default=True, description="Run visual regression tests")
    run_accessibility_tests: bool = Field(default=True, description="Run accessibility tests")
    run_performance_tests: bool = Field(default=False, description="Run performance tests")
    
    # Test Data
    use_faker: bool = Field(default=True, description="Use Faker for test data generation")
    locale: str = Field(default="en_US", description="Locale for test data generation")
    
    # Notifications (Optional)
    slack_webhook_url: str = Field(default="", description="Slack webhook URL for notifications")
    slack_notify_on_failure: bool = Field(default=False, description="Send Slack notification on failure")
    smtp_server: str = Field(default="", description="SMTP server for email notifications")
    smtp_port: int = Field(default=587, description="SMTP port")
    smtp_user: str = Field(default="", description="SMTP username")
    smtp_password: str = Field(default="", description="SMTP password")
    notify_email: str = Field(default="", description="Email address for notifications")
    
    @property
    def project_root(self) -> Path:
        """Return the project root directory."""
        return Path(__file__).parent.parent
    
    @property
    def reports_path(self) -> Path:
        """Return the reports directory path."""
        return self.project_root / self.html_report_dir
    
    @property
    def screenshots_path(self) -> Path:
        """Return the screenshots directory path."""
        return self.project_root / self.screenshot_dir
    
    @property
    def logs_path(self) -> Path:
        """Return the logs directory path."""
        return self.project_root / self.log_dir
    
    def get_user_credentials(self, user_type: str = "standard") -> tuple[str, str]:
        """
        Get username and password for specified user type.
        
        Args:
            user_type: Type of user (standard, locked, problem, performance, error, visual)
            
        Returns:
            Tuple of (username, password)
        """
        user_map = {
            "standard": self.standard_user,
            "locked": self.locked_user,
            "problem": self.problem_user,
            "performance": self.performance_user,
            "error": self.error_user,
            "visual": self.visual_user,
        }
        username = user_map.get(user_type, self.standard_user)
        return username, self.default_password


# Global settings instance
settings = Settings()
