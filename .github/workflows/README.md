# GitHub Actions CI/CD Workflow

This directory contains the GitHub Actions workflow for automated build, test, and deployment of Agent-Zero-HCK.

## Workflow: build.yml

The main build workflow provides comprehensive CI/CD automation with the following stages:

### 1. Lint (Code Quality)
- **Black** formatter check for consistent code style
- **Flake8** for Python linting and error detection
- **MyPy** for static type checking

### 2. Test (Unit & Integration)
- Runs pytest test suite with coverage reporting
- Tests all core modules:
  - Personality system
  - Transform Quirk
  - Security testing
  - Agent orchestration
- Generates coverage reports and uploads to Codecov

### 3. Build Package
- Creates Python package using setuptools
- Builds both wheel (.whl) and source distribution (.tar.gz)
- Validates package with twine
- Uploads package artifacts for distribution

### 4. Build Docker
- Builds Docker image with multi-stage optimization
- Tags images appropriately (branch, PR, SHA, latest)
- Pushes to GitHub Container Registry (ghcr.io)
- Uses layer caching for faster builds
- Tests Docker image after build

### 5. Integration Test
- Runs Docker Compose stack
- Validates service health
- Tests agent initialization in containerized environment
- Ensures all components work together

### 6. Deploy
- Triggers only on main branch pushes
- Deploys to production environment
- Makes artifacts available for download

### 7. Summary
- Generates build summary report
- Shows status of all stages
- Provides quick overview of build health

## Triggers

The workflow runs on:
- **Push** to `main` or `develop` branches
- **Pull requests** to `main` or `develop` branches
- **Manual trigger** via workflow_dispatch

## Environment Variables

The workflow uses the following environment variables:

- `PYTHON_VERSION`: Python version (3.11)
- `DOCKER_REGISTRY`: Container registry (ghcr.io)
- `IMAGE_NAME`: Docker image name

## Secrets Required

The workflow requires the following secrets:

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
  - Used for pushing Docker images to GHCR
  - Used for accessing repository

Optional:
- `CODECOV_TOKEN`: For uploading coverage reports to Codecov

## Artifacts

The workflow produces the following artifacts:

1. **Python Package** (`python-package`)
   - Wheel file (.whl)
   - Source distribution (.tar.gz)
   - Available for 90 days

2. **Docker Image**
   - Pushed to `ghcr.io/cogpy/agent-zero-hck`
   - Tagged with branch, SHA, and latest

3. **Coverage Reports**
   - XML format for Codecov
   - Terminal output in logs

## Local Testing

To test the workflow locally before pushing:

### Run Tests
```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/ -v --cov=agents --cov=python
```

### Build Package
```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

### Build Docker Image
```bash
# Build image
docker build -t agent-zero-hck:test .

# Test image
docker run --rm agent-zero-hck:test python3.11 -c "from agents.toga_hck import agent; print('Success')"
```

### Run Docker Compose
```bash
# Start services
docker compose up -d

# Check logs
docker compose logs -f

# Stop services
docker compose down
```

## Troubleshooting

### Lint Failures
- Run `black .` to auto-format code
- Fix flake8 errors manually
- MyPy warnings are informational only

### Test Failures
- Check test logs for specific failures
- Run tests locally to debug
- Ensure all dependencies are installed

### Build Failures
- Verify setup.py is correct
- Check MANIFEST.in includes all necessary files
- Ensure requirements.txt is up to date

### Docker Build Failures
- Check Dockerfile syntax
- Verify base image is available
- Ensure all COPY paths exist

### Integration Test Failures
- Check docker-compose.yml configuration
- Verify environment variables are set
- Check service health endpoints

## Optimization Tips

1. **Faster Builds**
   - Use pip caching (already enabled)
   - Use Docker layer caching (already enabled)
   - Minimize dependency changes

2. **Better Coverage**
   - Add more unit tests
   - Add integration tests
   - Test edge cases

3. **Improved Security**
   - Keep dependencies updated
   - Use Dependabot for automatic updates
   - Scan Docker images for vulnerabilities

## Status Badges

Add these badges to your README.md:

```markdown
[![Build Status](https://github.com/cogpy/agent-zero-hck/workflows/Build,%20Test%20&%20Deploy/badge.svg)](https://github.com/cogpy/agent-zero-hck/actions)
[![codecov](https://codecov.io/gh/cogpy/agent-zero-hck/branch/main/graph/badge.svg)](https://codecov.io/gh/cogpy/agent-zero-hck)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://github.com/cogpy/agent-zero-hck/pkgs/container/agent-zero-hck)
```

## Maintenance

- Review and update workflow quarterly
- Keep GitHub Actions versions updated
- Monitor build times and optimize as needed
- Update Python version as new releases become available
