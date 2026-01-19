import subprocess
import os

def split_video(input_file, segment_length):
    # Create output directory if it doesn't exist
    output_dir = 'segments'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the ffmpeg command to split the video
    command = [
        'ffmpeg',
        '-i', input_file,
        '-c', 'copy',
        '-map', '0',
        '-segment_time', str(segment_length),
        '-f', 'segment',
        os.path.join(output_dir, 'segment_%03d.mp4')
    ]

    # Run the ffmpeg command
    subprocess.run(command)

if __name__ == '__main__':
    # Example usage
    split_video('input_video.mp4', 10)  # Split the video into 10-second segments