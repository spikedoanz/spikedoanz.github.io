import matplotlib.font_manager

# List all available fonts
font_list = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
for font in font_list:
    print(font)
