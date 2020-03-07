#include<bits/stdc++.h>
using namespace std;

// const float r = 3.7;
const float x_0 = .7; //0.66666
const int N = 100;

int main(){
    ios_base::sync_with_stdio(0),cin.tie(0),cout.tie(0);
    for(float r = 1.; r < 4.; r+=1e-4){
        float x = x_0;
        for(int i = 0; i < N+10; i++){
             if(i>=N)
                cout<<x<<endl;
            x = r*x*(1-x);
        }
    }

}