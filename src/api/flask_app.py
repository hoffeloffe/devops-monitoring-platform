"""
Flask API Backend for DevOps Automation Hub

This module provides REST API endpoints for the automation system,
demonstrating full-stack development and API design skills.
"""

import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import threading
import time
from loguru import logger

# Import our automation modules
from automation.deployment_monitor import DeploymentMonitor
from automation.infrastructure_monitor import InfrastructureMonitor
from automation.cost_optimizer import CostOptimizer
from automation.alert_processor import AlertProcessor

class DevOpsAPI:
    """
    RESTful API for DevOps Automation Hub.
    """

    def __init__(self, deployment_monitor=None, infrastructure_monitor=None, cost_optimizer=None, alert_processor=None):
        self.app = Flask(__name__)
        CORS(self.app, origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","))

        self.deployment_monitor = deployment_monitor or DeploymentMonitor()
        self.infrastructure_monitor = infrastructure_monitor or InfrastructureMonitor()
        self.cost_optimizer = cost_optimizer or CostOptimizer()
        self.alert_processor = alert_processor or AlertProcessor()

        # Cache for storing latest data
        self.data_cache = {
            'deployments': {},
            'infrastructure': {},
            'costs': {},
            'alerts': {},
            'last_updated': datetime.now()
        }

        # Setup routes
        self._setup_routes()

        # Start background data collection
        self._start_background_tasks()

    def _setup_routes(self):
        """Setup all API routes"""

        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0',
                'services': {
                    'deployment_monitor': 'active',
                    'infrastructure_monitor': 'active',
                    'cost_optimizer': 'active',
                    'alert_processor': 'active'
                }
            })

        @self.app.route('/api/dashboard', methods=['GET'])
        def get_dashboard_data():
            """Get comprehensive dashboard data"""
            try:
                dashboard_data = {
                    'timestamp': datetime.now().isoformat(),
                    'deployments': self.data_cache.get('deployments', {}),
                    'infrastructure': self.data_cache.get('infrastructure', {}),
                    'costs': self.data_cache.get('costs', {}),
                    'alerts': self.data_cache.get('alerts', {}),
                    'system_status': {
                        'uptime': self._get_system_uptime(),
                        'last_updated': self.data_cache.get('last_updated', datetime.now()).isoformat(),
                        'automation_status': 'running'
                    }
                }

                return jsonify(dashboard_data)

            except Exception as e:
                logger.exception("Error getting dashboard data")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/deployments', methods=['GET'])
        def get_deployments():
            """Get deployment status information"""
            try:
                deployments = self.deployment_monitor.check_deployments()
                return jsonify(deployments)

            except Exception as e:
                logger.exception("Error getting deployments")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/infrastructure', methods=['GET'])
        def get_infrastructure():
            """Get infrastructure metrics and status"""
            try:
                infrastructure = self.infrastructure_monitor.collect_metrics()
                return jsonify(infrastructure)

            except Exception as e:
                logger.exception("Error getting infrastructure data")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/costs', methods=['GET'])
        def get_costs():
            """Get cost analysis and optimization recommendations"""
            try:
                costs = self.cost_optimizer.analyze_and_optimize()
                return jsonify(costs)

            except Exception as e:
                logger.exception("Error getting cost data")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/alerts', methods=['GET'])
        def get_alerts():
            """Get alert summary and recent alerts"""
            try:
                alert_summary = self.alert_processor.get_alert_summary()
                return jsonify(alert_summary)

            except Exception as e:
                logger.exception("Error getting alerts")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/alerts', methods=['POST'])
        def create_alert():
            """Create a new alert"""
            try:
                alert_data = request.get_json()

                if not alert_data:
                    return jsonify({'error': 'No alert data provided'}), 400

                alert = self.alert_processor.process_alert(alert_data)

                if alert:
                    notification_result = self.alert_processor.notify_alert(alert)

                    return jsonify({
                        'alert_id': alert.id,
                        'status': 'processed',
                        'notifications': notification_result
                    })
                else:
                    return jsonify({
                        'status': 'deduplicated',
                        'message': 'Alert was deduplicated or failed to process'
                    })

            except Exception as e:
                logger.exception("Error creating alert")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/metrics/system', methods=['GET'])
        def get_system_metrics():
            """Get detailed system metrics"""
            try:
                metrics = self.infrastructure_monitor.collect_system_metrics()

                if metrics:
                    return jsonify({
                        'timestamp': metrics.timestamp.isoformat(),
                        'cpu_percent': metrics.cpu_percent,
                        'memory_percent': metrics.memory_percent,
                        'disk_percent': metrics.disk_percent,
                        'network_io': metrics.network_io,
                        'process_count': metrics.process_count,
                        'load_average': metrics.load_average
                    })
                else:
                    return jsonify({'error': 'Failed to collect system metrics'}), 500

            except Exception as e:
                logger.exception("Error getting system metrics")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/optimization/recommendations', methods=['GET'])
        def get_optimization_recommendations():
            """Get cost optimization recommendations"""
            try:
                optimization_report = self.cost_optimizer.analyze_and_optimize()

                return jsonify({
                    'recommendations': optimization_report.get('recommendations', []),
                    'business_impact': optimization_report.get('business_impact', {}),
                    'timestamp': optimization_report.get('timestamp')
                })

            except Exception as e:
                logger.exception("Error getting optimization recommendations")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/api/automation/status', methods=['GET'])
        def get_automation_status():
            """Get status of all automation modules"""
            try:
                status = {
                    'timestamp': datetime.now().isoformat(),
                    'modules': {
                        'deployment_monitor': {
                            'status': 'active',
                            'last_check': self.deployment_monitor.last_check.isoformat() if self.deployment_monitor.last_check else None,
                            'cached_deployments': len(self.deployment_monitor.deployments_cache) if self.deployment_monitor.deployments_cache else 0
                        },
                        'infrastructure_monitor': {
                            'status': 'active',
                            'metrics_history_count': len(self.infrastructure_monitor.metrics_history),
                            'docker_available': self.infrastructure_monitor.docker_client is not None,
                            'kubernetes_available': self.infrastructure_monitor.k8s_core_v1 is not None
                        },
                        'cost_optimizer': {
                            'status': 'active',
                            'cached_recommendations': len(self.cost_optimizer.recommendations_cache),
                            'aws_available': self.cost_optimizer.aws_ce_client is not None
                        },
                        'alert_processor': {
                            'status': 'active',
                            'active_alerts': len(self.alert_processor.active_alerts),
                            'total_processed': len(self.alert_processor.alert_history),
                            'notification_channels': len(self.alert_processor.notification_channels)
                        }
                    },
                    'cache_status': {
                        'last_updated': self.data_cache.get('last_updated', datetime.now()).isoformat(),
                        'cached_data_types': list(self.data_cache.keys())
                    }
                }

                return jsonify(status)

            except Exception as e:
                logger.exception("Error getting automation status")
                return jsonify({'error': str(e)}), 500

        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Endpoint not found'}), 404

        @self.app.errorhandler(Exception)
        def handle_unexpected(e):
            logger.exception("Unhandled error in request")
            return jsonify({"error": "Internal server error"}), 500

    def _get_system_uptime(self):
        """Get system uptime information"""
        try:
            import psutil
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time

            return {
                'boot_time': boot_time.isoformat(),
                'uptime_seconds': int(uptime.total_seconds()),
                'uptime_human': str(uptime).split('.')[0]
            }
        except Exception:
            return {
                'boot_time': None,
                'uptime_seconds': 0,
                'uptime_human': 'Unknown'
            }

    def _start_background_tasks(self):
        """Start background tasks for data collection"""
        def background_data_collector():
            """Background thread to collect data periodically"""
            while True:
                try:
                    logger.info("Collecting background data...")

                    self.data_cache['deployments'] = self.deployment_monitor.check_deployments()
                    self.data_cache['infrastructure'] = self.infrastructure_monitor.collect_metrics()
                    self.data_cache['costs'] = self.cost_optimizer.analyze_and_optimize()
                    self.data_cache['alerts'] = self.alert_processor.get_alert_summary()
                    self.data_cache['last_updated'] = datetime.now()

                    logger.info("Background data collection completed")

                except Exception:
                    logger.exception("Error in background data collection")

                time.sleep(300)

        background_thread = threading.Thread(target=background_data_collector, daemon=True)
        background_thread.start()
        logger.info("Background data collection thread started")

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the Flask application"""
        logger.info(f"Starting DevOps Automation Hub API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

def create_app(deployment_monitor=None, infrastructure_monitor=None, cost_optimizer=None, alert_processor=None):
    """Factory function to create Flask app"""
    api = DevOpsAPI(deployment_monitor, infrastructure_monitor, cost_optimizer, alert_processor)
    return api.app

if __name__ == '__main__':
    api = DevOpsAPI()
    api.run(debug=False)
