# Taken to School

### Challenge Description

```
"I was reading the news this week, and I saw that a student tried to hack a school's computer system!" a worried professor remarked to an IT employee during lunch. "I'm glad we've got people like you keeping our network safe." While Bob the IT admin appreciated the warm comment, his stomach dropped. "Dang it.. I haven't checked that firewall since we set it up months ago!".

IT has pulled a log file of potentially anomolous events detected by the new (albeit poorly tuned) network security software for your school. Based on open-sourced intelligence (OSINT), identify the anomolous entry in the file.

Each log entry contains a single line, including an MD5 hash titled "eventHash". The challenge flag is `flag{hash}` containing the `eventHash` of the anomolous entry.
```

### Finding Breach IOCs Online

This is an easy-level OSINT challenge where participants research a recent hack against an education software called "PowerSchool". This breach was recently in the news after a student pleaded guilty to attempted data extortion this week.

By searching for recent news regarding school system hacks and breaches, the PowerSchool hack can be found from many sources.

Simply searching "school hack", two of the first three results discuss the PowerSchool hack (as of 5/22/2025).

![Finding PowerSchool](static/image-3.png)

Once participants search specifically for PowerSchool, they can find a few articles describing the recent events surrounding the breach.

(https://www.bleepingcomputer.com/news/security/powerschool-hacker-pleads-guilty-to-student-data-extortion-scheme)
![Google Search Image](static/image.png)

Reading the article, there is a link to a more technical report on the breach of the system, which happened in December of 2024 (which, as an added clue, correlates with the time stamps in the given log file).

https://www.bleepingcomputer.com/news/security/powerschool-hack-exposes-student-teacher-data-from-k-12-districts/

![Technical Report Link](static/image-1.png)

In this article, there is a section that gives basic IOCs (as well as a link to a more detailed writeup). The most promenant IOCs are a known malicious date (22 December 2024) and an IP address `91.218.50.11`.

![Breach IOCs](static/image-2.png)

### Finding the Flag in the Log File

Armed with the IOCs, participants can go to the provided log file to find the entry correlating with the breach. The log file consists of randomly generated events, but they all include IP addresses. Searching for `91.218.50.11` reveals a single entry in the log file.

```
2024-12-22T15:07:40 CEF:0|PaloAltoNetworks|PAN-OS|8.3|44985|Trojan Signature Match|9|src=91.218.50.11 dst=192.168.113.2 spt=27660 dpt=443 proto=HTTPS act=allowed fileName=chemistry_notes.pdf eventHash=5b16c7044a22ed3845a0ff408da8afa9 cs1Label=threatType cs1=trojan
```

The IP address should be the telltale sign this is the correct log entry. However, there are other indicators as well.

Other matching details:
- The date of the log entry closely matches the date provided in the report (one day after the first ovserved data leak)
- The action was "allowed", indicating it was more likely to be successful than other entries
- The filename "report.pdf" indicates someone may be trying to blend into an education IT network (this isn't a great peice of evidence by itself, but it's worth noting along with the rest).

The flag is the MD5 hash of that log entry wrapped in the `flag{md5}` format.

```
flag{5b16c7044a22ed3845a0ff408da8afa9}
```