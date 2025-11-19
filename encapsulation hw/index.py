"""
Complete Advanced Encapsulation System - All-in-One File
This file contains all classes for the Fintech Identity System
"""
import re
from datetime import datetime


# ============================================================================
# CLASS 1: UserIdentity
# ============================================================================
class UserIdentity:
    """
    Manages user identity with protected email, private phone, and verification status.
    Implements strict state transition rules and validation.
    """
    
    def __init__(self, username, email, phone_number):
        self.username = username  # Public attribute
        self._email = None  # Protected attribute
        self.__phone_number = None  # Private attribute
        self.__verification_status = "UNVERIFIED"  # Private attribute
        self.__state_history = []  # Private log of state changes
        
        # Initialize with validation
        self.set_email(email)
        self.__set_phone_number(phone_number)
        self.__log_state_change("INITIALIZED", "User identity created")
    
    # Email methods
    def get_email(self):
        return self._email
    
    def set_email(self, new_email):
        if self.__validate_email(new_email):
            old_email = self._email
            self._email = new_email
            self.__log_state_change("EMAIL_CHANGED", f"Email changed from {old_email} to {new_email}")
        else:
            raise ValueError(f"Invalid email format: {new_email}")
    
    # Phone number methods
    def get_phone_number(self):
        return self.__phone_number
    
    def __set_phone_number(self, phone):
        if self.__validate_phone(phone):
            self.__phone_number = phone
            self.__log_state_change("PHONE_SET", f"Phone number set to {phone}")
        else:
            raise ValueError(f"Invalid phone format: {phone}")
    
    # Verification status methods
    def get_verification_status(self):
        return self.__verification_status
    
    def request_verification(self):
        if self.__verification_status == "UNVERIFIED":
            self.__verification_status = "PENDING"
            self.__log_state_change("VERIFICATION_REQUESTED", "Status changed from UNVERIFIED to PENDING")
            return True
        else:
            self.__log_state_change("VERIFICATION_REQUEST_DENIED", 
                                   f"Cannot request verification from {self.__verification_status} state")
            return False
    
    def verify(self):
        if self.__verification_status == "PENDING":
            self.__verification_status = "VERIFIED"
            self.__log_state_change("VERIFIED", "Status changed from PENDING to VERIFIED")
            return True
        else:
            self.__log_state_change("VERIFICATION_DENIED", 
                                   f"Cannot verify from {self.__verification_status} state")
            return False
    
    # Private validation methods
    def __validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __validate_phone(self, phone):
        pattern = r'^\+\d{1,3}-\d{2,3}-\d{3,4}-\d{4,5}$'
        return bool(re.match(pattern, phone))
    
    def __log_state_change(self, action, description):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description,
            'status': self.__verification_status
        }
        self.__state_history.append(log_entry)
    
    def get_state_history(self):
        return self.__state_history.copy()
    
    def __str__(self):
        return (f"UserIdentity(username={self.username}, email={self._email}, "
                f"phone={self.__phone_number}, status={self.__verification_status})")


# ============================================================================
# CLASS 2: AccountAccess
# ============================================================================
class AccountAccess:
    """
    Manages user permissions with all private attributes.
    Returns copies of internal data to prevent external modification.
    """
    
    RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}
    ALLOWED_PERMISSIONS = {"VIEW_BALANCE", "VIEW_TRANSACTIONS", "TRANSFER", 
                          "WITHDRAW", "DEPOSIT", "UPDATE_PROFILE"}
    
    def __init__(self):
        self.__permissions = []
        self.__permission_history = []
        self.__log_permission_change("INITIALIZED", "Account access created")
    
    def get_permissions(self):
        """Return a COPY of permissions to prevent external modification"""
        return self.__permissions.copy()
    
    def add_permission(self, permission, is_verified=False):
        if permission not in self.ALLOWED_PERMISSIONS:
            message = f"Invalid permission: {permission}"
            self.__log_permission_change("ADD_FAILED", message)
            return (False, message)
        
        if permission in self.__permissions:
            message = f"Permission already granted: {permission}"
            self.__log_permission_change("ADD_DUPLICATE", message)
            return (False, message)
        
        if permission in self.RESTRICTED_PERMISSIONS and not is_verified:
            message = f"Cannot grant '{permission}' - user must be VERIFIED"
            self.__log_permission_change("ADD_DENIED", message)
            return (False, message)
        
        self.__permissions.append(permission)
        message = f"Permission granted: {permission}"
        self.__log_permission_change("ADD_SUCCESS", message)
        return (True, message)
    
    def remove_permission(self, permission):
        if permission in self.__permissions:
            self.__permissions.remove(permission)
            message = f"Permission revoked: {permission}"
            self.__log_permission_change("REMOVE_SUCCESS", message)
            return (True, message)
        else:
            message = f"Permission not found: {permission}"
            self.__log_permission_change("REMOVE_FAILED", message)
            return (False, message)
    
    def has_permission(self, permission):
        return permission in self.__permissions
    
    def __log_permission_change(self, action, description):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description,
            'current_permissions': self.__permissions.copy()
        }
        self.__permission_history.append(log_entry)
    
    def get_permission_history(self):
        return self.__permission_history.copy()
    
    def __str__(self):
        return f"AccountAccess(permissions={self.__permissions})"


