#include <bits/stdc++.h>
#define FOR(i,a,b) for(int i=(a); i<(b); i++)
using namespace std;

const int maxN = 1e5+2, maxA = 1e3+1, logMil = 200;
bool notPrime[maxA];
int A[maxN], res[maxN], comp[maxN], sieved[logMil], sn, cn, k, n;

// Sàng 1000 số đầu cho việc chia lên
void sieve() {
    notPrime[0] = notPrime[1] = true;
    for(int i = 2; i * i < maxA; i++) {
        if(notPrime[i]) continue;
        for(int j = i * i; j < maxA; j += i)
            notPrime[j] = true;
    }

    for(int i = 2; i < maxA; i++) {
        cout << i << ' ';
        if(!notPrime[i]) sieved[sn++] = i;
    }
}

int main() {
    sn = 0;
    cout << "Hello\n";
    sieve();
    cout << "Hello\n";
    memset(res, 0x3f, sizeof(res));

    cin.tie(0) -> sync_with_stdio(0);
    cin >> n; k = n;
    FOR(i, 0, n) cin >> A[i];

    cout << "Hello\n";

    FOR(p, 0, sn) {
        int pr = sieved[p]; // Số nguyên tố hiện tại
        int j = 0; // Trỏ lưu vị trí đúng sau xóa
        FOR(i, 0, k) {
            // Duyệt dãy A, Nếu hợp số thì dọn khỏi dãy và bỏ vô xử lí
            if(A[i] % pr == 0) {
                comp[cn++] = i;
                A[i] /= pr;
            }
            if(A[i] != 1) j++; // Nếu hết thì ném đi, không thì giữ lại
            A[j] = A[i];
        }
        cout << "Hello " << p << "\n";
        k -= cn; // Rút gọn kích thước dãy lại do xóa lười rồi
        FOR(i, 0, cn) {
            int close = res[comp[i]];
            if(i != 0) close = min(close, comp[i] - comp[i-1]);
            if(i != cn-1) close = min(close, comp[i] - comp[i-1]);
            res[comp[i]] = close;
        }
        cn = 0; // Dọn mảng đánh dấu
    }
    FOR(i, 0, n) cout << ((res[i] > 999999)? -1: res[i]);
}