# Users Table
Stores user details.
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    user_name VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active', -- e.g., 'active', 'inactive', 'banned'
    is_email_verified BOOLEAN DEFAULT FALSE, -- Tracks email verification status
    verification_token UUID DEFAULT gen_random_uuid(), -- Token for email verification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CONSTRAINT chk_email_format CHECK (email ~* '^[^@]+@[^@]+\.[^@]+$') -- Basic email format validation
);
```

# Roles Table
Defines user roles.
```sql
CREATE TABLE roles (
    role_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);
```

# User Roles Table
Links users to their roles.
```sql
CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Permissions Table
Defines permissions (e.g., CRUD operations).
```sql
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    permission_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);
```

# Role Permissions Table
Assigns permissions to roles.
```sql
CREATE TABLE role_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```


# Add a login_methods Table
This table defines the different login methods available in your application, such as "email/password" or social logins.
```sql
CREATE TABLE login_methods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    method_name VARCHAR(50) UNIQUE NOT NULL, -- e.g., 'email', 'google', 'github', 'facebook'
    description TEXT
);
```

# Add a user_social_logins Table
This table tracks the social accounts linked to each user. It allows users to log in with multiple social networks.
```sql
CREATE TABLE user_social_logins (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    login_method_id UUID REFERENCES login_methods(id) ON DELETE CASCADE,
    provider_user_id VARCHAR(255) NOT NULL, -- ID provided by the social network
    access_token TEXT, -- (Optional) For storing encrypted access tokens if needed
    refresh_token TEXT, -- (Optional) For storing encrypted refresh tokens if needed
    expires_at TIMESTAMP, -- (Optional) Token expiration time
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    CONSTRAINT unique_provider_user_id UNIQUE (login_method_id, provider_user_id) -- Ensure uniqueness for provider-user combos
);

-- Add indexes for performance
CREATE INDEX idx_user_id ON user_social_logins(user_id);
CREATE INDEX idx_login_method_id ON user_social_logins(login_method_id);
```

* Example Data in the `login_methods` Table

| login_method_id | method_name | description       |
|------------------|-------------|-------------------|
| 1               | email       | Email and password |
| 2               | google      | Google Login      |
| 3               | github      | GitHub Login      |
| 4               | facebook    | Facebook Login    |

# Plans Table
Defines the different subscription plans (e.g., Free, Standard, Premium).
```sql
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0, -- 0 for Free, set price for paid plans
    description TEXT,
    max_documents INT,
    max_storage NUMERIC(10, 2), -- in GB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Features
Lists features available in each plan. Allows for flexibility if new features are added.
```sql
CREATE TABLE features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL UNIQUE, -- e.g., 'API Access', '24/7 Support'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Plan_Features
A mapping table to associate features with specific plans (e.g., Premium has all features, Standard has a subset).
```sql
CREATE TABLE plan_features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (plan_id, feature_id)
);
```

# Subscriptions Table
Tracks user subscriptions.
```sql

CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, plan_id)
);

```

# Trial_Periods
Tracks trial periods if applicable.
```sql
CREATE TABLE trial_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Billing Table
Tracks billing details.
```sql
CREATE TABLE billing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
    amount NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    payment_status VARCHAR(50) DEFAULT 'pending', -- Pending, Paid, Failed
    payment_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Documents Table
