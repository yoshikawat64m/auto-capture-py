# Auto Capture CLI

A Python command-line tool for capturing screenshots of any window area at specified intervals and durations.

## 📁 Project Structure

```
auto-capture-py/
├── src/                    # Source code
│   ├── main.py            # Main script
│   ├── area_selector.py   # Area selection GUI
│   └── window_selector.py # Window selection GUI
├── docs/                  # Documentation
│   ├── README.md          # This file
│   ├── LOCAL_SETUP.md     # Local environment setup guide
│   ├── BUILD_GUIDE.md     # Build guide
│   ├── TEST_GUIDE.md      # Testing guide
│   └── LICENSE            # License
├── scripts/               # Scripts
│   ├── start_capture.sh   # Docker startup script
│   └── test_cli.sh        # Automated test script
├── build_tools/           # Build tools
│   ├── build.sh           # Unix/Linux build script
│   ├── build.bat          # Windows build script
│   ├── auto-capture.spec  # PyInstaller configuration
│   ├── setup.py           # Python setuptools configuration
│   └── build_requirements.txt # Build dependencies
├── tests/                 # Test files (future use)
├── captures/              # Screenshot output directory
├── dist/                  # Built executable files
├── .github/workflows/     # GitHub Actions CI/CD
├── requirements.txt       # Runtime dependencies
├── Dockerfile            # Docker configuration
└── docker-compose.yml    # Docker Compose configuration
```

## 🚀 Quick Start

### 1. Using Pre-built Executable (Recommended)

Download the latest executable from releases:

```bash
# Show help
./auto-capture --help

# Basic capture (5fps for 30 seconds)
./auto-capture --fps 5 --duration 30

# Single frame capture
./auto-capture --single

# Area-specific capture
./auto-capture --area 100,100,800,600 --fps 2 --duration 10
```

### 2. Running as Python Script

```bash
# Install dependencies
pip install -r requirements.txt

# Run
python src/main.py --fps 5 --duration 30
```

### 3. Using Docker

```bash
# Show help
docker-compose run help

# Single frame capture
docker-compose run single-capture
```

## 📖 Detailed Documentation

- **[Local Environment Setup](docs/LOCAL_SETUP.md)** - Development environment setup
- **[Build Guide](docs/BUILD_GUIDE.md)** - How to create executable files
- **[Testing Guide](docs/TEST_GUIDE.md)** - Testing methods and quality assurance

## ⚡ Key Features

- **Window Selection**: Select specific application windows
- **Area Selection**: Specify any area with mouse drag
- **Continuous Capture**: Record at specified FPS
- **Single Frame**: Take one screenshot
- **Cross-platform**: Windows, macOS, Linux support
- **GUI/CLI Support**: Both GUI mode and command-line mode

## 🛠️ For Developers

### Build

```bash
# Unix/Linux/macOS
./build_tools/build.sh

# Windows
build_tools\build.bat
```

### Testing

```bash
# Run automated tests
./scripts/test_cli.sh

# Manual testing
python src/main.py --no-gui --single --output-prefix test
```

### Docker Development Environment

```bash
# Start development container
docker-compose run auto-capture

# Test with virtual display
docker-compose run capture-headless
```

## 📋 Usage Examples

### Basic Usage

```bash
# Capture at 5fps for 30 seconds
./auto-capture --fps 5 --duration 30

# Specific area at 2fps for 10 seconds
./auto-capture --area 100,100,800,600 --fps 2 --duration 10

# Single frame capture
./auto-capture --single

# No-GUI mode (full screen)
./auto-capture --no-gui --fps 1 --duration 60
```

### Advanced Usage

```bash
# Custom filename prefix
./auto-capture --fps 5 --duration 30 --output-prefix my_capture

# High-frequency capture
./auto-capture --fps 30 --duration 5

# Long-duration low-frequency capture
./auto-capture --fps 0.5 --duration 3600  # 1 hour, once every 2 seconds
```

## 🔧 System Requirements

- **Python**: 3.11 or higher
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Memory**: Minimum 512MB, recommended 1GB+
- **Disk**: 100MB+ free space

### Required Permissions

- **macOS**: Screen recording permission, accessibility permission
- **Windows**: Administrator privileges (first run)
- **Linux**: X11 access permissions

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](docs/LICENSE) file for details.

## 🐛 Bug Reports & Feature Requests

Please submit bug reports and feature requests via [GitHub Issues](https://github.com/your-username/auto-capture-py/issues).

## 📞 Support

- **Documentation**: Various guides in the [docs/](docs/) folder
- **Testing**: Run `./scripts/test_cli.sh` to verify functionality
- **Troubleshooting**: See [TEST_GUIDE.md](docs/TEST_GUIDE.md#troubleshooting)

---

**Auto Capture CLI** - Efficient Screen Capture Tool 🎯
