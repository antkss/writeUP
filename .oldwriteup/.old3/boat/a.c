#include <stdio.h>
#include <openssl/evp.h>
#include <string.h>

// Encrypt function
int encrypt(
        unsigned char *plaintext,
        int plaintext_len,
        unsigned char *key,
        unsigned char *iv,
        unsigned char *ciphertext)
{
    EVP_CIPHER_CTX *ctx;
    int len;
    int ciphertext_len;

    // Create and initialize the context
    if(!(ctx = EVP_CIPHER_CTX_new())) {
        puts("E CTR ERROR");
        return -1;
    }

    // Initialize the encryption operation.
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)) {
        puts("E INIT ERR");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    // Provide the message to be encrypted, and obtain the encrypted output.
    if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) {
        puts("ENC UPDATE ERR");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len = len;

    // Finalize the encryption. Further ciphertext bytes may be written at this stage.
    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) {
        puts("ENC FINAL ERR");
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len += len;

    // Clean up
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_len;
}

// Example usage in main function
int main(void)
{
    // Example plaintext, key, and IV
    unsigned char *plaintext = (unsigned char *)"hellfdsafdsafdsafdshajkfsdh";
    unsigned char key[32] = {0}; // 256-bit key
    unsigned char iv[16] = {0};  // 128-bit IV
    unsigned char ciphertext[128];

    // Encrypt the plaintext
    int ciphertext_len = encrypt(plaintext, strlen((char *)plaintext), key, iv, ciphertext);

    // Print the ciphertext
    if (ciphertext_len != -1) {
        printf("Ciphertext is:\n");
        for(int i = 0; i < ciphertext_len; i++) {
            printf("%02x", ciphertext[i]);
        }
        printf("\n");
    }

    return 0;
}
