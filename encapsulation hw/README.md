# 🏦 Advanced Encapsulation Assignment - Fintech Identity System

A comprehensive demonstration of advanced object-oriented programming principles including encapsulation, composition, state management, and data integrity in a simulated fintech banking system.

---

## 📋 Project Overview

This project implements a secure user identity subsystem for a digital banking application with three tightly-coupled classes that demonstrate:

- **Strict encapsulation** (public, protected, and private attributes)
- **Input validation** (email and phone number formats)
- **State transition protection** (verification workflow)
- **Permission management** with verification requirements
- **Defensive copying** to prevent external modification
- **Comprehensive audit logging**
- **Composition pattern** for enhanced security

---

## 🗂️ File Structure

```
encapsulation hw/
├── user_identity.py      # UserIdentity class with validation & state management
├── account_access.py     # AccountAccess class for permission management
├── secure_user.py        # SecureUser class combining both via composition
├── main.py               # Comprehensive demonstration
├── EXPLANATION.md        # Detailed written explanation
└── README.md            # This file
```

---

## 🎯 Classes Overview

### 1️⃣ `UserIdentity`
Manages user personal information with strict encapsulation.

**Attributes:**
- `username` (public) - Username
- `_email` (protected) - Validated email address
- `__phone_number` (private) - Validated phone number
- `__verification_status` (private) - One of: "UNVERIFIED", "PENDING", "VERIFIED"

**Key Methods:**
- `get_email()`, `set_email(new_email)` - Controlled email access
- `get_phone_number()` - Read-only phone access
- `request_verification()` - Transition to PENDING state
- `verify()` - Transition to VERIFIED state
- `get_verification_status()` - Get current status

**Private Helper Methods:**
- `__validate_email()` - Email format validation
- `__validate_phone()` - Phone format validation (supports +XXX-XXX-XXXX-XXXX)
- `__log_state_change()` - State change auditing

---

### 2️⃣ `AccountAccess`
Manages user permissions with all private attributes.

**Attributes:**
- `__permissions` (private) - List of granted permissions
- `__permission_history` (private) - Audit trail

**Key Methods:**
- `get_permissions()` - Returns a **COPY** of permissions
- `add_permission(permission, is_verified)` - Add permission with verification check
- `remove_permission(permission)` - Revoke permission
- `has_permission(permission)` - Check if permission exists

**Restricted Permissions** (require verification):
- `TRANSFER`
- `WITHDRAW`

**Allowed Permissions:**
- `VIEW_BALANCE`
- `VIEW_TRANSACTIONS`
- `DEPOSIT`
- `UPDATE_PROFILE`

---

### 3️⃣ `SecureUser` (Composition)
Combines UserIdentity and AccountAccess with comprehensive auditing.

**Attributes:**
- `_identity` (protected) - UserIdentity instance
- `__access` (private) - AccountAccess instance
- `__audit_log` (private) - Complete action history

**Key Methods:**
- `grant_permission(permission)` - Grant permission with verification enforcement
- `revoke_permission(permission)` - Revoke permission
- `request_verification()` - Request identity verification
- `verify_identity()` - Complete verification
- `identity_status()` - Get formatted status
- `get_audit_log()` - Returns a **COPY** of audit log

---

## 🚀 How to Run

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Running the Demonstration

```bash
cd "encapsulation hw"
python main.py
```

### Expected Output

The demonstration will show:

1. ✅ **Valid user creation** with proper initialization
2. ❌ **Illegal direct access attempts** (all blocked)
3. ❌ **Illegal state transitions** (verification workflow enforcement)
4. ⚠️ **Restricted permissions before verification** (denied)
5. ✅ **Restricted permissions after verification** (granted)
6. 🔒 **List manipulation safety** (copies prevent modification)
7. 📊 **Final system state** with audit trails

---

## 🔍 Key Features Demonstrated

### 1. Encapsulation Levels
```python
user.username                    # ✅ Public - direct access
user._identity._email            # ⚠️ Protected - possible but discouraged
user._identity.__phone_number    # ❌ Private - AttributeError
```

