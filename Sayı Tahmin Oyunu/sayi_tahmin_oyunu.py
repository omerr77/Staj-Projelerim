import random

def sayi_tahmin_oyunu():
    """
    Bilgisayarın 1 ile 100 arasında rastgele bir sayı tuttuğu
    ve kullanıcının bu sayıyı tahmin etmeye çalıştığı interaktif oyun.
    """
    # Bilgisayar rastgele bir sayı tutuyor (1 ile 100 arası)
    tutulan_sayi = random.randint(1, 100)
    
    print("=" * 50)
    print("🎯 SAYI TAHMİN OYUNU 🎯")
    print("=" * 50)
    print("\nBilgisayar 1 ile 100 arasında bir sayı tuttu!")
    print("Bu sayıyı tahmin etmeye çalışın.\n")
    
    tahmin_sayisi = 0
    
    # Döngü: Kullanıcı doğru sayıyı bulana kadar devam eder
    while True:
        try:
            # Kullanıcıdan tahmin alınıyor
            tahmin = int(input("Tahmininizi girin (1-100): "))
            tahmin_sayisi += 1
            
            # Koşul yapıları: Tahminin doğruluğunu kontrol etme
            if tahmin < 1 or tahmin > 100:
                print("⚠️  Lütfen 1 ile 100 arasında bir sayı girin!\n")
                continue
            
            if tahmin < tutulan_sayi:
                print("⬆️  Daha yüksek bir sayı deneyin!\n")
            elif tahmin > tutulan_sayi:
                print("⬇️  Daha düşük bir sayı deneyin!\n")
            else:
                # Doğru tahmin!
                print("=" * 50)
                print(f"🎉 TEBRİKLER! Doğru tahmin! 🎉")
                print(f"Tutulan sayı: {tutulan_sayi}")
                print(f"Toplam tahmin sayısı: {tahmin_sayisi}")
                print("=" * 50)
                break
                
        except ValueError:
            print("⚠️  Lütfen geçerli bir sayı girin!\n")
            continue

# Oyunu başlat
if __name__ == "__main__":
    sayi_tahmin_oyunu()


