#!/usr/bin/python

import requests
import json
import random as rand
import argparse

STATUS = {"watching": 1,
          "finished": 2,
          "on-hold":  3,
          "dropped":  4,
          "ptw":      6}


def getArgs():
    parser = argparse.ArgumentParser(description="Get information about a user's watch list from MAL")
    parser.add_argument("user", help="Username from MAL", type=str)
    parser.add_argument("-s", "--status", help="Show only animes with this status", choices=STATUS.keys())
    parser.add_argument("-m", "--max-episodes", help="Show only animes with no more episodes than defined", type=int)
    parser.add_argument("-g", "--genre", help="Show only animes with this genre", type=str.title)
    parser.add_argument("-r", "--random", help="Show only one random anime from the available list", action="store_true")

    return parser.parse_args()


def validate(anime, args):
    if anime["anime_num_episodes"] == 0:
        return False

    if args.max_episodes is not None and anime["anime_num_episodes"] > args.max_episodes:
        return False

    if args.status is not None and anime["status"] != STATUS[args.status]:
        return False

    if args.genre is not None:
        found = False

        for g in anime["genres"]:
            if g["name"] == args.genre:
                found = True
                break
        if not found:
            return False

    return True


def getList(args):
    r = requests.get("https://myanimelist.net/animelist/{}/load.json".format(args.user))
    if not r:
        print("Error: could not fetch MAL info. Server responded with {} - {}".format(r.status_code, r.reason))
        exit()

    jsonObj = json.loads(r.text)
    jsonObj = [anime for anime in jsonObj if validate(anime, args)]

    if args.random is True:
        return rand.choice(jsonObj)
    else:
        return jsonObj


def printAnime(anime):
    if anime["anime_title_eng"] != "":
        title = anime["anime_title_eng"]
    else:
        title = anime["anime_title"]

    if anime["anime_num_episodes"] == 1:
        print("( film ) {}".format(title))
    else:
        print("({:2} eps) {}".format(anime["anime_num_episodes"], title))


if __name__ == '__main__':
    args = getArgs()

    for a in getList(args):
        printAnime(a)
