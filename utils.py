import os
import yaml
import logging
from pathlib import Path
import torch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path='config.yaml'):
    """Load YAML configuration file."""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Config file {config_path} not found")
        raise


def create_directory_structure():
    """Create required output and temp directories."""
    directories = [
        'output/sad',
        'output/funny',
        'output/fight',
        'output/interesting',
        'clips/temp_clips',
        'audio/temp_audio',
        'models'
    ]
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory created/verified: {dir_path}")


def detect_device():
    """Detect available compute device (CUDA, ROCm, or CPU)."""
    if torch.cuda.is_available():
        device = torch.device('cuda')
        device_name = torch.cuda.get_device_name(0)
        logger.info(f"CUDA device detected: {device_name}")
        return device, 'cuda'
    
    try:
        # Check for ROCm
        if torch.version.hip is not None:
            device = torch.device('cuda')  # ROCm uses cuda device interface
            logger.info("AMD ROCm GPU detected")
            return device, 'rocm'
    except Exception:
        pass
    
    logger.info("No GPU detected, using CPU")
    return torch.device('cpu'), 'cpu'


def get_cpu_count():
    """Get available CPU core count."""
    return os.cpu_count() or 4


def sanitize_filename(filename):
    """Remove invalid characters from filename."""
    invalid_chars = '<>:"|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def cleanup_temp_files():
    """Clean up temporary files after processing."""
    temp_dirs = ['clips/temp_clips', 'audio/temp_audio']
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                try:
                    os.remove(file_path)
                    logger.info(f"Removed temp file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove {file_path}: {e}")


def log_pipeline_progress(stage, status):
    """Log progress at each pipeline stage."""
    logger.info(f"[STAGE] {stage} - {status}")
