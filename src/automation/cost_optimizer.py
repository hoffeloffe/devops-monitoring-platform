"""
Cost Optimizer - Automated Cloud Cost Management

This module demonstrates advanced RPA and business intelligence skills
by automating cloud cost analysis and optimization recommendations.
"""

import boto3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
from dataclasses import dataclass
import json

@dataclass
class CostRecommendation:
    """Data class for cost optimization recommendations"""
    resource_type: str
    resource_id: str
    current_cost: float
    potential_savings: float
    recommendation: str
    confidence: str
    implementation_effort: str

@dataclass
class ResourceUsage:
    """Data class for resource usage metrics"""
    resource_id: str
    resource_type: str
    avg_cpu_utilization: float
    avg_memory_utilization: float
    avg_network_utilization: float
    cost_per_hour: float
    usage_pattern: str

class CostOptimizer:
    """
    Intelligent cloud cost optimization system.
    
    This class demonstrates enterprise-level automation skills:
    - Multi-cloud cost analysis (AWS, Azure, GCP)
    - Resource utilization monitoring
    - Automated optimization recommendations
    - ROI calculations and business impact analysis
    - Integration with cloud billing APIs
    """
    
    def __init__(self):
        self.cost_history = []
        self.recommendations_cache = []
        self.optimization_rules = self._load_optimization_rules()
        
        # Initialize cloud clients
        self._init_aws_client()
        self._init_azure_client()
        
    def _init_aws_client(self):
        """Initialize AWS clients for cost analysis"""
        try:
            self.aws_ce_client = boto3.client('ce')  # Cost Explorer
            self.aws_ec2_client = boto3.client('ec2')
            self.aws_cloudwatch = boto3.client('cloudwatch')
            logger.info("AWS clients initialized successfully")
        except Exception as e:
            logger.warning(f"Could not initialize AWS clients: {e}")
            self.aws_ce_client = None
            self.aws_ec2_client = None
            self.aws_cloudwatch = None
    
    def _init_azure_client(self):
        """Initialize Azure clients for cost analysis"""
        try:
            # Azure SDK initialization would go here
            # For demo purposes, we'll use placeholder
            self.azure_client = None
            logger.info("Azure client initialization - placeholder")
        except Exception as e:
            logger.warning(f"Could not initialize Azure client: {e}")
            self.azure_client = None
    
    def _load_optimization_rules(self) -> Dict:
        """Load cost optimization rules and thresholds"""
        return {
            'cpu_utilization_threshold': 20.0,  # Below 20% is underutilized
            'memory_utilization_threshold': 30.0,  # Below 30% is underutilized
            'idle_threshold_hours': 168,  # 1 week of idle time
            'right_sizing_threshold': 0.5,  # 50% utilization for right-sizing
            'reserved_instance_threshold': 0.7,  # 70% consistent usage for RI
            'spot_instance_threshold': 0.3,  # 30% utilization for spot instances
        }
    
    def analyze_aws_costs(self) -> Dict:
        """
        Analyze AWS costs and usage patterns.
        
        Demonstrates cloud cost management and API integration skills.
        """
        if not self.aws_ce_client:
            return self._generate_mock_aws_analysis()
        
        try:
            # Get cost and usage for last 30 days
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=30)
            
            response = self.aws_ce_client.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost', 'UsageQuantity'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                ]
            )
            
            # Process cost data
            total_cost = 0
            service_costs = {}
            
            for result in response['ResultsByTime']:
                for group in result['Groups']:
                    service = group['Keys'][0]
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    
                    if service not in service_costs:
                        service_costs[service] = 0
                    service_costs[service] += cost
                    total_cost += cost
            
            # Get top spending services
            top_services = sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:10]
            
            analysis = {
                'total_monthly_cost': round(total_cost, 2),
                'top_services': [
                    {'service': service, 'cost': round(cost, 2), 'percentage': round((cost/total_cost)*100, 1)}
                    for service, cost in top_services
                ],
                'cost_trend': 'stable',  # Would calculate actual trend
                'last_updated': datetime.now().isoformat()
            }
            
            logger.info(f"AWS cost analysis completed. Total monthly cost: ${total_cost:.2f}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing AWS costs: {e}")
            return self._generate_mock_aws_analysis()
    
    def _generate_mock_aws_analysis(self) -> Dict:
        """Generate mock AWS cost analysis for demo purposes"""
        return {
            'total_monthly_cost': 2847.32,
            'top_services': [
                {'service': 'Amazon Elastic Compute Cloud - Compute', 'cost': 1245.67, 'percentage': 43.7},
                {'service': 'Amazon Relational Database Service', 'cost': 456.78, 'percentage': 16.0},
                {'service': 'Amazon Simple Storage Service', 'cost': 234.56, 'percentage': 8.2},
                {'service': 'Amazon Elastic Load Balancing', 'cost': 123.45, 'percentage': 4.3},
                {'service': 'Amazon CloudWatch', 'cost': 89.12, 'percentage': 3.1}
            ],
            'cost_trend': 'increasing',
            'last_updated': datetime.now().isoformat(),
            'note': 'Mock data for demonstration'
        }
    
    def analyze_resource_utilization(self) -> List[ResourceUsage]:
        """
        Analyze resource utilization patterns for optimization.
        
        Demonstrates performance monitoring and data analysis skills.
        """
        # In a real implementation, this would:
        # 1. Query CloudWatch metrics for EC2 instances
        # 2. Analyze CPU, memory, network utilization
        # 3. Identify usage patterns and trends
        # 4. Calculate cost per resource
        
        # Mock data for demonstration
        mock_resources = [
            ResourceUsage(
                resource_id='i-0123456789abcdef0',
                resource_type='EC2 Instance (t3.large)',
                avg_cpu_utilization=15.2,
                avg_memory_utilization=25.8,
                avg_network_utilization=5.3,
                cost_per_hour=0.0832,
                usage_pattern='low_consistent'
            ),
            ResourceUsage(
                resource_id='i-0987654321fedcba0',
                resource_type='EC2 Instance (m5.xlarge)',
                avg_cpu_utilization=78.5,
                avg_memory_utilization=82.1,
                avg_network_utilization=45.7,
                usage_pattern='high_consistent',
                cost_per_hour=0.192
            ),
            ResourceUsage(
                resource_id='i-0abcdef123456789',
                resource_type='EC2 Instance (c5.2xlarge)',
                avg_cpu_utilization=35.4,
                avg_memory_utilization=28.9,
                avg_network_utilization=12.1,
                usage_pattern='variable',
                cost_per_hour=0.34
            )
        ]
        
        logger.info(f"Analyzed utilization for {len(mock_resources)} resources")
        return mock_resources
    
    def generate_cost_recommendations(self, resources: List[ResourceUsage]) -> List[CostRecommendation]:
        """
        Generate intelligent cost optimization recommendations.
        
        This demonstrates business intelligence and decision-making automation.
        """
        recommendations = []
        
        for resource in resources:
            # Right-sizing recommendations
            if (resource.avg_cpu_utilization < self.optimization_rules['cpu_utilization_threshold'] and
                resource.avg_memory_utilization < self.optimization_rules['memory_utilization_threshold']):
                
                # Calculate potential savings (assume 50% cost reduction with smaller instance)
                monthly_savings = resource.cost_per_hour * 24 * 30 * 0.5
                
                recommendations.append(CostRecommendation(
                    resource_type=resource.resource_type,
                    resource_id=resource.resource_id,
                    current_cost=resource.cost_per_hour * 24 * 30,
                    potential_savings=monthly_savings,
                    recommendation=f"Right-size to smaller instance type (CPU: {resource.avg_cpu_utilization}%, Memory: {resource.avg_memory_utilization}%)",
                    confidence="High",
                    implementation_effort="Medium"
                ))
            
            # Reserved Instance recommendations
            elif (resource.usage_pattern == 'high_consistent' and
                  resource.avg_cpu_utilization > self.optimization_rules['reserved_instance_threshold'] * 100):
                
                # Calculate RI savings (typically 30-60% discount)
                monthly_savings = resource.cost_per_hour * 24 * 30 * 0.4
                
                recommendations.append(CostRecommendation(
                    resource_type=resource.resource_type,
                    resource_id=resource.resource_id,
                    current_cost=resource.cost_per_hour * 24 * 30,
                    potential_savings=monthly_savings,
                    recommendation="Purchase Reserved Instance for consistent workload",
                    confidence="High",
                    implementation_effort="Low"
                ))
            
            # Spot Instance recommendations
            elif (resource.usage_pattern == 'variable' and
                  resource.avg_cpu_utilization < self.optimization_rules['spot_instance_threshold'] * 100):
                
                # Calculate spot savings (typically 70-90% discount)
                monthly_savings = resource.cost_per_hour * 24 * 30 * 0.8
                
                recommendations.append(CostRecommendation(
                    resource_type=resource.resource_type,
                    resource_id=resource.resource_id,
                    current_cost=resource.cost_per_hour * 24 * 30,
                    potential_savings=monthly_savings,
                    recommendation="Consider Spot Instances for fault-tolerant workloads",
                    confidence="Medium",
                    implementation_effort="High"
                ))
        
        # Sort by potential savings
        recommendations.sort(key=lambda x: x.potential_savings, reverse=True)
        
        logger.info(f"Generated {len(recommendations)} cost optimization recommendations")
        return recommendations
    
    def calculate_optimization_impact(self, recommendations: List[CostRecommendation]) -> Dict:
        """
        Calculate the business impact of optimization recommendations.
        
        This demonstrates ROI analysis and business value quantification.
        """
        total_current_cost = sum(rec.current_cost for rec in recommendations)
        total_potential_savings = sum(rec.potential_savings for rec in recommendations)
        
        # Calculate annual impact
        annual_savings = total_potential_savings * 12
        
        # Categorize recommendations by confidence
        high_confidence_savings = sum(
            rec.potential_savings for rec in recommendations 
            if rec.confidence == "High"
        )
        
        medium_confidence_savings = sum(
            rec.potential_savings for rec in recommendations 
            if rec.confidence == "Medium"
        )
        
        impact_analysis = {
            'total_monthly_savings': round(total_potential_savings, 2),
            'total_annual_savings': round(annual_savings, 2),
            'savings_percentage': round((total_potential_savings / total_current_cost) * 100, 1) if total_current_cost > 0 else 0,
            'high_confidence_savings': round(high_confidence_savings, 2),
            'medium_confidence_savings': round(medium_confidence_savings, 2),
            'recommendations_count': len(recommendations),
            'implementation_priority': [
                {
                    'resource_id': rec.resource_id,
                    'savings': rec.potential_savings,
                    'effort': rec.implementation_effort,
                    'priority_score': rec.potential_savings / (1 if rec.implementation_effort == 'Low' else 2 if rec.implementation_effort == 'Medium' else 3)
                }
                for rec in recommendations[:5]  # Top 5 recommendations
            ]
        }
        
        return impact_analysis
    
    def analyze_and_optimize(self) -> Dict:
        """
        Main method to perform comprehensive cost analysis and optimization.
        
        This orchestrates the entire cost optimization process.
        """
        logger.info("Starting cost optimization analysis")
        
        # Analyze current costs
        aws_analysis = self.analyze_aws_costs()
        
        # Analyze resource utilization
        resource_utilization = self.analyze_resource_utilization()
        
        # Generate recommendations
        recommendations = self.generate_cost_recommendations(resource_utilization)
        
        # Calculate business impact
        impact_analysis = self.calculate_optimization_impact(recommendations)
        
        # Compile comprehensive report
        optimization_report = {
            'timestamp': datetime.now().isoformat(),
            'current_costs': aws_analysis,
            'resource_analysis': {
                'total_resources_analyzed': len(resource_utilization),
                'underutilized_resources': len([r for r in resource_utilization 
                                              if r.avg_cpu_utilization < 30]),
                'high_utilization_resources': len([r for r in resource_utilization 
                                                 if r.avg_cpu_utilization > 80]),
                'average_cpu_utilization': round(
                    sum(r.avg_cpu_utilization for r in resource_utilization) / len(resource_utilization), 1
                ) if resource_utilization else 0
            },
            'recommendations': [
                {
                    'resource_type': rec.resource_type,
                    'resource_id': rec.resource_id,
                    'current_monthly_cost': round(rec.current_cost, 2),
                    'potential_monthly_savings': round(rec.potential_savings, 2),
                    'recommendation': rec.recommendation,
                    'confidence': rec.confidence,
                    'implementation_effort': rec.implementation_effort
                }
                for rec in recommendations
            ],
            'business_impact': impact_analysis,
            'next_actions': [
                "Review high-confidence recommendations for immediate implementation",
                "Schedule right-sizing activities during maintenance windows",
                "Evaluate Reserved Instance purchasing for consistent workloads",
                "Set up automated monitoring for cost anomalies"
            ]
        }
        
        # Cache recommendations
        self.recommendations_cache = recommendations
        
        total_savings = impact_analysis.get('total_monthly_savings', 0)
        logger.info(f"Cost optimization analysis completed. Potential monthly savings: ${total_savings}")
        
        return optimization_report
