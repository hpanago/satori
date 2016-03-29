# Satori (悟り)
A 'forensic oriented' filesystem image suite!

"Satori" is a Japanese Buddhist term for awakening, "comprehension; understanding" [...] enlightment. (en.wikipedia.org/wiki/Satori)

It is named after the spontaneous feeling of absolute knowledge, an analyst feels when he/she finally understands what exactly is happening in a system or network!



Satori has 3 basic tools:
<br>satori-imager</br>
<br>satori-differ</br>
<br>satori-browser</br>
  
  <b>Satori Imager</b> creates images of a File System saving key elements for its file like filename(duh!), privileges, size, type, and maybe content and hash, while maintaining the file system's tree structure.
The images are saved as (gzipped) Json files or python Pickles and also contain metadata about the system such as user that did the image dump, date of the image dump, system 'uname' and more.



