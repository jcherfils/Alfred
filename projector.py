import socket
from PySide2 import QtCore, QtGui, QtWidgets



    # def command(self,command):

#     def info(self):
#         print("ID: Projector" , self.id, '\n', "Label:", self.label, '\n', "IP Address:", self.ipAddress)

#     def test(self):
#         print("Test of Projector class seems to work.")

#     def ping(self):
#         print("Pinging", self.label, "(" + self.ipAddress + ")","...")
#         comm="ping -i 1 -n 3 " + self.ipAddress + " > $null 2>&1"
#         pingResult = not os.system(comm)
#         if pingResult :
#             print("Projector", self.label, "is up.")
#         else:
#             print("Projector", self.label, "ping failed.")
#         return pingResult

#     def hasBrain(self):
#         if self.ping() == 0:
#             print("Ping was good, let's try to connect...")
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             host = self.ipAddress
#             port = 3002
#             print("connecting to " + self.label + " on port " + str(port))
#             try :
#                 s.connect((host, port))
#             except e:
#                 print('something\'s wrong with %s:%d. Exception type is %s' % (host, port, e))
#             s.send("(PNG?)")
#             data = s.recv(1024)
#             if data == "(PNG! 031 001 000)":
#                 brain = 1
#             else:
#                 brain = 0
#             #s.close()
#             print(data)


#             brain = 1 # if connect is successful, and query (PNG?) returns something useful
#         else:
#             print("Braindead!")
#             brain = 0
#         return brain

#     def lightUp(self):
#         if self.ping():
#             print("Ping was good, let's try to connect...")
#             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             host = self.ipAddress
#             port = 3002
#             print("connecting to " + self.label + " on port " + str(port))
#             try :
#                 s.connect((host, port))
#             except e:
#                 print('something\'s wrong with %s:%d. Exception type is %s' % (host, port, e))
#             s.send("(PWR1)".encode())

#     def shutterOn(self):
#         # if self.ping():
#         #     print("Ping was good, let's try to connect...")
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         host = self.ipAddress
#         port = 3002
#         print("connecting to " + self.label + " on port " + str(port))
#         try :
#             s.connect((host, port))
#         except e:
#             print('something\'s wrong with %s:%d. Exception type is %s' % (host, port, e))
#         s.send("(SHU1)".encode())

#     def shutterOff(self):
#         # if self.ping():
#         #     print("Ping was good, let's try to connect...")
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         host = self.ipAddress
#         port = 3002
#         print("connecting to " + self.label + " on port " + str(port))
#         try :
#             s.connect((host, port))
#         except e:
#             print('something\'s wrong with %s:%d. Exception type is %s' % (host, port, e))
#         s.send("(SHU0)".encode())

#     # def lamp(self):
#     #     if brain == 1:
#     #         print("Has a brain, how's the lamp?")

#     #         lamp = 1 # if (PWR?) query returns (PWR! 001) or whatever
#     #     else:
#     #         print("Braindead, so not checking lamp.")
#     #         lamp = 0
#     #     return lamp

#     # def shutter(self):
#     #     if brain == 1 and lamp == 1:
#     #         print("Has a brain, how's the shutter?")
#     #         shutter = 1 # if (SHU?) query returns (SHU! 001)
#     #     else:
#     #         print("Braindead, so can't check shutter and STOP ASKING.")
#     #         shutter = 0
#     #     return shutter

#     # def signal(self):
#     #     if brain == 1:
#     #         print("Has a brain, how's the signal?")
#     #         signal = 1 # find way to check signal status. There's an FYI message? An SST query?
#     #     else:
#     #         print("Braindead, so can't check signal.")
#     #         signal = 0
#     #     return signal


# vpMur=Projector("Mur","192.168.95.21")
# vpSol=Projector("Sol","192.168.95.22")

# vpMur.connect()
# vpSol.connect()

# # vpMur.command('(PWR0)')
# # vpSol.command('(PWR0)')

# vpMur.command('(PWR1)')
# vpSol.command('(PWR1)')

# vpMur.disconnect()
# vpSol.disconnect()
# vpSol.command('(PWR0)')
# vpSol.command("(SST?)")
# vpMur.shutterOff()
# vpSol.shutterOff()
# # vpMur.shutterOn()
# # vpSol.shutterOn()