import socket
from matplotlib.pyplot import flag
from receiver import make_TCP_PACK, make_TCP_UNPACK , TCP_header_struct
from select import select
import argparse
from sys import argv

parser=argparse.ArgumentParser()
parser.add_argument('local_port', type=int, help='This is the recv port', action='store')
parser.add_argument('foreign_address', type=str, help='This is the recv port', action='store')
parser.add_argument('foreign_port', type=int, help='This is the recv port', action='store')


args = parser.parse_args(argv[1:])

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.foreign_address, args.foreign_port)
client_sock.bind(('', args.local_port))
client_sock.connect(server_addr)

    # #trim the line to avoid weird new line things
    # #now we write whatever the server tells us to the out_file
    # answer = client_sock.recv(512)
    # #decode answer
    # answer = answer.decode('utf-8')
coolNumber=0
oldNumber=0
with open('testfile.txt') as f:
  data = f.read()
  f.seek(0)
  number_of_characters = len(data)

  print('Number of characters in text file :', number_of_characters)
  while True:
    c = f.read(488)
    bool=True
    while bool:
        rlist, wlist, xlist = select([client_sock],[],[],0.0)
        
        packet_header=make_TCP_PACK(coolNumber,0)
        client_sock.sendto(packet_header+ c.encode('utf-8'),server_addr)
        
        if rlist:
            

            received=client_sock.recv(512)
            unpacked=make_TCP_UNPACK(received[:TCP_header_struct.size])
            coolNumber=unpacked['ack_number']
            print(unpacked)
            if unpacked['flags']['ACK']==1 and unpacked['ack_number'] > oldNumber and unpacked['ack_number'] > oldNumber:
                oldNumber=unpacked['ack_number'] 
                bool=False
             
        elif coolNumber != number_of_characters :
            print("timeout")
        else:
          finPacket = make_TCP_PACK(0,0, FIN = 1)
          client_sock.sendto(finPacket, server_addr)
          client_sock.close()
    

    
