#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>

char TOKEN[0x80];
char REPODIR[0x100];
char REPONAME[0x90];

void init()
{
	setbuf(stdin, 0);
	setbuf(stdout, 0);
	setbuf(stderr, 0);
}

void help()
{
	int i=0;

	puts(
		"* Configure command\n"
		"token    <TOKEN>                        Configure token\n"
		"repo     <USER/REPONAME>                Configure working repository\n"
		"\n* Interact command\n"
		"lsrepo                                  List all repositories\n"
		"ls                                      List all files in current directory of working repository\n"
		"cd       <DIRNAME>                      Change current directory of working repository\n"
		"get      <FILENAME>                     Download a file\n"
		"cat      <FILENAME>                     Read data of a file without downloading it\n"
		"q, quit                                 Exit program\n"
		);
}

unsigned int readline(char* buf, unsigned int size)
{
	unsigned int i;
	char c;
	for (i=0; i<size; i++)
	{
		c = fgetc(stdin);
		if (c=='\n')
			break;
		buf[i] = c;
	}
	buf[i]='\0';
}

struct memory {
	char *response;
	size_t size;
};
size_t curl_callback(char *data, size_t size, size_t nmemb, void *userdata)
{
	struct memory *chunk = userdata;
	size_t realsize = size * nmemb;

	char *ptr = realloc(chunk->response, chunk->size + realsize + 1);
	if (!ptr)
		return 0;		// Out of memory
	chunk->response = ptr;
	memcpy(&(chunk->response[chunk->size]), data, realsize);
	chunk->size += realsize;
	// chunk->response[chunk->size] = 0;
	return size * nmemb;
}
struct memory* curl_git(char *path)
{
	char url[0x2c0];
	char header_token[0x80 + 0x20];
	CURL *curl;
	struct curl_slist *list = NULL;
	struct memory *chunk;

	chunk = malloc(sizeof(struct memory));
 	memset(chunk, 0, sizeof(struct memory));
	curl = curl_easy_init();
	if(curl) {
		snprintf(url, sizeof(url)-1, "https://api.github.com%s", path);
		snprintf(header_token, sizeof(header_token)-1, "Authorization: Bearer %s", TOKEN);
		list = curl_slist_append(list, "Accept: application/vnd.github+json");
		list = curl_slist_append(list, header_token);
		list = curl_slist_append(list, "X-GitHub-Api-Version: 2022-11-28");
		list = curl_slist_append(list, "User-Agent: git-v1.0");

		curl_easy_setopt(curl, CURLOPT_URL, url);
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		curl_easy_setopt(curl, CURLOPT_TIMEOUT, 5);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl_callback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, chunk);

		curl_easy_perform(curl);

		curl_slist_free_all(list); /* free the list */
	}
	return chunk;
}
struct memory* curl(char *url)
{
	char header_token[0x80 + 0x20];
	CURL *curl;
	struct curl_slist *list = NULL;
	struct memory *chunk;

	chunk = malloc(sizeof(struct memory));
 	memset(chunk, 0, sizeof(struct memory));
	curl = curl_easy_init();
	if(curl) {
		snprintf(header_token, sizeof(header_token)-1, "Authorization: Bearer %s", TOKEN);
		list = curl_slist_append(list, "Accept: application/vnd.github+json");
		list = curl_slist_append(list, header_token);
		list = curl_slist_append(list, "X-GitHub-Api-Version: 2022-11-28");
		list = curl_slist_append(list, "User-Agent: git-v1.0");

		curl_easy_setopt(curl, CURLOPT_URL, url);
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl_callback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, chunk);

		curl_easy_perform(curl);

		curl_slist_free_all(list); /* free the list */
	}
	return chunk;
}
size_t curl_download_callback(char *data, size_t size, size_t nmemb, void *stream)
{
    size_t written = fwrite(data, size, nmemb, stream);
    return written;
}
void curl_download(char *filename, char *url)
{
	char header_token[0x80 + 0x20];
	CURL *curl;
	FILE *f;
	struct curl_slist *list = NULL;

	f = fopen(filename, "w");
	curl = curl_easy_init();
	if(curl) {
		snprintf(header_token, sizeof(header_token)-1, "Authorization: Bearer %s", TOKEN);
		list = curl_slist_append(list, "Accept: application/vnd.github+json");
		list = curl_slist_append(list, header_token);
		list = curl_slist_append(list, "X-GitHub-Api-Version: 2022-11-28");
		list = curl_slist_append(list, "User-Agent: git-v1.0");

		curl_easy_setopt(curl, CURLOPT_URL, url);
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, list);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl_download_callback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, f);

		curl_easy_perform(curl);

		curl_slist_free_all(list); /* free the list */
	}
	fclose(f);
}

