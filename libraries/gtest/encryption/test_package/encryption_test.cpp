// SOURCE CODE FROM https://wiki.openssl.org/index.php/EVP_Symmetric_Encryption_and_Decryption

#include <gtest/gtest.h>
#include "encrypter.h"

TEST(TestingEncryption, cipher) {

	  /* A 256 bit key */
	  unsigned char *key = (unsigned char *)"01234567890123456789012345678901";

	  /* A 128 bit IV */
	  unsigned char *iv = (unsigned char *)"01234567890123456";

	  /* Message to be encrypted */
	  unsigned char *plaintext = (unsigned char *) "The quick brown fox jumps over the lazy dog";
	  unsigned char ciphertext[128];

	  /* Buffer for the decrypted text */
	  unsigned char decryptedtext[128];

	  int decryptedtext_len, ciphertext_len;

	  /* Initialise the library */
	  ERR_load_crypto_strings();
	  OpenSSL_add_all_algorithms();
	  OPENSSL_config(NULL);

	  /* Encrypt the plaintext */
	  ciphertext_len = encrypt (plaintext, strlen ((char *)plaintext), key, iv, ciphertext);

	  /* Do something useful with the ciphertext here */
	  printf("Ciphertext is:\n");
	  BIO_dump_fp (stdout, (const char *)ciphertext, ciphertext_len);

	  /* Decrypt the ciphertext */
	  decryptedtext_len = decrypt(ciphertext, ciphertext_len, key, iv, decryptedtext);

	  decryptedtext[decryptedtext_len] = '\0';

	  /* Show the decrypted text */
	  printf("Decrypted text is:\n");
	  printf("%s\n", decryptedtext);

	  // The decoded data is the same that we encode
	  ASSERT_STREQ((const char*) decryptedtext, (const char*) plaintext);

	  /* Clean up */
	  EVP_cleanup();
	  ERR_free_strings();
}

