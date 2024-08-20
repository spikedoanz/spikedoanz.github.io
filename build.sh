#!/bin/bash

# build mal reviews
utils/mal/compile.py

# build and serve npx
npx quartz build --serve
