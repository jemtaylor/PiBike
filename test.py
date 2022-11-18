import time
import datetime
import sys

def main():

   i=0
   while (i<100):
      print (time.time())

      start = time.time()
      time.sleep(2)
      end = time.time()

      diff = end - start
      print (diff)

      dispStr = str(diff)
      print (dispStr)

      m, s = divmod(diff, 60)
      h, m = divmod(m, 60)

      print('{:.0f}h:{:.0f}m:{:.3f}s'.format(h, m, s))
      strTime = '{:.0f}h:{:.0f}m:{:.3f}s'.format(h, m, s)

      print strTime
      #print('{:d}:{:02d}:{:02d}'.format(h, m, s))
      #print(f'{h:d}:{m:02d}:{s:02d}')
   
      sys.stdout.flush()

      i = i+1

if __name__=="__main__":
   main()