Stores metadata of uploaded documents.
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL, -- Size in bytes
    file_type VARCHAR(50), -- File format (e.g., pdf, docx, txt)
    version INT DEFAULT 1, -- Versioning for document updates
    status VARCHAR(50) DEFAULT 'uploaded', -- Detailed status tracking
    failure_reason TEXT, -- Error details if processing fails
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Tracks updates to document info
    CONSTRAINT chk_file_size CHECK (file_size > 0) -- Ensures file size is valid
);
```

# Organization or Team Management Table
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    storage_limit BIGINT DEFAULT 1073741824, -- Storage limit in bytes
    custom_branding JSONB DEFAULT NULL, -- JSON for organization-specific settings
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member', -- e.g., 'admin', 'member'
    notifications_enabled BOOLEAN DEFAULT TRUE, -- User-specific settings
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    invited_by UUID REFERENCES users(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'pending', -- pending, accepted, declined
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Notifications Table
For in-app or email notifications.
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Tied to specific user
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE, -- Optional for team-wide notifications
    message TEXT NOT NULL, -- Notification content
    type VARCHAR(50) NOT NULL DEFAULT 'info', -- Type of notification ('info', 'error', 'success', etc.)
    channel VARCHAR(50) DEFAULT 'in-app', -- Delivery channel ('in-app', 'email', etc.)
    action_url TEXT, -- Optional URL for user actions
    priority VARCHAR(20) DEFAULT 'low', -- Notification priority ('low', 'medium', 'high')
    status VARCHAR(50) DEFAULT 'unread', -- Notification status ('unread', 'read')
    expires_at TIMESTAMP, -- Expiry time for the notification
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Timestamp for creation
);
```

# Custom User Settings Table
For managing user-specific preferences.
```sql
CREATE TABLE user_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    setting_key VARCHAR(255) NOT NULL, -- Key for the setting (e.g., 'theme', 'notifications')
    setting_value JSONB NOT NULL, -- Value of the setting, stored as JSON
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_setting UNIQUE (user_id, setting_key) -- Ensures unique settings per user
);
```




# Usage Logs Table ### TODO:
Tracks user actions, like document uploads or chats.
```sql
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    action VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);
```

# API Keys Table ### TODO: future implementation
For managing user API keys (optional for integrations).

Store permissions or scopes associated with the API key. For example:

- `read`: Read-only access.
- `write`: Ability to modify resources.
- `admin`: Full access.

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    api_key TEXT UNIQUE NOT NULL,
    name VARCHAR(255), -- Optional label for easier management
    permissions VARCHAR(255) DEFAULT 'read', -- Fine-grained access control
    is_revoked BOOLEAN DEFAULT FALSE, -- Track revocation status
    last_used_at TIMESTAMP, -- Tracks the last usage of the key
    request_count BIGINT DEFAULT 0, -- Tracks the number of API requests
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP -- Optional expiration date
);
```

# Audit Logs Table  ## TODO:
For tracking system-level changes and user activities.
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    table_name VARCHAR(255),
    record_id INT, -- Optional: the ID of the affected record
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Feature Flags Table  ## TODO:
For managing feature availability (useful for A/B testing or gradual rollouts).
```sql
CREATE TABLE feature_flags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    is_enabled BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Document Sharing Table  ## TODO:
If you allow document sharing between users.
```sql
CREATE TABLE document_sharing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    shared_with_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permission VARCHAR(50) DEFAULT 'read', -- e.g., 'read', 'write'
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Storage Quota Table  ## TODO:
For tracking user storage usage.
```sql
CREATE TABLE storage_quotas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    max_storage NUMERIC(10, 2), -- e.g., in GB
    used_storage NUMERIC(10, 2) DEFAULT 0, -- e.g., in GB
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Session Management Table  ## TODO:
For tracking active user sessions, especially for security and analytics.
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);
```

# Support Tickets Table  ## TODO:
For managing user support requests.
```sql
CREATE TABLE support_tickets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'in progress', 'resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# API Usage Logs Table  ## TODO:
For tracking API usage by users (if offering API access).
```sql
CREATE TABLE api_usage_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    api_key_id UUID REFERENCES api_keys(id) ON DELETE CASCADE,
    endpoint VARCHAR(255) NOT NULL,
    request_payload JSONB,
    response_status INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

# Email Queue Table  ## TODO:
For managing email notifications or alerts (e.g., reminders, invoices).
```sql
CREATE TABLE email_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    email_type VARCHAR(50), -- e.g., 'welcome', 'password_reset'
    subject VARCHAR(255),
    body TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'sent', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP
);
```

# Add a login_history Table  ## TODO:
This table tracks how users log in to the system (useful for analytics and auditing).
```sql
CREATE TABLE login_history (
    login_id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    login_method_id UUID REFERENCES login_methods(lid) ON DELETE CASCADE,
    ip_address VARCHAR(50),
    user_agent TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```




