**WHY?**

Because I can, that's why.
** **
**SERIOUSLY, WHY?**

Ok, so various "internal" (really external) services we use at work have blocked ICMP for "security reasons".
As ICMP is really ([mostly](https://github.com/jakkarth/icmptx)) harmless and there's far more effective ways to raise security concerns that don't harm a system admin's ability to do his job, this is rather infuriating.
However, the situation being what is is, if I can't use ICMP, I will interrogate whatever ports I know exist.
** **
**BUT YOU'RE NOT ACTUALLY PINGING ANYTHING**

I know.
** **
**WHY NOT USE NMAP?**

Because I don't want to, that's why.
** **
**SERIOUSLY, WHY NOT?**

Because I don't want to scan a range of ports, or deal with complex command line interfaces.
I'm not gunning at NMAP, it's a brilliant tool, but it is far more complex than what I require for a relatively simple task.
And even though this particular single task is quite simple with nmap, I just can't remember how to use it.
For example, to ask NMAP "is port 80 open on host google.com", I'll usually start by googling "nmap check if port is open" and the eventually run:

`nmap -p 80 google.com` which would yield a result like so:

```
Starting Nmap 7.91 ( https://nmap.org ) at 2021-06-11 16:03 W. Australia Standard Time
Nmap scan report for google.com (142.250.66.174)
Host is up (0.046s latency).
rDNS record for 142.250.66.174: syd09s22-in-f14.1e100.net

PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 0.72 seconds
```

but with my tool

`pping.py google.com http` which would yield a result like so

```
Port 142.250.66.206:80 is open
```

which is just simpler.
** **
**WHY NOT JUST WRAP AROUND NMAP AND PARSE AN EXIT STATUS AND PROVIDE YOUR OWN OUTPUT?**

I am not a smart man.
** **
**HOW DO I USE THIS POS?**

Running `pping.py` will explain all. However, try `pping.py google.com https`.
** **
**I FOUND A BUG!**

No, that's a feature I packed just for you. Maybe you might like to leave a comment below and share your very own personalised feature with the world? You're welcome.
** **
**YOU'RE QUITE POSSIBLY THE WORST CODER I HAVE EVER SEEN IN MY LIFE**

Thank you, that's quite the achievement and I have aspired to live up to that all my life.
