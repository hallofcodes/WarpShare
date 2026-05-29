import psutil
import socket

def get_local_ip() -> str | None:
   # Common Android/Linux hotspot interface names
   hotspot_interfaces = ['wlan1', 'ap0', 'wlan0:1', 'wlan0']
   
   interfaces = psutil.net_if_addrs()
   
   for iface_name in hotspot_interfaces:
      if iface_name in interfaces:
         for addr in interfaces[iface_name]:

         # Look for IPv4 addresses and exclude loopback
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):

               # Filter out cellular IP
               if not addr.address.startswith('10.'): 
                  return addr.address

   return None
