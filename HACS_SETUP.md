# HACS Setup Guide

This document explains the HACS (Home Assistant Community Store) setup for this integration.

## Files Added for HACS Compliance

### Root Directory Files

1. **`hacs.json`** - HACS metadata file
   - Defines integration name, domains, and minimum Home Assistant version
   - Required for HACS to recognize the integration

2. **`info.md`** - HACS information page
   - Displayed in HACS store when users view the integration
   - Contains features, use cases, and quick configuration example

3. **`CONTRIBUTING.md`** - Contribution guidelines
   - Instructions for contributors
   - Code style and testing guidelines

### GitHub Actions Workflows (`.github/workflows/`)

1. **`validate.yaml`** - Validation workflow
   - Runs HACS validation to ensure compliance
   - Runs Hassfest validation (Home Assistant's official validator)
   - Triggers on push, pull requests, and daily schedule

2. **`release.yaml`** - Release workflow
   - Automatically creates zip file when a new release is published
   - Updates manifest.json version from git tag
   - Uploads zip file to GitHub release

### GitHub Issue Templates (`.github/ISSUE_TEMPLATE/`)

1. **`bug_report.md`** - Bug report template
2. **`feature_request.md`** - Feature request template

### Other GitHub Configuration

1. **`.github/dependabot.yml`** - Dependabot configuration
   - Keeps GitHub Actions up to date automatically

## How to Submit to HACS

### Prerequisites

1. ✅ Integration is in a public GitHub repository
2. ✅ Repository has a proper LICENSE file (MIT License)
3. ✅ Repository has hacs.json in the root
4. ✅ Repository has proper manifest.json in custom_components/interpolation/
5. ✅ Repository has a README with installation instructions
6. ✅ Repository has at least one release/tag

### Steps to Submit

1. **Create a Release**
   ```bash
   git tag -a v1.0.0 -m "Initial release"
   git push origin v1.0.0
   ```
   - This will trigger the release workflow
   - GitHub will create a release with the zip file

2. **Submit to HACS**
   - Go to https://github.com/hacs/default/
   - Fork the repository
   - Add your integration to the appropriate JSON file:
     - For integrations: `integration` file
   - Create a pull request with your addition
   - Format:
     ```json
     "JoshuaLampert/homeassistant-interpolation"
     ```

3. **Wait for Approval**
   - HACS maintainers will review your submission
   - They may request changes or improvements
   - Once approved, your integration will be available in HACS

## Validation Badges

After setup, you can add these badges to your README (already added):

- HACS badge: Shows it's a HACS integration
- GitHub Release badge: Shows latest version
- License badge: Shows license type

## Maintaining the Integration

### Creating New Releases

1. Update version in `custom_components/interpolation/manifest.json`
2. Create a git tag:
   ```bash
   git tag -a v1.x.x -m "Release version 1.x.x"
   git push origin v1.x.x
   ```
3. The release workflow will automatically:
   - Create a GitHub release
   - Build and attach the zip file
   - Update the manifest version

### Validation

The validation workflow runs automatically on every push and pull request:
- HACS validation ensures continued compliance
- Hassfest validation checks Home Assistant requirements
- Daily runs catch any changes in validation rules

## Testing HACS Installation

Users can install from HACS by:

1. **Before HACS approval (Custom Repository)**
   - HACS → Integrations → Three dots → Custom repositories
   - Add: `https://github.com/JoshuaLampert/homeassistant-interpolation`
   - Category: Integration
   - Install

2. **After HACS approval (Default Repository)**
   - HACS → Integrations → Search "Interpolation"
   - Click Install

## Troubleshooting

### Validation Fails

- Check that all required files are present
- Verify JSON files are valid
- Ensure manifest.json has all required fields
- Check that there's at least one release/tag

### Release Workflow Fails

- Verify manifest.json is in the correct location
- Check that the tag format is correct (v1.0.0)
- Ensure GitHub Actions has proper permissions

## Additional Resources

- [HACS Documentation](https://hacs.xyz/)
- [HACS Integration Requirements](https://hacs.xyz/docs/publish/integration)
- [Home Assistant Integration Documentation](https://developers.home-assistant.io/)
- [Hassfest Documentation](https://developers.home-assistant.io/blog/2020/04/16/hassfest)
