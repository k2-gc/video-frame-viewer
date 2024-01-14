import argparse

from frame_viewer.app import run_app


def get_parser():
    parser = argparse.ArgumentParser(
        prog="Video frame view and save tool\n",
        description="Show how to use the tool",
    )
    parser.add_argument("--video-path", type=str, required=True, help="Path to video file.")
    return parser.parse_args()

if __name__ == "__main__":
    arg = get_parser()
    run_app(arg.video_path)