### 2. State Transition Protection
```python
# ❌ Cannot verify without requesting first
user.verify_identity()  # Returns False

# ✅ Proper workflow
user.request_verification()  # UNVERIFIED → PENDING
user.verify_identity()        # PENDING → VERIFIED
```

### 3. Verification-Based Permissions
```python
# ❌ Unverified user cannot get TRANSFER permission
unverified_user.grant_permission("TRANSFER")  # Denied

# ✅ After verification
user.verify_identity()
user.grant_permission("TRANSFER")  # Granted
```

### 4. Defensive Copying
```python
# Get permissions list
perms = user.get_permissions()

# Modify external list
perms.append("ADMIN_ACCESS")

# Internal data unchanged! ✅
actual = user.get_permissions()  # Original permissions intact
```

---

## 📊 Validation Rules

### Email Format
- Must match pattern: `name@domain.extension`
- Example: `john.doe@example.com` ✅
- Invalid: `invalid-email` ❌

### Phone Format
- Must match pattern: `+XXX-XXX-XXXX-XXXXX`
- Example: `+1-555-123-4567` ✅
- Invalid: `123456789` ❌

### Verification States
- **UNVERIFIED** → **PENDING** (via `request_verification()`)
- **PENDING** → **VERIFIED** (via `verify()`)
- All other transitions are blocked

---

## 🧪 Testing Different Scenarios

You can modify `main.py` to test additional scenarios:

```python
# Test invalid email
user.update_email("bad-email")  # Raises ValueError

# Test invalid state transition
user.verify_identity()  # Returns False if not PENDING

# Test permission without verification
user.grant_permission("WITHDRAW")  # Denied if not VERIFIED

# Test list manipulation
perms = user.get_permissions()
perms.clear()  # External list modified
user.get_permissions()  # Internal list unchanged ✅
```

---

## 📚 Learning Objectives

This project demonstrates:

1. **Encapsulation**: Using public, protected, and private access levels
2. **Data Validation**: Input sanitization and format checking
3. **State Management**: Enforcing valid state transitions
4. **Defensive Programming**: Returning copies to prevent external modification
5. **Composition over Inheritance**: Building complex systems from simple components
6. **Audit Logging**: Comprehensive action tracking for security
7. **Business Logic Enforcement**: Automatic rule checking (e.g., verification requirements)

---

## 🔐 Security Principles

### Defense in Depth
Multiple layers of protection ensure system integrity:
- Input validation at creation
- State transition rules
- Permission verification requirements
- Defensive copying of mutable data
- Comprehensive audit logging

### Principle of Least Privilege
- Unverified users have limited permissions
- Restricted operations require verification
- No direct access to sensitive internal state

### Immutability Where Possible
- Phone numbers cannot be changed after creation
- Verification status follows strict workflow
- Audit logs cannot be tampered with

---

## 💡 Real-World Applications

This pattern is used in:
- Banking systems (account verification, transaction permissions)
- Healthcare systems (patient data protection, access control)
- Government systems (identity verification, clearance levels)
- E-commerce platforms (account security, payment authorization)

---

## 📖 Additional Resources

For detailed explanations of the design decisions, see:
- **EXPLANATION.md** - In-depth analysis of encapsulation, list safety, and composition

---

## ✅ Assignment Requirements Met

- [x] `UserIdentity` with public, protected, and private attributes
- [x] Email and phone validation
- [x] Verification state management with transition protection
- [x] `AccountAccess` with all private attributes
- [x] Permission management with verification requirements
- [x] Defensive copying (returning list copies)
- [x] `SecureUser` using composition pattern
- [x] Comprehensive audit logging
- [x] `main.py` demonstration of all features
- [x] Illegal access attempt demonstrations
- [x] Written explanation of key concepts

---

## 👨‍💻 Author

Created as part of an advanced encapsulation assignment demonstrating professional-grade object-oriented programming in Python.

---

## 📝 License

Educational project - free to use for learning purposes.
