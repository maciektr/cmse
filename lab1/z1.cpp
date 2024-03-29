#include<bits/stdc++.h>
using namespace std;


#define simple 1
#define recursive 2
#define kahan 3
// #define TIME recursive
// Defines if programme should run one method only
// Not defined means running all
// Usefull for the purpose of time measurement

#ifndef TIME
    // #define STEPS 25000     
#endif
// Defines number of steps after which sum error 
// should be printed in simple_sum algorithm
// Not defined means non should be printed


const float v = 0.63211;
const int N = 10000000;
float tab[N+5];


float simple_sum(){
    float res = 0.0;

    for(int i = 0; i<N; i++){
        #ifdef STEPS
        if(i % STEPS == 0)
            cout<<(v*(float)i - res)<<endl;
            // cout<< abs(v*(float)i - res)<<endl;
        #endif

        res += tab[i];
    }
    return res;
}

float recursive_sum(int a=0, int b=N){
    if(a==b)
        return tab[a];
    if(abs(a-b)==1)
        return tab[a]+tab[b];
    int s=(a+b)/2;
    return recursive_sum(a,s)+recursive_sum(s+1,b);
}

float kahan_sum(){
    float sum = 0.0f;
    float err = 0.0f;
    for (int i = 0; i < N; ++i) {
        float y = tab[i] - err;
        float temp = sum + y;
        err = (temp - sum) - y;
        sum = temp;
    }
    return sum;
}

int main(){
    // Fill tab with N values equal to v
    for(int i = 0; i<N; i++)
        tab[i] = v;

    #ifndef TIME
        #ifndef STEPS
            // Calculate precise value of sum
            const float precise = N*v; 

            float simple_res = simple_sum();
            float recursive_res = recursive_sum();
            float kahan_res = kahan_sum();

            cout<<fixed;
            cout<<"Wynik sumowania prostego: "<<simple_res<<endl;
            cout<<"Wynik sumowania rekursywnego: "<<recursive_res<<endl;
            cout<<"Wynik sumowania kahana: "<<kahan_res<<endl;
            cout<<endl;
            cout<<"Blad bezwzgledny sumowania prostego: "<<precise - simple_res<<endl;
            cout<<"Blad bezwzgledny sumowania rekursywnego: "<<precise - recursive_res<<endl;
            cout<<"Blad bezwzgledny sumowania kahana: "<<precise - kahan_res<<endl;
            cout<<endl;
            cout<<"Blad wzgledny sumowania prostego: "<<100*((precise - simple_res)/precise)<<'%'<<endl;
            cout<<"Blad wzgledny sumowania rekursywnego: "<<100*((precise - recursive_res)/precise)<<'%'<<endl;
            cout<<"Blad wzgledny sumowania kahana: "<<100*((precise - kahan_res)/precise)<<'%'<<endl;
        #else
            simple_sum();
        #endif
    #else 
        #if TIME == simple
            simple_sum();
        #endif 
        #if TIME == recursive
            recursive_sum();
        #endif
        #if TIME == kahan
            kahan_sum();
        #endif
    #endif

}
