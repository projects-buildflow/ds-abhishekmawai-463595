import pandera as pa
from pandera import Column, Check

customer_schema = pa.DataFrameSchema(
    {
        "full_name": Column(str, nullable=True),
        "email_address": Column(str, Check.str_contains("@"), nullable=True),
        "age": Column(int, Check.in_range(0, 120), nullable=True),
        "gender": Column(str, Check.isin(["M", "F", "Other"]), nullable=True),
        "phone_number": Column(str, nullable=True),
        "location": Column(str),
        "country": Column(str),
        "date_joined": Column(str, Check.str_matches(r"^\d{4}-\d{2}-\d{2}$")),
        "lead_source": Column(str),
        "utm_campaign": Column(str, nullable=True),
        "utm_medium": Column(str, nullable=True),
        "notes": Column(str, nullable=True),
        "is_subscribed": Column(str),
    }
)


def validate_customers(df):
    """Validate customer DataFrame against schema."""
    return customer_schema.validate(df)

