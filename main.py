import subprocess
import logging
from multiprocessing import pool
import ipaddress

class InfiniTest:
    'Class structure to assist with OOB'

    def __init__(self):
        self.ib_logger = logging.basicConfig(filename='ib_health_log.log', level= logging.INFO,
                                          format='%(asctime)s:%(levelname)s:%(message)s')
        self.ip_logger = logging.basicConfig(filename='ib_health_log.log', level= logging.INFO,
                                          format='%(asctime)s:%(levelname)s:%(message)s')

    """
        definition to obtain the full output of `ibstat`
        will return the output, or None based on try/catch Exception
        returns `ibstat` output
    """
    def getIBPorts(self):
        try:
            result = subprocess.run(['ibstat'], stdout=subprocess.PIPE, text=True)

            if result.returncode != 0:
                raise Exception("Error executing ibstat: " + result.stderr)

            return result
        
        except Exception as e:
            print(f"Failed to get IB ports: {e}")
            return None
        
    """
        definition will validate link status, and link rate
        returns True if the link is healthy
    """
    def validateLinkStatus(self, link_speed=400):
        ib_ports = self.getIBPorts()

        for line in ib_ports.splitlines():
            if 'State' in line:
                state = line.split(":")[1].strip()
                if state != "Active":
                    return False, "port is not active"
            if 'Physical state' in line:
                physical_state = line.split(":")[1].strip()
                if physical_state != "LinkUp":
                    return False, "port is down"
            if 'Rate' in line:
                rate = int(line.split(":")[1].strip())
                if rate < link_speed:
                    return False, f"port is below expected ({link_speed} Gbps): {rate} Gbps"
        return True, "link is healthy"
    
    """
        definition will cross-check infiniband device names w/ network names
        uses `ibdev2netdev` to map devices to their network names

        this may not needed hence other discovery protocols can be in place
    """
    def getIBDev2NetDevMapping(self):
        try:
            result = subprocess.run(['ibdev2netdev'], stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, text=True)
            
            if result.returncode != 0:
                raise Exception("Error running ibdev2netdev: " + result.stderr)
            
            return result.stdout
        except Exception as e:
            print(f"Failed to get ibdev2netdev mapping: {e}")
            return None

    """
        definition will validate and log the ibstat & ibdev2netdev
        this will check if there are ports, if they are active, and log errors
    """
    def ibHealthCheckLogging(self):
        try:
            output = self.getIBPorts()
            if output is None:
                raise Exception("Failed to get IB ports")
            
            status, message = self.validateLinkStatus()
            if not status:
                raise Exception(message)
            
            mapping = self.getIBDev2NetDevMapping()
            if mapping is None:
                raise Exception("Failed to retrieve IB to NetDev mapping")
            
            self.ib_logger.info("All IB links are healthy")
            return "All IB links are healthy"
        except Exception as e:
            self.ib_logger.error(f"Health check failed : {e}")
            return f"Health check failed : {e}"
        
    """
        ping each node in the mesh to validate communication
        takes an ipaddress Network object from a string input
    """
    def pingNodes(self, oob_ip_subnet='192.168.1.0/24'):
        self.ip_logger.info(f"Pinging OOB IPs: {oob_ip_subnet}") # Prints the string object
        oob_network = ipaddress.ip_network(oob_ip_subnet) # creates the Network Obj

        for ip in oob_network.hosts():
            response = subprocess.run(
                ['ping', '-c', '1', '-W', '1', str(ip)], stdout=subprocess.DEVNULL
            )
        
            # check return code
            if response.returncode == 0:
                print(f"{ip} is reachable")
            else:
                self.ip_logger.error(f"{ip} is unreacable")
                print(f"{ip} is unreacable")

    """
        testing links between nodes
        uses `ib_send_lat` to test latency
        this process can be VERY time consuming

        Thoughts on this being added may need to be ran on another process 
        that executes via shell script since this is similar to iPerf
    """
    def testIBLinks(self, subnet, nodes):
        #TODO: Complete this with `ib_send_lat` will start the server
        #TODO: Will need to attach to EACH Node in cluster and attach to host
        print("Does nothing at this time.")
        self.ib_logger.error("INVALID USE OF testIBLinks() def")

    

