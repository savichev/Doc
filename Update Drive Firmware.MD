Summary
There are several ways to go about updating firmware on drives that largely depend on the system available to perform the upgrade or downgrade. The easiest method to update drive firmware is by using a server that has a RAID card (such as condado beach or coffee canyon) and using the StorCli utility to perform the update. CmdTool2 is an older utility that may also be used but only as a last resort. If you can determine the chipset of the RAID card, StorCli should be sued for any drive connected to a 3108 chipset RAID card, while CmdTool2 should be used when drives are connected to any 3008 chipset cards.

If you are using a system that does not have a RAID card inside (such as a Sika), you will first need to determine whether or not the drive is SAS or SATA. If it is a SAS drive you will need to us the sg3_util utilities package and the attached python script below to perform the update. If you need to update a SATA drive, you will need to use a Linux distro and utilize the hdparm utility. Each of the aforementioned methods to update drives is discussed in greater detail below.

 
Using StorCLI
 
To update drive FW through StorCLI, implement the following procedures.
 
1- Get enclosure and slot number:
        storcli -pdlist -a0
 
2- Use the following command to update fw:
        storcli /c0 /e*# /s*# download src=file.extension
    where e*# is the enclosure number (i.e. /e6) and s*# is the slot number (i.e.     /s1) and file.extension is the firmware file with its extension (i.e. D29A.bin)
 
Using CmdTool2
To update drive firmware (through Windows is recommended), the CmdTool2 utility, present on the Tools & Utilities USB or the Intel Tools folder, will be needed
Certain servers  lack enclosure numbers and render this utility unusable, so a Dragon server with a Condado Beach RAID controller is recommended.

Place the folder with the tool (typically named CmdTool2) onto your desktop, then via Command Prompt navigate to the inside of the folder with:

cd Desktop\CmdTool2\Cmdtool2\Windows
The desired firmware should be placed into the folder as well. From there,

CmdTool2.exe -pdlist -a0
will display all the drives, along with enclosure & slot numbers. To flash the drive with the desired firmware, run the command:

Cmdtool2.exe -pdfwdownload -physdrv[ENCLOSURE#:SLOT#] -f FWFILEHERE -a0
It will run for 3-5 minutes, then exit with a 0. 

Updating Multiple Drives Automatically

The beauty that is batch scripts can be used to automatically update large quantities of drives without having to wait for the current drive to finish updating its firmware. To do so, create a text document with notepad and with the first line change directories to the full location of CmdTool2 with:

cd C:\Users\Administrator\Desktop\CmdTool2\CmdTool2\Windows
Then enter in the drive firmware update command line-by-line. When finished select File -> Save-As, choose All Files under Save as Type, and add the file extension .bat to the end of your filename.
 
An example batch script is attached.
 
Using Sg3_utils for SAS Drives
 
To update SAS drive FW through Sg3_utils, you will first need a copy of sg3_utils from:
 
http://sg.danny.cz/sg/sg3_utils.html
 
You can use either a windows or linux version of the utility, however it is preferred to use the Linux utility. Download a tar ball and follow the readmes to copy the file to your server. In order to build sg3 utils you will need a c++ compiler on your system which should already be installed. You can then follow the directions at the above website to build sg3_utils on your server.
 
Once built, you can use the use the sgtools_fwload.py python script attached to this page and developed by GDE to load the firmware on to your specific disk. If you are unsure of which disk to load firmware to type:
sg_scan -i 
This command displays all the disk devices in the system allowing you to locate the path to the desired disk. Once you know the disk location, navigate to the location of the script and type:
python sgtools_fwload.py mode7 /PATH/TO/FWFILE/YOURFILE.LOD 32768 /dev/YOURDRIVE 
This will run the python script in mode 7 which is used to send the firmware file in chunks to the disk. The chunk size that should be used is 32768 as typed above.
 
Once the update is complete reboot your system, navigate to the directory where sg3_utils were installed and type:
sg_scan –i 
You should then be able to see if the new drive firmware has successfully been loaded and is recognized by sg3_utils. Assuming a successful load, your task is now complete.
 
Using hdparm for SATA Drives
 
In order to update drive firmware using hdparm, you will need to first install it onto your Linux system either by downloading a tar ball and building it yourself or by using yum. If you are in a RHEL OS you can use “yum install hdparm”  to download and install the hdparm utility on your system. This command will only work if you already have the proper repositories in place. The correct repositories can be linked by running the RHEL7_Repos_Config.sh script attached on this wiki page.
 
Once installed, you can run the following command to find the location of the disk you want to update:
fdisk –l
Once you have determined your device, you may run the following command to update the firmware:
hdparm --fwdownload /path/to/firmware/YOURFW.LOD --yes-i-know-what-i-am-doing --please-destroy-my-drive /dev/DEVICE 
The “yes I know” and “Please destroy” flags serve as dual conformations that you do want to run the fwdownload command as it is very powerful and can easily brick the drive if you use the wrong file. Once the command successfully completes reboot the machine and run the same command you used to find your disk originally in order to verify the update occurred.
