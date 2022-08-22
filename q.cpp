#include<iostream>
using namespace std;

template <class T> void maxval(T a,T b);
int main(){
    int a,b;
    cin>>a>>b;
    maxval<int>(a,b);
    return 0;
}

template <class T>
void maxval(T a,T b){
    cout<<max(a,b);
}
