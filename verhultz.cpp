#include <cstdio>
#include <math.h>


int main (int argc, char* argv[])
{

  FILE* output;
  output = fopen("verhultz.txt","w");
  double tumor_size = 1;
  double tumor_evo;
  double a = 1;
  double b = 20;
  double step = 0.001;
  double i;

  for (i=0;i<10;i+=step)
    {
      tumor_evo = tumor_size * a * (1-(tumor_size/b));
      tumor_size += step*tumor_evo;
      fprintf(output,"%lg  %lg\n",i,tumor_size);
    }

  fclose(output);

}
