# Initialisation

## flag 1 :

données :
```bash
POST-IT PASSWORD: ISECR0XX

U2FsdGVkX1/51wqD7PnMSuRkwL8czQ1S/AznUxY9Z+K2tN2o5LBv1C2cM2fDGGD9
hQym6B/W3VH0TNEn7dU2Xg==
```

decryptage :
```bash
# soit commande openssl :
openssl enc -d -base64 -aes-128-cbc -pbkdf2 -pass pass:"ISECR0XX" -in flag1_mdp.txt

# soit script python :
python3 flag1_register.py
```

flag register :
```bash
[security engine] register:136:1|99b75790fbdbdd3d6aac5199f666744ad95939df184fe9d9bae148672833729d
```


## flag 2 :

donnéees :
```bash
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvfOQoiH2KNKnDfJZmNAz
bTEY6+2bTDvwrphV7hkuxzOxtVb1hxhgFLdqGmvSdRkeEJjICgSmysVHPbs5A2RT
040U7EIXoxbd0/g1FpjDeEiSsxEZR2Lm/kCkUtU7F/UUUIz37DlxAiCvn5BvnYwf
2NZ2j0hDGCBHMKZj/SJga1KRkghdOZvtS1YwoN1dZpovZpOYRhttk2Nflx9qpiR7
vvW4FSNi8u63DbfaoKMDSWTXweJWLpEfoWfpLGLN16nCy0v7RvqfE0J2dtJLakAP
lbsm8NI0epwTs9CZmBmCbw7a3XauHqwGXcQjYltF0zwzx3fpxWDqN7ayznDB8kNt
mwIDAQAB
-----END PUBLIC KEY-----
```

encryptage :
```bash
# soit commande openssl :
echo -n "I got it!" | openssl pkeyutl -encrypt -pubin -inkey flag2_pki_tutorial_key.pem | xxd -p | tr -d '\n'

# soit script python :
python3 flag2_pki_tutorial.py
```
flag pki.tutorial :
```bash
[security engine]  pki.tutorial:136:1|78d578987ec1b855d24acd949d3e539c0e014982e4050cfb0add6e9dea3e40ce
```


## flag 3 :

génération des clés :
```bash
# soit commande openssl :
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048
openssl rsa -in flag3_pki_key.pem -pubout -out flag3_skey2.pem  # clé publique

# soit script python :
python3 flag3_pki_generate.py
```

flag pki.upload :
```bash
[security engine] pki.upload:136:1|63ce4e0e806c62dbd452054e03666ddb18cfa88833ef4950701dab7cb0fb0fb8
```

## flag 4 :

signer un message avec la clé privée :
```bash
# soit commande openssl :
openssl dgst -sha256 -sign <fichier contenant la clé secrète> <fichier contenant le message> | xxd -p -c 256 > <fichier pour contenir le msg signé>

# soit script python :
python3 flag4_power_on.py
```

```bash
[security engine] power.on:136:1|40294b7ff0ae55ea647d882de452b3de93b5226d6eff895f7abc1abcba5b89df
```