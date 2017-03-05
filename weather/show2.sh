#!/bin/sh

# lkp 696 138

#echo cmode black > ../FIFO
echo tmode hide > ../FIFO

for z in $(seq 128 -1 32)
do
  echo load weather/lkp_$z.pnm > ../FIFO
  sleep 0.1
done

sleep 3

#echo "clr;cmode color" > ../FIFO
echo "clr;tmode show" > ../FIFO
#!/bin/sh

# lkp 696 138

#echo cmode black > ../FIFO
echo tmode hide > ../FIFO

for z in $(seq 128 -1 32)
do
  echo load weather/lkp_$z.pnm > ../FIFO
  sleep 0.1
done

sleep 3

#echo "clr;cmode color" > ../FIFO
echo "clr;tmode show" > ../FIFO

