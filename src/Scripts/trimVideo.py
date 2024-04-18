from moviepy.editor import VideoFileClip

def trim_video(input_file_path, output_file_path, end_time):
    """
    Trims the input video file to the specified length.

    Args:
    input_file_path (str): The path to the input video file.
    output_file_path (str): The path where the trimmed video will be saved.
    end_time (int or float): The length in seconds to which the video will be trimmed.
    """
    # Load the video file
    video = VideoFileClip(input_file_path)
    
    # Trim the video
    trimmed_video = video.subclip(0, end_time)
    
    # Write the result to the output file
    trimmed_video.write_videofile(output_file_path, codec='libx264')

# Example usage
input_file = './video_storage/DJI_0003.mov'  # Replace with the path to your .mov file
output_file = './videos/trimmed_video.mov'  # Output file path
duration = 10  # Duration in seconds

trim_video(input_file, output_file, duration)
