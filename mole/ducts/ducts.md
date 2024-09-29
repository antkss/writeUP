# write up ducts 
- bài bao gồm có hàm talk dùng để tương tác chính và 1 hàm backend, hàm backend nhận buffer từ hàm talk, hàm talk sử dụng fork() để có thể listen được nhiều connection cùng 1 lúc, nhưng tuy nhiên sử dụng chung 1 pipe nên gây ra lỗi
- 