# ============================================================================
# CLASS 3: SecureUser (Composition)
# ============================================================================
class SecureUser:
    """
    Secure user system combining identity management and access control.
    Uses composition pattern with strict encapsulation and comprehensive auditing.
    """
    
    def __init__(self, username, email, phone_number):
        self._identity = UserIdentity(username, email, phone_number)  # Protected
        self.__access = AccountAccess()  # Private
        self.__audit_log = []  # Private
        
        self.__log_action("USER_CREATED", f"SecureUser created for {username}", success=True)
    
    # Permission management
    def grant_permission(self, permission):
        is_verified = self._identity.get_verification_status() == "VERIFIED"
        success, message = self.__access.add_permission(permission, is_verified)
        
        self.__log_action("GRANT_PERMISSION", f"Attempted to grant '{permission}': {message}",
                         success=success, details={'permission': permission, 'verified': is_verified})
        
        return (success, message)
    
    def revoke_permission(self, permission):
        success, message = self.__access.remove_permission(permission)
        self.__log_action("REVOKE_PERMISSION", f"Attempted to revoke '{permission}': {message}",
                         success=success, details={'permission': permission})
        return (success, message)
    
    def has_permission(self, permission):
        return self.__access.has_permission(permission)
    
    def get_permissions(self):
        return self.__access.get_permissions()
    
    # Identity management
    def request_verification(self):
        success = self._identity.request_verification()
        self.__log_action("REQUEST_VERIFICATION", 
                         f"Verification request: {'successful' if success else 'failed'}", success=success)
        return success
    
    def verify_identity(self):
        success = self._identity.verify()
        self.__log_action("VERIFY_IDENTITY", 
                         f"Identity verification: {'successful' if success else 'failed'}", success=success)
        return success
    
    def identity_status(self):
        return {
            'username': self._identity.username,
            'email': self._identity.get_email(),
            'phone': self._identity.get_phone_number(),
            'verification_status': self._identity.get_verification_status(),
            'permissions': self.__access.get_permissions()
        }
    
    def update_email(self, new_email):
        try:
            self._identity.set_email(new_email)
            self.__log_action("UPDATE_EMAIL", f"Email updated to {new_email}", success=True)
            return (True, "Email updated successfully")
        except ValueError as e:
            self.__log_action("UPDATE_EMAIL", f"Failed to update email: {str(e)}", success=False)
            return (False, str(e))
    
    # Audit log
    def get_audit_log(self):
        """Return a COPY of audit log to prevent external modification"""
        return self.__audit_log.copy()
    
    def __log_action(self, action, description, success=True, details=None):
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
    
    def __str__(self):
        status = self.identity_status()
        return (f"SecureUser(username={status['username']}, "
                f"status={status['verification_status']}, "
                f"permissions={len(status['permissions'])})")


# ============================================================================
# DEMONSTRATION
# ============================================================================
def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_status(user):
    status = user.identity_status()
    print(f"👤 User: {status['username']}")
    print(f"📧 Email: {status['email']}")
    print(f"📱 Phone: {status['phone']}")
    print(f"✅ Status: {status['verification_status']}")
    print(f"🔑 Permissions: {', '.join(status['permissions']) if status['permissions'] else 'None'}")


def main():
    print_section("🏦 FINTECH IDENTITY SYSTEM - DEMONSTRATION")
    
    # Create user
    print_section("Creating SecureUser")
    user = SecureUser("john_doe", "john.doe@example.com", "+1-555-123-4567")
    print_status(user)
    
    # Test illegal access
    print_section("Testing Encapsulation")
    try:
        phone = user._identity.__phone_number
        print(f"❌ BREACH: Accessed private phone: {phone}")
    except AttributeError:
        print("✅ Private attribute protected")
    
    # Test verification workflow
    print_section("Testing Verification Workflow")
    print("Attempting to grant TRANSFER (restricted)...")
    success, msg = user.grant_permission("TRANSFER")
    print(f"   Result: {msg}")
    
    print("\nRequesting verification...")
    user.request_verification()
    print(f"   Status: {user._identity.get_verification_status()}")
    
    print("\nCompleting verification...")
    user.verify_identity()
    print(f"   Status: {user._identity.get_verification_status()}")
    
    print("\nRetrying TRANSFER permission...")
    success, msg = user.grant_permission("TRANSFER")
    print(f"   Result: {msg}")
    
    # Test list safety
    print_section("Testing List Copy Safety")
    perms = user.get_permissions()
    print(f"Original: {perms}")
    perms.append("ADMIN")
    print(f"Modified external: {perms}")
    print(f"Actual permissions: {user.get_permissions()}")
    
    # Final status
    print_section("Final Status")
    print_status(user)
    print(f"\n📊 Audit entries: {len(user.get_audit_log())}")


if __name__ == "__main__":
    main()
