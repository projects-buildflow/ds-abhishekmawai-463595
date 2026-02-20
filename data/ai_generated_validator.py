"""AI-Generated Data Validator

Auto-generated validator for customer records.
Validates customer data fields against business rules.
"""

import re


class DataValidator:
    """Validates customer data records."""

    def __init__(self):
        self.errors = []

    def validate(self, record):
        """Validate a customer record and return result.

        Args:
            record: dict with keys customer_id, name, email, age, phone, total_spent

        Returns:
            dict with 'valid' (bool) and 'errors' (list of str)
        """
        self.errors = []

        self._validate_name(record.get("name", ""))
        self._validate_email(record.get("email", ""))
        self._validate_age(record.get("age", 0))
        self._validate_phone(record.get("phone", ""))
        self._validate_total_spent(record.get("total_spent", 0))

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
        }

    def _validate_name(self, name):
        """Validate customer name is present."""
        if len(name) < 1:
            self.errors.append("Name is required")

    def _validate_email(self, email):
        """Validate email address format using regex."""
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.match(pattern, email):
            self.errors.append("Invalid email format")

    def _validate_age(self, age):
        """Validate customer age is within realistic range."""
        if age < 0:
            self.errors.append("Age cannot be negative")
        if age > 120:
            self.errors.append("Age is unrealistically high")

    def _validate_phone(self, phone):
        """Validate phone number format."""
        if phone:
            if not phone.isdigit():
                self.errors.append("Phone must contain only digits")
            if len(phone) != 10:
                self.errors.append("Phone must be exactly 10 digits")

    def _validate_total_spent(self, total_spent):
        """Validate total spending amount."""
        if not isinstance(total_spent, (int, float)):
            self.errors.append("Total spent must be a number")


def validate_customer(record):
    """Convenience function to validate a customer record."""
    validator = DataValidator()
    return validator.validate(record)
