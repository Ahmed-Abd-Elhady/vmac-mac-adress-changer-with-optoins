import subprocess,optparse,re,random,time,sys
def generate_random_mac():
    # Generate the first octet with an even value
    first_octet = random.randint(0x00, 0x7F)  # Ensure LSB is 0 for even number
    if first_octet % 2 != 0:  # Check if LSB is odd
        first_octet += 1  # Increment by 1 to make it even
    # Generate the remaining octets
    mac_sections = [first_octet] + [random.randint(0x00, 0xff) for _ in range(5)]
    # Convert each octet to hexadecimal format and join them with ':'
    mac_address = ':'.join(f'{section:02x}' for section in mac_sections)
    return mac_address

def change(mac):
    try:
        subprocess.call(f"ifconfig {options.network_interface} down",shell=True)
        time.sleep(1)
        subprocess.call(f"ifconfig {options.network_interface} hw ether {mac}",shell=True)
        time.sleep(1)
        subprocess.call(f"ifconfig {options.network_interface} up",shell=True)
    except Exception:
        print("[log] bad mac adress")



parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="network_interface",help="Choose Netowrk Interface")
parser.add_option("-m", "--mac", dest="new_mac" ,help="Choose Custom Mac")
parser.add_option("--im", "--my_mac", action="store_true" ,dest="i_mac" ,help="Get your mac ")
parser.add_option("--rm", "--random_mac", action="store_true" ,dest="rm" ,help="Random Mac ")
parser.add_option("--rml", "--random_mac_list" ,dest="rml" ,help="Random Mac list auto genrated ")
parser.add_option("--t", "--time", action="store_true" ,dest="time" ,help="time between chane macs")
parser.add_option("--lm", "--mac_list" ,dest="mlist" ,help="Choose Random Mac From txt file , note this options need -t with it")
options , arguments = parser.parse_args()

#handel error no -i
if not options.network_interface:
    parser.error("[Log] use -h to see arguments")
#im option
if options.i_mac:
    try:
        ifconfig_result = subprocess.check_output("ifconfig "+options.network_interface, shell=True).decode("UTF-8")
        mac =re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        print("[+] Your mac for "+options.network_interface+f" is: {mac[0]}")
        sys.exit()
    except Exception:
        parser.error("[log] no such network interface")


try :
    print("[log] "+ options.network_interface +" shutiing down..")
    subprocess.call("ifconfig " + options.network_interface+" down",shell=True)
    if not options.rm:
        if options.mlist:
            if options.time:
                print(f"[Log] Start Read Mac From {options.mlist} with delay {options.time}")
                with open(options.mlist,'r') as file:
                    for line in file:
                        time.sleep(options.time)
                        print(f"[Log] Changing to {line.strip()}")
                        change(line.strip())
                print("[log] Opretion State : Done ")
                sys.exit()

            else:
                print("[log] u need to use --t too ")
                sys.exit()
        elif options.rml:
            if not options.time:
                print("[log] u need to use --t")
            if options.rml is None:
                print("[log] Must write how many macs")
            print("[log] starting mac random list ")
            for inline in range(int(options.rml)):
                macinline = generate_random_mac()
                time.sleep(options.time)
                print(f"[Log] Changing to {macinline}")
                change(macinline)
        elif not options.new_mac:
            print("[log] use -m custom mac or -rm to random mac")
        #subprocess.call("ifconfig " + options.network_interface+" hw ether "+ options.new_mac,shell=True)

            



    else:
        options.new_mac = generate_random_mac()
        subprocess.call("ifconfig " + options.network_interface+" hw ether "+ options.new_mac,shell=True)
        
    print("[log] Changing Mac.....")
    subprocess.call("ifconfig " + options.network_interface+" up",shell=True)
    print("[log] "+ options.network_interface +" Starting....")
    time.sleep(2)
except Exception:
    print("[log] See the tool doc")
    sys.exit()
finally:
    print("[+] Mac Adress For Interface "+options.network_interface+" to " +f"[{options.new_mac}]" + " State : Changed!")