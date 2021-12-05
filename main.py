import requests
import os
from PIL import Image
import math

def download_tile(x, y, z):
    url = "https://khms.google.com/kh/v=908?x=" + str(x) + "&y=" + str(y) + "&z=" + str(z)
    imagefile = requests.get(url)
    try:
        os.mkdir("./tiles/")
    except:
        q = 0
    filename = './tiles/tile_' + str(x) + '_' + str(y) + '_' + str(z) + '.jpeg'
    open(filename, 'wb').write(imagefile.content)
    print("Downloading:", filename)

def dl_all_tiles_from_zoom(zoom, stitch=False):
    xtile = 0
    ytile = 0
    max_tile = 2**zoom-1
    while xtile <= max_tile:
        while ytile <= max_tile:
            download_tile(xtile, ytile, zoom)
            ytile += 1
        ytile = 0
        xtile += 1
    print("Finished downloading files.")

def stitch_tiles(x, y, size, z):
    width = size * 256
    height = size * 256
    max_x = x + size - 1
    max_y = y + size - 1
    x2 = x
    y2 = y
    progress = 0
    total = size*size
    output = Image.new(mode = "RGB", size = (width, height))
    while x2 <= max_x:
        while y2 <= max_y:
            img = Image.open('tiles/tile_' + str(x2) + '_' + str(y2) + '_' + str(z) + '.jpeg')
            position_x = (x2 - x) * 256
            position_y = (y2 - y) * 256
            output.paste(img, (position_x, position_y))
            y2 += 1
            progress += 1
            print("Stitching:", str(progress) + "/" + str(total))
        y2 = y
        x2 += 1
    print("Writing stitched image to file...")
    output.save('stitched.jpg')
    print("Done stitching images.")

def dl_square(x, y, z, size):
    max_x = x + size - 1
    max_y = y + size - 1
    y2 = y
    while x <= max_x:
        while y <= max_y:
            download_tile(x, y, z)
            y += 1
        y = y2
        x += 1

def latlong_to_xy(lat, lon, zoom):
    lonRad = math.radians(lon)
    latRad = math.radians(lat)
    columnIndex = lonRad
    rowIndex = math.log(math.tan(latRad) + (1.0 / math.cos(latRad)))
    columnNormalized = (1 + (columnIndex / math.pi)) / 2
    rowNormalized = (1 - (rowIndex / math.pi)) / 2
    tilesPerRow = 2 ** zoom
    column = round(columnNormalized * (tilesPerRow - 1))
    row = round(rowNormalized * (tilesPerRow - 1))
    return [column, row]

lat = float(input("Enter latitude:"))
longi = float(input("Enter longitude:"))
zoom = int(input("Enter zoom level:"))
size_deg = float(input("Enter size in longitute degrees:"))
size = int(size_deg * 2 ** zoom / 360)
coords = latlong_to_xy(lat, longi, zoom)
dl_square(coords[0], coords[1], zoom, size)
stitch_tiles(coords[0], coords[1], size, zoom)