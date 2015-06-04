import os
import sqlite3
conn = sqlite3.connect('nessus.db')
c = conn.cursor()
os.mkdir('nessus_report_output')

departments = []
c.execute('SELECT DISTINCT Department FROM dates ORDER BY Department')
for row in c.fetchall():
 departments.append(row[0])

vulnerabilities = ['MySQL Default Account Credentials','SNMP Agent Default Community Name (public)','Microsoft SQL Server sa Account Default Blank Password','Microsoft Windows SMB Registry : Autologon Enabled','Microsoft Windows Guest Account Belongs to a Group','Microsoft Windows SMB Shares Unprivileged Access','Microsoft Windows 2000 Unsupported Installation Detection','Microsoft Windows Administrator Default Password Detection (W32/Deloder Worm Susceptibility)','NFS Share User Mountable']
nonmsapplicationsall = ['%Adobe Reader%','%Flash Player%','%Adobe AIR%','%Shockwave Player%','%Oracle Java%','%Sun Java%','%iTunes%','%Adobe Acrobat%','%Google Chrome%','%Quicktime%','%Safari%','%RealPlayer%','%Opera%','%Firefox%','%Foxit Reader%','%VLC%','%Google Picasa%','%Adobe Photoshop%','%Netscape Browser%','%Winamp%','%HP System Management%','%Adobe Illustrator%','%IrfanView%','%PHP%','%Wireshark%','%VMware vCenter%','%AIX 6.1 TL%','%Oracle Database%','%Apache%','%SAP Sybase Adaptive Server Enterprise%','%DB2%','%IBM WebSphere Application%']

e = open('nessus_report_output/combined.txt', 'w')
for department in departments:
 mspatchingpresent = 0 
 nonmspatchingpresent = 0
 vulnerabilitypresent = 0
 f = open('nessus_report_output/' + department + '.tex', 'w')
 f.write(r"""
\documentclass[12pt]{article}
\usepackage{longtable}
\usepackage{rotating}
\usepackage{color}
\usepackage{lscape}
""")
 f.write('\\title{Vulnerability Report for ' + department.replace("_"," ") + '}')
 f.write(r"""
\author{Author}
\date{\today} 
\begin{document}
\maketitle
\newpage
\tableofcontents
\newpage
\section{Executive Summary}
""")
 count = c.execute('SELECT COUNT(DISTINCT Host) FROM nessus WHERE (Department LIKE ?)', (department,)).fetchone()[0]
 f.write(r"""Number of hosts scanned: """ + str(count) + r"""\\""")
 date = c.execute('SELECT Date FROM dates WHERE (Department LIKE ?)', (department,)).fetchone()[0]
 f.write(r"""Scan date: """ + str(date) + r"""\\""")
 f.write(r"""
\newpage
\section{Microsoft Patching Report}
\begin{center}
\begin{longtable}{ | l | l | }
\hline
Host & Number of Missing Microsoft Patches \endhead \hline\hline
""")
 microsoftTable = []
 for row in c.execute('SELECT DISTINCT(Host), "Plugin Output" FROM nessus WHERE ("Plugin ID" LIKE "38153" and Department LIKE ?)', (department,)):
  count = row[1].count('\n')-2
  microsoftTable.append([row[0],count])
  mspatchingpresent = 1
 for host, count in sorted(microsoftTable,key=lambda row: -row[1]):
  if (count > 25): f.write(host + ' & \\textcolor{red}{' + str(count) + '} \\\\ \\hline\n')
  else: f.write(host + ' & ' + str(count) + ' \\\\ \\hline\n')
 f.write(r"""\end{longtable}\end{center}""")
 if mspatchingpresent: f.write('All other hosts are up-to-date on Microsoft Patches.')
 else: f.write('All hosts up-to-date on Microsoft Patches, or no Microsoft Patching information in scan results.')
 f.write(r"""\newpage""")
 f.write(r"""\section{Non-Microsoft Patching Report}""")
 nonmsapplications = []
 for application in nonmsapplicationsall:
  count = c.execute('SELECT COUNT(DISTINCT "Plugin ID") FROM nessus WHERE (Risk LIKE "High" OR Risk LIKE "Critical") and Name LIKE ? and Department LIKE ?', (application,department,)).fetchone()[0]
  if count: nonmsapplications.append(application)
 f.write(r"""
The following table lists the number of missing patches for each application on each host:
\begin{longtable}{ | l""")
 for application in nonmsapplications: f.write(' | l ')
 f.write(r""" | }
\hline
Host""")
 for application in nonmsapplications:
  f.write(' & \\begin{sideways}' + application[1:len(str(application))-1] + ' \\end{sideways} ')
 f.write('\\endhead \\hline\\hline\n')
 hosts = []
 nonmsapplicationscollapsed = '" OR Name LIKE "'.join(nonmsapplicationsall)
 c.execute('SELECT DISTINCT Host FROM nessus WHERE (Risk LIKE "High" OR Risk LIKE "Critical") AND Department like ? AND (Name LIKE "' + nonmsapplicationscollapsed + '")',(department,))
 for row in c.fetchall():
  hosts.append(row[0])
 for host in hosts:
  f.write(host[:20])
  for application in nonmsapplications:
   count = c.execute('SELECT COUNT(DISTINCT "Plugin ID") FROM nessus WHERE (Risk LIKE "High" OR Risk LIKE "Critical") and Host LIKE ? and Name LIKE ? and Department LIKE ?', (host,application,department,)).fetchone()[0]
   if (count > 10): f.write(' & \\textcolor{red}{' + str(count) + '}')
   elif (count > 0): f.write(' & ' + str(count))
   else: f.write(' & ')
   nonmspatchingpresent = 1
  f.write('\\\\ \\hline\n')
 f.write(r"""
\end{longtable}
""")
 if nonmspatchingpresent: f.write('All other hosts are up-to-date on Non-Microsoft Patches.')
 else: f.write('All hosts up-to-date on Non-Microsoft Patches, or No Non-Microsoft Patching information in scan results.')
 f.write(r"""
\newpage 
\section{Other Vulnerabilities}
\begin{center}
\begin{longtable}{ | l | l | }
\hline
Issue & Host \\ \hline
""")
 for vulnerability in vulnerabilities: 
  for row in c.execute('SELECT DISTINCT Host FROM nessus WHERE (Department LIKE ? and Name LIKE ?)', (department, vulnerability,)):    
    f.write(vulnerability + ' & ' + row[0] + ' \\\\ \\hline\n')
    e.write(department + ',' + vulnerability + ',' + row[0] + '\n')
    vulnerabilitypresent = 1
 f.write(r"""
\end{longtable}
\end{center}
""")
 if not vulnerabilitypresent: f.write('No Other Vulnerabilities in scan results.')
 f.write(r"""
\end{document}
""")
 f.close()
 os.system('texi2pdf -q -o nessus_report_output/' + department + '.pdf nessus_report_output/' + department + '.tex')
e.close()
