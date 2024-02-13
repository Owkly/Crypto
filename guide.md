# Connexion
```bash
telnet m1.tme-crypto.fr 1337
```

# Initialisation

## flag 1 :

données :
```bash
#POST-IT PASSWORD: 
ISECR0XX

# Message chiffré dans flag1_mdp.txt :
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
# clé publique dans flag2_pki_tutorial_pkey.pem :
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
openssl pkeyutl -encrypt -pubin -inkey flag2_pki_tutorial_pkey.pem -in flag2_msg.txt -out flag2_msg_encrypted.bin
xxd -p -c 256 flag2_msg_encrypted.bin

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
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out flag3_pkey # clé privée
openssl rsa -in flag3_pki_key.pem -pubout -out flag3_skey.pem  				 # clé publique

# soit script python :
python3 flag3_pki_generate.py

# stockés dans flag3_pkey.pem et flag3_skey2.pem
```

flag pki.upload :
```bash
[security engine] pki.upload:136:1|63ce4e0e806c62dbd452054e03666ddb18cfa88833ef4950701dab7cb0fb0fb8
```

## flag 4 :

signer un message avec la clé privée :
```bash
# soit commande openssl :
openssl dgst -sha256 -sign <fichier contenant la clé secrète> <fichier contenant le message> 
xxd -p -c 256 <nom du fichier contenant la signature>

	# exemple
	openssl dgst -sha256 -sign flag3_skey.pem -out flag4_signature_challenge.bin flag4_challenge.txt
	xxd -p -c 256 flag4_signature_challenge.bin

	openssl dgst -sha256 -sign flag3_skey.pem -out flag4_signature_upload.bin flag4_upload.txt
	xxd -p -c 256 flag4_signature_upload.bin

# soit script python :
python3 flag4_power_on.py
```
flag power.on :

```bash
[security engine] power.on:136:1|40294b7ff0ae55ea647d882de452b3de93b5226d6eff895f7abc1abcba5b89df
```


## flag 5 :

```bash
# données :
Une feuille A4, 80g/m². Un utilisateur a imprimé dessus une trace du protocole 
d'authentification CHAP. Peut-être qu'il essayait de mettre au point un client
personnalisé pour se connecter ? Il y a écrit :
---> {"jsonrpc": "2.0", "method": "protagonist.CHAP-challenge", "params": {"world_id": "8bef1547cc426dea0b72577e78cf6172", "username": "isabela51"}, "id": 5}
<--- {"jsonrpc": "2.0", "result": "U2FsdGVkX1+JDJgfeCeSjMJI4KkUMSFQ3Ai2ZyUFIAeyeabQ2JYbfJt66sUKMfur\n", "id": 5}
---> {"jsonrpc": "2.0", "method": "protagonist.CHAP-response", "params": {"world_id": "8bef1547cc426dea0b72577e78cf6172", "response": "snood wafts lusts niece bulgy"}, "id": 6}
<--- {"jsonrpc": "2.0", "result": null, "id": 6}

# mot de passe dans flag5_words.txt :
```

recherche du bon mot de passe qui decrypte le message :
```bash
# via script python :
python3 flag5_dict_atk.py
```

flag dict.atk :
```
isabela51
seacoast
[security engine] dict.atk:136:1|caf41960020e8bcd070c2edc00819e50600ec196bbd91680f6e0d9dda67f8c44
```

## flag 6 :

données :
```bash
# pas de fichier directement dans le script python
U2FsdGVkX1+29XFd2I+IEnjBbrRsDKkGSafinx7U0rCHvJTjdHb1BX+ZtTeFujdr\n
```

decryptage :
```bash
# via script python :
python3 flag6_chap_login.py 
```

flag chap.login :
```
[security engine] chap.login:136:1|220a64ceae1061053e72c55547379acb7d5b8f0ae5ff4eba87b10b146808eb4d
```	

## flag 7 :

calcul de p et g :
```bash
# via script python :
python3 flag7_tme.generator.py
```
flag tme.generator :
```
[security engine] tme.generator:136:1|951f2d9e86f9a4c46b61c325f4b8d9f42e2448f8a725bfede0003865346a92ae
```

## flag 8 :

calcul de g, et p avec avec la décomposition de (p-1)//q :
```bash
# via script python :
python3 flag8_tme.primitive_1.py # beaucoup plus long (20-30 minutes) mais quasi sûr de trouver la solution

python3 flag8_tme.primitive_2.py # plus rapide mais selon le n choisi peut ne pas trouver de solution
```

flag tme.primitive :
```
[security engine] tme.primitive:136:1|7a555996d42b91dd6204ab9abd23c41f7d2699b89032e5ecb36a57c2e7a614cd
```

## flag 9 :


```bash
# via script python :
python3 flag9_pk.login.py
```

flag pk.login :

```
[security engine] pk.login:136:1|c69f45f34f051cf8a8b63b90453be12daed50212019c64f6ff7756e79df239cb
```