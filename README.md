# vesm3-lokaverkefni
## vesm3 lokaverkefni, gróðurhúsa og sólar panel kerfi

verkefnið sem ég gerði er gróðurhúsar og sólar panel stýrikerfi sem mælir rakastig í mold á plontum og vökvar þær, mælir birtustig í gróðurhúsinu og kveikir á ljósi ef það er of lágt og reiknar staðsetningu sólar og beinir sólar panelum að henni á hverjum klukkutíma.

notaðir eru tveir esp32-s3 sem tengjast saman með espnow. Fyrsti tengist við netið, mælir rakastig moldar, birtustig og reiknar staðsetningu sólar og bæði birtir þær upplýsingar á vefsíðu og sendir yfir á hinn esp.
annar esp fær upplýsingar frá fyrsta með espnow og kveikjir á dælu til að vökva ef moldin er þurr eða kveikjir á ljósi ef að birtustig er lágt.

![circuit diagram](https://github.com/hinrikfp/vesm3-lokaverkefni/blob/main/circuit.svg)

![esp with soil sensor and servo connected](https://github.com/hinrikfp/vesm3-lokaverkefni/blob/main/IMG_3532.jpg)

https://drive.google.com/file/d/1LOFXYiJNOa53rkoNjpzBQU1xcAUyFkOI/view?usp=sharing

```

       ║    WiFi
 NETIÐ ║╺╺╺╺╺╺╺╺┓
       ║        ╏
═══════╝        ╏
           ┌──────────┐
 ┏━━━┓     │          │      ▗▄▄▄▄▄▖
 ┃LDR┃━━━━━│ ESP32 #1 │━━━━━━▐SERVO▌
 ┗━━━┛     │          │      ▝▀▀▀▀▀▘
           └┃─────────┘
            ┃    ╎
 ┏━━━━━━━━━━┗┓   ╎
 ┃SOIL SENSOR┃   ╎
 ┗━━━━━━━━━━━┛   ╎
                 ╎ESPNow
                 ╎       ┌──────────┐
                 ╎       │          │
                 └╶╶╶╶╶╶>│ ESP32 #2 │
                         │          │
                         └──┃────┃──┘
                            ┃    ┃
                    ▗▄▄▄▄▖  ┃    ┃ ▗▄▄▄▄▄▖
                    ▐LJÓS▌━━┛    ┗━▐PUMPA▌
                    ▝▀▀▀▀▘         ▝▀▀▀▀▀▘


```

kóði fyrir fyrsta ESP sem tengist við wifi, reiknar staðsetningu sólar, snýr servóinum og birtir vefsíðuna: [hér](https://github.com/hinrikfp/vesm3-lokaverkefni/blob/main/lokaverkefni.py)

kóði fyrir annan ESP sem talar við fyrsta ESP og kveikjir/slekkur á dælu eða ljósi: [hér](https://github.com/hinrikfp/vesm3-lokaverkefni/blob/main/lokaverk-recv.py)

## heimildir

[servo library](https://github.com/Freenove/Freenove_ESP32_S3_WROOM_Board/blob/main/Python/Python_Libraries/myservo.py)

[formúlur fyrir staðsetningu sólar](https://www.omnicalculator.com/physics/sun-angle)





