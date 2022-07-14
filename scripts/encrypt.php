<?php
//this code encrypts plain text to ciphertext as per provided params
$cert_file="file://".$argv[1];
$plain_text=$argv[2];
openssl_public_encrypt($plain_text, $cipher_text, $cert_file, OPENSSL_PKCS1_PADDING);
echo base64_encode($cipher_text);
?>
