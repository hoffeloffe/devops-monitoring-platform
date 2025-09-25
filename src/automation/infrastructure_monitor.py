"""
Infrastructure Monitor - Automated System Health Monitoring

This module demonstrates advanced RPA skills by automating infrastructure
monitoring tasks across multiple platforms and services.
"""

import psutil
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from dataclasses import dataclass
import docker
from kubernetes import client, config

@dataclass
class SystemMetrics:
    """Data class for system metrics"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict
    process_count: int
    load_average: List[float]

@dataclass
class ServiceHealth:
    """Data class for service health status"""
    name: str
    status: str
    response_time: float
    last_check: datetime
    error_message: Optional[str] = None

class InfrastructureMonitor:
    """
    Comprehensive infrastructure monitoring system.
    
    This class showcases enterprise automation capabilities:
    - Multi-platform monitoring (local, Docker, Kubernetes)
    - Performance metrics collection
    - Health check automation
    - Anomaly detection
    - Auto-healing capabilities
    """
    
    def __init__(self):
        self.metrics_history = []
        self.services_to_monitor = []
        self.alert_thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'response_time': 5.0
        }
        
        # Initialize Docker client
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize Docker client: {e}")
            self.docker_client = None
        
        # Initialize Kubernetes client
        try:
            try:
                config.load_incluster_config()
            except:
                config.load_kube_config()
            self.k8s_core_v1 = client.CoreV1Api()
            self.k8s_metrics = client.CustomObjectsApi()
            logger.info("Kubernetes client initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize Kubernetes client: {e}")
            self.k8s_core_v1 = None
            self.k8s_metrics = None
    
    def collect_system_metrics(self) -> SystemMetrics:
        """
        Collect comprehensive system metrics.
        
        Demonstrates system monitoring and performance analysis skills.
        """
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Process count
            process_count = len(psutil.pids())
            
            # Load average (Unix-like systems)
            try:
                load_average = list(psutil.getloadavg())
            except AttributeError:
                # Windows doesn't have load average
                load_average = [0.0, 0.0, 0.0]
            
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_io,
                process_count=process_count,
                load_average=load_average
            )
            
            # Store in history for trend analysis
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 entries
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            logger.info(f"System metrics collected - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent}%")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return None
    
    def monitor_docker_containers(self) -> List[Dict]:
        """
        Monitor Docker container health and performance.
        
        Demonstrates containerization monitoring skills.
        """
        if not self.docker_client:
            return []
        
        containers_status = []
        
        try:
            containers = self.docker_client.containers.list(all=True)
            
            for container in containers:
                try:
                    # Get container stats
                    stats = container.stats(stream=False)
                    
                    # Calculate CPU percentage
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                               stats['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                                  stats['precpu_stats']['system_cpu_usage']
                    
                    cpu_percent = 0.0
                    if system_delta > 0:
                        cpu_percent = (cpu_delta / system_delta) * 100.0
                    
                    # Calculate memory usage
                    memory_usage = stats['memory_stats'].get('usage', 0)
                    memory_limit = stats['memory_stats'].get('limit', 0)
                    memory_percent = 0.0
                    if memory_limit > 0:
                        memory_percent = (memory_usage / memory_limit) * 100.0
                    
                    container_info = {
                        'name': container.name,
                        'id': container.short_id,
                        'status': container.status,
                        'image': container.image.tags[0] if container.image.tags else 'unknown',
                        'cpu_percent': round(cpu_percent, 2),
                        'memory_percent': round(memory_percent, 2),
                        'memory_usage_mb': round(memory_usage / 1024 / 1024, 2),
                        'created': container.attrs['Created'],
                        'ports': container.ports
                    }
                    
                    containers_status.append(container_info)
                    
                except Exception as e:
                    logger.warning(f"Error getting stats for container {container.name}: {e}")
                    containers_status.append({
                        'name': container.name,
                        'id': container.short_id,
                        'status': container.status,
                        'error': str(e)
                    })
            
            logger.info(f"Monitored {len(containers_status)} Docker containers")
            
        except Exception as e:
            logger.error(f"Error monitoring Docker containers: {e}")
        
        return containers_status
    
    def monitor_kubernetes_nodes(self) -> List[Dict]:
        """
        Monitor Kubernetes node health and resource usage.
        
        Demonstrates Kubernetes monitoring and troubleshooting skills.
        """
        if not self.k8s_core_v1:
            return []
        
        nodes_status = []
        
        try:
            nodes = self.k8s_core_v1.list_node()
            
            for node in nodes.items:
                node_info = {
                    'name': node.metadata.name,
                    'status': 'Unknown',
                    'roles': [],
                    'version': node.status.node_info.kubelet_version,
                    'os': f"{node.status.node_info.os_image}",
                    'kernel': node.status.node_info.kernel_version,
                    'container_runtime': node.status.node_info.container_runtime_version,
                    'conditions': [],
                    'capacity': {},
                    'allocatable': {}
                }
                
                # Get node status from conditions
                if node.status.conditions:
                    for condition in node.status.conditions:
                        if condition.type == 'Ready':
                            node_info['status'] = 'Ready' if condition.status == 'True' else 'NotReady'
                        
                        node_info['conditions'].append({
                            'type': condition.type,
                            'status': condition.status,
                            'reason': condition.reason,
                            'message': condition.message
                        })
                
                # Get node roles from labels
                if node.metadata.labels:
                    for label, value in node.metadata.labels.items():
                        if 'node-role.kubernetes.io' in label:
                            role = label.split('/')[-1]
                            node_info['roles'].append(role)
                
                # Get resource capacity and allocatable
                if node.status.capacity:
                    node_info['capacity'] = dict(node.status.capacity)
                if node.status.allocatable:
                    node_info['allocatable'] = dict(node.status.allocatable)
                
                nodes_status.append(node_info)
            
            logger.info(f"Monitored {len(nodes_status)} Kubernetes nodes")
            
        except Exception as e:
            logger.error(f"Error monitoring Kubernetes nodes: {e}")
        
        return nodes_status
    
    def check_service_health(self, services: List[Dict]) -> List[ServiceHealth]:
        """
        Check health of web services and APIs.
        
        Demonstrates service monitoring and availability checking.
        """
        health_results = []
        
        for service in services:
            try:
                start_time = time.time()
                
                response = requests.get(
                    service['url'],
                    timeout=service.get('timeout', 10),
                    headers=service.get('headers', {})
                )
                
                response_time = time.time() - start_time
                
                health = ServiceHealth(
                    name=service['name'],
                    status='Healthy' if response.status_code == 200 else f'Error {response.status_code}',
                    response_time=response_time,
                    last_check=datetime.now()
                )
                
                if response.status_code != 200:
                    health.error_message = f"HTTP {response.status_code}: {response.text[:200]}"
                
            except requests.exceptions.Timeout:
                health = ServiceHealth(
                    name=service['name'],
                    status='Timeout',
                    response_time=service.get('timeout', 10),
                    last_check=datetime.now(),
                    error_message='Request timed out'
                )
            
            except Exception as e:
                health = ServiceHealth(
                    name=service['name'],
                    status='Error',
                    response_time=0.0,
                    last_check=datetime.now(),
                    error_message=str(e)
                )
            
            health_results.append(health)
        
        logger.info(f"Health checked {len(health_results)} services")
        return health_results
    
    def detect_anomalies(self, current_metrics: SystemMetrics) -> List[Dict]:
        """
        Detect performance anomalies using simple threshold-based rules.
        
        This demonstrates basic anomaly detection - can be enhanced with ML later.
        """
        anomalies = []
        
        # CPU anomaly detection
        if current_metrics.cpu_percent > self.alert_thresholds['cpu_percent']:
            anomalies.append({
                'type': 'cpu_high',
                'severity': 'warning' if current_metrics.cpu_percent < 95 else 'critical',
                'message': f"High CPU usage: {current_metrics.cpu_percent}%",
                'value': current_metrics.cpu_percent,
                'threshold': self.alert_thresholds['cpu_percent']
            })
        
        # Memory anomaly detection
        if current_metrics.memory_percent > self.alert_thresholds['memory_percent']:
            anomalies.append({
                'type': 'memory_high',
                'severity': 'warning' if current_metrics.memory_percent < 95 else 'critical',
                'message': f"High memory usage: {current_metrics.memory_percent}%",
                'value': current_metrics.memory_percent,
                'threshold': self.alert_thresholds['memory_percent']
            })
        
        # Disk anomaly detection
        if current_metrics.disk_percent > self.alert_thresholds['disk_percent']:
            anomalies.append({
                'type': 'disk_high',
                'severity': 'critical',
                'message': f"High disk usage: {current_metrics.disk_percent}%",
                'value': current_metrics.disk_percent,
                'threshold': self.alert_thresholds['disk_percent']
            })
        
        if anomalies:
            logger.warning(f"Detected {len(anomalies)} anomalies")
        
        return anomalies
    
    def collect_metrics(self) -> Dict:
        """
        Main method to collect all infrastructure metrics.
        
        This orchestrates all monitoring activities and returns a comprehensive report.
        """
        logger.info("Starting infrastructure monitoring cycle")
        
        # Collect system metrics
        system_metrics = self.collect_system_metrics()
        
        # Monitor Docker containers
        docker_containers = self.monitor_docker_containers()
        
        # Monitor Kubernetes nodes
        k8s_nodes = self.monitor_kubernetes_nodes()
        
        # Check service health (example services)
        example_services = [
            {'name': 'Google', 'url': 'https://www.google.com'},
            {'name': 'GitHub', 'url': 'https://api.github.com'},
        ]
        service_health = self.check_service_health(example_services)
        
        # Detect anomalies
        anomalies = []
        if system_metrics:
            anomalies = self.detect_anomalies(system_metrics)
        
        # Compile comprehensive report
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_metrics': {
                'cpu_percent': system_metrics.cpu_percent if system_metrics else 0,
                'memory_percent': system_metrics.memory_percent if system_metrics else 0,
                'disk_percent': system_metrics.disk_percent if system_metrics else 0,
                'process_count': system_metrics.process_count if system_metrics else 0,
                'load_average': system_metrics.load_average if system_metrics else [0, 0, 0]
            },
            'docker_containers': docker_containers,
            'kubernetes_nodes': k8s_nodes,
            'service_health': [
                {
                    'name': s.name,
                    'status': s.status,
                    'response_time': s.response_time,
                    'error_message': s.error_message
                }
                for s in service_health
            ],
            'anomalies': anomalies,
            'summary': {
                'total_containers': len(docker_containers),
                'healthy_containers': len([c for c in docker_containers if c.get('status') == 'running']),
                'total_nodes': len(k8s_nodes),
                'ready_nodes': len([n for n in k8s_nodes if n.get('status') == 'Ready']),
                'healthy_services': len([s for s in service_health if s.status == 'Healthy']),
                'total_anomalies': len(anomalies)
            }
        }
        
        logger.info(f"Infrastructure monitoring completed. Anomalies: {len(anomalies)}")
        
        return report
