# Received Access-Request Id 126 from 192.168.10.1:47811 to 192.168.230.130:1912 length 169
#   Service-Type = Framed-User
#   Framed-Protocol = PPP
#   NAS-Port = 15728641
#   NAS-Port-Type = Ethernet
#   User-Name = "matt"
#   Calling-Station-Id = "54:B2:03:9B:29:65"
#   Called-Station-Id = "radius-test"
#   NAS-Port-Id = "ether3"
#   Acct-Session-Id = "81900001"
#   CHAP-Challenge = 0x77063a012fbc9446e234be03e4a69fec
#   CHAP-Password = 0x017a7a347c4a5fd26d34fe5ce9b3e2034f
#   NAS-Identifier = "office.azorian.solutions"
#   NAS-IP-Address = 192.168.10.1

# Hashed Password To Match
# 7a7a347c4a5fd26d34fe5ce9b3e2034f

# Clear-Text Password Hash
# b653e16c50efde5b2af141640462e6e1

# Clear-Text Password Double Hash
# 0054095c6dd11a39eda8facf09bf7249

# Clear-Text Secret Hash
# 79fad3501827a8d5c8e7c2b286f44adf

# Clear-Text Challenge Hash
# c470734effbc982afc3fa00a32d2ea2e


echo -n "1263825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5
echo -n "1263825u0x77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5

echo -n "013825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5

echo -n "0013825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5


echo -n "13825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5
echo -n "13825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5
echo "013825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5
echo "13825u77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5


echo -n "13825u79fad3501827a8d5c8e7c2b286f44adf" | openssl dgst -md5
echo -n "13825uas3825test" | openssl dgst -md5
echo -n "3825u" | openssl dgst -md5
echo -n "77063a012fbc9446e234be03e4a69fec" | openssl dgst -md5
echo -n "as3825test" | openssl dgst -md5

echo -n "2116977063a012fbc9446e234be03e4a69fecas3825test" | openssl dgst -md5

