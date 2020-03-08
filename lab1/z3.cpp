#include<bits/stdc++.h>
using namespace std;

double c_wprzod(const double s, const int n){
    double res = 0;
    for(int i = 1; i<=n; i++){
        res += 1.0/pow(i,s);
    }
    return res;
}
double c_wstecz(const double s, const int n){
    double res = 0.0;
    for(int i = n; i>0; i--){
        res += 1.0/pow(i,s);
    }
    return res;
}

double n_wprzod(const double s, const int n){
    double res = 0.0;
    for(int i = 1 ; i<=n; i++){
        res+=(pow(-1.0,i-1)/pow(i,s));
    }
    return res;
}
double n_wstecz(const double s, const int n){
    double res = 0.0;
    for(int i = n ; i>0; i--){
        res+=(pow(-1.0,i-1)/pow(i,s));
    }
    return res;
}
int main(){
    cout<<fixed;
    const double s[] = {2,3.6667,5,7.2,10};
    const int n[] = {50,100,200,500,1000};
    for(int k = 0; k<5; k++)
        for(int i = 0; i<5; i++){
            cout<<"s = "<<s[i]<<" | n = "<<n[k]<<endl;
            cout<<"zeta wprzod: "<<c_wprzod(s[i],n[k])<<endl
                <<"zeta wstecz: "<<c_wstecz(s[i],n[k])<<endl;
            cout<<"eta wprzod: "<<n_wprzod(s[i],n[k])<<endl
                <<"eta wstecz: "<<n_wstecz(s[i],n[k])<<endl;
            cout<<endl;
        }
}