# Connexion
```bash
telnet m1.tme-crypto.fr 1337
```

# Initialisation

Allez dans le dossier Initialisation

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

# Exploration

Allez dans le dossier Exploration

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

## flag 10 :

```bash
# via script python :
python3 flag10_pk.sign.py

# ou via commande openssl :
openssl req -new -key flag10_skey.pem -batch -subj '/CN=Yannick' -out flag10_csr.pem
```

flag pki.cert :

```
[security engine] pki.cert:136:1|c8ad30faa28983690a3b96f26e2a9b631e328988db0ac4bef62e3a7ff5300a25
```

## flag 11:


```bash
# via script python 
# pour générer les clés
python3 flag11_rsa.keygen.py
# pour vérifier la signature
python3 flag11_challenge.py
```

```bash
[security engine] rsa.keygen:136:1|940e6ea8d01a14159b3dfeae0a6ae9be1a3a67e4d2fc2a9efeb820b57b8cf279
```


```bash
Ici se trouve une serrure sans contact (NFC) sur la grille.

>>> use card
        challenge: barfs finds viers hypos libra

        signature:  683fe62b98f2dd2f06f920bfb80733e4b398624f98d642eba0d7e8605654e596c8f73a2f4eda47987de1b2aded7f06b7cd36cc1e1a150e7a629272c39bf3e82d665db1555aa644caac45bcede4da7d88250545b1a3e24f76859a8ec2f62b60d42a5214c128c670d3f621ee46764b5e5c943fdc552aa0d82ef78a843b6c9ff2da033eeee8fb05518228778540ed927b04c2a8dd4f315feef33691d9bdb472f89f78d67889afdd945faf18276a11ed48e9a9e4d54e31ca0b16ed9b7baf3091d004f39537867dceedc53aa0f45da2ce6b35649b5313ed37da6620e01ea9c2c35f0324e3e53cfa1fa35ddd0ae723a1d3b0a89d4bb693ee172fa664ae3350534dbd30

Une lumière verte s'allume sur le lecteur de badge.
La porte vitrée se déverrouille et vous pénetrez à l'intérieur.
(la prochaine fois, au lieu de refaire tout ce cirque, il suffira
(d'utiliser le lecteur de badge et ça suffira).

Vous êtes dans un petit espace gris et bétonné qui sépare le jardinet de
l'intérieur du bâtiment.  Au nord et au sud, il est fermé par deux grilles
métalliques, et le tout fait penser à une cellule de prison.  La personne
qui fait le ménage par ici a pris l'habitude d'y laisser son petit charriot.
Au nord, on peut accéder à un couloir turquoise.

[1d2d542cb79a9949f40890da7bc05324] {"session-key": "2c8fb8a556e75119c8ebf6e13c870890df50faae454e8aae97a2f5e701a5cd68bb233f388f89deed50b64769ef0321f542908e2c8477330eba72950d52d17cbd422387d273fa054c40983f5358da2209fe28f511d15392d266ef21c3029ef2b37db658b1fa2710dc2fb68faca48fcf4857ad87ee72da64410f8b1768a2365751489dce38a98a6868c538abe1aaf45945c11e91b64fd4e3025facf88aba536a0178fa0a008c290e19652c2d4fb8e072ef1fe02ff6c99b218db5d70f05f118f125d191214738548d72f653de6bd1bcb28b2334dbf7245302268de0a3210a750d226bad3338e6daf7732476c66390c591f1c30035f1364f91a27f454d42d6bc461d", "ciphertext": "U2FsdGVkX1+qPoHYhjwHQPt/EAzMqZO3Deu8qKe15JI="}
[security engine] rsa.keygen:136:1|940e6ea8d01a14159b3dfeae0a6ae9be1a3a67e4d2fc2a9efeb820b57b8cf279
```

# flag 12:

```bash
[security engine] rsa.shared:136:1|867f790029d943d1c164febbc296af1952766639a3af26bc107da2254a94e50c
```

# flag 13:

```bash
[security engine] rsa.reduction:136:1|0e99697ed1c938d5b9280fc4d5cbcc75ffee7f6e4d419ce7011d31bc776d4c90
```

# flag 14

```bash
[security engine] web.of.trust:136:1|5ab545ed72ce4ea958a06a954b4aa4fcfcc17b1a357e3d5f4a68a2f37176977a
```

# flag 15
```bash
[security engine] secure.vault:136:1|35cc552dc6e2fcf35d243e61d44fc94150093e0e001b737aa7127a837b423c8c
```