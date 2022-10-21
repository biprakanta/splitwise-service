import json
import os

from .consts import FunctionsConsts


def get_build_info():
    # the programs searches for build.info in 2 locations before returning BuildInfoNotFound
    fname = "./build_info.json"
    fname1 = "/app/build_info.json"
    file = None
    build_meta = {
        FunctionsConsts.VERSION: "BuildInfoNotFound",
    }
    try:
        if os.path.isfile(fname):
            file = fname
        elif os.path.isfile(fname1):
            file = fname1
        else:
            return build_meta
        with open(file, "r") as input_file:

            build_json = json.loads(input_file.read())
            build_meta[FunctionsConsts.VERSION] = build_json.get(
                FunctionsConsts.VERSION
            )
            return build_meta
    except:
        return build_meta
