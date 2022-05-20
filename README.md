# CS682
In order to read from and write data to Google Sheets in Python, we will have to create a Service Account. I have taken reference from the link https://blog.coupler.io/python-to-google-sheets/ . According to google cloud docs, "A service account is a special kind of account used by an application or a virtual machine (VM) instance, not a person. Applications use service accounts to make authorized API calls, authorized as either the service account itself or as Google Workspace or Cloud Identity users through domain-wide delegation."

#Creating a service account
1. Go to [Google developer console] (https://console.cloud.google.com/) and click on **Create Project**
2. Search for Google Drive API and click on “Enable”. Do the same for the Google Sheets API. <img src =https://raw.githubusercontent.com/prabinsharmaa/CS682/main/Images/Screen%20Shot%202022-05-20%20at%2012.32.03%20PM.png height=400 width = 900>
3. Search for Google Drive API and click on “Enable”. Do the same for the Google Sheets API. <img src =https://raw.githubusercontent.com/prabinsharmaa/CS682/main/Images/Screen%20Shot%202022-05-20%20at%206.36.34%20PM.png height=400 width = 900>
4. Click on “Create Credentials”
5. Click on Add key <img src =https://raw.githubusercontent.com/prabinsharmaa/CS682/main/Images/Screen%20Shot%202022-05-20%20at%207.03.37%20PM.png height=400 width = 900>
6. The credentials will be created and downloaded as a JSON file. 
7. Open up the JSON file , share your spreadsheet with the XXX-compute@developer.gservice.com email listed.
8. Copy the newly created JSON file and place it in the Utils folder and rename it to credentils.json 
9. Run final_bt.py as python3 final_bt.py -r 80 -t 60 -u 300
10. Once executed, your program runs forever with an infinite loop that keeps sensing BT beacons. (The user stops it with Ctrl-C.) The loop iterates with a T-second interval (T = 60 seconds, by default).
11. Once you run the program , the output will be seen in the google spreadsheet like this . 
<img src = https://raw.githubusercontent.com/prabinsharmaa/CS682/main/Images/Screen%20Shot%202022-05-20%20at%207.19.07%20PM.png height= 400 width = 900>



