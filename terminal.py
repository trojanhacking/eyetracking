import time
from  eyeAngle import *
bg = time.time()
lastTrue = -1
def count_seconds():
    seconds = 0
    try:
        while True:
            print(f"Time elapsed: {time.time()-bg} seconds")
            
            lastTrue
            
    except KeyboardInterrupt:
        print("\nCounter stopped!")

if __name__ == "__main__":
    count_seconds()