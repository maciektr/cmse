#include<bits/stdc++.h>
using namespace std;

const float x_0 = 0.77;
const int N = 100;

// #define R 1.

int main(){
    ios_base::sync_with_stdio(0),cin.tie(0),cout.tie(0);
    float x = x_0;
    #ifdef R
        for(int i = 0; i<N; i++){
            cout<<x<<endl;
            x = ((float)R)*(x)*(1.-x);
        }
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