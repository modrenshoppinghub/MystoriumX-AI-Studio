"""
Stereo Width Enhancement Engine.
Applies Mid-Side processing to widen stereo field.
"""

import torch

class StereoEngine:
    """Mid-Side Stereo Width Adjuster Engine."""

    def adjust_width(self, audio: torch.Tensor, width_factor: float = 1.3) -> torch.Tensor:
        """
        Adjusts stereo field width.
        width_factor = 1.0 (unchanged), 0.0 (mono), > 1.0 (widened)
        """
        if audio.shape[0] < 2:
            return audio  # Cannot expand mono track

        left = audio[0, :]
        right = audio[1, :]

        # Mid-Side Encoding
        mid = 0.5 * (left + right)
        side = 0.5 * (left - right)

        # Scale Side channel
        side_enhanced = side * width_factor

        # Mid-Side Decoding
        left_out = mid + side_enhanced
        right_out = mid - side_enhanced

        return torch.stack([left_out, right_out], dim=0)
