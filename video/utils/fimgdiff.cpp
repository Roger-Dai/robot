// fimgdiff.cpp
//
// compares two float images and outputs statistics if they differ

#include <math.h>
#include "imageLib.h"

void fimgdiff(CFloatImage im1, CFloatImage im2)
{
    CShape sh  = im1.Shape();
    CShape sh2 = im2.Shape();
    int w = sh.width, h = sh.height, nB = sh.nBands;
    int w2 = sh2.width, h2 = sh2.height, nB2 = sh2.nBands;

    if (sh != sh2) {
	fprintf(stderr, "differ in shape: ");
	fprintf(stderr, " %dx%d, nB=%d  vs.", w, h, nB);
	fprintf(stderr, " %dx%d, nB=%d\n", w2, h2, nB2);
	return;
    }

    float sumdiff = 0;
    int numdiff = 0;
    int numdiff1 = 0;
    int numgood = 0;
    int numoneinf = 0;
    int numbothinf = 0;
    
    int warnNaN = 5;

    for (int y = 0; y < h; y++) {
	for (int x = 0; x < w; x++) {
	    float d = 0;
	    int inf1 = 0, inf2 = 0;
	    for (int b = 0; b < nB; b++) {
		float f1 = im1.Pixel(x, y, b);
		float f2 = im2.Pixel(x, y, b);
		if (f1 == INFINITY) inf1 = 1;
		if (f2 == INFINITY) inf2 = 1;
		float a = 0;
		if (f1 == INFINITY || f2 == INFINITY)
		    a = 0; // don't count in difference
		else
		    a = fabs(f1 - f2);
		if (isnan(a)) {
		    if (warnNaN > 0) {
			fprintf(stderr, "Warning: vals at  %d, %d: %f %f\n", x, y, f1, f2);
			warnNaN--;
			if (warnNaN == 0)
			    fprintf(stderr, "...\n");
		    }
		    a = 0;
		}
		d += a;
	    }
	    d /= nB;
	    sumdiff += d;
	    if (d>0) numdiff++;
	    if (d>1) numdiff1++;
	    if (inf1 && inf2)
		numbothinf++;
	    else if (inf1 || inf2)
		numoneinf++;
	    else
		numgood++;
	}
    }
    float f = 100.0 / (w * h );
    if (numdiff == 0 && numoneinf == 0) {
	fprintf(stderr, "are identical\n");
    } else {
	float avgd = sumdiff / numgood;
	if (numdiff1 > 0) {
	    fprintf(stderr, "are different (mean diff = %.4g, %.4f%% of pixels differ by more than 1)\n",
		    avgd, f * numdiff1);
	} else {
	    fprintf(stderr, "are virtually identical (mean diff = %.4g)\n", avgd);
	}
    }
    fprintf(stderr, "INF: both:%.4f%%, neither:%.4f%%, disagree:%.4f%%\n", 
	    f * numbothinf, f * numgood, f * numoneinf);
}

int main(int argc, char *argv[])
{
    try {
	if (argc != 3)
	    throw CError("\n  usage: %s im1 im2\n", argv[0]);

	CFloatImage im1, im2;
	ReadImageVerb(im1, argv[1], 0);
	ReadImageVerb(im2, argv[2], 0);
	fprintf(stderr, "%s and %s ", argv[1], argv[2]);
	fimgdiff(im1, im2);
    }
    catch (CError &err) {
	fprintf(stderr, err.message);
	fprintf(stderr, "\n");
	return -1;
    }

    return 0;
}
