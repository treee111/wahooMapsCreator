#!/usr/bin/python

import argparse
import sys
import time


class MapFileReader:
    def __init__(self, filename) -> None:
        self.mapFile = open(filename, "rb")

    def close(self):
        self.mapFile.close()

    def readMagic(self):
        return self.mapFile.read(20).decode('utf-8')

    def readByte(self):
        return self.mapFile.read(1)[0]

    def readShort(self):
        b = self.mapFile.read(2)
        return b[0] << 8 | b[1]

    def readInt(self):
        b = self.mapFile.read(4)
        return b[0] << 24 | b[1] << 16 | b[2] << 8 | b[3]

    def readDegrees(self):
        return float(self.readInt())/1000000

    def readLong(self):
        b = self.mapFile.read(8)
        return b[0] << 56 | b[1] << 48 | b[2] << 40 | b[3] << 32 | b[4] << 24 | b[5] << 16 | b[6] << 8 | b[7]

    def readVBEU(self):
        res, shift, buf = 0, 0, 0
        while True:
            buf = int.from_bytes(self.mapFile.read(1), byteorder="big")
            if (buf & 0x80) == 0:
                break

            res |= (buf & 0x7f) << shift
            shift += 7

        return res | (buf << shift)

    def readString(self):
        return self.mapFile.read(self.readVBEU()).decode('utf-8')

    def readTags(self):
        amount = self.readShort()
        tags = []
        for _ in range(amount):
            tags.append(self.readString())

        return tags

    def readZoomIntervals(self):
        amount = self.readByte()
        intervals = []
        for _ in range(amount):
            values = (
                self.readByte(),
                self.readByte(),
                self.readByte(),
                self.readLong(),
                self.readLong(),
            )
            intervals.append(values)
        return intervals


def main(args):
    r = MapFileReader(args.mapfile)

    magic = r.readMagic()
    print("Magic:", magic)
    if magic != "mapsforge binary OSM":
        print("invalid magic bytes")
        sys.exit(1)

    print("Header size:", r.readInt())
    print("File version:", r.readInt())
    print("File size:", r.readLong())
    print("Date of creation:", time.ctime(r.readLong()/1000))
    print("Bounding box:")
    print(
        " - minLat: {:f} minLon: {:f}".format(r.readDegrees(), r.readDegrees()))
    print(
        " - maxLat: {:f} maxLon: {:f}".format(r.readDegrees(), r.readDegrees()))
    print("Tile size:", r.readShort())
    print("Projection:", r.readString())

    flags = r.readByte()
    print("Flags: {:08b}".format(flags))
    if (flags & 0x80) != 0:
        print(" - Debug file")
    if (flags & 0x40) != 0:
        print(
            " - Map start position: lat: {:f} lon: {:f}", r.readDegrees(), r.readDegrees())
    if (flags & 0x20) != 0:
        print(" - Start zoom level", r.readByte())
    if (flags & 0x10) != 0:
        print(" - Languages", r.readString())
    if (flags & 0x08) != 0:
        print(" - Comment", r.readString())
    if (flags & 0x04) != 0:
        print(" - Created by", r.readString())

    poiTags = r.readTags()
    print("Poi tags:", len(poiTags))
    if args.pois:
        for tag in poiTags:
            print(" -", tag)

    wayTags = r.readTags()
    print("Way tags:", len(wayTags))
    if args.ways:
        for tag in wayTags:
            print(" -", tag)

    zoomIntervals = r.readZoomIntervals()
    print("Zoom intervals:", len(zoomIntervals))
    if args.zoom_intervals:
        for zi in zoomIntervals:
            print(
                " - Base: {} Min: {} Max: {} Pos: {} Size: {}".format(zi[0], zi[1], zi[2], zi[3], zi[4]))

    r.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', "--pois", help="show poi tags", action="store_true")
    parser.add_argument(
        '-w', "--ways", help="show way tags", action="store_true")
    parser.add_argument('-z', "--zoom-intervals",
                        help="show zoom intervals", action="store_true")
    parser.add_argument('mapfile', help='map file')
    main(parser.parse_args())
