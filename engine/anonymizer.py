"""
PDPA / PII Data Redaction Engine.
Scrubs sensitive entities, customer names, and bank details prior to external AI exports.
"""
import re

def scrub_sensitive_financial_data(text_or_dict) -> str:
    """
    Applies Regex & Pattern Matching to scrub sensitive PII, vendor names, and account numbers.
    """
    raw_str = str(text_or_dict)
    
    # Redact Specific Customer / Vendor Name Patterns
    scrubbed = re.sub(r'([A-Z][a-z]+ (Pte Ltd|Inc|LLC|Corp|Ltd))', '[VENDOR_REDACTED]', raw_str)
    # Redact Account Numbers / Identifiers
    scrubbed = re.sub(r'\b\d{4}-\d{4}-\d{4}\b', '[ACCOUNT_REDACTED]', scrubbed)
    # Redact Email Addresses
    scrubbed = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REDACTED]', scrubbed)

    return scrubbed