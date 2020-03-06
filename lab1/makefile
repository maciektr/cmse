# Makefile


main: 
	g++ -static -O2 z1.cpp -o z1.o

debug:
	g++ -O2 -Wall -Wshadow -fsanitize=address z1.cpp -o z1.o

time_simple: 
	g++ -DTIME=simple -O2 z1.cpp -o z1.o
	oiejq ./z1.o

time_recursive: 
	g++ -DTIME=recursive -O2 z1.cpp -o z1.o
	oiejq ./z1.o	

time_kahan: 
	g++ -DTIME=kahan -O2 -Wall z1.cpp -o z1.o
	oiejq ./z1.o	

time: time_simple time_recursive time_kahan
	rm z1.o

steps:
	g++ -DSTEPS=25000 -O2 z1.cpp -o z1_steps.o	
	python plot_error.py
	rm z1_steps.o