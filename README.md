# satori
A filesystem image suite

Satori has 3 basic tools:
  satori-imager
  satori-differ
  satori-browser
  
Satori Imager creates images of your File System saving key elements for its file like filename(duh!), privileges, size, type, and maybe content and hash.




usage: satori-imager.py [-h] [--type {pickle,json,sqlite}] [--no-gzip]
                        [--verbose | --debug | --quiet] [--filetypes | --text]
                        [--hash] [--threads THREADS]
                        [image]

Crawls the whole filesystem and creates an image of it to a file.

positional arguments:
  image                 Set image filename. Default filename for this system
                        is "Linux-3.19.0-32-generic-x86_64-with-
                        LinuxMint-17.3-rosa.*"

optional arguments:
  -h, --help            show this help message and exit
  --type {pickle,json,sqlite}, -t {pickle,json,sqlite}
                        Choose the file type of the images
  --no-gzip, -ng        Image IO will *NOT* use gzip (larger but readable
                        files)
  --verbose, -v         verbose mode
  --debug, -d           debugging mode
  --quiet, -q           quiet mode
  --filetypes           Try to guess filetypes with mimes and 'file' command
                        (slower)
  --text                Guess file types and save all text contents of a file
                        in the image (very slow! Useful for config files)
  --hash                Calculate and store the SHA-256 of every file in the
                        image (slower)
  --threads THREADS     Use threads to create the Filesystem Image (good for
                        multiple IO calls)




