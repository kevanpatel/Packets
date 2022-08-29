import socket
from receiver import make_TCP_PACK, make_TCP_UNPACK , TCP_header_struct
from select import select
import argparse
from sys import argv
import time


def countCharacters(file):
  data=file.read()
  number_of_characters = len(data)
  return number_of_characters
def checkFileFinished(size, charCounter):
  if size >= charCounter:
    return True



parser=argparse.ArgumentParser()
parser.add_argument('local_port', type=int, help='This is the recv port', action='store')
parser.add_argument('foreign_address', type=str, help='This is the recv port', action='store')
parser.add_argument('foreign_port', type=int, help='This is the recv port', action='store')
parser.add_argument('window', type=int, help='This This is the window size', default=4096, action='store')

args = parser.parse_args(argv[1:])
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.foreign_address, args.foreign_port) 
client_sock.bind(('', args.local_port))
client_sock.connect(server_addr)
acknowledge=488
sequence=0

windowSize= args.window
log=0
nextSeq=0
nextAck=488
with open('testfile.txt') as f:
  number_of_characters = countCharacters(f)
  print('Number of characters in text file :', number_of_characters)
  while True:
    c = f.read(488)
    rlist, wlist, xlist = select([client_sock],[],[],0.0)
    if rlist:
        received=client_sock.recv(512)
        unpacked=make_TCP_UNPACK(received[:TCP_header_struct.size])
        coolNumber=unpacked['ack_number']
        print(unpacked)
        if checkFileFinished(coolNumber,number_of_characters):  
            break
        if coolNumber>=acknowledge:
          windowSize += 488
          sequence = coolNumber
          acknowledge = sequence + 488
          log = time.time()
        elif(coolNumber == acknowledge-244):
          windowSize+=244
          sequence=coolNumber
          acknowledge=sequence+244
          log = time.time()
          nextSeq=sequence
          nextAck=acknowledge
    if (nextSeq+488 <= windowSize):
      f.seek(nextSeq)  
      c=f.read(488)
      packet_header=make_TCP_PACK(nextSeq,nextAck)
      client_sock.sendto(packet_header+c.encode('utf-8'),server_addr)
      log = time.time()
      nextSeq += 488
      nextAck = nextSeq + 488
    timeout=time.time()-log
    if(timeout> 0.1):
      nextSeq = sequence
      nextAck = acknowledge
      continue
finPacket = make_TCP_PACK(0,0, FIN = 1)
client_sock.sendto(finPacket, server_addr)
client_sock.close()





            
    #if more_legal_packets(packets in window that havent been sent)
  #send a window of packets
  # continue sending packets 
  # only highest ack counts
  # if timer too long
  # timeout  