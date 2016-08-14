#
"""
(c) Nils Jacob Berland 2016

"""
import os

from saivas import SaivasServer

# set the directory to store the text files retrieved from the FTP server
LOCALDIR = "textfiles/"

FTPSERVER = "station.saivas.net"
USERNAME_Gabriel = "14000000"
PASSWORD_Gabriel = "apb5"
SERVERDIR = "14000000/ctd"

if __name__ == "__main__":

    # check if the directory exists first and make it if not
    if not os.path.exists(LOCALDIR):
        os.makedirs(LOCALDIR)

    gabrielserver = SaivasServer(FTPSERVER,USERNAME_Gabriel,PASSWORD_Gabriel,SERVERDIR, LOCALDIR)
    gabrielserver.make_connection()
    gabrielserver.fetchdata()
    gabrielserver.decodeall()

    #print("Done fetching - number of stored dives = {}".format(gabrielserver.storedentries()))
