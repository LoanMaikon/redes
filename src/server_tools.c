#include "../header/server_tools.h"

unsigned int get_num_files_dir(DIR *dir) {
    struct dirent *entry;
    unsigned int num_files = 0;
    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            num_files++;
        }
    }
    rewinddir(dir);

    return num_files;
}

unsigned long int get_file_size(const char *file_path) {
    struct stat st;

    if (stat(file_path, &st) == 0) {
        return st.st_size;
    } 
    else {
        return 0;
    }
}

/* (Aloca memoria) Adiciona um vetor de nomes de arquivos em movies. */
void list_files_in_dir(char *dir_path, movies_t *movies) {
    DIR *dir;
    struct dirent *entry;

    if (!(dir = opendir(dir_path))) {
        return;
    }

    unsigned int i = 0;
    unsigned long int num_files = get_num_files_dir(dir);
    movies->num_movies = num_files;

    movies->movies = malloc(sizeof(char *) * num_files);

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            movies->movies[i] = entry->d_name;
            i++;
        }
    }
    closedir(dir);
}

int send_movies_list(int sockfd, movies_t *movies) {
    return 1;
}

/* Retorna 1 se todos os pacotes foram enviados com sucesso e 0 se nao foram. */
int send_seg_packets(unsigned char **packets, int sockfd) {
    unsigned char *buffer = malloc(sizeof(unsigned char) * PACKET_SIZE);
    unsigned char seq = 0, seq_ack = 0;
    unsigned long int i = 0;
    short n = 0;

    while (packets[i]) {
        if (send_packet(sockfd, packets[i]) == -1) {
            continue;
        }

        n = recv(sockfd, buffer, PACKET_SIZE, 0);

        if (n == -1) {
            continue;
        }

        n = validate_packet(buffer, n);

        seq = get_packet_seq(packets[i]);

        if (n && (get_packet_code(buffer) == ACK_COD)) {
            seq_ack = get_packet_seq(buffer);
            if (seq == seq_ack) {
                i++;
            }
        } 
    }
    return 1;
}

/* Retorna 1 se o arquivo foi enviado com sucesso e 0 se nao foi. */
int send_file(int sockfd, char *file_name) {
    FILE *file = fopen(file_name, "rb");
    if (file == NULL) {
        return 0;
    }

    unsigned char *buffer_data = malloc(sizeof(unsigned char) * DATA_SIZE);
    unsigned long int file_size = get_file_size(file_name);
    if (file_size == 0) {
        return 0;
    }
    unsigned long int num_bytes_read = 0;
    unsigned long int num_segs = file_size / DATA_SIZE;

    if (file_size % DATA_SIZE != 0) {
        num_segs++;
    }

    while(num_segs > 1) {
        num_bytes_read = fread(buffer_data, 1, DATA_SIZE, file);
        unsigned char **packets = segment_data_in_packets(buffer_data, num_bytes_read, DATA_COD);
        send_seg_packets(packets, sockfd);
        free_packets(&packets);
        num_segs--;
    }
    num_bytes_read = fread(buffer_data, 1, DATA_SIZE, file);
    unsigned char **packets = segment_data_in_packets(buffer_data, num_bytes_read, END_DATA_COD);
    send_seg_packets(packets, sockfd);
    free_packets(&packets);

    fclose(file);
    free(buffer_data);

    return 1;
}

unsigned long int get_file_index(const unsigned char *packet) {
    return *((unsigned long int *) (packet + 3));
}

/* (Aloca memoria) Retorna NULL em caso de falha. */
unsigned char *create_packet_file_desc(int sockfd, char *file_name){
    unsigned long int file_size = get_file_size(file_name);
    struct stat attr;
    if (stat(file_name, &attr) < 0) {
        return NULL;
    }
    time_t mod_time = attr.st_mtime;
    struct tm *timeinfo = localtime(&mod_time);
    unsigned short day, month, year;
    day = timeinfo->tm_mday;
    month = timeinfo->tm_mon + 1;
    year = timeinfo->tm_year + 1900;

    unsigned char data[12] = {0};
    memcpy(data, &file_size, sizeof(unsigned long int));
    data[8] = day;
    data[9] = month;
    data[10] = year >> 8;
    data[11] = year;

    return create_packet(data, 12, 0, FILE_DESC_COD);
}
