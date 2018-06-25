// imgdiff.cpp
//
// compares two images and outputs statistics if they differe

#include "imageLib.h"

void imgdiff(CByteImage im1, CByteImage im2)
{
    CShape sh  = im1.Shape();
    CShape sh2 = im2.Shape();
    int w = sh.width, h = sh.height, nB = sh.nBands;
    int w2 = sh2.width, h2 = sh2.height, nB2 = sh2.nBands;

    if (sh != sh2) {
	fprintf(stderr, "differ in shape: ");
	fprintf(stderr, " %dx%d,nB=%d  vs.", w, h, nB);
	fprintf(stderr, " %dx%d, nB=%d\n", w2, h2, nB2);
	return;
    }

    int sumdiff = 0;
    int numdiff = 0;
    int numdiff1 = 0;

    for (int y = 0; y < h; y++) {
	for (int x = 0; x < w; x++) {
	    int d = 0;
	    for (int b = 0; b < nB; b++) {
		int a = im1.Pixel(x, y, b) - im2.Pixel(x, y, b);
		d += (a < 0? -a : a);
	    }
	    d /= nB;
	    sumdiff += d;
	    if (d>0) numdiff++;
	    if (d>1) numdiff1++;
	}
    }
    if (numdiff == 0) {
	fprintf(stderr, "are identical\n");
    } else {
	int pd = (int)(0.5 + (100.0 * numdiff1 / (w*h)));
	float avgd = (float)sumdiff / (w*h);
	if (numdiff1 > 0) {
	    fprintf(stderr,
 "are different (mean diff = %.2g, %d%% of pixels differ by more than 1)\n",
		    avgd, pd);
	} else {
	    fprintf(stderr, "are virtually identical (mean diff = %.2g)\n",
		    avgd);
	}
    }
}

int main(int argc, char *argv[])
{
    try {
	if (argc != 3)
	    throw CError("\n  usage: %s im1 im2\n", argv[0]);

	CByteImage im1, im2;
	ReadImageVerb(im1, argv[1], 0);
	ReadImageVerb(im2, argv[2], 0);
	fprintf(stderr, "%s and %s ", argv[1], argv[2]);
	imgdiff(im1, im2);
    }
    catch (CError &err) {
	fprintf(stderr, err.message);
	fprintf(stderr, "\n");
	return -1;
    }

    return 0;
}
