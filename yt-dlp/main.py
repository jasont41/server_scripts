import json 
import yaml
import os 
import subprocess

def get_num_files(directory):
    number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
    return number_of_files

def write_dict_to_yaml(dict):
    with open('channels.yml', 'w') as outfile:
        yaml.dump(dict, outfile, default_flow_style=False)

def get_command_string(dict, key):
    cmd_part1 = "yt-dlp -S ext:mp4:m4a --autonumber-start " # + index 
    cmd_part2 = " --download-archive " # + path to history txt  
    cmd_part3 = " --playlist-reverse --add-metadata --embed-thumbnail -o \"S01E%(autonumber)03d " # + channel abbv 
    cmd_part4 = " %(title)s.%(ext)s\" " # + url 
    index = str(dict[key]['numOfVideos'] + 1)
    sending_cmd =  cmd_part1 + index + cmd_part2 + dict[key]['history_txt'] + cmd_part3 + dict[key]['abbv'] + cmd_part4 + dict[key]['url']
    return sending_cmd




def main():
    cwd = os.getcwd() 
    print("current pwd  {0}".format(os.getcwd()))
    f = open("channels.yml", "r")
    dict = yaml.safe_load(f)
    os.chdir(dict['julian']['path'])
    cmd = get_command_string(dict, "julian")

    subprocess.run(cmd, shell=True)
    f.close()

if __name__ == "__main__":
    main()