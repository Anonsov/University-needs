"""
AccountAccess Class - Manages user permissions with strict encapsulation
"""
from datetime import datetime


class AccountAccess:
    """
    Manages user permissions with all private attributes.
    Returns copies of internal data to prevent external modification.
    """
    
    # Class-level constants for restricted permissions
    RESTRICTED_PERMISSIONS = {"TRANSFER", "WITHDRAW"}
    ALLOWED_PERMISSIONS = {
        "VIEW_BALANCE", "VIEW_TRANSACTIONS", "TRANSFER", 
        "WITHDRAW", "DEPOSIT", "UPDATE_PROFILE"
    }
    
    def __init__(self):
        """Initialize AccountAccess with empty permissions list."""
        self.__permissions = []  # Private list of permissions
        self.__permission_history = []  # Private log of permission changes
        self.__log_permission_change("INITIALIZED", "Account access created")
    
    def get_permissions(self):
        """
        Get a COPY of permissions list to prevent external modification.
        
        Returns:
            list: Copy of permissions list
        """
        return self.__permissions.copy()
    
    def add_permission(self, permission, is_verified=False):
        """
        Add a permission to the user's access list.
        
        Args:
            permission (str): Permission to add
            is_verified (bool): Whether user is verified (required for restricted permissions)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validate permission exists
        if permission not in self.ALLOWED_PERMISSIONS:
            message = f"Invalid permission: {permission}"
            self.__log_permission_change("ADD_FAILED", message)
            return (False, message)
        
        # Check if permission already exists
        if permission in self.__permissions:
            message = f"Permission already granted: {permission}"
            self.__log_permission_change("ADD_DUPLICATE", message)
            return (False, message)
        
        # Check verification requirement for restricted permissions
        if permission in self.RESTRICTED_PERMISSIONS and not is_verified:
            message = f"Cannot grant '{permission}' - user must be VERIFIED"
            self.__log_permission_change("ADD_DENIED", message)
            return (False, message)
        
        # Add permission
        self.__permissions.append(permission)
        message = f"Permission granted: {permission}"
        self.__log_permission_change("ADD_SUCCESS", message)
        return (True, message)
    
    def remove_permission(self, permission):
        """
        Remove a permission from the user's access list.
        
        Args:
            permission (str): Permission to remove
            
        Returns:
            tuple: (success: bool, message: str)
        """
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
        """
        Check if user has a specific permission.
        
        Args:
            permission (str): Permission to check
            
        Returns:
            bool: True if permission exists, False otherwise
        """
        return permission in self.__permissions
    
    def clear_all_permissions(self):
        """
        Clear all permissions (for security purposes).
        
        Returns:
            int: Number of permissions cleared
        """
        count = len(self.__permissions)
        self.__permissions.clear()
        self.__log_permission_change(
            "CLEAR_ALL",
            f"Cleared {count} permissions"
        )
        return count
    
    def __log_permission_change(self, action, description):
        """
        Private method to log permission changes.
        
        Args:
            action (str): Action type
            description (str): Description of the change
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'description': description,
            'current_permissions': self.__permissions.copy()
        }
        self.__permission_history.append(log_entry)
    
    def get_permission_history(self):
        """
        Get a copy of permission history (for auditing).
        
        Returns:
            list: Copy of permission history
        """
        return self.__permission_history.copy()
    
    def __str__(self):
        """String representation of AccountAccess."""
        return f"AccountAccess(permissions={self.__permissions})"
    
    def __repr__(self):
        """Detailed representation of AccountAccess."""
        return self.__str__()
