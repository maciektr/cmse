# Makefile

main: z1 z4 z3

z1:
	g++ -static -O2 z1.cpp -o z1.o

z3:
	g++ -static -O2 z3.cpp -o z3.o

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

plotting: 
	g++ -DR -static -O2 z4.cpp -o z4.o
	rm -f plot_z4.png plot_z4.gif

gif: plotting
	python plot_z4.py -n
	rm -f z4.o

plot: plotting 	
	python plot_z4.py -s
	rm -f z4.o

zero:
	g++ -DR -DZ -static -O2 z4.cpp -o z4.o
	./z4.o