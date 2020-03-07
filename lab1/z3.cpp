#include<bits/stdc++.h>
using namespace std;

float c_wprzod(const float s, const int n){
    float res = 0;
    // cout<<1.0/pow(50,2)<<endl;
    for(int i = 0; i<n; i++){
        float k = 1.0/powf(i,s);
        cout<<k<<" : "<<res<<endl;
        res = res + k;
    }
    return res;
}
float c_wstecz(const float s, const int n){
    float res = 0.0;
    for(int i = n-1; i>=0; i--){
        res += 1.0/powf(i,s);
    }
    return res;
}

float n_wprzod(const float s, const int n){
    float res = 0.0;
    for(int i = 0 ; i<n; i++){
        res+=(powf(-1.0,i-1)/powf(i,s));
    }
    return res;
}
float n_wstecz(const float s, const int n){
    float res = 0.0;
    for(int i = n-1 ; i>=9; i--){
        res+=(powf(-1.0,i-1)/powf(i,s));
    }
    return res;
}
int main(){
    const float s = 2;
    // const float s = 3.6667;
    // const float s = 5;
    // const float s = 7.2;
    // const float s = 10;

    const int n = 50;
    // const int n = 100;
    // const int n = 200;
    // const int n = 500;
    // const int n = 1000;

    cout<<"c_ w przod: "<<c_wprzod(s,n)<<endl<<"c_ wstecz: "<<c_wstecz(s,n)<<endl;
    // cout<<"n_ w przod: "<<n_wprzod(s,n)<<endl<<"n_ wstecz: "<<n_wstecz(s,n)<<endl;
}