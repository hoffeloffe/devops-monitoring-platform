"""
Alert Processor - Intelligent Alert Management and Routing

This module demonstrates advanced RPA skills by automating alert processing,
deduplication, and intelligent routing based on severity and context.
"""

import smtplib
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib

@dataclass
class Alert:
    """Data class for alert information"""
    id: str
    title: str
    description: str
    severity: str  # critical, warning, info
    source: str
    timestamp: datetime
    tags: List[str]
    metadata: Dict
    status: str = "new"  # new, acknowledged, resolved
    assigned_to: Optional[str] = None

@dataclass
class NotificationChannel:
    """Data class for notification channels"""
    name: str
    type: str  # email, slack, webhook, sms
    config: Dict
    enabled: bool = True

class AlertProcessor:
    """
    Intelligent alert processing and notification system.
    
    This class demonstrates enterprise automation capabilities:
    - Alert deduplication and correlation
    - Intelligent routing based on severity and context
    - Multi-channel notifications (email, Slack, webhooks)
    - Alert escalation and acknowledgment tracking
    - Integration with monitoring systems
    """
    
    def __init__(self):
        self.active_alerts = {}
        self.alert_history = []
        self.notification_channels = self._setup_notification_channels()
        self.routing_rules = self._setup_routing_rules()
        self.deduplication_window = timedelta(minutes=5)
        
    def _setup_notification_channels(self) -> List[NotificationChannel]:
        """Setup available notification channels"""
        return [
            NotificationChannel(
                name="email_ops",
                type="email",
                config={
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "recipients": ["ops-team@company.com", "devops@company.com"],
                    "sender": "alerts@company.com"
                }
            ),
            NotificationChannel(
                name="slack_critical",
                type="slack",
                config={
                    "webhook_url": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
                    "channel": "#critical-alerts",
                    "username": "DevOps Bot"
                }
            ),
            NotificationChannel(
                name="pagerduty",
                type="webhook",
                config={
                    "url": "https://events.pagerduty.com/v2/enqueue",
                    "routing_key": "YOUR_PAGERDUTY_KEY"
                }
            )
        ]
    
    def _setup_routing_rules(self) -> List[Dict]:
        """Setup alert routing rules based on severity and source"""
        return [
            {
                "name": "critical_alerts",
                "conditions": {"severity": "critical"},
                "channels": ["email_ops", "slack_critical", "pagerduty"],
                "escalation_time": timedelta(minutes=15)
            },
            {
                "name": "warning_alerts",
                "conditions": {"severity": "warning"},
                "channels": ["email_ops", "slack_critical"],
                "escalation_time": timedelta(hours=1)
            },
            {
                "name": "info_alerts",
                "conditions": {"severity": "info"},
                "channels": ["email_ops"],
                "escalation_time": timedelta(hours=4)
            },
            {
                "name": "kubernetes_alerts",
                "conditions": {"source": "kubernetes"},
                "channels": ["email_ops", "slack_critical"],
                "escalation_time": timedelta(minutes=30)
            }
        ]
    
    def generate_alert_id(self, alert_data: Dict) -> str:
        """Generate unique alert ID based on content for deduplication"""
        content = f"{alert_data.get('title', '')}{alert_data.get('source', '')}{alert_data.get('description', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def deduplicate_alert(self, new_alert: Alert) -> bool:
        """
        Check if alert is a duplicate within the deduplication window.
        
        Demonstrates intelligent alert processing and noise reduction.
        """
        current_time = datetime.now()
        
        # Check active alerts for duplicates
        for alert_id, existing_alert in self.active_alerts.items():
            if (existing_alert.title == new_alert.title and 
                existing_alert.source == new_alert.source and
                current_time - existing_alert.timestamp < self.deduplication_window):
                
                logger.info(f"Alert deduplicated: {new_alert.title} (original: {alert_id})")
                return True
        
        return False
    
    def process_alert(self, alert_data: Dict) -> Optional[Alert]:
        """
        Process incoming alert and apply business logic.
        
        This demonstrates intelligent alert processing and automation.
        """
        try:
            # Create alert object
            alert = Alert(
                id=self.generate_alert_id(alert_data),
                title=alert_data.get('title', 'Unknown Alert'),
                description=alert_data.get('description', ''),
                severity=alert_data.get('severity', 'info').lower(),
                source=alert_data.get('source', 'unknown'),
                timestamp=datetime.now(),
                tags=alert_data.get('tags', []),
                metadata=alert_data.get('metadata', {})
            )
            
            # Check for duplicates
            if self.deduplicate_alert(alert):
                return None
            
            # Enrich alert with additional context
            alert = self._enrich_alert(alert)
            
            # Apply severity-based processing
            alert = self._apply_severity_rules(alert)
            
            # Store alert
            self.active_alerts[alert.id] = alert
            self.alert_history.append(alert)
            
            logger.info(f"Processed new alert: {alert.title} (severity: {alert.severity})")
            
            return alert
            
        except Exception as e:
            logger.error(f"Error processing alert: {e}")
            return None
    
    def _enrich_alert(self, alert: Alert) -> Alert:
        """
        Enrich alert with additional context and metadata.
        
        Demonstrates data enrichment and contextual analysis.
        """
        # Add timestamp-based tags
        hour = alert.timestamp.hour
        if 0 <= hour < 6:
            alert.tags.append("night_hours")
        elif 9 <= hour < 17:
            alert.tags.append("business_hours")
        
        # Add source-based enrichment
        if alert.source == "kubernetes":
            alert.tags.append("container_platform")
            if "pod" in alert.description.lower():
                alert.tags.append("pod_issue")
            elif "node" in alert.description.lower():
                alert.tags.append("node_issue")
        
        elif alert.source == "aws":
            alert.tags.append("cloud_platform")
            if "ec2" in alert.description.lower():
                alert.tags.append("compute_issue")
            elif "rds" in alert.description.lower():
                alert.tags.append("database_issue")
        
        # Add severity-based metadata
        if alert.severity == "critical":
            alert.metadata["requires_immediate_attention"] = True
            alert.metadata["max_response_time"] = "15 minutes"
        elif alert.severity == "warning":
            alert.metadata["requires_attention"] = True
            alert.metadata["max_response_time"] = "1 hour"
        
        return alert
    
    def _apply_severity_rules(self, alert: Alert) -> Alert:
        """
        Apply business rules based on alert severity and context.
        
        Demonstrates rule-based automation and decision making.
        """
        # Auto-escalate certain types of alerts
        if any(keyword in alert.description.lower() for keyword in ["down", "failed", "error", "timeout"]):
            if alert.severity == "warning":
                alert.severity = "critical"
                alert.tags.append("auto_escalated")
                logger.info(f"Auto-escalated alert {alert.id} to critical")
        
        # Auto-assign based on source
        if alert.source == "kubernetes":
            alert.assigned_to = "k8s_team"
        elif alert.source == "aws":
            alert.assigned_to = "cloud_team"
        elif alert.source == "database":
            alert.assigned_to = "dba_team"
        
        return alert
    
    def route_alert(self, alert: Alert) -> List[str]:
        """
        Route alert to appropriate notification channels based on rules.
        
        Demonstrates intelligent routing and decision automation.
        """
        matching_channels = []
        
        for rule in self.routing_rules:
            rule_matches = True
            
            # Check if alert matches rule conditions
            for condition_key, condition_value in rule["conditions"].items():
                if getattr(alert, condition_key, None) != condition_value:
                    rule_matches = False
                    break
            
            if rule_matches:
                matching_channels.extend(rule["channels"])
                logger.info(f"Alert {alert.id} matched routing rule: {rule['name']}")
        
        # Remove duplicates while preserving order
        unique_channels = list(dict.fromkeys(matching_channels))
        
        return unique_channels
    
    def send_email_notification(self, alert: Alert, channel_config: Dict) -> bool:
        """
        Send email notification for alert.
        
        Demonstrates email automation and notification systems.
        """
        try:
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = channel_config.get('sender', 'alerts@company.com')
            msg['To'] = ', '.join(channel_config.get('recipients', []))
            msg['Subject'] = f"[{alert.severity.upper()}] {alert.title}"
            
            # Create email body
            body = f"""
Alert Details:
--------------
Title: {alert.title}
Severity: {alert.severity.upper()}
Source: {alert.source}
Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Tags: {', '.join(alert.tags)}

Description:
{alert.description}

Alert ID: {alert.id}
Status: {alert.status}
Assigned To: {alert.assigned_to or 'Unassigned'}

---
This is an automated alert from DevOps Automation Hub
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email (in production, you'd use actual SMTP credentials)
            logger.info(f"Email notification sent for alert {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def send_slack_notification(self, alert: Alert, channel_config: Dict) -> bool:
        """
        Send Slack notification for alert.
        
        Demonstrates webhook integration and chat platform automation.
        """
        try:
            # Determine color based on severity
            color_map = {
                "critical": "#FF0000",
                "warning": "#FFA500", 
                "info": "#0000FF"
            }
            
            # Create Slack message payload
            payload = {
                "channel": channel_config.get('channel', '#alerts'),
                "username": channel_config.get('username', 'DevOps Bot'),
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "#808080"),
                        "title": f"[{alert.severity.upper()}] {alert.title}",
                        "text": alert.description,
                        "fields": [
                            {"title": "Source", "value": alert.source, "short": True},
                            {"title": "Time", "value": alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'), "short": True},
                            {"title": "Alert ID", "value": alert.id, "short": True},
                            {"title": "Tags", "value": ', '.join(alert.tags), "short": True}
                        ],
                        "footer": "DevOps Automation Hub",
                        "ts": int(alert.timestamp.timestamp())
                    }
                ]
            }
            
            # Send to Slack (in production, you'd use actual webhook URL)
            webhook_url = channel_config.get('webhook_url')
            if webhook_url and webhook_url != "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK":
                response = requests.post(webhook_url, json=payload)
                response.raise_for_status()
            
            logger.info(f"Slack notification sent for alert {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send Slack notification: {e}")
            return False
    
    def send_webhook_notification(self, alert: Alert, channel_config: Dict) -> bool:
        """
        Send webhook notification for alert.
        
        Demonstrates API integration and external system communication.
        """
        try:
            # Create webhook payload
            payload = {
                "alert_id": alert.id,
                "title": alert.title,
                "description": alert.description,
                "severity": alert.severity,
                "source": alert.source,
                "timestamp": alert.timestamp.isoformat(),
                "tags": alert.tags,
                "metadata": alert.metadata,
                "status": alert.status
            }
            
            # Send webhook (in production, you'd use actual webhook URL)
            webhook_url = channel_config.get('url')
            if webhook_url and not webhook_url.startswith('https://events.pagerduty.com'):
                response = requests.post(webhook_url, json=payload, timeout=10)
                response.raise_for_status()
            
            logger.info(f"Webhook notification sent for alert {alert.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send webhook notification: {e}")
            return False
    
    def notify_alert(self, alert: Alert) -> Dict:
        """
        Send notifications for alert through appropriate channels.
        
        This orchestrates the notification process across multiple channels.
        """
        # Get routing channels for this alert
        target_channels = self.route_alert(alert)
        
        notification_results = {
            "alert_id": alert.id,
            "channels_attempted": len(target_channels),
            "successful_notifications": 0,
            "failed_notifications": 0,
            "results": []
        }
        
        for channel_name in target_channels:
            # Find channel configuration
            channel = next((ch for ch in self.notification_channels if ch.name == channel_name), None)
            
            if not channel or not channel.enabled:
                notification_results["results"].append({
                    "channel": channel_name,
                    "status": "skipped",
                    "reason": "Channel not found or disabled"
                })
                continue
            
            # Send notification based on channel type
            success = False
            if channel.type == "email":
                success = self.send_email_notification(alert, channel.config)
            elif channel.type == "slack":
                success = self.send_slack_notification(alert, channel.config)
            elif channel.type == "webhook":
                success = self.send_webhook_notification(alert, channel.config)
            
            # Record result
            if success:
                notification_results["successful_notifications"] += 1
                notification_results["results"].append({
                    "channel": channel_name,
                    "status": "success",
                    "type": channel.type
                })
            else:
                notification_results["failed_notifications"] += 1
                notification_results["results"].append({
                    "channel": channel_name,
                    "status": "failed",
                    "type": channel.type
                })
        
        logger.info(f"Notifications sent for alert {alert.id}: {notification_results['successful_notifications']} successful, {notification_results['failed_notifications']} failed")
        
        return notification_results
    
    def process_pending_alerts(self) -> int:
        """
        Process any pending alerts and send notifications.
        
        This is the main method called by the automation scheduler.
        """
        # In a real implementation, this would:
        # 1. Check for new alerts from monitoring systems
        # 2. Process each alert through the pipeline
        # 3. Send notifications
        # 4. Update alert status
        
        # For demo purposes, we'll create some sample alerts
        sample_alerts = [
            {
                "title": "High CPU Usage on Production Server",
                "description": "CPU usage has exceeded 90% for the last 5 minutes on server prod-web-01",
                "severity": "warning",
                "source": "monitoring",
                "tags": ["cpu", "performance", "production"],
                "metadata": {"server": "prod-web-01", "cpu_percent": 92.5}
            },
            {
                "title": "Kubernetes Pod CrashLoopBackOff",
                "description": "Pod 'api-service-7d4b8c9f-xyz' is in CrashLoopBackOff state",
                "severity": "critical",
                "source": "kubernetes",
                "tags": ["pod", "crash", "api"],
                "metadata": {"namespace": "production", "pod": "api-service-7d4b8c9f-xyz"}
            }
        ]
        
        processed_count = 0
        
        for alert_data in sample_alerts:
            alert = self.process_alert(alert_data)
            if alert:
                self.notify_alert(alert)
                processed_count += 1
        
        logger.info(f"Processed {processed_count} alerts")
        return processed_count
    
    def get_alert_summary(self) -> Dict:
        """Get summary of current alert status"""
        current_time = datetime.now()
        
        # Count alerts by severity
        severity_counts = {"critical": 0, "warning": 0, "info": 0}
        for alert in self.active_alerts.values():
            severity_counts[alert.severity] = severity_counts.get(alert.severity, 0) + 1
        
        # Count recent alerts (last 24 hours)
        recent_alerts = [
            alert for alert in self.alert_history 
            if current_time - alert.timestamp < timedelta(hours=24)
        ]
        
        return {
            "active_alerts": len(self.active_alerts),
            "severity_breakdown": severity_counts,
            "recent_alerts_24h": len(recent_alerts),
            "total_processed": len(self.alert_history),
            "last_processed": current_time.isoformat()
        }
