"""
Deployment Monitor - Automated CI/CD Pipeline Monitoring

This module demonstrates RPA skills by automating deployment monitoring tasks
that would typically require manual checking across multiple platforms.
"""

import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from kubernetes import client, config
from dataclasses import dataclass

@dataclass
class DeploymentStatus:
    """Data class for deployment status information"""
    name: str
    namespace: str
    status: str
    replicas: int
    ready_replicas: int
    timestamp: datetime
    issues: List[str]

class DeploymentMonitor:
    """
    Automated deployment monitoring system.
    
    This class showcases enterprise automation skills:
    - Kubernetes API integration
    - Automated health checking
    - Issue detection and reporting
    - Clean, maintainable code structure
    """
    
    def __init__(self):
        self.deployments_cache = {}
        self.last_check = None
        
        # Initialize Kubernetes client
        try:
            # Try to load in-cluster config first, then local config
            try:
                config.load_incluster_config()
                logger.info("Loaded in-cluster Kubernetes configuration")
            except:
                config.load_kube_config()
                logger.info("Loaded local Kubernetes configuration")
                
            self.k8s_apps_v1 = client.AppsV1Api()
            self.k8s_core_v1 = client.CoreV1Api()
            
        except Exception as e:
            logger.warning(f"Could not initialize Kubernetes client: {e}")
            self.k8s_apps_v1 = None
            self.k8s_core_v1 = None
    
    def check_kubernetes_deployments(self) -> List[DeploymentStatus]:
        """
        Check all Kubernetes deployments across namespaces.
        
        This demonstrates:
        - API integration skills
        - Error handling
        - Data processing
        """
        if not self.k8s_apps_v1:
            logger.warning("Kubernetes client not available")
            return []
        
        deployments = []
        
        try:
            # Get all namespaces
            namespaces = self.k8s_core_v1.list_namespace()
            
            for namespace in namespaces.items:
                ns_name = namespace.metadata.name
                
                # Skip system namespaces for demo purposes
                if ns_name.startswith(('kube-', 'default')):
                    continue
                
                # Get deployments in this namespace
                deps = self.k8s_apps_v1.list_namespaced_deployment(namespace=ns_name)
                
                for dep in deps.items:
                    issues = []
                    
                    # Check for common issues
                    if dep.status.replicas != dep.status.ready_replicas:
                        issues.append(f"Not all replicas ready: {dep.status.ready_replicas}/{dep.status.replicas}")
                    
                    if dep.status.unavailable_replicas and dep.status.unavailable_replicas > 0:
                        issues.append(f"{dep.status.unavailable_replicas} replicas unavailable")
                    
                    # Check if deployment is stuck
                    for condition in dep.status.conditions or []:
                        if condition.type == "Progressing" and condition.status == "False":
                            issues.append(f"Deployment stuck: {condition.reason}")
                    
                    deployment_status = DeploymentStatus(
                        name=dep.metadata.name,
                        namespace=ns_name,
                        status="Healthy" if not issues else "Issues Detected",
                        replicas=dep.status.replicas or 0,
                        ready_replicas=dep.status.ready_replicas or 0,
                        timestamp=datetime.now(),
                        issues=issues
                    )
                    
                    deployments.append(deployment_status)
            
            logger.info(f"Checked {len(deployments)} deployments across {len(namespaces.items)} namespaces")
            
        except Exception as e:
            logger.error(f"Error checking Kubernetes deployments: {e}")
        
        return deployments
    
    def check_github_actions(self) -> Dict:
        """
        Check GitHub Actions workflow status.
        
        This would integrate with GitHub API to monitor CI/CD pipelines.
        Demonstrates API integration and webhook processing skills.
        """
        # Placeholder for GitHub Actions integration
        # In a real implementation, this would:
        # 1. Connect to GitHub API
        # 2. Check workflow runs
        # 3. Identify failed builds
        # 4. Generate reports
        
        return {
            "status": "placeholder",
            "message": "GitHub Actions integration - coming in Phase 2",
            "workflows_checked": 0,
            "failed_workflows": []
        }
    
    def check_jenkins_jobs(self) -> Dict:
        """
        Check Jenkins job status.
        
        Demonstrates integration with popular CI/CD tools.
        """
        # Placeholder for Jenkins integration
        return {
            "status": "placeholder",
            "message": "Jenkins integration - coming in Phase 2",
            "jobs_checked": 0,
            "failed_jobs": []
        }
    
    def generate_deployment_report(self, deployments: List[DeploymentStatus]) -> Dict:
        """Generate a comprehensive deployment status report"""
        total_deployments = len(deployments)
        healthy_deployments = len([d for d in deployments if d.status == "Healthy"])
        problematic_deployments = total_deployments - healthy_deployments
        
        # Calculate uptime percentage
        uptime_percentage = (healthy_deployments / total_deployments * 100) if total_deployments > 0 else 100
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_deployments": total_deployments,
                "healthy_deployments": healthy_deployments,
                "problematic_deployments": problematic_deployments,
                "uptime_percentage": round(uptime_percentage, 2)
            },
            "deployments": [
                {
                    "name": d.name,
                    "namespace": d.namespace,
                    "status": d.status,
                    "replicas": f"{d.ready_replicas}/{d.replicas}",
                    "issues": d.issues
                }
                for d in deployments
            ]
        }
        
        return report
    
    def check_deployments(self) -> Dict:
        """
        Main method to check all deployment sources.
        
        This orchestrates all deployment checks and generates a unified report.
        Perfect for demonstrating system integration skills.
        """
        logger.info("Starting deployment monitoring cycle")
        
        # Check Kubernetes deployments
        k8s_deployments = self.check_kubernetes_deployments()
        
        # Check other CI/CD systems (placeholders for now)
        github_status = self.check_github_actions()
        jenkins_status = self.check_jenkins_jobs()
        
        # Generate comprehensive report
        report = self.generate_deployment_report(k8s_deployments)
        
        # Add other system statuses
        report["integrations"] = {
            "github_actions": github_status,
            "jenkins": jenkins_status
        }
        
        # Cache results
        self.deployments_cache = report
        self.last_check = datetime.now()
        
        logger.info(f"Deployment monitoring completed. Status: {report['summary']['uptime_percentage']}% uptime")
        
        return report
    
    def get_cached_status(self) -> Optional[Dict]:
        """Get the last cached deployment status"""
        return self.deployments_cache if self.deployments_cache else None