# Received Access-Request Id 130 from 192.168.10.1:38819 to 192.168.230.130:1912 length 196
#   User-Name = "54:B2:03:9B:29:65"
#   NAS-Port-Type = Ethernet
#   NAS-Port = 2209361663
#   Service-Type = Framed-User
#   Calling-Station-Id = "1:54:b2:3:9b:29:65"
#   Called-Station-Id = "radius-test"
#   Agent-Remote-Id = 0x0a003eb77184
#   ADSL-Agent-Remote-Id = 0x0a003eb77184
#   Agent-Circuit-Id = 0x0a003eb2f75a
#   ADSL-Agent-Circuit-Id = 0x0a003eb2f75a
#   User-Password = ""
#   NAS-Identifier = "office.azorian.solutions"
#   NAS-IP-Address = 192.168.10.1
#
# Received Accounting-Request Id 18 from 192.168.10.1:32972 to 192.168.230.130:1913 length 162
#   Service-Type = Framed-User
#   Framed-Protocol = PPP
#   NAS-Port = 15728655
#   NAS-Port-Type = Ethernet
#   User-Name = "matt"
#   Calling-Station-Id = "54:B2:03:9B:29:65"
#   Called-Station-Id = "radius-test"
#   NAS-Port-Id = "ether3"
#   Acct-Session-Id = "8190000f"
#   Framed-IP-Address = 192.168.70.254
#   Acct-Authentic = RADIUS
#   Event-Timestamp = "Dec 29 2022 17:19:47 UTC"
#   Acct-Status-Type = Start
#   NAS-Identifier = "office.azorian.solutions"
#   Acct-Delay-Time = 0
#   NAS-IP-Address = 192.168.10.1
#
# Received Accounting-Request Id 19 from 192.168.10.1:41361 to 192.168.230.130:1913 length 276
#   Service-Type = Framed-User
#   Framed-Protocol = PPP
#   NAS-Port = 15728655
#   NAS-Port-Type = Ethernet
#   User-Name = "matt"
#   Calling-Station-Id = "54:B2:03:9B:29:65"
#   Called-Station-Id = "radius-test"
#   NAS-Port-Id = "ether3"
#   Acct-Session-Id = "8190000f"
#   Framed-IP-Address = 192.168.70.254
#   Acct-Authentic = RADIUS
#   Event-Timestamp = "Dec 29 2022 17:20:02 UTC"
#   Acct-Session-Time = 15
#   Idle-Timeout = 0
#   Session-Timeout = 180
#   X-Ascend-Data-Rate = 31000000
#   Ascend-Xmit-Rate = 31000000
#   X-Ascend-Data-Rate = 6000000
#   Ascend-Data-Rate = 6000000
#   Mikrotik-Rate-Limit = "6000000/31000000"
#   Acct-Input-Octets = 7251
#   Acct-Input-Gigawords = 0
#   Acct-Input-Packets = 84
#   Acct-Output-Octets = 4068
#   Acct-Output-Gigawords = 0
#   Acct-Output-Packets = 39
#   Acct-Status-Type = Interim-Update
#   NAS-Identifier = "office.azorian.solutions"
#   Acct-Delay-Time = 0
#   NAS-IP-Address = 192.168.10.1
#
# Received Accounting-Request Id 29 from 192.168.10.1:45930 to 192.168.230.130:1913 length 282
#   Service-Type = Framed-User
#   Framed-Protocol = PPP
#   NAS-Port = 15728655
#   NAS-Port-Type = Ethernet
#   User-Name = "matt"
#   Calling-Station-Id = "54:B2:03:9B:29:65"
#   Called-Station-Id = "radius-test"
#   NAS-Port-Id = "ether3"
#   Acct-Session-Id = "8190000f"
#   Framed-IP-Address = 192.168.70.254
#   Acct-Authentic = RADIUS
#   Event-Timestamp = "Dec 29 2022 17:22:19 UTC"
#   Acct-Session-Time = 152
#   Idle-Timeout = 0
#   Session-Timeout = 180
#   X-Ascend-Data-Rate = 31000000
#   Ascend-Xmit-Rate = 31000000
#   X-Ascend-Data-Rate = 6000000
#   Ascend-Data-Rate = 6000000
#   Mikrotik-Rate-Limit = "6000000/31000000"
#   Acct-Input-Octets = 74761
#   Acct-Input-Gigawords = 0
#   Acct-Input-Packets = 377
#   Acct-Output-Octets = 53712
#   Acct-Output-Gigawords = 0
#   Acct-Output-Packets = 246
#   Acct-Status-Type = Stop
#   Acct-Terminate-Cause = User-Request
#   NAS-Identifier = "office.azorian.solutions"
#   Acct-Delay-Time = 0
#   NAS-IP-Address = 192.168.10.1
#
# Received Accounting-Request Id 15 from 192.168.10.1:46140 to 192.168.230.130:1913 length 224
#   User-Name = "54:B2:03:9B:29:65"
#   NAS-Port-Type = Ethernet
#   NAS-Port = 2209361939
#   Service-Type = Framed-User
#   Calling-Station-Id = "1:54:b2:3:9b:29:65"
#   Framed-IP-Address = 192.168.70.102
#   Called-Station-Id = "radius-test"
#   Agent-Remote-Id = 0x0a003eb77184
#   ADSL-Agent-Remote-Id = 0x0a003eb77184
#   Agent-Circuit-Id = 0x0a003eb2f75a
#   ADSL-Agent-Circuit-Id = 0x0a003eb2f75a
#   Event-Timestamp = "Dec 29 2022 17:18:24 UTC"
#   Acct-Status-Type = Interim-Update
#   Acct-Session-Id = "83b03013"
#   Acct-Authentic = RADIUS
#   Acct-Session-Time = 390
#   NAS-Identifier = "office.azorian.solutions"
#   Acct-Delay-Time = 0
#   NAS-IP-Address = 192.168.10.1
#
# Received Accounting-Request Id 16 from 192.168.10.1:54360 to 192.168.230.130:1913 length 260
#   User-Name = "54:B2:03:9B:29:65"
#   NAS-Port-Type = Ethernet
#   NAS-Port = 2209361939
#   Service-Type = Framed-User
#   Calling-Station-Id = "1:54:b2:3:9b:29:65"
#   Framed-IP-Address = 192.168.70.102
#   Called-Station-Id = "radius-test"
#   Agent-Remote-Id = 0x0a003eb77184
#   ADSL-Agent-Remote-Id = 0x0a003eb77184
#   Agent-Circuit-Id = 0x0a003eb2f75a
#   ADSL-Agent-Circuit-Id = 0x0a003eb2f75a
#   Event-Timestamp = "Dec 29 2022 17:18:50 UTC"
#   Acct-Status-Type = Stop
#   Acct-Session-Id = "83b03013"
#   Acct-Authentic = RADIUS
#   Acct-Session-Time = 416
#   Acct-Input-Octets = 158737
#   Acct-Input-Gigawords = 0
#   Acct-Input-Packets = 0
#   Acct-Output-Octets = 128035
#   Acct-Output-Gigawords = 0
#   Acct-Output-Packets = 0
#   NAS-Identifier = "office.azorian.solutions"
#   Acct-Delay-Time = 0
#   NAS-IP-Address = 192.168.10.1