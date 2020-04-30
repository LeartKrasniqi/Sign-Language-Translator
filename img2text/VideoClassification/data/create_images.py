import csv
import glob
import os
from subprocess import call


def extract_files():
    data_file = []
    folders = ['train', 'test']

    for folder in folders:
        # Obtain list of files in train and test folder
        class_folders = glob.glob(os.path.join(folder, '*'))

        # Obtain all videos in each class
        for vid_class in class_folders:
            class_files = glob.glob(os.path.join(vid_class, '*.mp4'))

            for video_path in class_files:
                # Get video infomation
                video_parts = get_video_parts(video_path)

                folder, classname, file, filename = video_parts

                # Create destination file name based on classification and image number
                src = os.path.join(folder, classname, filename)
                dest = os.path.join(folder, classname, file + '-%04d.jpg')

                # `ffmpeg -i video.mpg image-%04d.jpg`
                # ffmpeg used to create images from a video
                call(["ffmpeg", "-i", src, dest])

                num_frames = get_num_frames_for_video(video_parts)

                # Add row for each video for CSV file
                data_file.append([folder, classname, file, num_frames])

    # Write video information to file in order to make training and difference generator easier
    with open('data_file.csv', 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(data_file)


# Obtain the number of frames in each video by counting the amount images generated
def get_num_frames_for_video(video_parts):
    folder, classname, filename, _ = video_parts
    img_list = glob.glob(os.path.join(folder, classname, filename + '*.jpg'))
    return len(img_list)


# Return Train/Test, Classification and file name
def get_video_parts(video_path):
    parts = video_path.split(os.path.sep)
    filename = parts[2]
    file = filename.split('.')[0]

    return parts[0], parts[1], file, filename


if __name__ == '__main__':
    extract_files()
