-- Initialize DevOps Automation Hub Database
-- This script creates the necessary tables for the automation system

-- Create database if it doesn't exist (handled by docker-compose)

-- Users table for authentication and user management
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Deployments table for tracking deployment status
CREATE TABLE IF NOT EXISTS deployments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    namespace VARCHAR(100),
    status VARCHAR(50),
    replicas INTEGER,
    ready_replicas INTEGER,
    issues TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Infrastructure metrics table
CREATE TABLE IF NOT EXISTS infrastructure_metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpu_percent DECIMAL(5,2),
    memory_percent DECIMAL(5,2),
    disk_percent DECIMAL(5,2),
    network_io JSONB,
    process_count INTEGER,
    load_average DECIMAL[],
    metadata JSONB
);

-- Alerts table for alert management
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL,
    source VARCHAR(100),
    status VARCHAR(20) DEFAULT 'new',
    tags TEXT[],
    metadata JSONB,
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cost optimization recommendations table
CREATE TABLE IF NOT EXISTS cost_recommendations (
    id SERIAL PRIMARY KEY,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    current_cost DECIMAL(10,2),
    potential_savings DECIMAL(10,2),
    recommendation TEXT,
    confidence VARCHAR(20),
    implementation_effort VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Automation jobs table for tracking scheduled tasks
CREATE TABLE IF NOT EXISTS automation_jobs (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(255) NOT NULL,
    job_type VARCHAR(100),
    status VARCHAR(50),
    last_run TIMESTAMP,
    next_run TIMESTAMP,
    run_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failure_count INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit log table for tracking system changes
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_deployments_status ON deployments(status);
CREATE INDEX IF NOT EXISTS idx_deployments_namespace ON deployments(namespace);
CREATE INDEX IF NOT EXISTS idx_infrastructure_metrics_timestamp ON infrastructure_metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_status ON alerts(status);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_cost_recommendations_status ON cost_recommendations(status);
CREATE INDEX IF NOT EXISTS idx_automation_jobs_status ON automation_jobs(status);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Insert default admin user (password: admin123 - change in production!)
INSERT INTO users (email, password_hash, first_name, last_name, role) 
VALUES (
    'admin@devops-hub.local', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6hsxq5S/kS', -- admin123
    'Admin', 
    'User', 
    'admin'
) ON CONFLICT (email) DO NOTHING;

-- Insert sample automation jobs
INSERT INTO automation_jobs (job_name, job_type, status, next_run) VALUES
    ('deployment_monitor', 'monitoring', 'active', CURRENT_TIMESTAMP + INTERVAL '5 minutes'),
    ('infrastructure_monitor', 'monitoring', 'active', CURRENT_TIMESTAMP + INTERVAL '5 minutes'),
    ('cost_optimizer', 'optimization', 'active', CURRENT_TIMESTAMP + INTERVAL '1 hour'),
    ('alert_processor', 'alerting', 'active', CURRENT_TIMESTAMP + INTERVAL '1 minute')
ON CONFLICT DO NOTHING;

-- Create a function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers to automatically update updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deployments_updated_at BEFORE UPDATE ON deployments 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alerts_updated_at BEFORE UPDATE ON alerts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cost_recommendations_updated_at BEFORE UPDATE ON cost_recommendations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_automation_jobs_updated_at BEFORE UPDATE ON automation_jobs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions to the devops_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO devops_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO devops_user;
