"""
UserIdentity Class - Handles user identity with strict encapsulation and validation
"""
import re
from datetime import datetime


class UserIdentity:
    """
    Manages user identity with protected email, private phone, and verification status.
    Implements strict state transition rules and validation.
    """
    
    def __init__(self, username, email, phone_number):
        """
        Initialize UserIdentity with username, email, and phone number.
        
        Args:
            username (str): Public username
            email (str): Protected email (validated)
            phone_number (str): Private phone number (validated)
        """
        self.username = username  # Public attribute
        self._email = None  # Protected attribute
        self.__phone_number = None  # Private attribute
        self.__verification_status = "UNVERIFIED"  # Private attribute
        self.__state_history = []  # Private log of state changes
        
        # Initialize with validation
        self.set_email(email)
        self.__set_phone_number(phone_number)
        self.__log_state_change("INITIALIZED", "User identity created")
    
    # Email methods (protected attribute with public accessors)
    def get_email(self):
        """Get the protected email address."""
        return self._email
    
    def set_email(self, new_email):
        """
        Set email with validation.
        
        Args:
            new_email (str): New email to set
            
        Raises:
            ValueError: If email format is invalid
        """
        if self.__validate_email(new_email):
            old_email = self._email
            self._email = new_email
            self.__log_state_change(
                "EMAIL_CHANGED", 
                f"Email changed from {old_email} to {new_email}"
            )
        else:
            raise ValueError(f"Invalid email format: {new_email}")
    
    # Phone number methods (private attribute)
    def get_phone_number(self):
        """Get the private phone number (read-only access)."""
        return self.__phone_number
    
    def __set_phone_number(self, phone):
        """
        Private method to set phone number with validation.
        
        Args:
            phone (str): Phone number to set
            
        Raises:
            ValueError: If phone format is invalid
        """
        if self.__validate_phone(phone):
            self.__phone_number = phone
            self.__log_state_change("PHONE_SET", f"Phone number set to {phone}")
        else:
            raise ValueError(f"Invalid phone format: {phone}")
    
    # Verification status methods
    def get_verification_status(self):
        """Get current verification status."""
        return self.__verification_status
    
    def request_verification(self):
        """
        Request verification. Transitions from UNVERIFIED to PENDING.
        
        Returns:
            bool: True if transition successful, False otherwise
        """
        if self.__verification_status == "UNVERIFIED":
            self.__verification_status = "PENDING"
            self.__log_state_change(
                "VERIFICATION_REQUESTED",
                "Status changed from UNVERIFIED to PENDING"
            )
            return True
        else:
            self.__log_state_change(
                "VERIFICATION_REQUEST_DENIED",
                f"Cannot request verification from {self.__verification_status} state"
            )
            return False
    
    def verify(self):
        """
        Complete verification. Transitions from PENDING to VERIFIED.
        
        Returns:
            bool: True if transition successful, False otherwise
        """
        if self.__verification_status == "PENDING":
            self.__verification_status = "VERIFIED"
            self.__log_state_change(
                "VERIFIED",
                "Status changed from PENDING to VERIFIED"
            )
            return True
        else:
            self.__log_state_change(
                "VERIFICATION_DENIED",
                f"Cannot verify from {self.__verification_status} state"
            )
            return False
    
    # Private validation methods
    def __validate_email(self, email):
        """
        Private method to validate email format.
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __validate_phone(self, phone):
        """
        Private method to validate phone number format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Phone pattern: +XXX-XXX-XXXX or similar formats
        # Accepts formats like: +1-234-567-8900, +998-90-123-4567, etc.
        pattern = r'^\+\d{1,3}-\d{2,3}-\d{3,4}-\d{4,5}$'
        return bool(re.match(pattern, phone))
    
    def __log_state_change(self, action, description):
        """
        Private method to log state changes.
        
        Args:
            action (str): Action type
            description (str): Description of the change
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description,
            'status': self.__verification_status
        }
        self.__state_history.append(log_entry)
    
    def get_state_history(self):
        """
        Get a copy of the state history (for debugging/auditing).
        
        Returns:
            list: Copy of state history
        """
        return self.__state_history.copy()
    
    def __str__(self):
        """String representation of UserIdentity."""
        return (f"UserIdentity(username={self.username}, "
                f"email={self._email}, "
                f"phone={self.__phone_number}, "
                f"status={self.__verification_status})")
    
    def __repr__(self):
        """Detailed representation of UserIdentity."""
        return self.__str__()
