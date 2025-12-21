# Build Documentation for Agent Zero (Cog-Zero)

This document describes the build process, GitHub Actions workflow, and deployment procedures for the Agent Zero with OpenCog integration (Cog-Zero).

## Overview

The repository includes a comprehensive GitHub Actions workflow that:

1. **Validates** repository structure and Python syntax
2. **Tests** Python environment and OpenCog integration
3. **Builds** Docker images for both Standard and Hacking editions
4. **Tests** Docker containers for functionality
5. **Pushes** images to Docker Hub (on main branches)

## GitHub Actions Workflow

The main build workflow is defined in `.github/workflows/build.yml`.

### Workflow Triggers

The workflow runs on:

- **Push** to branches: `main`, `hacking`, `development`, `testing`
- **Pull requests** to `main` and `hacking` branches
- **Manual dispatch** with optional Docker Hub push

### Jobs Overview

#### 1. Validate Structure

Validates that all required files are present and have correct syntax:

- `requirements.txt` with all dependencies
- Docker build files (`Dockerfile`, `DockerfileKali`)
- Core Python files (`agent.py`, `models.py`, etc.)
- OpenCog integration files
- Python syntax validation

#### 2. Test Python Environment

Sets up Python 3.11 and tests:

- Installation of all dependencies from `requirements.txt`
- OpenCog AtomSpace functionality
- Critical package imports
- Pattern matching and cognitive operations

#### 3. Build Standard Edition

Builds Docker images for `development` and `testing` branches:

- Uses Docker Buildx for multi-platform support
- Builds for `linux/amd64` (testing phase)
- Tests container startup and basic functionality
- Exports images as artifacts

#### 4. Build Hacking Edition

Builds the Kali Linux-based hacking edition:

- Uses `DockerfileKali`
- Includes cybersecurity tools
- Tests container startup
- Exports image as artifact

#### 5. Push to Registry

Conditionally pushes images to Docker Hub:

- Only runs on main branch pushes or manual dispatch
- Builds multi-platform images (`linux/amd64`, `linux/arm64`)
- Tags appropriately based on branch
- Requires Docker Hub credentials in secrets

#### 6. Build Summary

Generates a summary report showing:

- Status of all jobs
- OpenCog integration confirmation
- Overall build success/failure

## Local Development

### Prerequisites

- Docker with Buildx support
- Python 3.11+
- Git

### Running Tests Locally

```bash
# Clone the repository
git clone https://github.com/cogpy/agent-zero-hck.git
cd agent-zero-hck

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run OpenCog tests
python test_opencog.py
```

### Building Docker Images Locally

#### Standard Edition

```bash
cd docker/run

# Build for local testing
docker build \
  -t agent-zero-run:local \
  --build-arg BRANCH=development \
  --build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S) \
  .

# Run locally
docker run -p 50080:80 agent-zero-run:local
```

#### Hacking Edition

```bash
cd docker/run

# Build Kali-based image
docker build \
  -f DockerfileKali \
  -t agent-zero-run:hacking \
  --build-arg BRANCH=hacking \
  --build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S) \
  .

# Run locally
docker run -p 50080:80 agent-zero-run:hacking
```

#### Multi-Platform Build

```bash
cd docker/run

# Create and use buildx builder
docker buildx create --name multiplatform --use

# Build for multiple platforms
docker buildx build \
  --build-arg BRANCH=development \
  --build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S) \
  --platform linux/amd64,linux/arm64 \
  -t cogpy/agent-zero-run:development \
  --push \
  .
```

## GitHub Secrets Configuration

To enable Docker Hub pushing, configure these secrets in your repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub access token

## Branch Strategy

### Main Branches

- **`main`**: Production releases, tagged as `latest`
- **`hacking`**: Kali Linux-based hacking edition
- **`development`**: Active development, tagged as `development`
- **`testing`**: Testing builds, tagged as `testing`

### Build Behavior by Branch

| Branch | Docker Tag | Multi-Platform | Auto-Push |
|--------|-----------|----------------|-----------|
| `main` | `latest` | Yes | Yes |
| `hacking` | `hacking` | Yes | Yes |
| `development` | `development` | Yes | Yes |
| `testing` | `testing` | Yes | Yes |
| PR branches | N/A | No | No |

## OpenCog Integration

The build process ensures OpenCog cognitive architecture is properly integrated:

### Required Dependencies

- `networkx==3.2.1` - Graph operations for hypergraph structure
- `hyperon==0.2.8` - Symbolic reasoning extensions

### Validated Components

- **AtomSpace**: Hypergraph-based knowledge representation
- **Cognitive Orchestrator**: Multi-agent coordination
- **Pattern Matching**: Advanced query capabilities
- **Attention Allocation**: Resource management
- **Adaptive Evolution**: Dynamic knowledge structures

### Test Coverage

The `test_opencog.py` suite validates:

1. AtomSpace creation and management
2. Node and link operations
3. Pattern matching with wildcards
4. Attention spreading mechanisms
5. Statistics generation
6. Export/import functionality
7. Multi-agent orchestration
8. Global orchestrator singleton

## Troubleshooting

### Build Failures

**Problem**: Docker build fails with "BRANCH is not set"

**Solution**: Ensure `--build-arg BRANCH=<branch_name>` is provided

---

**Problem**: Python dependency installation fails

**Solution**: Check `requirements.txt` for version conflicts, update as needed

---

**Problem**: Container fails to start

**Solution**: Check logs with `docker logs <container_id>` and verify all installation scripts completed

### Test Failures

**Problem**: OpenCog tests fail with import errors

**Solution**: Ensure `networkx` is installed: `pip install networkx==3.2.1`

---

**Problem**: Pattern matching tests fail

**Solution**: Verify AtomSpace implementation in `python/helpers/opencog_atomspace.py`

## Continuous Integration Best Practices

1. **Always run tests locally** before pushing
2. **Use feature branches** for development
3. **Create pull requests** for review before merging to main
4. **Monitor GitHub Actions** for build status
5. **Review build logs** for warnings or errors
6. **Test Docker images** locally before deploying

## Docker Image Artifacts

Build artifacts are stored for 7 days and include:

- `agent-zero-development-image` - Development edition
- `agent-zero-testing-image` - Testing edition
- `agent-zero-hacking-image` - Hacking edition

Download artifacts from the Actions tab to test specific builds.

## Performance Optimization

### Build Cache

The workflow uses Docker layer caching to speed up builds:

- Base system packages are cached
- Python dependencies are cached
- Only changed layers are rebuilt

### Cache Busting

The `CACHE_DATE` argument forces reinstallation of Agent Zero code:

```bash
--build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S)
```

This ensures the latest code is always pulled from the repository.

## Contributing

When contributing to the build system:

1. Test changes locally first
2. Update this documentation for any workflow changes
3. Ensure all tests pass
4. Maintain backward compatibility
5. Document new build arguments or secrets

## Support

For build-related issues:

1. Check GitHub Actions logs
2. Review this documentation
3. Open an issue on GitHub
4. Contact the maintainers

## Version History

- **v1.0** - Initial GitHub Actions workflow
  - Multi-platform Docker builds
  - OpenCog integration testing
  - Automated Docker Hub deployment
  - Comprehensive validation and testing

## License

Same as Agent Zero - see [LICENSE](./LICENSE)