void listrepo()
{
	char path[0x20];
	int i=1, count=0;
	struct memory *mem;
	cJSON *root, *response, *repo;

	if (!TOKEN[0])
	{
		puts("Token is null");
		return;
	}

	while (1)
	{
		sprintf(path, "/user/repos?page=%d", i);
		mem = curl_git(path);
		root = cJSON_Parse(mem->response);
		response = root->child;
		if (!response)
		{
			cJSON_Delete(root);
			break;
		}
		do
		{
			repo = response->child;
			do
			{
				if (!strcmp(repo->string, "full_name")){
					printf("%d. %s\n", ++count, repo->valuestring);
					break;
				}
			}
			while (repo = repo->next, repo!=NULL);
		}while ( response = response->next, response!=NULL );
		cJSON_Delete(root);
		i++;
	}
}

int check_repo(char *reponame)
{
	char path[0x110];
	struct memory *mem;
	cJSON *response;

	sprintf(path, "/repos/%s/contents", reponame);
	mem = curl_git(path);
	if (!mem->response)
	{
		puts("Request timeout");
		return 0;
	}
	response = cJSON_Parse(mem->response);
	if (!cJSON_IsArray(response))
	{
		cJSON_Delete(response);
		return 0;		// Invalid repo
	}
	cJSON_Delete(response);
	return 1;			// valid repo
}

void listfile()
{
	char path[0x1a0], *name, *type;
	cJSON *root, *response, *repo;
	struct memory *mem;

	if (!TOKEN[0])
	{
		puts("Token is null");
		return;
	}
	if (!REPONAME[0])
	{
		puts("Repo name is null");
		return;
	}

	snprintf(path, sizeof(path)-1, "/repos/%s/contents%s", REPONAME, REPODIR);
	mem = curl_git(path);
	if (!mem->response)
	{
		puts("Request timeout");
		return;
	}
	root = cJSON_Parse(mem->response);
	if (!cJSON_IsArray(root))
	{
		puts("Something wrong!");
		cJSON_Delete(root);
		return;
	}
	response = root->child;
	do
	{
		repo = response->child;
		do
		{
			if (!strcmp(repo->string, "name"))
				name = strdup(repo->valuestring);
			else if (!strcmp(repo->string, "type"))
				type = strdup(repo->valuestring);
		}
		while (repo = repo->next, repo!=NULL);
		if (!strcmp(type, "dir"))
			printf("[D] %s\n", name);
		else
			printf("[ ] %s\n", name);
	}while ( response = response->next, response!=NULL );
	cJSON_Delete(root);
}

void changedir(char *dirname)
{
	// char tmpdir[0x200];
	char path[0x200];
	cJSON *response;
	struct memory *mem;
	int len;

	if (!TOKEN[0])
	{
		puts("Token is null");
		return;
	}
	if (!REPONAME[0])
	{
		puts("Repo name is null");
		return;
	}

	if (!strcmp(dirname, ".") || !strcmp(dirname, "./"))
		return;
	
	if (!strcmp(dirname, "..") || !strcmp(dirname, "../"))
	{
		for (int i=strlen(REPODIR)-2; i>-1; i--)
		{
			if (REPODIR[i] == '/'){
				REPODIR[i] = '\0';
				break;
			}
		}
		return;
	}

	while (1)
	{
		len = strlen(dirname);
		if (dirname[len-1]=='/')
			dirname[len-1] = '\0';
		else
			break;
	}
	// len = strlen(strcpy(tmpdir, REPODIR));
	// tmpdir[len] = '/';
	// memcpy(tmpdir[len+1], dirname, 0x100);

	// sprintf(tmpdir, "%s/%s", REPODIR, dirname);
	
	REPODIR[strlen(REPODIR)] = '/';
	strcpy(&REPODIR[strlen(REPODIR)], dirname);
	sprintf(path, "/repos/%s/contents%s", REPONAME, REPODIR);
	mem = curl_git(path);
	if (!mem->response)
	{
		puts("Request timeout");
		return;
	}
	response = cJSON_Parse(mem->response);
	if (!cJSON_IsArray(response))
	{
		changedir("..");
		// printf("Invalid directory: %s\n", tmpdir);
		return;
	}
	// strcpy(REPODIR, tmpdir);
	cJSON_Delete(response);
}

