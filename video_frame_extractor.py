import cv2
import os

def extract_frame(video_path, frame_number):
    # Load the video
    video = cv2.VideoCapture(video_path)
    
    # Check if the video is opened successfully
    if not video.isOpened():
        print("Error: Unable to open video file.")
        return
    
    # Set the frame number to be extracted
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    ret, frame = video.read()
    
    # Check if the frame is read successfully
    if not ret:
        print(f"Error: Unable to extract frame {frame_number} from the video.")
        return
    
    # Extract the file name and extension from the video path
    video_file_name = os.path.basename(video_path)
    video_name, video_extension = os.path.splitext(video_file_name)
    
    # Save the extracted frame as PNG
    output_path = f"{video_name}_frame_{frame_number}.png"
    cv2.imwrite(output_path, frame)
    
    print(f"Frame {frame_number} extracted and saved as {output_path}")
    
    return output_path

if __name__ == "__main__":
    # Prompt the user for the video file path
    video_path = input("Enter the video file path (.mkv): ")
    
    while True:
        # Prompt the user for the frame number
        frame_number = int(input("Enter the frame number to extract: "))
        
        # Extract the frame
        extracted_frame_path = extract_frame(video_path, frame_number)
        
        # Ask the user if they want to extract another frame
        choice = input("Do you want to extract another frame from this video? (yes/no): ").lower()
        if choice != 'yes':
            break
