#!/usr/bin/env python
import requests, os, sys, getopt, ast
from tqdm import tqdm

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://thermal.us.bramblexpress.com/api/v1/"
FILE_DIR = os.path.abspath(os.path.dirname(__file__))

### usuario guido:
##### email: pusiol@stanford.edu
### usuario guido.pusiol:
##### email: g@gmail.com
#user information
default_email = ""
default_password = "aaaaaa"
#user must have access to this groups
default_groups_to_download = []

#default_labels_in_groups_to_download = ["lying", "sitting", "standing", "indoor", "close up", "outdoor"]
default_labels_in_groups_to_download = ["lying", "sitting", "standing", "indoor","close up"]

#videos of each group will be divided in folders inside output_dir (one folder per group)
default_output_dir = os.path.join(FILE_DIR,"downloads")

default_thermal_image_modes = ["4_tim"]

default_order_by_semantic = False

default_incremental_download = False

def login(email, password):
    if not email or not password:
        raise "remember to set 'email' and 'password' with valid user information"

    data=requests.post('%susers/auth/' % BASE_URL,
                       verify=False,
                       data = {"username":email,"password":password});
    if data.status_code == 200:
        return data.json()['token']
    else:
        return None

"""return a list of ("groupName",id). Example: [("pepito group",255),...]"""
def get_groups_of_user_with_token(token):
    total_number_of_groups = 1
    page_number = 1
    non_member_groups = 0
    groups = []
    while len(groups) < total_number_of_groups-non_member_groups:
        data = requests.get('%sgroups/' % (BASE_URL),
                            verify=False,
                            params={"page":page_number},
                            headers={'Authorization':'Token %s' % token});
        if data.status_code == 200:
            json = data.json()
            total_number_of_groups = json["count"]
            for group in json["results"]:
                if not group["i_am_member"]:
                    non_member_groups += 1
                    continue
                name = group["name"]
                id = group["chat_id"]
                groups.append((name,id))
        else:
            return None

        page_number = page_number+1

    return groups

def is_video_on_disk(output_dir, group_name, order_by_semantic, semantic, orientation, thermal_image_mode, url):
    group_dir = os.path.join(output_dir, group_name)
    if not os.path.exists(group_dir):
        return False

    if order_by_semantic:
        destination_dir = os.path.join(group_dir, semantic, orientation, thermal_image_mode)
    else:
        destination_dir = os.path.join(group_dir, thermal_image_mode)
        
    filename = url.split("?")[0].replace("/","_").split("_",3)[-1]

    filepath = os.path.join(destination_dir,filename)
    if os.path.exists(filepath):
        return True
    
    return False

