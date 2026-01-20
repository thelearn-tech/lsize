<!-- # lsize -->

```pre 
.__         .__               
|  |   _____|__|_______ ____  
|  |  /  ___/  \___   // __ \ 
|  |__\___ \|  |/    /\  ___/ 
|____/____  >__/_____ \\___  >
          \/         \/    \/              
```

A Python CLI tool to calculate and display the total size of files and directories in Linux.

<p>
<img src="https://img.shields.io/badge/Code_in--lightgrey?style=flat-square">
<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" style="margin-right:6px;">
<img src="https://img.shields.io/badge/Installer--lightgrey?style=flat-square" style="margin-left:12px;">
<img src="https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=fff" style="margin-right:6px;">
<img src="https://img.shields.io/badge/OS--lightgrey?style=flat-square" style="margin-left:12px;">
<img src="https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black" style="margin-right:6px;">
<img src="https://img.shields.io/badge/Tested_on--lightgrey?style=flat-square" style="margin-left:12px;">
<img src="https://img.shields.io/badge/Debian-A81D33?style=flat-square&logo=debian&logoColor=white" style="margin-right:6px;">
</p>

## Features

- Calculates the total size of files and directories recursively.
- Provides a clear, human-readable output of sizes in bytes, KB, MB, and GB.
- Supports both file and directory size reporting.
- Simple, fast, and lightweight (No External Dependency).

## Usage

```bash
lsize <path>
```

Example:
```bash
lsize /home/user/documents
```

This will display the total size of all files and subdirectories under the specified path.

## Installation

```bash
Requires python 3.13.5 or above.
```

```bash
git clone https://github.com/thelearn-tech/lsize
cd lsize
chmod +x install.sh
./install.sh
```


## Example

Here is the structure of a dir `test` and the file names correspond to the file sizes.

![tree structure of test dir](.repo/tree.png)

Running `lsize` on this dir.

![lsize demo on dir tree](.repo/lsize-demo.png)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT License