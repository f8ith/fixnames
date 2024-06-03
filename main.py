import PTN
import sys
import os

VID_FORMATS = (".mkv", ".mp4")
SUB_FORMATS = (".ass", ".srt")

def log(string):
    with open("fixnames.log") as file:
        print(string)
        file.write(f"{string}\n")

def main():

    full_path = sys.argv[1]
    directory = os.fsencode(full_path)
    series_name = full_path.split("\\")[-2]
    season_number = full_path.split("\\")[-1].partition(" ")[2]

    vid_files = []
    sub_files = []

    new_vid_files = []
    new_sub_files = []

    os.chdir(directory)
    if os.path.exists("fixnames.log"):
        if input("fixnames.log exists. Continue? [y/n] ") != 'y':
            sys.exit(0)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(VID_FORMATS):
            vid_files.append(filename)
        elif filename.endswith(SUB_FORMATS):
            sub_files.append(filename)

    assert len(vid_files) == len(sub_files), "Number of videos & subs do not match!"

    if input("Rename videos? [y/n] ") == 'y':
        for vid_file in vid_files:
            parsed = PTN.parse(vid_file)
            new_vid_file = f"{series_name} - S{season_number}E{str(parsed["episode"]).zfill(2)}.{vid_file.partition(".")[2]}"
            log(f"{vid_file} -> {new_vid_file}")
            new_vid_files.append(new_vid_file)
            os.rename(vid_file, new_vid_file)
    else:
        new_vid_files = vid_files

    new_vid_files.sort()
    sub_files.sort()

    if input("Rename subs? [y/n] ") == 'y':
        for index, vid_file in enumerate(new_vid_files):
            sub_file = sub_files[index]
            new_sub_file = f"{vid_file.partition(".")[0]}.{sub_file.partition(".")[2]}"
            log(f"{sub_file} -> {new_sub_file}")
            new_sub_files.append(new_sub_file)
            os.rename(sub_file, new_sub_file)


if __name__ == '__main__':
    main()