def get_video_urls_of_group_with_id(group_id, token, thermal_image_modes, 
                                    incremental=False, output_dir=None, group_name=None, 
                                    order_by_semantic=None):
    total_number_of_videos = 1
    page_number = 1
    video_urls = []
    extra_videos_count = 0
    finish_incremental = False
    while len(video_urls) < total_number_of_videos+extra_videos_count and \
          (not incremental or not finish_incremental):
        data=requests.get('%schats/verzus/%d/videos/' % (BASE_URL, group_id),
                          verify=False,
                          params={"page":page_number},
                          headers={'Authorization':'Token %s' % token})
        if data.status_code == 200:
            json = data.json()
            total_number_of_videos = json["count"]
            for video in json["results"]:
                entry_id = video["entry"]["id"]
                url = video["entry"]["file"]["file"]
                thermal_image_mode = None
                avoid_video = False
                video_semantic = video["entry"]["semantics"]["emoji"]

                # UIDeviceOrientationUnknown,
                # UIDeviceOrientationPortrait,            // Device oriented vertically, home button on the bottom
                # UIDeviceOrientationPortraitUpsideDown,  // Device oriented vertically, home button on the top
                # UIDeviceOrientationLandscapeLeft,       // Device oriented horizontally, home button on the right
                # UIDeviceOrientationLandscapeRight,      // Device oriented horizontally, home button on the left
                # UIDeviceOrientationFaceUp,              // Device oriented flat, face up
                # UIDeviceOrientationFaceDown             // Device oriented flat, face down
                video_orientation = "1"
                for semantic in video["entry"]["semantics"]["results"]:
                    if semantic["category"] == "has_video" and int(float(semantic["score"])) == 0:
                        avoid_video = True
                        break

                    if semantic["category"] == "thermalImageMode":
                        tim = int(float(semantic["score"]))
                        tim = tim if tim != 12 else 4
                        tim = tim if tim != 14 else 15
                        thermal_image_mode = "%d_tim" % tim
                        if thermal_image_mode not in thermal_image_modes:
                            avoid_video = True

                    if semantic["category"] == "includeRgb":
                        if "15_tim" not in thermal_image_modes:
                            continue

                        extra_files = requests.get('%sentries/verzus/waitings/%d/extra_files/' % (BASE_URL, entry_id),
                                                   verify=False,
                                                   params={"page":page_number},
                                                   headers={'Authorization':'Token %s' % token})

                        if extra_files.status_code == 200:
                            extra_files = extra_files.json()
                            for extra_file in extra_files["extra_files"]:
                                extra_file_url = extra_file["file"]
                                extra_file_base_url = extra_file_url.split("?")[0]
                                if extra_file_base_url.endswith("_1.mov"):
                                    video_urls.append(("15_tim", video_semantic, video_orientation,extra_file_url))
                                    if incremental and is_video_on_disk(output_dir, group_name, order_by_semantic, 
                                                                        video_semantic, video_orientation, "15_tim", 
                                                                        extra_file_url):
                                        finish_incremental=True

                                    extra_videos_count += 1  
                                    break
                        
                            
                    if semantic["category"] == "includeThermalData":
                        if "14_tim" not in thermal_image_modes:
                            continue

                        extra_files = requests.get('%sentries/verzus/waitings/%d/extra_files/' % (BASE_URL, entry_id),
                                                   verify=False,
                                                   params={"page":page_number},
                                                   headers={'Authorization':'Token %s' % token})

                        if extra_files.status_code == 200:
                            extra_files = extra_files.json()
                            for extra_file in extra_files["extra_files"]:
                                extra_file_url = extra_file["file"]
                                extra_file_base_url = extra_file_url.split("?")[0]
                                if extra_file_base_url.endswith("_1.mov"):
                                    exist_2 = False
                                    for extra_file2 in extra_files["extra_files"]:
                                        extra_file_url2 = extra_file2["file"]
                                        extra_file_base_url2 = extra_file_url2.split("?")[0]
                                        if extra_file_base_url2.endswith("_2.mov"):
                                            exist_2 = True
                                            video_urls.append(("14_tim", video_semantic, video_orientation,extra_file_url2))
                                            if incremental and is_video_on_disk(output_dir, group_name, order_by_semantic, 
                                                                                video_semantic, video_orientation, "14_tim", 
                                                                                extra_file_url2):
                                                finish_incremental=True
                                                
                                            extra_videos_count += 1  
                                            break
                                    if not exist_2:
                                        video_urls.append(("14_tim", video_semantic, video_orientation,extra_file_url))
                                        if incremental and is_video_on_disk(output_dir, group_name, order_by_semantic, 
                                                                            video_semantic, video_orientation, "14_tim", 
                                                                            extra_file_url):
                                                finish_incremental=True
                                        extra_videos_count += 1
                                        break

                    if semantic["category"] == "videoOrientation":
                        video_orientation = "%s" % str(semantic["score"])

                if avoid_video:
                    print "Avoiding video with tim %s: %s" % (thermal_image_mode, url)
                    continue

                if not thermal_image_mode:
                    thermal_image_mode = "unspecified"

                video_urls.append((thermal_image_mode,video_semantic,video_orientation,url))
                if incremental and is_video_on_disk(output_dir, group_name, order_by_semantic, 
                                                    video_semantic, video_orientation, thermal_image_mode, 
                                                    url):
                    finish_incremental=True
        else:
            return video_urls

        page_number = page_number+1

    video_urls.reverse()
    return video_urls

def download_videos_of_group(videos_urls, group_name, group_id, output_dir, order_by_semantic):
    group_dir = os.path.join(output_dir, group_name)
    if not os.path.exists(group_dir):
        os.makedirs(group_dir)

    for thermal_image_mode, semantic, orientation, url in videos_urls:
        if order_by_semantic:
            destination_dir = os.path.join(group_dir, semantic, orientation, thermal_image_mode)
        else:
            destination_dir = os.path.join(group_dir, thermal_image_mode)

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        filename = url.split("?")[0].replace("/","_").split("_",3)[-1]
        print filename.encode('ascii', 'ignore')

        filepath = os.path.join(destination_dir,filename)
        if os.path.exists(filepath):
            continue

        response = requests.get(url, stream=True)
        with open(filepath, "wb") as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

