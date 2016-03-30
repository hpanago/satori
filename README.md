# Satori (悟り)
<u>*A 'forensic oriented' filesystem image suite!*</u>

*"_Satori_"* is a Japanese Buddhist term for *awakening*, "*comprehension*; *understanding*" [...] *enlightment*. [en.wikipedia.org/wiki/Satori](en.wikipedia.org/wiki/Satori)

It is named after the spontaneous feeling of absolute knowledge, an analyst feels when he/she finally understands what exactly is happening in a system or network!

<i>The idea (and inspiration) for development of this tool came from mr. Vivek Ramachandran, [Securitytube.net](Securitytube.net) founder, as the main project for Module 8 of the *'SecurityTube Python Scripting Expert (SPSE)' Course*. I thank him from the bottom of my heart for his contribution in security community (and my personal development)!</i>
<p><br>

Satori has 3 basic tools:
####<i>satori-imager</i>

  <b>Satori Imager</b> creates images of a File System saving key elements for each file like: _filename_(duh!), _privileges_, _size_, _type_, _text content_ and _hash_ (if chosen), while maintaining the File System's tree-like structure.
The images are saved as (gzipped) Json files or python Pickles and also contain metadata about the system such as user that did the image dump, date of the image dump, system 'uname' and more.
<p><p><br>
####<i>satori-browser</i>

  <b>Satori Browser</b> is a tool that loads those image files and spawns a custom UNIX-like shell in the underlying File System. The user can freely '*ls*', '*cd*' and '*stat*' all files in the FileSystem image.<p>
The shell's capabilities depend on the choices made when creating the image, for example: if <b>Satori Imager</b> was configured to dump text content of files then, also, a '*cat*' command would be available.
<p>
``` Example
{Satori} n0p_sl3d@kali-laptop / $ ls 
0               dev             initrd.img      lib32           live-build      opt             run             sys             var
bin             etc             initrd.img.old  lib64           lost+found      proc            sbin            tmp             vmlinuz
boot            home            lib             libx32          media           root            srv             usr             vmlinuz.old
{Satori} n0p_sl3d@kali-laptop / $ cd etc
{Satori} n0p_sl3d@kali-laptop /etc $ stat passwd
	SHA2 : N/A
	group : 0
	privileges : 0100644
	filename : passwd
	owner : 0
	path : /etc
	type : N/A
	size : 2825
{Satori} n0p_sl3d@kali-laptop /etc $ 
```
<p><p><br>

####<i>satori-differ</i>

  <b>Satori Differ</b> is the real magic! Here is how it works:
<p>
* Let's say you get your hands on a File System where something has gone wrong. Either you know it is 'rootable' (maybe a vulnhub VM?) or it has been under attack and there may exist a backdoor in it. Running the <b>Satori Imager</b> on it you acquire an image of it.
* Given it is a Linux Distro you can find its clean form online. So by downloading, *checking the hash* and installing it in a VM you can run again the <b>Satori Imager</b> and get the clean image of the very same distribution.
* Now, by running the <b>Satori Differ</b> in the 2 images (let's call them 'original' and 'dirty') you get every kind of difference between them, being _privilege_ alteration, different _size_ for crucial files, _missing_ or _renamed_ files, '_chowned_' files, etc...
<p>
There are even features for hash comparison of binaries (backdoored /bin/ files) and text-file 'diffing' for configuration files (you don't remember you allowed 'root login' in /etc/ssh/sshd_config ? ...well you maybe didn't!)
<p><p><p>
Well, while *Satori* doesn't reveal vulnerabilities or misconfiguration, it gives you a place to start by showing you all the "*_Deviations_*". The magic word in forensics!




