import time
import smtplib
import datetime
import socket


# Methods
def send_email(msg_text):
    fromaddr = ''  # Email address the application will send alerts through.
    toaddrs = ''  # Email address to recieve alerts. Can setup multiple using a list.
    username = ''  # Email account name. Usually the same as 'fromaddr'
    password = ''  # Password for the Email account.
    server = smtplib.SMTP('smtp.gmail.com:587')  # Server for the 'fromaddr' Email address (defualt is gmail).
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

# Initial run

# Assign host names to real name
host_name = socket.gethostname()
if 'name1' in host_name:
    host_name = 'Location 1'
elif 'name2' in host_name:
    host_name = 'Location 2'
elif 'name3' in host_name:
    host_name = 'Location 3'
elif 'name4' in host_name:
    host_name = 'Location 4'
elif 'name5' in host_name:
    host_name = 'Location 5'

# Read in file into a list
with open('/var/run/stats.file') as f:
    lines = f.readlines()

# Instantiate variables
defunct_init = 0
overheat_init = 0
hash_stuck_init = 0
outofmemory_init = 0
hash_rate_init = 0
gpus_init = 0

# Assign wanted variables from file
for text in lines:
    if 'defunct:' in text:
        defunct_init = int(text.rsplit(':', 1)[-1].rstrip())
    if 'overheat:' in text:
        overheat_init = int(text.split(':', 1)[-1].rstrip())
    if 'hash_stuck:' in text:
        hash_stuck_init = int(text.split(':', 1)[-1].rstrip())
    if 'outofmemory:' in text:
        outofmemory_init = int(text.split(':', 1)[-1].rstrip())
    if 'hash:' in text:
        hash_rate_init = float(text.split(':', 1)[-1].rstrip())
    if 'gpus:' in text:
        gpus_init = int(text.split(':', 1)[-1].rstrip())

# Display data to user
print("--HashAlert Application Start--\n")
print("Miner Name: " + host_name)
print("Defunct: " + str(defunct_init))
print("Overheat: " + str(overheat_init))
print("Hash Stuck: " + str(hash_stuck_init))
print("Out of Memory: " + str(outofmemory_init))
print("Hash Rate: " + str(hash_rate_init))
print("GPUs: " + str(gpus_init))

# Error checking
if defunct_init == 1:
    miner_error = True
elif overheat_init == 1:
    miner_error = True
elif hash_stuck_init == 1:
    miner_error = True
elif outofmemory_init == 1:
    miner_error = True
elif hash_rate_init == 0:
    miner_error = True
else:
    miner_error = False
if not miner_error:
    print("\nStatus: OK!\n")

# Instantiate variables
defunct = 0
overheat = 0
hash_stuck = 0
outofmemory = 0
hash_rate = 0
gpus = 0

# Main loop
always = True
while always:
    # Save previous gpu count
    gpu_previous = gpus

    # Read in file into a list
    with open('/var/run/stats.file') as f:
        lines = f.readlines()

    # Assign wanted variables from file
    for text in lines:
        if 'defunct:' in text:
            defunct = int(text.rsplit(':', 1)[-1].rstrip())
        if 'overheat:' in text:
            overheat = int(text.split(':', 1)[-1].rstrip())
        if 'hash_stuck:' in text:
            hash_stuck = int(text.split(':', 1)[-1].rstrip())
        if 'outofmemory:' in text:
            outofmemory = int(text.split(':', 1)[-1].rstrip())
        if 'hash:' in text:
            hash_rate = float(text.split(':', 1)[-1].rstrip())
        if 'gpus:' in text:
            gpus = int(text.split(':', 1)[-1].rstrip())

    # Reset error variables
    miner_error = False
    miner_error_msg = "Errors Include:\n"

    # Error checking
    if defunct == 1:
        miner_error_msg += "Miner is defunct!\n"
        miner_error = True
    if overheat == 1:
        miner_error_msg += "Miner has overheated!\n"
        miner_error = True
    if hash_stuck == 1:
        miner_error_msg += "Miner is hash stuck!\n"
        miner_error = True
    if outofmemory == 1:
        miner_error_msg += "Miner is out of memory!\n"
        miner_error = True
    if hash_rate == 0:
        miner_error_msg += "Miner hashrate is 0!\n"
        miner_error = True
    if gpus < gpu_previous:
        print("Sending email alert...\n")
        send_email("Miner has lost one or more GPU's! Current GPU count: "+str(gpus)+". Previous: "+str(gpu_previous))
    if miner_error:
        print("\n" + miner_error_msg)
        print("Sending email alert...")
        send_email(miner_error_msg)

    # Wait for miner to free of error
    while miner_error:
        print("Waiting for miner to resume...")

        # Read in file into a list
        with open('/var/run/stats.file') as f:
            lines = f.readlines()

        # Assign wanted variables from file
        for text in lines:
            if 'defunct:' in text:
                defunct = int(text.rsplit(':', 1)[-1].rstrip())
            if 'overheat:' in text:
                overheat = int(text.split(':', 1)[-1].rstrip())
            if 'hash_stuck:' in text:
                hash_stuck = int(text.split(':', 1)[-1].rstrip())
            if 'outofmemory:' in text:
                outofmemory = int(text.split(':', 1)[-1].rstrip())
            if 'hash:' in text:
                hash_rate = float(text.split(':', 1)[-1].rstrip())
            if 'gpus:' in text:
                gpus = int(text.split(':', 1)[-1].rstrip())

        # Error checking
        if defunct == 1:
            miner_error = True
        elif overheat == 1:
            miner_error = True
        elif hash_stuck == 1:
            miner_error = True
        elif outofmemory == 1:
            miner_error = True
        elif hash_rate == 0:
            miner_error = True
        else:
            miner_error = False

        # Wait
        time.sleep(300)

    # If clear of error, display hash rate
    if not miner_error:
        now = datetime.datetime.now()
        print("Miner Running. Hash Rate is " + str(hash_rate) + " MH/s")

    # Wait
    time.sleep(300)
