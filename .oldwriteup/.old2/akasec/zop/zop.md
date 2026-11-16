# write up zop
- với bài này sẽ phải fake cái file zip custom theo chương trình, 
```c
typedef struct ZIP_CFH{			// central directory file header
	uint16_t	version;
	uint16_t	version_needed;
	uint16_t	flags;
	uint16_t	compression;
	uint16_t	mod_time;
	uint16_t	mod_date;
	uint32_t	crc_checksum_32;
	uint32_t	compressed_size;
	uint32_t	uncompressed_size;
	uint16_t	fname_len;			// filename_len
	uint16_t	extra_feild_len;
	uint16_t	file_comm_len;			// comment length
	uint16_t	disk_start;
	uint16_t	internal_attrs;
	uint32_t	external_attrs;
	uint32_t	local_header;
	char		*filename;
	char		*extra_feild;
	char		*file_comment;
}ZIP_CFH;
...
```
- có 3 loại zip fake thì nó dạng như vầy 
- chỉ cần copy struct của nó làm mấy cái class để fake trong python là xong 
- sau khi fake được file zip bao gồm các thông tin hợp lệ để chương trình parse ra thì 
cần chú ý đến cái signature, trong chương trình chỉ cần dùng 2 trong số 3 là ok
```c

		if (signature == 67324752){
			bzero(lfh, sizeof(ZIP_LFH));
			zip_ptr = parse_lfh(zip_ptr, lfh);
			if (files_iter < 30 && lfh->fname_len > 0){
				if (lfh->compression == 0)
					files[files_iter] = write_file(lfh, zip_ptr);
				if (files[files_iter] != NULL)
					files_iter++;
				zip_ptr += lfh->uncompressed_size;
			}
		} else if (signature == 33639248){
			bzero(cfh, sizeof(ZIP_CFH));
			zip_ptr = parse_cfh(zip_ptr, cfh);
			write_symbol(cfh);
			
		} else if (signature == 101010256){
			zip_ptr = parse_cdr(zip_ptr, cdr);
		}
		else {
			errx(1, "Corrupted header byte %zu\n",
					zip_ptr - zip_data);
			exit(EXIT_FAILURE);
		}
	}
```
- ở hàm write_file nó sẽ write cái đường dẫn vào file nó mở content/flag.txt
```c
	write(fd, content, lfh->uncompressed_size);
```
- ở hàm main có phần này dùng để đọc cái đường dẫn nó đã ghi trước  đó ra, và in ra, tuy nhiên ta có thể truyền vào 2 file zip fake cùng 1 lúc để xử lý cùng lúc trong hàm extract_zip
```c
		printf("-- %s \n", files[i]);
		fd = open(files[i], O_RDONLY, 0644);
		if (fd < 0){
			printf("%s: %s %m\n", argv[0], files[i]);
			return (EXIT_FAILURE);
		}
		read_size = lseek(fd, 0, SEEK_END);
		lseek(fd, 0, SEEK_SET);
		if (read_size > 0x4000)
			read_size = 0x4000;
		read(fd, zip_file, read_size);
		zip_file[read_size] = '\0';

```
- vì nó nhảy xuống symlink luôn nên file lúc này flag.txt chứa đường dẫn, nó sẽ đọc đường dẫn đó và tạo ra symlink thành flag.txt từ đường dẫn mà ta bỏ vào content/flag.txt từ file zip fake thứ 1 thay vì chạy như thông thường, vì thế khi ra main thay vì nó in nội dung đường dẫn files thì nó in flag
```c
void write_symbol(ZIP_CFH *cfh){
	char	*filename;
	char	*symbol_name;
	int	fd;

	filename = malloc(strlen("content/") + cfh->fname_len + 1);
	memcpy(filename, "content/", strlen("content/") + 1);
	memcpy(filename + strlen("content/"), cfh->filename, strlen(cfh->filename));
	if ((cfh->external_attrs | 0xa0000000) == cfh->external_attrs){
		fd = open(filename, O_RDONLY);
		if (fd < 0)
			return;
		symbol_name = malloc(cfh->uncompressed_size + 1);
		read(fd, symbol_name, cfh->uncompressed_size);
		close(fd);
		remove(filename);
		symlink(symbol_name, filename);

```
- flag flag
```c
[*] Switching to interactive mode
 -- content/flag.txt 
------------------------------------------------------------------------

AKASEC{I7_wa5_700_0BVi0u5_ri9H7?}

------------------------------------------------------------------------

[*] Got EOF while reading in interactive
$  
```

