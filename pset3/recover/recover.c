// https://docs.cs50.net/2019/x/psets/3/recover/recover.html
// Implement a program that recovers JPEGs from a forensic image.

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");

        return 1;
    }

    // remember filename
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");

    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);

        return 2;
    }

    // create output file
    FILE *outptr = NULL;

    // buffer and filename arrays
    unsigned char buffer[512];
    char filename[8];

    // filename counter
    int counter = 0;

    // do we currently have found a jpg?
    int foundjpeg = 0;

    // read the file
    while (fread(buffer, 512, 1, inptr) == 1)
    {
        // compare the first four bytes with a JPEG header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if we were already on a JPEG, close the previous file pointer because we have found a new JPEG
            if (foundjpeg)
            {
                fclose(outptr);
            }
            else
                // if we have found a new JPEG, open a file pointer in write mode
            {
                foundjpeg = 1;
            }

            sprintf(filename, "%03i.jpg", counter);
            outptr = fopen(filename, "w");
            counter++;
        }

        // if we currently are on a JPEG and found a new 512 bytes block, write it
        if (foundjpeg)
        {
            fwrite(&buffer, 512, 1, outptr);
        }
    }

    // close all file pointers
    fclose(inptr);
    fclose(outptr);

    return 0;
}
