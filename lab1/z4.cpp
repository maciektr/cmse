#include<bits/stdc++.h>
using namespace std;

const float x_0 = 0.8;
const int N = 100;

// #define R 

int main(){
    ios_base::sync_with_stdio(0),cin.tie(0),cout.tie(0);
    float x = x_0;
    #ifdef R
        #ifdef Z
            // Find number of steps when logistic map zeros
            const float r = 4.;
            const float eps = 5.5e-6;
            int res = 0;
            while(x > eps){
                x = r*x*(1-x);
                res++;
            }
            cout<<res<<endl;
        #else
            for(float r = 1.; r < 4.; r+=1e-2){
                x = x_0;
                for(int i = 0; i < N; i++){
                    cout<<x<<endl;
                    x = r*x*(1-x);
                }
            }
        #endif
        // for(int i = 0; i<N; i++){
        //     cout<<x<<endl;
        //     x = ((float)R)*(x)*(1.-x);
        // }
        
    #else
        for(float r = 1.; r < 4.; r+=1e-3){
            x = x_0;
            for(int i = 0; i < N+10; i++){
                if(i>=N)
                    cout<<x<<endl;
                x = r*x*(1-x);
            }
        }
    #endif

}