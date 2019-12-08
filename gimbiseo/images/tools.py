#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import numpy as np

im = Image.open('logo.png')

im = im.resize((60,60))
im.save('logo.png')
