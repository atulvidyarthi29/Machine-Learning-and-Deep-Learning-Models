#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


typedef
struct instance{
	int ar[64];
	int label;
	double distance;
}INSTANCE;



double dist(int p, INSTANCE ar1, INSTANCE ar2){
	double sqsum = 0.0;
	for (int i= 0;i<64;i++){
		sqsum += pow(abs(ar1.ar[i]-ar2.ar[i]),p);
	}
	ar1.distance = pow(sqsum,(double)1/p);
	// printf("%lf\n", ar1.distance);
	return 0;
}


INSTANCE* sort(INSTANCE array[], int l){
	INSTANCE* ar1;
	for (int i = 0;i < l; i++){
		for (int j = 0; j<64; j++){
			ar1[i].ar[j] = array[i].ar[j]; 
		}
		ar1[i].label= array[i].label;
		ar1[i].distance = array[i].distance;
	}

	for(int i = 0;i<l-1;i++){
		double minm = ar1[i].distance;
		int min_ind = i;
		for(int j = i+1;j<l;j++)
		{
			if(ar1[j].distance < minm)
			{
				minm = ar1[j].distance;
				min_ind = j;
			}
		}
		if(min_ind != i){
			for(int k = 0;k < 64;k++){
				int temp = ar1[i].ar[k];
				ar1[i].ar[k] = ar1[min_ind].ar[k];
				ar1[min_ind].ar[k] = temp;
			}
			int temp =	ar1[i].label;
			ar1[i].label = ar1[min_ind].label;
			ar1[min_ind].label = temp;

			int temp2 =	ar1[i].distance;
			ar1[i].distance = ar1[min_ind].distance;
			ar1[min_ind].distance = temp2;
		}
	}
	return ar1;
}



int training_validation(INSTANCE list1[], INSTANCE list2[], INSTANCE list3[], int l){
	INSTANCE merged[2*l];
	for(int s=0;s<l;s++){
		for(int t=0;t<64;t++){
			merged[s].ar[t] = list1[s].ar[t];
			merged[s+l].ar[t] = list2[s].ar[t];
		}
		merged[s].label = list1[s].label;
		merged[s+l].label =  list2[s].label;
	}

	int best_p=0,best_k=0;
	int best_case = 0;
	double accuracy = 0;
	for(int p = 1;p<=8;p++){
		for (int k=3;k<=14;k++){
			int no_correct = 0;
			for (int i=0;i<l;i++){
				for(int j = 0;j<2*l-1;j++){
					dist(p,merged[j], list3[i]);
					printf("%ddone\n",j);
				}

				INSTANCE* l1 = sort(merged, 2*l);

				for(int b=0;b<2*l;b++){
					for(int d=0;d<64;d++){
						printf("%d,",l1[b].ar[d]);
					}
					printf("%d\n", l1[b].label);
				}

				// int class1=0,class2=0,class3=0;
				
				// for(int m=0;m<=k;m++){
				// 	if((int)l1[m][7]==1){
				// 		class1++;

				// 	}
				// 	else if((int)l1[m][7]==2)
				// 		class2++;
				// 	else
				// 		class3++;
				// }
				// for(int m=0;m<=k;m++){
				// 	if((int)l2[m][7]==1){
				// 		class1++;
				// 		// printf("1gcfh");
				// 	}
				// 	else if((int)l2[m][7]==2)
				// 		class2++;
				// 	else
				// 		class3++;
				// }


				// int maxm = class1;
				// if(class1>class2 && class1 > class3)
				// 	maxm = 1;
				// else if(class2> class3)
				// 	maxm = 2;
				// else
				// 	maxm = 3;
				// if (maxm == (int)list3[i][7])
				// 	no_correct++;
				// printf("(%d,%d)\t%d\n",p,k,no_correct);
			}

			// if(no_correct>=best_case){
			// 	best_case = no_correct;
			// 	best_p=p;
			// 	best_k = k;
			// 	accuracy = (double)(no_correct*100/70.0);
			// }
		}
	}
	printf("best k=%d\tbest p=%d\taccuracy=%lf\n",best_k, best_p, accuracy);
}








int main(){

	FILE *fp;
	int length;  // length of the dataset 


	fp = fopen("optdigits.tra", "r");
	if (fp == NULL){
		printf("Error in opening this file");
		return 0;
	}
	printf("Enter the no. of instances : ");
	scanf("%d", &length);


	char buffer[1000];
	INSTANCE instance[length];

	int k = 0;
	while(fgets(buffer, 1000, fp) != NULL){
		char num[1000] = "";
		char empty[1000];
		int pointer1 = 0;
		int th_element = 0;
		for (int i = 0;i< strlen(buffer); i++){
			if(buffer[i] != ',' && buffer[i] != '\n')
			{
				num[pointer1] = buffer[i];
				pointer1++;
			}
			else{
				if (th_element<=63)
					instance[k].ar[th_element] =strtod(num, NULL);
				else if (th_element == 64)
					instance[k].label=strtod(num, NULL);
				strcpy(num, empty);
				th_element++;
				pointer1=0;
			}
		}
		k++;
	}


	

	int list_instance = floor(length/3);
	printf("%d", list_instance);


	INSTANCE list1[list_instance], list2[list_instance], list3 [list_instance];
	int i1 = 0, i2 = 0, i3=0;

	for(int i= 0; i< length; i++)
	{
		if (i % 3 == 0){
			for (int j=0;j<64;j++)
				list1[i1].ar[j]= instance[i].ar[j];
			list1[i1].label = instance[i].label;
			i1++;
		}
		else if(i % 3 == 1){
			for (int j=0;j<64;j++)
				list2[i2].ar[j]= instance[i].ar[j];
			list2[i2].label = instance[i].label;
			i2++;
		}
		else if(i%3 == 2){
			for (int j=0;j<64;j++)
				list3[i3].ar[j]= instance[i].ar[j];
			list3[i3].label = instance[i].label;
			i3++;
		}
	}

	// printf("List1\n");
	// for (int i= 0;i <list_instance; i++){
	// 	for(int j= 0;j<64;j++){
	// 		printf("%d", list1[i].ar[j]);
	// 	}
	// 	printf("%d\n", list1[i].label);
	// }


	// printf("List2\n");
	// for (int i= 0;i <list_instance; i++){
	// 	for(int j= 0;j<64;j++){
	// 		printf("%d", list2[i].ar[j]);
	// 	}
	// 	printf("%d\n", list2[i].label);
	// }


	// printf("List3\n");
	// for (int i= 0;i <list_instance; i++){
	// 	for(int j= 0;j<64;j++){
	// 		printf("%d", list3[i].ar[j]);
	// 	}
	// 	printf("%d\n", list3[i].label);
	// }

	fclose(fp);

	printf("List 3 as validation");
	training_validation(list1,list2,list3,list_instance);
	// printf("List 1 as validation");
	// training_validation(list2,list3,list1,list_instance);
	// printf("List 2 as validation");
	// training_validation(list3,list1,list2,list_instance);

	return 0;
}