def download_files_from_groups(email=default_email,
                               password=default_password,
                               groups_to_download=default_groups_to_download,
                               output_dir=default_output_dir,
                               thermal_image_modes=default_thermal_image_modes,
                               labels_in_groups_to_download=default_labels_in_groups_to_download,
                               order_by_semantic=default_order_by_semantic,
                               incremental_download=default_incremental_download):
    token = login(email, password)
    if not token:
        raise "email and/or password does not match a valid user"

    print "token: %s" % token

    all_groups_of_user = get_groups_of_user_with_token(token)
    if not all_groups_of_user:
        raise "error getting groups of user"

    print "all user's groups:"
    for g in all_groups_of_user:
        print "\t%s" % g[0].encode('ascii', 'ignore')

    groups_tuples = []
    for group_name in groups_to_download:
        group_tuple = [item for item in all_groups_of_user if item[0] == group_name]
        if len(group_tuple) == 0:
            print "group with name %s does not exist" % group_name.encode('ascii', 'ignore')
            raise "group with name %s does not exist" % group_name.encode('ascii', 'ignore')
        elif len(group_tuple) > 1:
            for name,id in group_tuple:
                groups_tuples.append(("%s_%d"%(name,id), id))
        else:
            groups_tuples.append(group_tuple[0])

    for group_name, group_id in all_groups_of_user:
        #if was added before, continue
        is_group_in_groups_to_download = len([item for item in groups_to_download if item == group_name]) > 0
        if is_group_in_groups_to_download:
            continue

        #if no label in group, continue
        is_any_label_in_group = len([item for item in labels_in_groups_to_download if item in group_name]) > 0
        if not is_any_label_in_group:
            continue

        groups_tuples.append((group_name,group_id))

    print "getting groups videos urls for groups:"
    for gname, gid in groups_tuples:
        print "id:%d\tname:%s" % (gid,gname.encode('ascii', 'ignore'))

    for group_name, group_id in groups_tuples:
        try:
            video_urls = get_video_urls_of_group_with_id(group_id, token, thermal_image_modes, 
                                                         incremental_download, output_dir, group_name, order_by_semantic)
            if not video_urls:
                raise "error getting video urls of group %s" % group_name

            print "urls of group %s ok" % group_name.encode('ascii', 'ignore')

            download_videos_of_group(video_urls, group_name, group_id, output_dir, order_by_semantic)
        except Exception as e:
            print e
            print "error getting video urls of group %s" % group_name.encode('ascii', 'ignore')
            continue

    print "downloads completed"

def main(argv):
    new_config = {}
    try:
        opts, args = getopt.getopt(argv,"he:p:g:o:l:t:",["help","email=","password=","groups=",
                                                         "output=","labels=","thermal_modes=","order_by_semantic", 
                                                         "incremental"])
    except getopt.GetoptError:
        print """video_downloader.py -e <email> -p <password> -g '["<groupName1>","<groupName2>"]' """ + \
              """-o <outputDir> -l '["<groupName1>","<groupName2>"]' -t '["4_tim","14_tim"]' --incremental"""
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print """video_downloader.py -e <email> -p <password> -g '["<groupName1>","<groupName2>"]' """ + \
                  """-o <outputDir> -l '["<groupName1>","<groupName2>"]' -t '["4_tim","14_tim"]' --incremental"""
            sys.exit()
        elif opt in ("-e", "--email"):
            new_config["email"] = arg
        elif opt in ("-p", "--password"):
            new_config["password"] = arg
        elif opt in ("-g", "--group"):
            new_config["groups_to_download"] = ast.literal_eval("%s" % arg)
        elif opt in ("-o", "--output"):
            new_config["output_dir"] = arg
        elif opt in ("-l", "--labels"):
            new_config["labels_in_groups_to_download"] = ast.literal_eval("%s" % arg)
        elif opt in ("-t", "--thermal_modes"):
            new_config["thermal_image_modes"] = ast.literal_eval("%s" % arg)
        elif opt in ("--order_by_semantic"):
            new_config["order_by_semantic"] = True
        elif opt in ("--incremental"):
            new_config["incremental_download"] = True
            
    download_files_from_groups(**new_config)

if __name__ == "__main__":
   main(sys.argv[1:])
