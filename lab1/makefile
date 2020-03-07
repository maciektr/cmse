# Makefile

main: z1 z4 

z1:
	g++ -static -O2 z1.cpp -o z1.o

z4:
	g++ -static -O2 z4.cpp -o z4.o

debug:
	g++ -O2 -Wall -Wshadow -fsanitize=address z1.cpp -o z1.o
	g++ -O2 -Wall -Wshadow -fsanitize=address z4.cpp -o z4.o

time_simple: 
	g++ -DTIME=simple -O2 z1.cpp -o z1.o
	oiejq ./z1.o

time_recursive: 
	g++ -DTIME=recursive -O2 z1.cpp -o z1.o
	oiejq ./z1.o	

time_kahan: 
	g++ -DTIME=kahan -O2 -Wall z1.cpp -o z1.o
	oiejq ./z1.o	

time_z1: time_simple time_recursive time_kahan
	rm z1.o

steps:
	g++ -DSTEPS=25000 -O2 z1.cpp -o z1_steps.o	
	python plot_error.py
	rm z1_steps.o

bifurcation: z4
	rm -f plot_z4.png
	python plot_z4.py
	rm -f z4.o

plot: 
	g++ -DR=2.6 -static -O2 z4.cpp -o z4.o
	rm -f plot_z4.png plot_z4.gif
	python plot_z4.py -n
	rm -f z4.o