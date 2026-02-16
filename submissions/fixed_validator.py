
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

        if not isinstance(record, dict):
            return {"valid": False, "errors": ["Record must be a dictionary"]}

        # Normalize and validate fields
        self._validate_name(record.get("name"))
        self._validate_email(record.get("email"))
        self._validate_age(record.get("age"))
        self._validate_phone(record.get("phone"))
        self._validate_total_spent(record.get("total_spent"))

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
        }

    def _validate_name(self, name):
        """Validate customer name is present and valid."""
        if name is None:
            self.errors.append("Name is required")
            return
            
        if not isinstance(name, str):
            self.errors.append("Name must be a string")
            return
            
        if len(name.strip()) < 1:
            self.errors.append("Name cannot be empty")

    def _validate_email(self, email):
        """Validate email address format using regex."""
        if email is None:
            self.errors.append("Email is required")
            return

        if not isinstance(email, str):
            self.errors.append("Email must be a string")
            return

        # Fixed: Added re.IGNORECASE to handle uppercase letters in emails
        # Fixed: Improved regex for better coverage
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        if not re.match(pattern, email, re.IGNORECASE):
            self.errors.append("Invalid email format")

    def _validate_age(self, age):
        """Validate customer age is within realistic range."""
        # Handle cases where age might be missing (None) or a string
        if age is None:
            # Assuming age is optional or defaults need to be handled. 
            # If required, uncomment below:
            # self.errors.append("Age is required") 
            return

        try:
            age_val = int(age)
        except (ValueError, TypeError):
            self.errors.append("Age must be a valid number")
            return

        if age_val < 0:
            self.errors.append("Age cannot be negative")
        if age_val >= 120:
            self.errors.append("Age is unrealistically high")

    def _validate_phone(self, phone):
        """Validate phone number format."""
        if phone is None:
            return  # Assuming optional

        # Convert to string if it's an integer
        phone_str = str(phone).strip()

        # Check if it contains only digits
        if not phone_str.isdigit():
            self.errors.append("Phone must contain only digits")
        
        if len(phone_str) != 10:
            self.errors.append("Phone must be exactly 10 digits")

    def _validate_total_spent(self, total_spent):
        """Validate total spending amount."""
        if total_spent is None:
            return # Assuming optional or 0 default handled elsewhere

        try:
            amount = float(total_spent)
        except (ValueError, TypeError):
            self.errors.append("Total spent must be a number")
            return

        if amount < 0:
            self.errors.append("Total spent cannot be negative")


def validate_customer(record):
    """Convenience function to validate a customer record."""
    validator = DataValidator()
    return validator.validate(record)
