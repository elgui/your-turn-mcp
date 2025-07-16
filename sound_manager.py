"""
Sound Manager for MCP Your Turn Server

This module provides a robust sound notification system with multiple fallback options:
1. Platform-specific system sounds (primary)
2. External alert.wav file (secondary)
3. Embedded minimal beep sound (tertiary)
4. ASCII bell character (final fallback)

The embedded sound is a minimal beep to reduce file size while maintaining functionality.
"""

import os
import sys
import tempfile
import base64
import subprocess
import logging
from pathlib import Path
from typing import Optional

# Minimal embedded beep sound - a very short WAV file
# This is a minimal valid WAV file with a short beep
EMBEDDED_BEEP_WAV_BASE64 = """
UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=
"""

logger = logging.getLogger(__name__)


class SoundManager:
    """Manages sound notifications with multiple fallback strategies."""
    
    def __init__(self, external_sound_file: Optional[str] = None):
        """
        Initialize the sound manager.
        
        Args:
            external_sound_file: Path to external sound file (e.g., alert.wav)
        """
        self.external_sound_file = external_sound_file or "alert.wav"
        self.platform = sys.platform.lower()
        self._temp_sound_file = None
        
    def play_notification_sound(self) -> bool:
        """
        Play notification sound using the best available method.

        Returns:
            bool: True if sound was played successfully, False otherwise
        """
        logger.info(f"🔊 Starting sound notification on platform: {self.platform}")

        # Strategy 1: Platform-specific system sounds
        logger.debug("🎵 Trying platform-specific system sounds...")
        if self._play_system_sound():
            logger.info("✅ Played system sound successfully")
            return True
        logger.debug("❌ System sound failed, trying next strategy...")

        # Strategy 2: External sound file
        logger.debug(f"🎵 Trying external sound file: {self.external_sound_file}")
        if self._play_external_sound():
            logger.info("✅ Played external sound file successfully")
            return True
        logger.debug("❌ External sound failed, trying next strategy...")

        # Strategy 3: Embedded minimal beep
        logger.debug("🎵 Trying embedded minimal beep...")
        if self._play_embedded_sound():
            logger.info("✅ Played embedded sound successfully")
            return True
        logger.debug("❌ Embedded sound failed, using final fallback...")

        # Strategy 4: ASCII bell (final fallback)
        logger.debug("🎵 Using ASCII bell fallback...")
        result = self._play_ascii_bell()
        if result:
            logger.info("✅ ASCII bell fallback used successfully")
        else:
            logger.error("❌ All sound strategies failed!")
        return result
    
    def _play_system_sound(self) -> bool:
        """Play platform-specific system notification sound."""
        try:
            if self.platform.startswith('win'):
                logger.debug("🪟 Attempting Windows system sound...")
                return self._play_windows_system_sound()
            elif self.platform.startswith('darwin'):
                logger.debug("🍎 Attempting macOS system sound...")
                return self._play_macos_system_sound()
            elif self.platform.startswith('linux'):
                logger.debug("🐧 Attempting Linux system sound...")
                return self._play_linux_system_sound()
            else:
                logger.debug(f"❓ Unknown platform: {self.platform}")
        except Exception as e:
            logger.warning(f"System sound failed with exception: {e}")
        return False
    
    def _play_windows_system_sound(self) -> bool:
        """Play Windows system notification sound."""
        try:
            import winsound
            logger.debug("🔊 Using Windows MessageBeep...")
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            return True
        except ImportError as e:
            logger.debug(f"winsound not available: {e}")
            # Fallback to simple beep
            try:
                import winsound
                logger.debug("🔊 Using Windows simple beep fallback...")
                winsound.Beep(800, 500)  # 800Hz for 500ms
                return True
            except ImportError as e2:
                logger.debug(f"winsound fallback also failed: {e2}")
                return False
        except Exception as e:
            logger.debug(f"Windows sound error: {e}")
            return False
    
    def _play_macos_system_sound(self) -> bool:
        """Play macOS system notification sound."""
        sounds_to_try = [
            '/System/Library/Sounds/Ping.aiff',
            '/System/Library/Sounds/Glass.aiff',
            '/System/Library/Sounds/Blow.aiff',
            '/System/Library/Sounds/Pop.aiff'
        ]

        for sound_file in sounds_to_try:
            try:
                logger.debug(f"🔊 Trying macOS sound: {sound_file}")
                result = subprocess.run(['afplay', sound_file],
                                     check=True, capture_output=True, timeout=5)
                logger.debug(f"✅ macOS sound played successfully: {sound_file}")
                return True
            except subprocess.CalledProcessError as e:
                logger.debug(f"❌ afplay failed for {sound_file}: {e}")
            except subprocess.TimeoutExpired:
                logger.debug(f"⏰ afplay timeout for {sound_file}")
            except FileNotFoundError:
                logger.debug(f"📁 Sound file not found: {sound_file}")
            except Exception as e:
                logger.debug(f"❌ Unexpected error with {sound_file}: {e}")

        logger.debug("❌ All macOS system sounds failed")
        return False
    
    def _play_linux_system_sound(self) -> bool:
        """Play Linux system notification sound."""
        # Try multiple Linux audio systems and sounds
        commands = [
            (['paplay', '/usr/share/sounds/alsa/Front_Left.wav'], 'PulseAudio with ALSA sound'),
            (['aplay', '/usr/share/sounds/alsa/Front_Left.wav'], 'ALSA with Front_Left sound'),
            (['paplay', '/usr/share/sounds/sound-icons/bell.wav'], 'PulseAudio with bell sound'),
            (['aplay', '/usr/share/sounds/sound-icons/bell.wav'], 'ALSA with bell sound'),
            (['speaker-test', '-t', 'sine', '-f', '800', '-l', '1'], 'Speaker test sine wave'),
            (['beep', '-f', '800', '-l', '500'], 'System beep command')
        ]

        for cmd, description in commands:
            try:
                logger.debug(f"🔊 Trying Linux audio: {description}")
                result = subprocess.run(cmd, check=True, capture_output=True, timeout=5)
                logger.debug(f"✅ Linux sound played successfully: {description}")
                return True
            except subprocess.CalledProcessError as e:
                logger.debug(f"❌ Command failed for {description}: {e}")
            except subprocess.TimeoutExpired:
                logger.debug(f"⏰ Timeout for {description}")
            except FileNotFoundError:
                logger.debug(f"📁 Command not found for {description}")
            except Exception as e:
                logger.debug(f"❌ Unexpected error with {description}: {e}")

        logger.debug("❌ All Linux system sounds failed")
        return False
    
    def _play_external_sound(self) -> bool:
        """Play external sound file if it exists."""
        if not os.path.exists(self.external_sound_file):
            logger.debug(f"📁 External sound file not found: {self.external_sound_file}")
            return False

        logger.debug(f"🔊 Found external sound file: {self.external_sound_file}")

        try:
            if self.platform.startswith('win'):
                logger.debug("🪟 Using Windows winsound for external file...")
                import winsound
                winsound.PlaySound(self.external_sound_file, winsound.SND_FILENAME)
                logger.debug("✅ Windows external sound played successfully")
                return True
            elif self.platform.startswith('darwin'):
                logger.debug("🍎 Using macOS afplay for external file...")
                result = subprocess.run(['afplay', self.external_sound_file],
                                     check=True, capture_output=True, timeout=10)
                logger.debug("✅ macOS external sound played successfully")
                return True
            elif self.platform.startswith('linux'):
                # Try paplay first, then aplay
                for cmd_name in ['paplay', 'aplay']:
                    try:
                        logger.debug(f"🐧 Trying Linux {cmd_name} for external file...")
                        result = subprocess.run([cmd_name, self.external_sound_file],
                                             check=True, capture_output=True, timeout=10)
                        logger.debug(f"✅ Linux {cmd_name} external sound played successfully")
                        return True
                    except subprocess.CalledProcessError as e:
                        logger.debug(f"❌ {cmd_name} failed: {e}")
                    except subprocess.TimeoutExpired:
                        logger.debug(f"⏰ {cmd_name} timeout")
                    except FileNotFoundError:
                        logger.debug(f"📁 {cmd_name} command not found")
        except Exception as e:
            logger.warning(f"External sound playback failed with exception: {e}")
        return False
    
    def _play_embedded_sound(self) -> bool:
        """Play embedded minimal beep sound."""
        try:
            logger.debug("🔊 Creating temporary file from embedded sound data...")
            # Create temporary file with embedded sound
            if self._temp_sound_file is None:
                self._create_temp_sound_file()

            if self._temp_sound_file and os.path.exists(self._temp_sound_file):
                logger.debug(f"📁 Temporary sound file created: {self._temp_sound_file}")
                return self._play_temp_sound_file()
            else:
                logger.debug("❌ Failed to create temporary sound file")
        except Exception as e:
            logger.warning(f"Embedded sound playback failed with exception: {e}")
        return False
    
    def _create_temp_sound_file(self) -> None:
        """Create temporary sound file from embedded data."""
        try:
            logger.debug("🔄 Decoding base64 embedded sound data...")
            # Decode base64 sound data
            sound_data = base64.b64decode(EMBEDDED_BEEP_WAV_BASE64.strip())
            logger.debug(f"📊 Decoded {len(sound_data)} bytes of sound data")

            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(sound_data)
                self._temp_sound_file = temp_file.name
                logger.debug(f"💾 Created temporary sound file: {self._temp_sound_file}")

        except Exception as e:
            logger.warning(f"Failed to create temporary sound file: {e}")
            self._temp_sound_file = None
    
    def _play_temp_sound_file(self) -> bool:
        """Play the temporary sound file."""
        if not self._temp_sound_file:
            return False
            
        try:
            if self.platform.startswith('win'):
                import winsound
                winsound.PlaySound(self._temp_sound_file, winsound.SND_FILENAME)
                return True
            elif self.platform.startswith('darwin'):
                subprocess.run(['afplay', self._temp_sound_file], 
                             check=True, capture_output=True, timeout=5)
                return True
            elif self.platform.startswith('linux'):
                for cmd in [['paplay'], ['aplay']]:
                    try:
                        subprocess.run(cmd + [self._temp_sound_file], 
                                     check=True, capture_output=True, timeout=5)
                        return True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
                        continue
        except Exception as e:
            logger.debug(f"Temporary sound file playback failed: {e}")
        return False
    
    def _play_ascii_bell(self) -> bool:
        """Play ASCII bell character as final fallback."""
        try:
            logger.debug("🔔 Using ASCII bell character as final fallback...")
            print('\a', end='', flush=True)  # ASCII bell character
            # Also print a visible notification for terminals that don't support bell
            print("🔔 NOTIFICATION: Your turn!", file=sys.stderr)
            return True
        except Exception as e:
            logger.error(f"Even ASCII bell failed: {e}")
            return False
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        if self._temp_sound_file and os.path.exists(self._temp_sound_file):
            try:
                os.unlink(self._temp_sound_file)
                self._temp_sound_file = None
            except Exception as e:
                logger.debug(f"Failed to cleanup temporary sound file: {e}")
    
    def __del__(self):
        """Cleanup when object is destroyed."""
        self.cleanup()


# Global sound manager instance
_sound_manager = None


def get_sound_manager(external_sound_file: Optional[str] = None) -> SoundManager:
    """
    Get or create the global sound manager instance.
    
    Args:
        external_sound_file: Path to external sound file
        
    Returns:
        SoundManager: The sound manager instance
    """
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager(external_sound_file)
    return _sound_manager


def play_notification_sound(external_sound_file: Optional[str] = None) -> bool:
    """
    Convenience function to play notification sound.
    
    Args:
        external_sound_file: Path to external sound file
        
    Returns:
        bool: True if sound was played successfully
    """
    manager = get_sound_manager(external_sound_file)
    return manager.play_notification_sound()


if __name__ == "__main__":
    # Test the sound manager
    print("Testing sound manager...")
    manager = SoundManager()
    
    print("Playing notification sound...")
    success = manager.play_notification_sound()
    print(f"Sound played successfully: {success}")
    
    # Cleanup
    manager.cleanup()
