// imginfo.cpp
//
// Print width, height, and nBands of input image to stdout

#include "imageLib.h"

#define VERBOSE 1

int main(int argc, char *argv[])
{
    try {
	if (argc != 2)
	    throw CError("\n  usage: %s imagefile\n", argv[0]);

	CByteImage im;
	ReadImageVerb(im, argv[1], VERBOSE);
	CShape sh = im.Shape();
	printf("width = %d, height = %d, nBands = %d\n", 
	       sh.width, sh.height, sh.nBands);
    }
    catch (CError &err) {
	fprintf(stderr, err.message);
	fprintf(stderr, "\n");
	return -1;
    }

    return 0;
}