void getfile(char *filename)
{
	char path[0x2a0], *download_url;
	struct memory *mem;
	struct cJSON *root, *response;

	if (!TOKEN[0])
	{
		puts("Token is null");
		return;
	}
	if (!REPONAME[0])
	{
		puts("Repo name is null");
		return;
	}
	snprintf(path, sizeof(path), "/repos/%s/contents%s/%s", REPONAME, REPODIR, filename);
	mem = curl_git(path);
	if (!mem->response)
	{
		puts("Request timeout");
		return;
	}
	root = cJSON_Parse(mem->response);
	if (cJSON_IsArray(root) || !strcmp(root->child->string, "message"))
	{
		puts("Invalid file");
		return;
	}
	response = root->child;
	do
	{
		if (!strcmp(response->string, "download_url"))
			download_url = strdup(response->valuestring);
	}while ( response = response->next, response!=NULL );

	curl_download(filename, download_url);

	cJSON_Delete(root);
}

void readfile(char *filename)
{
	char path[0x2a0], *download_url;
	struct memory *mem;
	struct cJSON *root, *response;

	if (!TOKEN[0])
	{
		puts("Token is null");
		return;
	}
	if (!REPONAME[0])
	{
		puts("Repo name is null");
		return;
	}
	snprintf(path, sizeof(path), "/repos/%s/contents%s/%s", REPONAME, REPODIR, filename);
	mem = curl_git(path);
	if (!mem->response)
	{
		puts("Request timeout");
		return;
	}
	root = cJSON_Parse(mem->response);
	if (cJSON_IsArray(root) || !strcmp(root->child->string, "message"))
	{
		puts("Invalid file");
		return;
	}
	response = root->child;
	do
	{
		if (!strcmp(response->string, "download_url"))
			download_url = strdup(response->valuestring);
	}while ( response = response->next, response!=NULL );

	mem = curl(download_url);
	puts(mem->response);

	cJSON_Delete(root);

}

// token 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
int main(int argc, char *argv[]) 
{
	int size;
	char cmd[0x100], *operator;

	init();
	// if (argc==2)
	// {
	// 	if (setregid(geteuid(), geteuid())!=0)
	// 		printf("hihi");
	// 	char* test[] = {
	// 		"/bin/sh",
	// 		NULL
	// 	};
	// 	execve(test[0], test, NULL);
	// 	exit(0);
	// }

	while (1)
	{
		printf("---[%s] [%s]\n> ", REPONAME, REPODIR);
		readline(cmd, sizeof(cmd)-1);
		operator = strtok(cmd, " ");
		if (!strcmp(operator, "help") || !strcmp(operator, "?"))
			help();
		else if (!strcmp(operator, "quit") || !strcmp(operator, "q"))
			exit(1);
		else if (!strcmp(operator, "token"))
		{
			operator = strtok(NULL, " ");
			if (!operator)
				printf("Token: %s\n", TOKEN);
			else
			{
				memcpy(TOKEN, operator, sizeof(TOKEN));
				printf("Working token: %s\n", TOKEN);
			}
		}
		else if (!strcmp(operator, "repo"))
		{
			operator = strtok(NULL, " ");
			if (!operator)
				puts("Missing required parameter: <USER/REPONAME>");
			else if (check_repo(operator))
			{
				memset(REPODIR, 0, sizeof(REPODIR));
				memcpy(REPONAME, operator, sizeof(REPONAME));
				printf("Working repo: %s\n", REPONAME);
			}
			else
				puts("Invalid repo name");
		}
		else if (!strcmp(operator, "repos"))
			listrepo();
		else if (!strcmp(operator, "ls"))
			listfile();
		else if (!strcmp(operator, "cd")){
			operator = strtok(NULL, " ");
			if (!operator)
				puts("Missing required parameter: <DIRNAME>");
			else
				changedir(operator);
		}
		else if (!strcmp(operator, "get")){
			operator = strtok(NULL, " ");
			if (!operator)
				puts("Missing required parameter: <FILENAME>");
			else
				getfile(operator);
		}
		else if (!strcmp(operator, "cat")){
			operator = strtok(NULL, " ");
			if (!operator)
				puts("Missing required parameter: <FILENAME>");
			else
				readfile(operator);
		}
	}

	return 0; 
} 
