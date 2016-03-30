# Satori (悟り)
<u>A 'forensic oriented' filesystem image suite!</u>

"Satori" is a Japanese Buddhist term for awakening, "comprehension; understanding" [...] enlightment. (en.wikipedia.org/wiki/Satori)

It is named after the spontaneous feeling of absolute knowledge, an analyst feels when he/she finally understands what exactly is happening in a system or network!

<i>The idea (and inspiration) for development of this tool came from mr. Vivek Ramachandran, Securitytube.net founder, as the main project for Module 8 of the <b>'SecurityTube Python Scripting Expert (SPSE)' Course </b>. I thank him from the bottom of my heart for his contribution in security community!</i>


Satori has 3 basic tools:
<i>satori-imager</i>
<i>satori-browser</i>
<i>satori-differ</i>

<p><p>
  <b>Satori Imager</b> creates images of a File System saving key elements for its file like filename(duh!), privileges, size, type, text content and hash (if chosen), while maintaining the File System's tree-like structure.
The images are saved as (gzipped) Json files or python Pickles and also contain metadata about the system such as user that did the image dump, date of the image dump, system 'uname' and more.
<p><p>

  <b>Satori Browser</b> is a tool that loads those image files and spawns a custom UNIX-like shell in the underlying File System. The user can freely 'ls', 'cd' and 'stat' all files in the FileSystem image.<p>
The shell's capabilities depend on the choices made when creating the image, for example: if <b>Satori Imager</b> was configured to dump text content of files then, also, a 'cat' command would be available.
<p>
``` Example
{Satori} n0p_sl3d@kali-laptop / $ ls
bin	home	tmp	lib	media	boot	0	usr	var	lib64	proc	opt	live-build	run	sys	initrd.img.old	libx32	lost+found	sbin	lib32	vmlinuz.old	dev	etc	vmlinuz	srv	root	initrd.img
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
  <b>Satori Differ</b> is the real 

