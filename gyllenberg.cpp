/* 
-------------------------------------------------------------------------------------------------------------
Gyllenberg-Webb
-------------------------------------------------------------------------------------------------------------
dpc = [b - ro(tc)]*pc + ri(tc)*qc
dqc = ro(tc)*pc - [ri(tc) + mu]*qc
tc = pc + qc;
-------------------------------------------------------------------------------------------------------------



In this model, if mu = 0, quiescent cells and necrosed (dead) cells both fall under the 'quiescent' category
*/


#include <cstdio>
#include <math.h>


// evaluating dpc according to Gyllenberg-Webb model
double dpc_evaluate (double, double, double, double, double, double);


// evaluating dqc according to Gyllenberg-Webb model
double dqc_evaluate (double, double, double, double, double, double, double);


// function corresponding to the cell transformation rate from proliferent to quiescent
// params : total number of cells (variable of the function), b (growth factor) ; and alpha and teta from gompertz or verhulst model
double ro_evaluate (double, double, double, double);  


// function corresponding to the cell transformation rate from quiescent to proliferent
// params : total number of cells (variable of the function)
double ri_evaluate (double);  



int main (int argc, char* argv[])
{

  FILE* output;
  output = fopen("gyllenberg.txt","w");

  double scheme = 0;       // defines which scheme will be used to solve the equations (0 = Euler expl., 1 = Heun (trapeziums))

  double ipc = 1;          // initial number of proliferating cells
  double iqc = 1;          // initial number of quiescent cells
  double itc = ipc + iqc;  // initial total number of cells
  double pc = ipc;         // number of proliferating cells
  double qc = iqc;         // number of quiescent cells
  double tc = pc + qc;     // total number of cells
  //double dpc;              // pc derivative
  //double dqc;              // qc derivative

  double temp_pc;          // temporary approximation of pc (used for trapezium method)
  double temp_qc;          // temporary approximation of qc
  double temp_tc;          // temporary approximation of tc


  // implicit parameters if using gompertz or verhuslt as the ro function
  double alpha = 0.1;       // growth factor
  double teta = 1000000;     // maximum tumor size


  double b;              // effective growth factor (births - deaths)
  double mu = 0;         // death rate of quiescent cells (equals 0 if quiescent cells and necrosed (dead) cells both fall under the 'quiescent' category)

  double step = 0.01;
  double i;
  double length = 10;    // simulation length


  // specific parameter initialization

  // if using a gompertz model as the ro function
  b = alpha * (itc/ipc) * log(teta/itc);


  for (i=0;i<length;i+=step)
    {
      //dpc = pc * (b - ro_evaluate(tc,b,alpha,teta)) + qc * ri_evaluate(tc);
      //dqc = pc * ro_evaluate(tc,b,alpha,teta) - qc * (mu + ri_evaluate(tc));

      if (scheme == 0)
        {
          // Using explicit version of Euler
          pc += step * dpc_evaluate(pc, qc, tc, b, alpha, teta);
          qc += step * dqc_evaluate(pc, qc, tc, b, alpha, teta, mu);
          tc = pc + qc;
        }

      if (scheme == 1)
        {
          // Using method of trapeziums (Heun's scheme)
          temp_pc = pc + step * dpc_evaluate(pc, qc, tc, b, alpha, teta);
          temp_qc = qc + step * dqc_evaluate(pc, qc, tc, b, alpha, teta, mu);
          temp_tc = temp_pc + temp_qc;
          pc += (step/2) * ( dpc_evaluate(pc, qc, tc, b, alpha, teta) + dpc_evaluate(temp_pc, temp_qc, temp_tc, b, alpha, teta) );
          qc += (step/2) * ( dqc_evaluate(pc, qc, tc, b, alpha, teta, mu) + dqc_evaluate(temp_pc, temp_qc, temp_tc, b, alpha, teta, mu) );
          tc = pc + qc;
        }   

      fprintf(output,"%lg  %lg  %lg  %lg\n",i,pc,qc,tc);
    }

  fclose(output);

  return 0;

}


double dpc_evaluate (double pc, double qc, double tc, double b, double alpha, double teta)
{

  return (pc * (b - ro_evaluate(tc,b,alpha,teta)) + qc * ri_evaluate(tc));

}


double dqc_evaluate (double pc, double qc, double tc, double b, double alpha, double teta, double mu)
{

  return (pc * ro_evaluate(tc,b,alpha,teta) - qc * (mu + ri_evaluate(tc)));

}




double ro_evaluate (double value, double b, double alpha, double teta)
{

  // if using a gompertz model as the ro function
  return (alpha * (1 - log(teta/value)) + b);
}


double ri_evaluate (double value)
{


  /* basic case : no quiescent cells turn to proliferating cells ;
     it corresponds to the situation where quiescent cells are actually all necrosed (dead) 
  */
  return 0;
}
