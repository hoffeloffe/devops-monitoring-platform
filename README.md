# DevOps Monitoring Platform

A real-time monitoring dashboard for infrastructure and system health. Built with Python/Flask backend and a clean web interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

## Features

- **Real-time Dashboard** - Live system metrics and health status
- **REST API** - Endpoints for health checks and system data
- **Interactive Charts** - CPU, memory, and service monitoring
- **Docker Ready** - Easy deployment with containers
- **Clean UI** - Professional monitoring interface

## Quick Start

```bash
# Clone the repository
git clone https://github.com/hoffeloffe/devops-monitoring-platform.git
cd devops-monitoring-platform

# Start with Docker
docker-compose up -d

# View the dashboard
open dashboard.html

# Check API health
curl http://localhost:5000/api/health
```

## API Endpoints

- `GET /api/health` - System health check
- `GET /api/dashboard` - Dashboard data  
- `GET /api/metrics/system` - System metrics
- `GET /api/automation/status` - Service status

## Technology Stack

- **Python/Flask** - Backend API
- **HTML/CSS/JavaScript** - Frontend dashboard  
- **Docker** - Containerization
- **PostgreSQL** - Database
- **Redis** - Caching

## License

MIT License - see [LICENSE](LICENSE) file for details.
