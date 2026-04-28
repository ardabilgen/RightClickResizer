import os
import subprocess
import sys


# Supported video extensions for context menu
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpeg', '.mpg']


def get_ffmpeg_path():
    """Get ffmpeg executable path, checking embedded resource first."""
    # If running as frozen exe (PyInstaller), look for embedded ffmpeg
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts to a temp folder at runtime
        base_path = sys._MEIPASS
        ffmpeg_path = os.path.join(base_path, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path

    # Fallback: look in same directory as executable
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
        ffmpeg_path = os.path.join(exe_dir, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path
    else:
        # Development mode - look in project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        ffmpeg_path = os.path.join(project_root, 'ffmpeg.exe')
        if os.path.exists(ffmpeg_path):
            return ffmpeg_path

    # Last resort: rely on system PATH
    return 'ffmpeg'


def convert_to_mp4(input_path, crf=23, preset='medium', max_width=None, max_height=None):
    """
    Convert video to MP4 with H.264 encoding.
    
    Args:
        input_path: Path to input video file
        crf: Constant Rate Factor (18-28, lower=better quality, 23=default)
        preset: Encoding preset (faster=slower encoding but smaller file)
        max_width: Optional max width to scale down
        max_height: Optional max height to scale down
    
    Returns:
        Path to output MP4 file, or None on failure
    """
    try:
        ffmpeg_path = get_ffmpeg_path()
        
        # Get original video dimensions to calculate scaling
        scale_filter = ''
        if max_width or max_height:
            # First, get original dimensions
            probe_cmd = [
                ffmpeg_path, '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0', '-i', input_path
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                original_width, original_height = map(int, result.stdout.strip().split('\n'))
                
                # Calculate new dimensions maintaining aspect ratio
                if max_width and original_width > max_width:
                    scale_filter += f',scale=w={max_width}:-1'
                if max_height and original_height > max_height:
                    scale_filter += f',scale=-1:h={max_height}'
            
        # Build filter string
        filter_str = scale_filter.lstrip(',')
        
        # Construct output path
        directory, filename = os.path.split(input_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(directory, f'{name}_converted.mp4')
        
        # FFmpeg command for high-quality conversion with size reduction
        cmd = [
            ffmpeg_path,
            '-i', input_path,
            '-c:v', 'libx264',           # H.264 video codec
            '-crf', str(crf),             # Quality (23 = good balance)
            '-preset', preset,            # Encoding speed/size tradeoff
            '-c:a', 'copy',               # Copy audio without re-encoding
            '-movflags', '+faststart',    # Web optimization
            '-pix_fmt', 'yuv420p',        # Compatibility
        ]
        
        if filter_str:
            cmd.extend(['-vf', filter_str])
        
        cmd.append(output_path)
        
        # Run conversion
        print(f'Converting: {input_path} -> {output_path}')
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 min timeout for large files
        )
        
        if result.returncode == 0 and os.path.exists(output_path):
            # Compare file sizes
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size * 100)
            print(f'Conversion successful! Size reduction: {reduction:.1f}%')
            return output_path
        else:
            print(f'FFmpeg error: {result.stderr}')
            return None
            
    except subprocess.TimeoutExpired:
        print('Error: Conversion timed out (file may be too large)')
        return None
    except FileNotFoundError:
        print('Error: ffmpeg.exe not found. Please install ffmpeg or place it in the project directory.')
        return None
    except Exception as e:
        print(f'Error converting {input_path}: {e}')
        return None


def get_video_info(input_path):
    """Get video file information (duration, resolution, codec)."""
    try:
        ffmpeg_path = get_ffmpeg_path()
        cmd = [
            ffmpeg_path, '-v', 'error',
            '-show_entries', 'format=duration',
            '-show_entries', 'stream=width,height,codec_name',
            '-of', 'default=noprint_wrappers=1',
            input_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return result.stdout
        return None
    except Exception:
        return None
