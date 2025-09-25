"""
DevOps Automation Hub - Main Entry Point

This is the core automation engine that orchestrates all DevOps automation tasks.
Perfect for demonstrating RPA and DevOps skills to potential employers.
"""

import os
import time
import schedule
from datetime import datetime
from loguru import logger
from dotenv import load_dotenv

from automation.deployment_monitor import DeploymentMonitor
from automation.infrastructure_monitor import InfrastructureMonitor
from automation.cost_optimizer import CostOptimizer
from automation.alert_processor import AlertProcessor
from api.flask_app import create_app

# Load environment variables
load_dotenv()

class DevOpsAutomationHub:
    """
    Main orchestrator for all DevOps automation tasks.
    
    This class demonstrates enterprise-level automation architecture
    and is designed to impress potential employers with:
    - Clean code structure
    - Proper error handling
    - Comprehensive logging
    - Modular design
    """
    
    def __init__(self):
        self.deployment_monitor = DeploymentMonitor()
        self.infrastructure_monitor = InfrastructureMonitor()
        self.cost_optimizer = CostOptimizer()
        self.alert_processor = AlertProcessor()
        
        # Configure logging
        logger.add(
            "logs/automation_{time}.log",
            rotation="1 day",
            retention="30 days",
            level="INFO"
        )
        
        logger.info("DevOps Automation Hub initialized")
    
    def run_health_checks(self):
        """Run comprehensive infrastructure health checks"""
        logger.info("Starting health check cycle")
        
        try:
            # Check deployment status
            deployment_status = self.deployment_monitor.check_deployments()
            logger.info(f"Deployment check completed: {deployment_status}")
            
            # Monitor infrastructure metrics
            infra_metrics = self.infrastructure_monitor.collect_metrics()
            logger.info(f"Infrastructure metrics collected: {len(infra_metrics)} services")
            
            # Process any alerts
            alerts_processed = self.alert_processor.process_pending_alerts()
            logger.info(f"Processed {alerts_processed} alerts")
            
        except Exception as e:
            logger.error(f"Error during health checks: {str(e)}")
    
    def run_cost_optimization(self):
        """Run cost optimization analysis and recommendations"""
        logger.info("Starting cost optimization cycle")
        
        try:
            savings = self.cost_optimizer.analyze_and_optimize()
            logger.info(f"Cost optimization completed. Potential savings: ${savings}")
            
        except Exception as e:
            logger.error(f"Error during cost optimization: {str(e)}")
    
    def schedule_tasks(self):
        """Schedule all automation tasks"""
        # Health checks every 5 minutes
        schedule.every(5).minutes.do(self.run_health_checks)
        
        # Cost optimization daily at 2 AM
        schedule.every().day.at("02:00").do(self.run_cost_optimization)
        
        logger.info("All tasks scheduled successfully")
    
    def start(self):
        """Start the automation hub"""
        logger.info("🚀 Starting DevOps Automation Hub")
        
        # Schedule all tasks
        self.schedule_tasks()
        
        # Run initial health check
        self.run_health_checks()
        
        # Start the Flask API in a separate thread
        app = create_app()
        
        # Start Flask server in a separate thread
        import threading
        flask_thread = threading.Thread(
            target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False),
            daemon=True
        )
        flask_thread.start()
        
        logger.info("✅ DevOps Automation Hub is running")
        logger.info("📊 Web dashboard available at: http://localhost:5000")
        logger.info("🔄 Automation tasks scheduled and running")
        
        # Main loop
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Shutting down DevOps Automation Hub")

def main():
    """Main entry point"""
    print("🤖 DevOps Automation Hub")
    print("=" * 50)
    print("A comprehensive RPA system for DevOps automation")
    print("Perfect for demonstrating automation skills to employers!")
    print("=" * 50)
    
    # Create and start the automation hub
    hub = DevOpsAutomationHub()
    hub.start()

if __name__ == "__main__":
    main()
