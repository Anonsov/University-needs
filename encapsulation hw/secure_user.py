"""
SecureUser Class - Composition of UserIdentity and AccountAccess with enhanced security
"""
from datetime import datetime
from user_identity import UserIdentity
from account_access import AccountAccess


class SecureUser:
    """
    Secure user system combining identity management and access control.
    Uses composition pattern with strict encapsulation and comprehensive auditing.
    """
    
    def __init__(self, username, email, phone_number):
        """
        Initialize SecureUser with identity and access management.
        
        Args:
            username (str): Username
            email (str): Email address
            phone_number (str): Phone number
        """
        # Protected UserIdentity instance
        self._identity = UserIdentity(username, email, phone_number)
        
        # Private AccountAccess instance
        self.__access = AccountAccess()
        
        # Private audit log
        self.__audit_log = []
        
        # Log creation
        self.__log_action(
            "USER_CREATED",
            f"SecureUser created for {username}",
            success=True
        )
    
    # Permission management methods
    def grant_permission(self, permission):
        """
        Grant a permission to the user with verification enforcement.
        
        Args:
            permission (str): Permission to grant
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Check if user is verified for restricted permissions
        is_verified = self._identity.get_verification_status() == "VERIFIED"
        
        # Attempt to add permission
        success, message = self.__access.add_permission(permission, is_verified)
        
        # Log the action
        self.__log_action(
            "GRANT_PERMISSION",
            f"Attempted to grant '{permission}': {message}",
            success=success,
            details={'permission': permission, 'verified': is_verified}
        )
        
        return (success, message)
    
    def revoke_permission(self, permission):
        """
        Revoke a permission from the user.
        
        Args:
            permission (str): Permission to revoke
            
        Returns:
            tuple: (success: bool, message: str)
        """
        success, message = self.__access.remove_permission(permission)
        
        # Log the action
        self.__log_action(
            "REVOKE_PERMISSION",
            f"Attempted to revoke '{permission}': {message}",
            success=success,
            details={'permission': permission}
        )
        
        return (success, message)
    
    def has_permission(self, permission):
        """
        Check if user has a specific permission.
        
        Args:
            permission (str): Permission to check
            
        Returns:
            bool: True if permission exists
        """
        return self.__access.has_permission(permission)
    
    def get_permissions(self):
        """
        Get a copy of user's permissions.
        
        Returns:
            list: Copy of permissions list
        """
        return self.__access.get_permissions()
    
    # Identity management methods
    def request_verification(self):
        """
        Request identity verification.
        
        Returns:
            bool: True if successful
        """
        success = self._identity.request_verification()
        self.__log_action(
            "REQUEST_VERIFICATION",
            f"Verification request: {'successful' if success else 'failed'}",
            success=success
        )
        return success
    
    def verify_identity(self):
        """
        Complete identity verification.
        
        Returns:
            bool: True if successful
        """
        success = self._identity.verify()
        self.__log_action(
            "VERIFY_IDENTITY",
            f"Identity verification: {'successful' if success else 'failed'}",
            success=success
        )
        return success
    
    def identity_status(self):
        """
        Get formatted identity status information.
        
        Returns:
            dict: Identity status details
        """
        return {
            'username': self._identity.username,
            'email': self._identity.get_email(),
            'phone': self._identity.get_phone_number(),
            'verification_status': self._identity.get_verification_status(),
            'permissions': self.__access.get_permissions()
        }
    
    def update_email(self, new_email):
        """
        Update user's email address.
        
        Args:
            new_email (str): New email address
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            self._identity.set_email(new_email)
            self.__log_action(
                "UPDATE_EMAIL",
                f"Email updated to {new_email}",
                success=True
            )
            return (True, "Email updated successfully")
        except ValueError as e:
            self.__log_action(
                "UPDATE_EMAIL",
                f"Failed to update email: {str(e)}",
                success=False
            )
            return (False, str(e))
    
    # Audit log methods
    def get_audit_log(self):
        """
        Get a COPY of the audit log to prevent external modification.
        
        Returns:
            list: Copy of audit log
        """
        return self.__audit_log.copy()
    
    def __log_action(self, action, description, success=True, details=None):
        """
        Private method to log all actions for auditing.
        
        Args:
            action (str): Action type
            description (str): Description of the action
            success (bool): Whether action was successful
            details (dict): Additional details
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description,
            'success': success,
            'user': self._identity.username,
            'verification_status': self._identity.get_verification_status()
        }
        
        if details:
            log_entry['details'] = details
        
        self.__audit_log.append(log_entry)
    
    def get_full_report(self):
        """
        Generate a comprehensive security report.
        
        Returns:
            dict: Complete user security report
        """
        return {
            'identity': self.identity_status(),
            'audit_log_entries': len(self.__audit_log),
            'last_action': self.__audit_log[-1] if self.__audit_log else None
        }
    
    def __str__(self):
        """String representation of SecureUser."""
        status = self.identity_status()
        return (f"SecureUser(username={status['username']}, "
                f"status={status['verification_status']}, "
                f"permissions={len(status['permissions'])})")
    
    def __repr__(self):
        """Detailed representation of SecureUser."""
        return self.__str__()
