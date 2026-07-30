import torch

class HardwareDeviceEngine:
    """Detects available hardware accelerators (CUDA, Apple Silicon MPS, or CPU)."""

    @staticmethod
    def detect_device() -> str:
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            logger.info(f"CUDA Hardware detected: {device_name}")
            return "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            logger.info("Apple Silicon Metal (MPS) detected.")
            return "mps"
        else:
            logger.warning("No GPU detected. Falling back to CPU execution.")
            return "cpu"

    @staticmethod
    def optimize_memory():
        """Clears hardware VRAM caches across platforms."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
