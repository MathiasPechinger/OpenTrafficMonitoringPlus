import argparse
import os
from preprocess import preprocess, preprocess_images
from postprocess import postprocess
from inference import run_inference
from config import config_by_config_name, config_by_video_name


def parse_args():
    parser = argparse.ArgumentParser('OpenTrafficMonitoring+ Argument Parser')

    parser.add_argument(
        '--videos',
        default=None,
        type=str,
        help=
        "Folder that contains the videos to process. Should be in the Format inputFolder:outputFolder"
        "The Config gets chosen by the video name")

    parser.add_argument(
        '--images',
        default=None,
        type=str,
        help=
        "Folder that contains images to process. Images are internally ordered alphabetically"
    )
    parser.add_argument(
        '--config',
        default=None,
        type=str,
        help=
        "Config used by vehicle tracker. Mandatory when evaluating images. Optional when evaluating on Videos (CAUTION: "
        "if specified when using the '--videos' approach, the given value overwrites the config for every Video)"
    )

    global args
    args = parser.parse_args()


def process_images(image_folder, output_folder, cfg):
    temp_path = os.path.join(output_folder, "temp") + "/"
    os.makedirs(temp_path, exist_ok=True)

    preprocess_images(image_folder, temp_path, cfg)

    run_inference(temp_path, cfg)

    postprocess(temp_path, cfg)


def process_videos(video_folder, output_folder):

    video_list = [
        video for video in os.listdir(video_folder)
        if video.endswith((".mp4", ".mov", ".avi"))
    ]
    assert len(
        video_list) > 0, "The specified folder {} contains no video".format(
            video_folder)

    for video_name in video_list:

        if not args.config:
            cfg = config_by_video_name(video_name)
        else:
            cfg = config_by_config_name(args.config)

        temp_path = output_folder + video_name.split(".")[0] + "/temp/"
        os.makedirs(temp_path, exist_ok=True)

        preprocess(video_folder + video_name, temp_path, cfg)

        run_inference(temp_path, cfg)

        postprocess(temp_path, cfg)


if __name__ == "__main__":
    parse_args()

    if args.videos:
        print("processing videos...")
        process_videos(*args.videos.split(":"))

    if args.images:
        print("processing images...")

        subfolders = [f.path + "/" for f in os.scandir(args.images.split(":")[0]) if f.is_dir()]
        if len(subfolders) == 0:
            # Single dir with images
            if not args.config:
                raise ValueError(
                    "'--config' is required when evaluating on images")
            cfg = config_by_config_name(args.config)
            print("Process single image folder : {}".format(args.images.split(":")[0]))
            process_images(*args.images.split(":"), cfg)

        else:
            # Multiple dirs
            base_output_folder = args.images.split(":")[1]
            print("Process a total amount of {} folders : {}".format(len(subfolders), subfolders))
            for subfolder in subfolders:
                if not args.config:
                    video_name = os.path.basename(os.path.normpath(subfolder))
                    cfg = config_by_video_name(video_name)
                else:
                    cfg = config_by_config_name(args.config)
                output_folder = os.path.join(base_output_folder,os.path.normpath(subfolder)) + "/"
                process_images(subfolder, output_folder, cfg)

