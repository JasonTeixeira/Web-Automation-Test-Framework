"""
Test data generation utilities using Faker.
"""
from dataclasses import dataclass
from typing import Optional

from faker import Faker

from config import settings


@dataclass
class CheckoutData:
    """Checkout form data."""
    first_name: str
    last_name: str
    postal_code: str


@dataclass
class UserCredentials:
    """User login credentials."""
    username: str
    password: str
    user_type: str


class TestDataGenerator:
    """Generate realistic test data using Faker."""
    
    def __init__(self, locale: Optional[str] = None):
        """
        Initialize test data generator.
        
        Args:
            locale: Locale for data generation (defaults to settings.locale)
        """
        self.faker = Faker(locale or settings.locale)
        Faker.seed(42)  # For reproducible data in tests
    
    def generate_checkout_data(self) -> CheckoutData:
        """
        Generate random checkout form data.
        
        Returns:
            CheckoutData instance with randomized values
        """
        return CheckoutData(
            first_name=self.faker.first_name(),
            last_name=self.faker.last_name(),
            postal_code=self.faker.postcode()
        )
    
    def get_user_credentials(self, user_type: str = "standard") -> UserCredentials:
        """
        Get credentials for specified user type.
        
        Args:
            user_type: Type of user (standard, locked, problem, performance, error, visual)
            
        Returns:
            UserCredentials instance
        """
        username, password = settings.get_user_credentials(user_type)
        return UserCredentials(
            username=username,
            password=password,
            user_type=user_type
        )
    
    def get_all_user_types(self) -> list[str]:
        """
        Get list of all available user types.
        
        Returns:
            List of user type strings
        """
        return ["standard", "locked", "problem", "performance", "error", "visual"]
    
    def generate_invalid_credentials(self) -> list[UserCredentials]:
        """
        Generate various invalid credential combinations for negative testing.
        
        Returns:
            List of invalid UserCredentials
        """
        return [
            UserCredentials(username="", password="", user_type="empty"),
            UserCredentials(username="invalid_user", password="wrong_pass", user_type="invalid"),
            UserCredentials(username="standard_user", password="wrong_password", user_type="wrong_password"),
            UserCredentials(username="", password="secret_sauce", user_type="empty_username"),
            UserCredentials(username="standard_user", password="", user_type="empty_password"),
            UserCredentials(username=self.faker.email(), password=self.faker.password(), user_type="random"),
        ]
    
    def generate_malicious_inputs(self) -> list[str]:
        """
        Generate malicious input strings for security testing.
        
        Returns:
            List of malicious input strings
        """
        return [
            "<script>alert('XSS')</script>",
            "' OR '1'='1",
            "'; DROP TABLE users--",
            "../../../etc/passwd",
            "${7*7}",
            "{{7*7}}",
            "AAAA" * 1000,  # Long string
            "\x00\x00",  # Null bytes
        ]
    
    def generate_postal_codes(self, count: int = 10) -> list[str]:
        """
        Generate multiple postal codes.
        
        Args:
            count: Number of postal codes to generate
            
        Returns:
            List of postal codes
        """
        return [self.faker.postcode() for _ in range(count)]
    
    def generate_names(self, count: int = 10) -> list[tuple[str, str]]:
        """
        Generate multiple first name and last name pairs.
        
        Args:
            count: Number of name pairs to generate
            
        Returns:
            List of (first_name, last_name) tuples
        """
        return [(self.faker.first_name(), self.faker.last_name()) for _ in range(count)]


# Global instance
test_data = TestDataGenerator()
