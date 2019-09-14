#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double dist(int p, double ar1[], double ar2[]){
	double sqsum = 0.0;
	for (int i= 0;i<8;i++){
		sqsum += pow(abs(ar1[i]-ar2[i]),p);
	}
	ar1[8] = pow(sqsum,(double)1/p);
	// printf("%f\n", ar1[8]);
	return 0;
}


double** sort(double ar[][9], int l){
	double ** ar1 = (double **)malloc( sizeof (double * ) * l);
	for (int i = 0; i<l; i++){
		ar1[i] = (double*)malloc(sizeof(double)*9);
	}
	for (int i = 0;i < l; i++){
		for (int j = 0; j<9; j++){
			ar1[i][j] = ar[i][j]; 
		}
	}
	for(int i = 0;i<l-1;i++){
		double minm = ar1[i][8];
		int min_ind = i;
		for(int j = i+1;j<l;j++)
		{
			if(ar1[j][8]<minm)
			{
				minm = ar1[j][8];
				min_ind = j;
			}
		}
		if(min_ind != i){
			for(int k = 0;k < 9;k++){
				double temp = ar1[i][k];
				ar1[i][k] = ar1[min_ind][k];
				ar1[min_ind][k] = temp;
			}
		}
		
	}
	// printf("List1 \n");
	// for(int i=0;i<70;i++){
	// 	for(int j=0;j<9;j++){
	// 		printf("%f\t", ar[i][j]);
	// 	}
	// 	printf("\n");

	// }
	return ar1;
}



int training_validation(double list1[][9], double list2[][9], double list3[][9], int l){
	
	
	int best_p=0,best_k=0;
	int best_case = 0;
	double accuracy = 0;
	for(int p = 3;p<=8;p++){
		for (int k=3;k<=14;k++){
			int no_correct = 0;
			for (int i=0;i<l;i++){
				for(int j = 0;j<l;j++){
					dist(p,list1[j], list3[i]);
					dist(p,list2[j], list3[i]);
				// printf("%f \t %f\n", list1[i][8], list2[i][8]);
				}
				double lt[140][9];
				for (int z=0;z<70;z++){
					for (int z2=0;z2<9;z2++){
						lt[z][z2]=list1[z][z2];
						lt[70+z][z2]=list2[z][z2];
						// printf("Done%d",z);
					}
				}

				double** l1 = sort(lt, 140);
				// double** l2 = sort(list2, l);


				int class1=0,class2=0,class3=0;
				
				for(int m=0;m<=k;m++){
					if((int)l1[m][7]==1){
						class1++;

					}
					else if((int)l1[m][7]==2)
						class2++;
					else
						class3++;
				}

				int maxm = class1;
				if(class1>class2 && class1 > class3)
					maxm = 1;
				else if(class2> class3)
					maxm = 2;
				else
					maxm = 3;
				if (maxm == (int)list3[i][7])
					no_correct++;
				
			}

			if(no_correct>=best_case){
				best_case = no_correct;
				best_p=p;
				best_k = k;
				accuracy = (double)(no_correct*100/70.0);
			}
			printf("(%d,%d)\t%d\n",p,k,no_correct);
		}
	}
	printf("best k=%d\tbest p=%d\taccuracy=%lf\n",best_k, best_p, accuracy);
}








int main(){

	FILE *fp;
	int length;  // length of the dataset 


	fp = fopen("seeds_dataset.txt", "r");
	if (fp == NULL){
		printf("Error in opening this file");
		return 0;
	}
	printf("Enter the no. of instances : ");
	scanf("%d", &length);


	char buffer[1000];
	double dataset[length][9];
	int k = 0;



	while(fgets(buffer, 1000, fp) != NULL){

		char num[1000] = "";
		char empty[1000];
		int pointer1 = 0;
		int th_element = 0;
		for (int i = 0;i< strlen(buffer); i++){
			if(buffer[i] != '\t' && buffer[i] != '\n')
			{
				num[pointer1] = buffer[i];
				pointer1++;
			}
			else{
				dataset[k][th_element] =strtod(num, NULL);
				strcpy(num, empty);
				th_element++;
				pointer1=0;
			}
		}
		k++;
	}




	double list1[70][9], list2[70][9], list3 [70][9];
	int i1 = 0, i2 = 0, i3=0;

	for(int i= 0; i< length; i++)
	{

		if (i % 3 == 0){
			for (int j=0;j<8;j++)
				list1[i1][j]=dataset[i][j];
			i1++;
		}
		else if(i % 3 == 1){
			for (int j=0;j<8;j++)
				list2[i2][j]=dataset[i][j];
			i2++;
		}
		else if(i%3 == 2){
			for (int j=0;j<8;j++)
				list3[i3][j]=dataset[i][j];
			i3++;
		}
	}

	// printf("List1 \n");
	// for(int i=0;i<70;i++){
	// 	for(int j=0;j<8;j++){
	// 		printf("%f\t", list1[i][j]);
	// 	}
	// 	printf("\n");

	// }

	// printf("List2 \n");
	// for(int i=0;i<70;i++){
	// 	for(int j=0;j<8;j++){
	// 		printf("%f\t", list2[i][j]);
	// 	}
	// 	printf("\n");

	// }

	// printf("List3 \n");
	// for(int i=0;i<70;i++){
	// 	for(int j=0;j<8;j++){
	// 		printf("%f\t", list3[i][j]);
	// 	}
	// 	printf("\n");
	// }


	fclose(fp);

	printf("List 3 as validation");
	training_validation(list1,list2,list3,70);
	printf("List 1 as validation");
	training_validation(list2,list3,list1,70);
	printf("List 2 as validation");
	training_validation(list3,list1,list2,70);

	return 0;
}

