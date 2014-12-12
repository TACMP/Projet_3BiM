#include <cstdio>
#include <math.h>


int main (int argc, char* argv[])
{

  FILE* output;
  output = fopen("gompertz.txt","w");
  double tumor_size = 1;
  double tumor_evo;
  double a = 1;         // grow speed
  double b = 20;        // maximum size
  double step = 0.001;
  double i;

  for (i=0;i<10;i+=step)
    {
      tumor_evo = tumor_size * a * log(b/(tumor_size));
      tumor_size += step*tumor_evo;
      fprintf(output,"%lg  %lg\n",i,tumor_size);
    }

  fclose(output);

}
