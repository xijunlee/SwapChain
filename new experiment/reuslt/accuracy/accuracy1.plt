set size ratio 0.8
aqua = "#00FFFF"; azure = "#F0FFFF";
aliceblue = "#F0F8FF"

set style line 1 lc rgb "red"
set style line 2 lc rgb "black"
set style line 3 lc rgb aqua
set style line 4 lc rgb azure

set grid ytics
set nokey
set yrange [995:1015];
set ylabel "Cost" font "Verdana,15";
set ytics 2; 

set boxwidth 0.5
set style fill solid

plot "accuracy1.txt" every ::0::0 using 1:3:xtic(2) with boxes ls 1, \
     ''	every ::1::1 using 1:3:xtic(2) with boxes ls 2, \
     ''	every ::2::2 using 1:3:xtic(2) with boxes ls 3, \
     '' every ::3::3 using 1:3:xtic(2) with boxes ls 4