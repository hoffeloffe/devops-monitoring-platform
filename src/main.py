"""
DevOps Automation Hub - Main Entry Point

This is the core automation engine that orchestrates all DevOps automation tasks.
"""

import time
import schedule
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
    """Main orchestrator for all DevOps automation tasks."""

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
            deployment_status = self.deployment_monitor.check_deployments()
            logger.info(f"Deployment check completed: {deployment_status}")

            infra_metrics = self.infrastructure_monitor.collect_metrics()
            logger.info(f"Infrastructure metrics collected: {len(infra_metrics)} services")

            alerts_processed = self.alert_processor.process_pending_alerts()
            logger.info(f"Processed {alerts_processed} alerts")

        except Exception:
            logger.exception("Error during health checks")

    def run_cost_optimization(self):
        """Run cost optimization analysis and recommendations"""
        logger.info("Starting cost optimization cycle")

        try:
            savings = self.cost_optimizer.analyze_and_optimize()
            logger.info(f"Cost optimization completed. Potential savings: ${savings}")

        except Exception:
            logger.exception("Error during cost optimization")

    def schedule_tasks(self):
        """Schedule all automation tasks"""
        schedule.every(5).minutes.do(self.run_health_checks)
        schedule.every().day.at("02:00").do(self.run_cost_optimization)

        logger.info("All tasks scheduled successfully")

    def start(self):
        """Start the automation hub"""
        logger.info("Starting DevOps Automation Hub")

        self.schedule_tasks()

        self.run_health_checks()

        app = create_app(
            self.deployment_monitor,
            self.infrastructure_monitor,
            self.cost_optimizer,
            self.alert_processor,
        )

        import threading
        flask_thread = threading.Thread(
            target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False),
            daemon=True
        )
        flask_thread.start()

        logger.info("DevOps Automation Hub is running")
        logger.info("Web dashboard available at: http://localhost:5000")
        logger.info("Automation tasks scheduled and running")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Shutting down DevOps Automation Hub")

def main():
    """Main entry point"""
    print("DevOps Automation Hub")
    print("=" * 50)
    print("A comprehensive RPA system for DevOps automation")
    print("=" * 50)

    hub = DevOpsAutomationHub()
    hub.start()

if __name__ == "__main__":
    main()
