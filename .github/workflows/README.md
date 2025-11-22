# GitHub Actions Workflows

## build-and-publish.yml

Automated workflow for building cross-platform wheels and publishing to PyPI.

### Features

- **Multi-platform support**: Builds wheels for:
  - Linux: x86_64, ARM64
  - macOS: x86_64 (Intel), ARM64 (Apple Silicon)
  - Windows: x86_64, ARM64
- **Python version support**: Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Automated dependency updates**: Runs weekly to incorporate latest dependencies
- **Automatic publishing**: Publishes to PyPI on releases

### Triggers

1. **Push to master**: Builds wheels but does not publish
2. **Pull requests**: Builds wheels for testing
3. **Releases**: Builds and publishes to PyPI
4. **Weekly schedule**: Runs every Monday at 00:00 UTC to check for dependency updates
5. **Manual dispatch**: Can be triggered manually with option to publish

### Setup Requirements

#### PyPI Trusted Publishing (Recommended)

The workflow uses PyPI's trusted publishing feature, which is more secure than API tokens.

1. Go to your PyPI project settings: https://pypi.org/manage/project/sprocket-carball/settings/
2. Navigate to "Publishing" section
3. Add a new publisher with:
   - **PyPI Project Name**: `sprocket-carball`
   - **Owner**: Your GitHub username or organization
   - **Repository name**: `carball`
   - **Workflow name**: `build-and-publish.yml`
   - **Environment name**: `pypi`

#### Alternative: API Token Method

If you prefer to use API tokens:

1. Generate a PyPI API token at https://pypi.org/manage/account/token/
2. Add it as a GitHub secret named `PYPI_API_TOKEN`
3. Modify the publish step in the workflow to use:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
       skip-existing: true
       verbose: true
   ```

### Manual Publishing

To manually trigger a build and publish:

1. Go to Actions tab in GitHub
2. Select "Build and Publish to PyPI" workflow
3. Click "Run workflow"
4. Select the branch
5. Set "Publish to PyPI" to "yes"
6. Click "Run workflow"

### Monitoring Builds

- Check the Actions tab to see build progress
- Artifacts (wheels and sdist) are stored for 7 days for each build
- Failed builds will show detailed logs for debugging

### Weekly Dependency Updates

The workflow runs automatically every Monday to:
1. Pull latest versions of dependencies (pandas, numpy, sprocket-boxcars-py, etc.)
2. Build wheels with these updated dependencies
3. Store artifacts for review

To publish these builds, either:
- Create a new release with the updated version
- Manually trigger the workflow with publish=yes

### Wheel Building Details

The workflow uses `cibuildwheel` which:
- Builds wheels in isolated environments
- Ensures compatibility with target platforms
- Runs basic import tests on built wheels
- Handles protobuf compilation during build

### Protobuf Handling

The workflow automatically:
1. Installs protobuf compiler (version 3.6.1) on all platforms
2. Runs `init.py` to generate proto files before building
3. Includes generated files in the wheel

### Troubleshooting

**Build failures on specific platforms:**
- Check the platform-specific logs in GitHub Actions
- ARM64 builds may take longer due to QEMU emulation

**Publishing failures:**
- Verify PyPI trusted publishing is configured correctly
- Check that the version in setup.py doesn't already exist on PyPI
- Ensure you have maintainer access to the PyPI project

**Import errors in test:**
- Check that all dependencies are specified in setup.py
- Verify protobuf files are being generated correctly
