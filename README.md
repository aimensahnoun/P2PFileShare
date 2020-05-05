
# P2P File Sharing Application

## How It Works
- **P2P_Server gets the file name from the host and searchs for any files in the same directory as the executable for a file with the same name, If there exists multiple files with the same name but different extensions, the server would ask the host to specify the extension of the file to be hosted. splitting it into 5 chunks and storing it in the same directory**
- **Service_Announcer asks the host for their username, after getting it the Announcer would then go through the same directory that it's stored in getting a list of all the files that exist there and sends a JSON to the Service_Listener containing the username and the files they host**
- **Service_Listener displays the files and the username of every person who is hosting and announcing in the service, storing each file with the a list of IP addresses that are hosting it**
- **P2P_Downloader asks for the name of the file that is requested by the client and goes through the list of IP addresses for that file trying to fetch the requested chunks and then repacking them into the original file**

## Tested Aspects
The program has been tested and succeeded in the following aspects:

  - **Announcing users and their hosted file correctly in 60 seconds intervals**
  - **Listening and displaying each online and their files**
  - **Correctly creating a content dictionary as well as appending the IP addresses of other users hosting the same file**
  - **Correctly identifying the file to hosted by asking the user for correct file extension**
  - **Displaying error and asking for new file name if the file to be hosted cannot be found in the directory**
  - **Displaying timeout error in case the connection with server lost or not being able to connect**
  - **Displaying an error if the requested file cannot be found in the content dictionary**
  - **Asking the user if they want the corrupted (files that miss a chunk) to be deleted, and then correctly deleted the file**
  - **Displaying Download Failed message if the Downloader can't get any chunk of the file**
  - **Server being able to host multiple files with different extensions without the need to change the code**
  - **Downloader being able to download multiple files with different extensions without the need to change the code**
  - **Downloading and receiving files both on local networks and Hamachi VPN** 
  - **Correctly displaying a Download and Server log in the same directory**
  - **Tested on Linux, Windows, and Mac OS**
 
## Known Limitations

   - **IP address needs to be hardcoded on MacOS since it cannot run the following code correctly**
```bash
socket.gethostbyname(socket.gethostname())
```
   **PS: This might be an error that happens only on the MacBook that was tested on**
   - **Program that runs on Mac OS can only serve but not receive**
   - **While using Hamachi VPN the IP addresses of the users need to be hardcoded since the code itself gets the local network IP addresses**
   - **Problems when sending big files on poor internet connection**



