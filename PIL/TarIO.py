#
# The Python Imaging Library.
# $Id: TarIO.py 2134 2004-10-06 08:55:20Z fredrik $
#
# read files from within a tar file
#
# History:
# 95-06-18 fl   Created
# 96-05-28 fl   Open files in binary mode
#
# Copyright (c) Secret Labs AB 1997.
# Copyright (c) Fredrik Lundh 1995-96.
#
# See the README file for information on usage and redistribution.
#

import ContainerIO

##
# A file object that provides read access to a given member of a TAR
# file.

class TarIO(ContainerIO.ContainerIO):

    ##
    # Create file object.
    #
    # @param tarfile Name of TAR file.
    # @param file Name of member file.

    def __init__(self, tarfile, file):

        fh = open(tarfile, "rb")

        while 1:

            s = fh.read(512)
            if len(s) != 512:
                raise IOError("unexpected end of tar file")

            name = s[:100]
            i = name.find(b'\x00')
            if i == 0:
                raise IOError("cannot find subfile")
            if i > 0:
                name = name[:i]

            size = int(s[124:136], 8)

            if file == name:
                break

            fh.seek((size + 511) & (~511), 1)

        # Open region
        ContainerIO.ContainerIO.__init__(self, fh, fh.tell(), size)
