import json, requests, pathlib, configparser
import os, sys

def get_versions(api_url):
    completejson = requests.get(api_url)
    currentversion = json.loads(completejson.text)['data']['game']['latest']['version']
    return currentversion

def get_wallpaper(api_url):
    c_j = requests.get(api_url)
    r_j = json.loads(c_j.text)['data']['adv']['background']
    
    name = r_j.split("/")[-1]
    wallpaper_file = pathlib.Path(__file__).parents[1].resolve().joinpath('backgrounds').joinpath(name)

    
    if wallpaper_file.is_file():
        pass
    else:
        with open(wallpaper_file, 'wb') as f:
            f.write(requests.get(r_j).content)
    
    return name

def get_details(game):
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)

    lau_loc = data[game]["launcher_path"]
    gam_loc = data[game]["path"]
    gam_ver = data[game]["downloaded_version"] 
    ren_ver = data[game]["recent_version"] 
    
    return gam_ver, ren_ver, gam_loc, lau_loc

def get_res(game):
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)

    wd = data[game]["width"]
    hd = data[game]["height"]

    return wd, hd

def get_general():
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)

    default = data["general"]["first"]
    game_name = data["general"]["game"]
    wallpaper_name = data[game_name]["background_name"] 
    
    return game_name, wallpaper_name, default

def update_versions():
    res = None
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)

    for x in data:
        if x not in ["general","starrail", "zenless"]:
            r_v_a = data[x]["recent_version"]
            data[x]["recent_version"] = get_versions(data[x]["resource_url"])
            if r_v_a != data[x]["recent_version"]:
                res = 1 
    with open(config_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)
    
    return res

def update_wallpapers():
    res = None
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)
    
    for x in data:
        if x not in ["general","starrail","zenless"]:
            r_v_a = data[x]["background_name"]
            data[x]["background_name"] = get_wallpaper(data[x]["content_url"]) 
            if r_v_a != data[x]["background_name"]:
                res = 1 

    with open(config_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)      
    
    return res


def update_c_version():
    res = None
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)
    
    for x in data:
        if x not in ["general","starrail", "zenless"] and data[x]["path"] != "":
            file = pathlib.Path(data[x]["path"]).joinpath('config.ini')
            if file.exists() and file.is_file():
                parser = configparser.ConfigParser()
                parser.read(file, encoding='utf-8-sig')
                gameversion = parser.get('General', 'game_version')
                r_v_a = data[x]["downloaded_version"]
                data[x]["downloaded_version"] = gameversion
                if r_v_a != data[x]["downloaded_version"]:
                    res = 1 
            else:
                print(f"The configuration file for {x} could not be found.")
        elif x not in ["general","starrail", "zenless"] and data[x]["path"] == "None":
            print("The game path was not defined yet.")

    with open(config_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)
    
    return res

def define(game, param, value):
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)
    data[game][param] = value
    with open(config_file, "w") as jsonFile:
        json.dump(data, jsonFile, indent=2)

def read(game, param):
    config_file = pathlib.Path(__file__).parents[3].resolve().joinpath('AGL/settings.json')
    with open(config_file, "r") as jsonFile:
        data = json.load(jsonFile)
    return data[game][param]

if __name__ == "__main__":
    pass