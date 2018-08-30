# -*- coding: utf-8 -*-   

import os


def file_name(dir, reg):
    L = []
    for root, dirs, files in os.walk(dir):
        if "." not in os.path.basename(root):
            for file in files:
                if os.path.splitext(file)[1] == reg:
                    L.append(os.path.join(root, file))
    return L
